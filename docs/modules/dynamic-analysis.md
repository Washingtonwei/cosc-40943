# Dynamic analysis

> **Purpose (one line):** a student can judge how strong a test oracle is, write preconditions, postconditions, and invariants as in-source assertions on a real service method, and run a fuzz or property-based harness against their own project and triage what it reports.


!!! note "This module is still being written"
    The course is being revamped this term, so modules go up as they are written rather than all at once. What is here is usable; the rest is coming. Lectures and studio do not depend on the missing parts.

<!--
DRAFT. Authored from CMU 17-313 "Beyond Traditional Testing with Dynamic Analysis"
(reference/courses/CMU-17-313-foundations-of-software-engineering/12-dynamic-analysis.pdf) and the
reading notes in notes/dynamic-analysis.md, per DECISION-add-missing-topics. Tier is Exposure, so
class time is part of one week; the written notes carry the rest.

Open dependency: section 4's oracle ladder assumes MODULE-testing names the word "oracle" in week 9.
If that does not happen, this module has to define it cold and loses three minutes.

Code facts verified against https://github.com/Washingtonwei/project-pulse (branch main):
EvaluationService.getPeerEvaluationAverage ends in .average().orElse(0.0);
Rating.setActualScore throws IllegalArgumentException outside [0, criterion.getMaxScore()];
PeerEvaluation.calculateTotalScore sums Rating::getActualScore. Re-check before this goes stable,
since the running example is a live repository.
-->

## 1. Learning objectives

By the end of this module, a student can:

1. Say which defect classes static analysis finds, which appear only at run time, and pick the right tool for a given defect.
2. Explain why example-based tests cannot cover a real input space, and describe how coverage-guided fuzzing explores it.
3. Judge an oracle's strength: state what a given oracle detects and what it silently passes.
4. Write preconditions, postconditions, and invariants as in-source assertions on a Project Pulse service method, following the assertion guidelines.
5. Run a property-based or fuzz harness on their own project and triage the failures it reports.
6. Explain why an agent-generated test suite tends to carry a weak oracle, and write the invariant that fixes it.

## 2. Where it fits

- **Prerequisites:** testing (the pyramid, and the oracle named there), static analysis in week 10 (the half that never runs the program), and AI-assisted implementation.
- **Leads into:** observability and debugging, which shares this week, then maintainability and software metrics in week 13.
- **How it's taught:** part of week 12, sharing Monday and Wednesday with observability and debugging; Friday studio applies it to your own repository. These notes go further than class time does, so read them if the topic interests you.
- **Course outcome it delivers:** [applying static and dynamic analysis to reason about quality, maintainability, and technical debt](../syllabus.md#learning-outcomes) (outcome 5).

## 3. Motivation

- **The problem, on Project Pulse:** `EvaluationService.getPeerEvaluationAverage` averages a student's peer-evaluation total scores for one week. The last thing it does to that number is `.average().orElse(0.0)`. So a student nobody evaluated that week is reported with an average total score of **0.0**, indistinguishable from a student whose teammates all rated her zero. Nothing throws and nothing is logged. The individual numbers are all legal, because `Rating.setActualScore` already rejects anything outside `[0, criterion.maxScore]`. It is the aggregate that lies, and any test written by reading this method passes, because the method does exactly what it says.

- **A real failure it prevents:** Heartbleed (CVE-2014-0160). OpenSSL trusted a length field supplied by the caller and copied that many bytes out of a buffer that could be far smaller, leaking up to 64KB of adjacent process memory, private keys included. The flaw shipped in December 2011 and was disclosed in April 2014. Two years of review and compilation missed it, because nothing in the source reads as wrong. It was found by running the code: Codenomicon's fuzzing tool, and independently a Google engineer. One assertion relating the claimed length to the buffer's actual length turns a silent leak into a crash on the first malformed packet.

## 4. Core concepts

### The two halves

Static analysis reads the blueprint. Dynamic analysis drives the car.

| | Static analysis (week 10) | Dynamic analysis (this week) |
|---|---|---|
| Runs the program | no | yes |
| Examples | compiler, SpotBugs, ESLint, SonarQube | unit tests, fuzzers, profilers, sanitizers |
| Finds | pattern-level defects, style, some null and resource paths | crashes, memory errors, races, wrong answers |
| A false positive costs | wasted triage | nothing, the failure actually happened |
| Blind to | anything that depends on a run-time value | any path this run did not take |

Neither contains the other. Static analysis sees every path but no values; dynamic analysis sees real values but only the paths it happened to execute. Run both, and run both in CI, because the later a defect surfaces the more it costs to fix.

### Why "write more tests" is not the answer

A test is one point in an input space that is effectively infinite. Developers write the cases they can imagine, and defects live in the cases they cannot: empty input, Unicode, negative numbers, a malformed file, a field nobody ever filled in.

### Fuzzing

Let a machine generate the inputs instead. The loop is four steps: generate an input, run the program, detect a failure, save the interesting ones.

Miller, Fredriksen, and So established the idea in 1990 by feeding random bytes to UNIX utilities and crashing a large fraction of them. Two refinements make it practical:

- **Mutation-based.** Start from valid seed inputs and perturb them (flip bits, delete bytes, insert syntax) rather than generating from nothing, so inputs survive the parser.
- **Coverage-guided.** Measure coverage on each run, and promote any mutation that reaches new code into the seed pool. AFL popularized this, and it is why modern fuzzing reaches deep logic that random generation never does.

At scale this is infrastructure, not an exercise: Google's OSS-Fuzz and ClusterFuzz run continuously against roughly a thousand open-source projects and have reported tens of thousands of bugs. Current research pushes further, using language models to generate seeds and harnesses that get past a parser faster than mutation alone.

### The oracle is the hard part

An **oracle** decides whether an execution was correct. Without one, running a program is just running a program: you generated a million inputs and learned nothing.

Oracles form a ladder, weak to strong:

| Oracle | Detects | Misses |
|---|---|---|
| It did not crash | crashes, hangs, timeouts | every wrong answer that stays inside the type |
| Crash plus a sanitizer | also out-of-bounds access, use-after-free, leaks | logic errors that touch no illegal memory |
| `assertEquals` in a written test | the one case its author thought of | every case they did not think of |
| An in-source invariant | any execution that violates it, in tests, under a fuzzer, in production | whatever the invariant does not talk about |

Most fuzzing campaigns find only crashes, and they find only crashes because "it did not crash" is the oracle they were given. Strengthening the oracle is what turns a fuzzer from a crash-finder into a bug-finder, and that is why assertions belong beside fuzzing rather than beside JUnit.

### Assertions as in-source oracles

`assertEquals(5, add(2,3))` is an oracle for one input. `assert amount >= 0` is an oracle for **every** execution of that line: every unit test, every fuzzed input, and, where they are enabled, every production request.

Put a postcondition on the aggregation from section 3:

```java
List<PeerEvaluation> evaluations =
        this.evaluationRepository.findByWeekAndEvaluateeId(week, student.getId());

double averageTotalScore = evaluations.stream()
        .mapToDouble(PeerEvaluation::getTotalScore)
        .average()
        .orElse(0.0);

// Postcondition: an average lies within the range of the values it averaged.
DoubleSummaryStatistics inputs = evaluations.stream()
        .mapToDouble(PeerEvaluation::getTotalScore)
        .summaryStatistics();
assert averageTotalScore >= inputs.getMin() && averageTotalScore <= inputs.getMax()
    : "average " + averageTotalScore + " outside its input range for "
      + student.getEmail() + " in week " + week;
```

The postcondition does not know the right answer, and that is precisely why it is strong. It holds for every rubric, every team, and every week, and it fails on the whole family of aggregation bugs (dividing by the wrong count, dropping a rating, counting one evaluator twice) without anyone working out an expected value by hand. Oracles that state a **property** survive; oracles that state an **answer** cover one row of a table.

It also fires on Project Pulse today. Over an empty list, `DoubleSummaryStatistics` reports a minimum of positive infinity and a maximum of negative infinity, so the assertion trips on exactly the case section 3 described: `0.0` is not within the range of no values, because an average over nothing is not a number and `.orElse(0.0)` invented one.

Then notice what the assertion does **not** do. It does not fix the defect. It tells you the postcondition is false, and the repair is to the design (return something that can say "no evaluations", rather than a number that cannot), not to the assertion. That is the normal outcome: an assertion surfaces a design flaw, and the temptation to weaken it until it passes is the mistake to name out loud.

An assertion also moves a failure to where it is cheap. Without it, the invented `0.0` is persisted, folded into the section's weekly report, and questioned weeks later by an instructor with no way to tell which service produced it.

Four guidelines:

- **Express an invariant,** something that must be true whenever the code is correct.
- **No side effects.** Java disables assertions unless you pass `-ea`, so anything you do inside one may simply never happen.
- **Never a replacement for error handling.** Malformed input from a browser is an expected condition and earns a `400`, not an `AssertionError`. Project Pulse already gets this right: `Rating.setActualScore` throws on a score outside the criterion's range, because a bad score can arrive from a client. The postcondition above is the other kind, unreachable from outside and impossible unless the code is wrong.
- **Not for user errors.** Assertions catch programmer errors: broken internal state and violated contracts between your own methods.

This is ordinary production practice, not an academic exercise. Cassandra asserts algorithm invariants while sorting; SQLite and LLVM assert preconditions on function entry; Firefox asserts postconditions after processing. Kudrjavets, Nagappan, and Ball, studying two large Microsoft components, found assertion density and post-release fault density negatively correlated.

## 5. The AI-native lens

- **Delegate to AI:** writing the fuzz or property harness, producing seed inputs, converting an example-based test into a property-based one, proposing candidate invariants from a method's body, and clustering a fuzzer's crashes into distinct root causes. Ask it for the harness, never for the verdict.
- **Keep human:** the oracle. Whether an invariant is *true* is a question about the requirement, not about the code. "The overall grade lies within the criterion score range" comes from the rubric contract and the business rules, not from reading `getPeerEvaluationAverage`.
- **Context to supply:** the business rules and quality attributes that define legal state (active weeks, submission windows, score ranges), the units and bounds the type system does not carry, and which conditions are expected user errors rather than programmer errors, because an agent will assert on both without being told.
- **How to verify:** negate a condition or delete the line an assertion guards, and confirm it fires. An invariant that survives an injected fault is decoration. Then confirm `-ea` is actually set in your test profile, or none of it ran at all.

**The circular oracle.** Asked to test `getPeerEvaluationAverage`, an agent reads the implementation and writes assertions that restate it, `orElse(0.0)` included: it will assert that a student with no evaluations scores zero, because that is what the code does. The suite is green, and it stays green if the computation is wrong from top to bottom, which is the week 1 story's 312 passing tests all over again. An invariant derived from the rubric contract is the one an agent cannot satisfy by paraphrasing the code, because its source is a document the code does not contain.

## 6. Risks & mitigations

| Risk (classic + AI-introduced) | Human judgment that catches it | Mitigation |
|---|---|---|
| Assertions used to validate user input, so a bad request becomes a 500 (classic). An agent generates assertions on request payloads because it cannot tell a programmer error from a user error (AI). | Can anyone outside this codebase cause this condition? If yes, it is not an assertion. | Validate at the boundary and return `400`; assert only on internal state. Review every generated assertion against that one question. |
| A fuzzing run finds nothing and the team concludes the code is fine (classic). An agent-written harness never gets past the parser, so every input dies in the first ten lines (AI). | Did coverage move while the fuzzer ran? | Measure coverage under the harness. A harness that does not increase coverage is not testing anything. |
| Assertions ship disabled everywhere, so they document intent instead of checking it (classic). Agent-generated invariants pile up and are never executed (AI). | Have any of these ever actually run? | `-ea` in the test profile and in CI; mutate one invariant and watch the build go red. |

## 7. Hands-on (studio + individual assignment)

**Studio (team, own project)**

- **Goal:** one method in your own project acquires an oracle worth the name.
- **In studio (own project):** pick the method with the most arithmetic or the most mutable state. Write its preconditions and its postcondition as assertions. Turn its example-based test into a property-based one (`jqwik` on JUnit 5 for the Java side, `fast-check` for the Vue side), run a few thousand generated cases, and triage what comes back.
- **Deliverable & assessment:** a pull request carrying the assertions and the property test, plus an issue for anything the run surfaced. Graded on whether the postcondition states a property rather than restating the implementation, and on the quality of the triage, not the number of failures found.

**Individual assignment (Project Pulse)**: none of its own. This module supplies the last step of assignment 5, **Hunt the bug** (due Fri Nov 20): the regression test that would have caught the planted bug. Write it as an invariant wherever you can, not as one more example.

## 8. Summary / key takeaways

- Static and dynamic analysis fail in opposite directions: every path but no real values, real values but only the paths that ran. Use both, in CI.
- Coverage-guided fuzzing beats random fuzzing because it keeps the mutations that reach new code, and both beat hand-written examples on volume.
- A test is only as good as its oracle. "It did not crash" is the weakest one on the ladder, and it is why most fuzzing finds only crashes.
- An in-source assertion is an oracle on every execution instead of on one input. Express invariants, keep them free of side effects, and never use one where a user error belongs.
- An oracle that states a property outlives one that states an answer, and it is the one an agent cannot fake by paraphrasing the code it is supposed to be testing.

## 9. Key papers & further reading

- Miller, Fredriksen, and So, "An Empirical Study of the Reliability of UNIX Utilities," *CACM* 33(12), 1990. The paper that started fuzzing.
- Kudrjavets, Nagappan, and Ball, "Assessing the Relationship Between Software Assertions and Faults: An Empirical Investigation," ISSRE 2006.
- Zeller, Gopinath, Böhme, Fraser, and Holler, *The Fuzzing Book*, free online and the best practical introduction.
- Google OSS-Fuzz and ClusterFuzz: the public reports show what continuous fuzzing finds at scale.
- The OpenSSL Heartbleed advisory, CVE-2014-0160. Short, and worth reading as a source rather than as a story.
- CMU 17-313 *Foundations of Software Engineering*, "Beyond Traditional Testing with Dynamic Analysis," the lecture this module is built from.

## 10. Self-check

1. A fuzzer runs for six hours against `EvaluationService` and reports no failures. Name two different reasons this tells you nothing about whether the aggregation is correct.
2. Rewrite `assertEquals(87.5, average.getAverageTotalScore())` as an assertion that holds for every student, every team, and every week.
3. A teammate adds `assert request.getWeek() != null;` at the top of a REST controller method. What is wrong with it, and what should be there instead?
4. Your project runs its whole suite green, and assertions are disabled in the test profile. What exactly have the assertions in the codebase been testing?
5. You ask an agent for tests covering `getPeerEvaluationAverage` and it returns twelve passing tests. What is the single question that tells you whether its oracle is real?

## Related

- [SE and What AI Changes](se-and-ai.md), for the green-tests story this module's circular-oracle section pays off.
- [Requirements traceability](traceability.md), for the verification edge: an invariant is one more way a requirement gets verified.
