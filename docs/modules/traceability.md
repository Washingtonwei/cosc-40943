# Requirements Traceability

**Slides:** [Requirements Traceability](../slides/traceability.html) (the fast version).

> **Purpose (one line):** keep every use case honest end to end, tracing it forward (is it built and tested?) and backward (why does this code exist?), say before a requirement changes what the change will touch, and place every use case in the release it ships in.

## 1. Learning objectives

By the end of this module, a student can:

1. Trace a use case forward to its design, code, and tests, and a file backward to the requirement that authorized it, in the team's `traceability.md`.
2. Mark a row Verified only when a named test exercises its main flow and extensions.
3. Classify a divergence between the specification and the code as one of three shapes, repair it the right way, and record the ones not yet repaired in a register.
4. Run an impact analysis before a change: list what a changed requirement touches, hand that list to the agent as the change's scope, and review the pull request against it.
5. Split traceability upkeep three ways: what to delegate to the agent, what to check with a deterministic tool, and what to keep human.
6. Give every row a Release, forecast whether the MVP still fits, and change the scope with the client when it does not.

## 2. Where it fits

- **Prerequisites:** [Spec-Driven Requirements](spec-driven-requirements.md), where every traceable item gets its stable ID and the first two tables of `traceability.md` are written; [AI-Assisted Implementation](implementation.md), whose estimates the release plan is built from; and [Code Review](code-review.md), which reviews a change against its contract.
- **Leads into:** testing (what makes a Verify cell true), CI/CD (running the checks on every pull request), and maintainability, where the payoff lands.
- **How it's taught:** two lecture days in week 9. Wednesday covers the spine, forward and backward, the three drift shapes, and the release plan. Friday opens with impact analysis on Project Pulse, before testing. After that it is practised every week on the team's growing codebase. You keep the spine current; the rest of the graph ([4.4](#44-the-rest-of-the-graph)) is shown so you recognise it, not so you maintain it.
- **Course outcome it delivers:** [maintaining living traceability from specification to design to code to test, and keeping it honest with tooling](../syllabus.md#learning-outcomes) (outcome 8).

## 3. Motivation

**The problem, on Project Pulse:** an agent can turn an approved use case into working code in minutes, so the codebase grows faster than anyone's memory of what maps to what. Without a durable map, "which code satisfies this use case?" and "why does this class exist?" become unanswerable, and those are the questions maintenance depends on.

**Why it matters more with AI.** Traceability is the antidote to the specific way AI-generated code rots. A human who writes code carries the "why" in their head; that tacit memory is what lets them maintain it later. An agent doesn't carry that memory across sessions, and it generates plausible code faster than any human, so unmapped code accumulates faster than on any human team. The traceability matrix is that lost memory, externalized into a durable artifact. So traceability isn't just as important for vibe-coded projects, it's arguably more important than it ever was for hand-written code, precisely because AI removed the natural friction that used to cap how fast un-understood code piled up. In ISO-25010 terms it buys you analysability (locate what a change affects) and testability (every requirement has a verifying test), the two maintainability sub-characteristics vibe coding destroys first.

**The evidence.** For years the benefit was taken on faith, and practitioners doubted it. Then it was measured. In a controlled experiment, 71 developers doing real maintenance tasks on unfamiliar systems were about 24% faster with traceability and produced about 50% more correct solutions (Mäder and Egyed 2015). Across 24 open-source projects, components with more complete traceability had lower defect rates (Rempel and Mäder 2017).

**Why we can finally afford it.** Traceability is not a new idea. The literature always prescribed it; in practice it was done ad hoc and after the fact, or not at all (Cleland-Huang et al. 2014). Maintaining the matrix was tedious, error-prone, unrewarding labor, and writing code was more fun. In six open-source projects, only about 60% of commits even named the issue they worked on (Rath et al. 2018). The research community's answer was *ubiquitous* traceability: links produced as a by-product of the work, not as a separate chore. An agent works tirelessly with text and does not lose patience, so the old objection "a stale matrix is worse than none" flips from a reason to skip traceability into a reason to *delegate its upkeep*. Once the human cost of a discarded practice collapses, it becomes worth reinstating.

**The honesty rule.** Cheap to maintain is not the same as safe to trust. Language models now recover trace links better than the older retrieval tools, and their authors still say the approach is not ready for practice (Fuchß et al. 2025): some share of the links are wrong, and nothing in a wrong link looks wrong. An agent can produce plausible but wrong links faster than any human, so *unverified* traceability rots faster than the hand-drawn kind ever did. What makes it safe is a three-way split: the agent does the upkeep; **deterministic tooling** does the checking (do the IDs resolve? does every requirement have a verifying test?); a human keeps the *meaning* (what should trace to what; is this untraced code dead or a missing requirement). Letting the agent judge its own links brings the drift back as confident, false assurance.

## 4. Core concepts

### 4.1 The spine: one row per use case

The part you keep is a chain of four links: **use case → design → code → test**. In `docs/traceability.md` it is table 3, one row per use case and one per functional requirement that no single use case owns (`FR-<AREA>-<slug>`, such as a scheduled reminder). The row is added the day the use case is written, not the day it is built.

Two columns carry the state, kept apart on purpose so that built and tested never blur into one "done":

- **Build:** `❌ Not started`, `📐 Designed` (the design pull request merged), `🟡 In progress`, `✅ Built`.
- **Verify:** `✅ Verified`, `🟡 Partial` (the Tests cell names the gap), `🔎 None`, or blank while nothing is built.

Everything above the use case (feature, business objective) is already in table 1, and the use case inherits its objective through its feature. That is why the row has no objective column.

### 4.2 Forward and backward

The same row answers two questions, and they start at opposite ends.

**Forward, coverage:** start at a requirement and ask whether it is built and tested. Project Pulse's [`UC-EVA-submit-evaluation`](https://github.com/Washingtonwei/project-pulse/blob/main/docs/traceability.md) row names `SubmitTeamsEvaluations.vue`, `EvaluationService.addPeerEvaluation`, and the tests that pin each extension, and reads `✅ Built`, `✅ Verified`. A requirement with no row, or a row that stops at Design, is promised scope that does not exist yet.

**Backward, justification:** start at a piece of code and ask which requirement authorized it. `WeeklyReminderScheduler` traces to `FR-NOT-weekly-reminder`, a row of its own because no use case owns a job that runs on a timer. Code that no row names is either dead or a decision nobody wrote down, and which one it is takes a human ([4.5](#45-three-ways-the-specification-and-the-code-drift-apart)).

Both directions matter: forward finds work missing, backward finds work nobody asked for. ISO/IEC/IEEE 29148 requires both.

### 4.3 A requirement with no test is not traced

The last link, test → use case, is the one that closes the loop, and it is the one teams fake. A row reads `✅ Verified` only when you can name a test that exercises the main flow and every extension, and the test passes. Project Pulse's `UC-WAR-student-war-report` is `✅ Built` and `🟡 Partial`, and its Tests cell says why: "no dedicated period integration test". That is an honest row. A row that reads Verified because some test file exists is not.

The check is mechanical: open each test the row cites and confirm it exercises that use case, extensions included. An agent can do the opening and the reporting. It cannot be the only one who does it, because the agent that wrote the row is the one reporting that the row is right.

### 4.4 The rest of the graph

Project Pulse's [`traceability.md`](https://github.com/Washingtonwei/project-pulse/blob/main/docs/traceability.md) carries more than the spine, and you will meet all of it in industry. A second axis runs in parallel for quality attributes (quality attribute → quality scenario `QS-<slug>` → test), because a response-time requirement is never verified through a use case. Each business objective traces to a success metric, which asks whether the objective was *achieved*, not just built. And its business-rule index, which lists every requirement that cites each `BR-*`, is **generated** from the use cases' Business Rules fields, never edited by hand. The full model is in [The Method](../method.md#the-traceability-model). Recognise these; your team keeps only the spine and the two week 4 tables.

### 4.5 Three ways the specification and the code drift apart

The backward question often gets the answer "none", and that answer comes in three shapes, repaired three different ways.

| Shape | What you see | Repair |
|---|---|---|
| Specification right, code behind | A rule is written down and the code does not enforce it | Conform the code |
| Code right, specification stale | The document describes behavior the system no longer has | Amend the document |
| Neither says anything | The code made a decision no document records | Decide it, then write it down |

**Specification right, code behind.** `FR-NOT-weekly-reminder` was amended on 2026-10-03 to remind only the students who still owe something, as `BR-submission-owed` defines it. `WeeklyReminderScheduler.sendWeeklyReminders` kept emailing every student in the course section on the due day, and its tests checked that it did. For three weeks the row said so in its Code cell and read `📐 Designed`, not `✅ Built`, so the gap was traced rather than hidden. It closed on 2026-10-25, when pull request [#102](https://github.com/Washingtonwei/project-pulse/pull/102) brought the scheduler in line and moved the row to `✅ Built` and `✅ Verified`: the code and its row changed in one pull request.

**Neither says anything.** `getPeerEvaluationAverage` ends in `.average().orElse(0.0)`, so a student nobody evaluated is reported with an average of `0.0`, the same number as a student her teammates all rated zero. No business rule covers the empty case. Trace backward from that `0.0` and you arrive nowhere. It is not a violation, because there is nothing to violate. Someone decided in code that "not evaluated" and "rated zero" are the same value, and no document records the decision or what it does to the section's weekly report.

The third shape is the one that scales badly once an agent is writing the code. The first two are inconsistencies, and an inconsistency can be found by machine, because two artifacts exist and they disagree. The third produces no inconsistency at all: only one artifact ever spoke. An agent handed an under-specified use case always picks something, picks it in seconds, and emits code indistinguishable from code implementing a decision you actually made. That is how an implementation quietly becomes the specification, and it is the reason to ask the backward question out loud rather than assume the forward map covers you.

You will meet the opposite advice, and it is good advice. Guidance on reading an unfamiliar codebase tells you to treat documentation as a starting point rather than truth, because it is often out of date. That is the other half of this course's position, not its opposite. Neither artifact is true by default: a contract can be behind the system, and a system can be wrong about the contract. Which of the two is wrong is decided per item, and deciding it is what a register is for.

**Keep a register.** Project Pulse reconciles the two in [`docs/requirements/OPEN-ISSUES.md`](https://github.com/Washingtonwei/project-pulse/blob/main/docs/requirements/OPEN-ISSUES.md), under a "Doc ↔ Code Gap Analysis" heading. Each entry names the rule, the `file:method` that diverges from it, and the direction the divergence will be resolved. It is not a bug list: each entry is a claim about *which of the two artifacts is currently wrong*, which is why several resolve by changing the document. OI-24 shows the whole cycle. On 2026-06-20 the client decided that `BR-evaluation-submission-window` binds edits as well as first submissions; `updatePeerEvaluation` checked nothing, so a student could rewrite an old evaluation forever. The register held that gap for 82 days, until both paths went through one check on 2026-09-10 and the entry closed. A divergence you have decided not to fix yet is traced. A divergence nobody noticed is not.

### 4.6 Impact analysis: what a change touches, before you make it

Forward and backward ask about what exists. Every change request asks a third question: **if this requirement changes, what else has to?** Answering it before anyone edits code is **impact analysis**, and the matrix turns it from a memory test into a lookup.

**On Project Pulse.** Suppose the client asks for two weeks, not one, to finish a peer evaluation. That changes one rule, `BR-evaluation-submission-window`.

1. **Read the matrix from the changed node.** The business-rule index lists two use cases that cite the rule. `UC-EVA-submit-evaluation` is built, and its row names the code (`SubmitTeamsEvaluations.vue`, `EvaluationService.addPeerEvaluation`) and the tests that pin the window (`testAddPeerEvaluationNotForPreviousWeek`, `testUpdatePeerEvaluationAfterTheSubmissionWindowClosed`, and their integration twins). `UC-NOT-remind-non-submitters` is built too, since 2026-10-25: its row names `ReminderController.sendReminders`, the dialog, and `ReminderIntegrationTest`, and the reminder is always for the previous week, which the server recomputes and checks at send time. Two weeks earlier the row read `📐 Designed`, and this change would have been a few minutes' edit to [`design/not.md`](https://github.com/Washingtonwei/project-pulse/blob/main/docs/design/not.md). Now it is code and tests. A change caught at design is cheap; the same change after the build is not.
2. **Search for the ID.** The index records which requirements cite a rule, not which rules cite each other. A search of `docs/` for `BR-evaluation-submission-window` adds two rules that lean on it, `BR-active-weeks` ("each active week is evaluated during the *following* calendar week") and `BR-evaluation-editable-until-close`, and the use case's extension 1b, whose message tells the student about "its one-week window".
3. **Hand the agent the list as the scope.** The issue lists every ID and file from steps 1 and 2. The agent's job is the reach that no requirement names: `WeekKeys.previousWeek`, which the evaluation window, the reminder, and the scheduled job share, and `getPreviousWeek()` in the frontend's `utils/week`, which decides which week the form opens on.

**The list is also the review's checklist.** A pull request that touches a file outside the list either found an edge the matrix lacks (add it to the matrix) or wandered (send it back). A file on the list that the pull request left alone needs a reason. Before the change, the IDs steer the agent; after it, the matrix checks what came back.

**The list surfaces questions nobody has answered.** Two weeks means two weeks are open at once. Which one does the form open on? Is a reminder about the older one or the newer one? Does "cannot be made up" still mean anything? No document says, so an agent told to "make it two weeks" will answer all three silently, and that is the third drift shape, made on purpose. Those questions go to the client first. The change starts once the answers are written down.

**The length of the list is the change's size.** A rule cited by two use cases is a small change. `BR-role-based-access`, cited by 41, is a project-wide one, and the index makes that visible before anyone estimates it.

### 4.7 From estimates to a release plan

An estimate answers "when can I use this one?" The client's next question is "what will I have in December?" Answering it takes a **release plan**: every use case placed in the release it ships in. Agile planning has always done this with stories and velocity (Beck and Fowler 2000; Cohn 2005). The course keeps the idea and changes the units.

**It is a column, not a document.** Your `traceability.md` already has one row per use case (and per non-use-case FR) with its Build and Verify state. The plan is one more column, **Release**: `v0.1.0` (the proving slice), `v0.2.0` (Checkpoint 3), `v1.0.0` (the December MVP), `Spring`, or `Out`. Plan and progress share a row, so they cannot disagree, and an empty cell is work nobody has planned. Your client agrees to scope by feature in vision and scope's MVP Scope section; the column carries that agreement down to use cases.

**Placing the rows.** Risk first, for the reason your proving slice went first ([the spiral model](se-and-ai.md#spiral-let-risk-choose-the-next-step)): a wrong decision found in week 9 is cheap, and in week 14 it is not. Then what the client needs first, then dependencies. When something goes ahead of risk, the pull request that changes the column says why: the column holds the decision, and git holds the reason.

**Project Pulse's plan.** Project Pulse shipped up to `v1.5.0` without a release plan. Its [Release column](https://github.com/Washingtonwei/project-pulse/blob/main/docs/traceability.md#release-legend) starts with the work that is left:

| Release | What ships | Why there |
|---|---|---|
| `v1.6.0` | The reminders: on-demand (`UC-NOT-remind-non-submitters`), and the scheduled one brought in line with `BR-submission-owed` | Built in week 8 and merged 2026-10-25 ([#102](https://github.com/Washingtonwei/project-pulse/pull/102)); the next tag |
| `v1.7.0` | The rest of the requirements editor: artifact and link screens, comments, review, export | Backends built and tested; the client wants the editor finished first |
| `v1.8.0` | The first AI assistant end to end: `UC-AI-critique`, the proposal loop, its settings, the model proxy | The riskiest work: the first model call, with the outage scenario measured |
| `v1.9.0` | ReqLint and the tutor | The tutor explains ReqLint's findings, so it follows ReqLint |
| `v2.0.0` | The other six assistants | The Fall 2027 classroom deployment |

Risk alone would put `v1.8.0` before `v1.7.0`. The client chose otherwise, and the plan records that trade instead of hiding it. Writing the column also exposed a disagreement: the vision listed real-time co-editing as out of the MVP, while traceability showed it as unstarted work. The use case's own Status line already said Deferred, so that line settles it, and its Release cell stays empty: one fact, one owner.

**The forecast.** A use case that is not designed yet has no test list, so it carries its [coarse estimate](implementation.md#41-an-estimate-is-a-range-made-twice), made by [planning poker](implementation.md#42-where-the-hours-go-now) from its main scenario and extensions and written on its issue; when its design is approved, the refined estimate replaces it. Then:

> **Hours still needed** = the sum of the estimate midpoints of every unfinished `v1.0.0` row × your team's calibration ratio

Use the coarse ratio for rows still on their coarse estimate. Until your team has closed a use case that had one, use the ratio from your refined estimates.

Compare that with the hours your team will have before the MVP demo, judged from what your weekly activity reports show you actually work. If the plan does not fit, move rows out of `v1.0.0` with your client at the next meeting. This is the [estimate's rule](implementation.md#41-an-estimate-is-a-range-made-twice) in practice: when the estimate and the target disagree, change the scope, not the estimate. Write the result as one line under your [calibration table](implementation.md#44-recording-and-calibrating):

`Forecast: 6 rows left in v1.0.0, 38 to 60 h at ratio 1.4; about 70 h available. Fits, with no slack for the high end.`

Cross-check it by counting. If your team closes about 1.5 use cases a week and 6 rows remain, that is four weeks whatever the hours say. When the count and the hours disagree badly, one of them is fooling you; find out which before you talk to the client.

Revise the column at every use-case close ([the method, Phase C](../method.md#phase-c-fan-out-per-use-case)), and recompute the forecast whenever the ratio moves.

## 5. The AI-native lens

- **Delegate to AI:** updating a use case's row in the same pull request that builds it; running the checks and reporting what fails; drafting an impact list from the matrix and a search of `docs/`, then finding the code no document names; drafting the Release column and adding up the forecast.
- **Keep human:** what *should* trace to what; whether untraced code is dead or a missing requirement; which artifact is wrong when they disagree; the questions an impact list raises, which go to the client; and the cut line, which use cases leave `v1.0.0`.
- **Context to supply:** the stable IDs and the documents that define them; for a change, the impact list as the scope. The agent cannot invent a consistent ID space; it has to be given one.
- **How to verify:** run the checks and read the report; spot-check one row in both directions by opening each end; review a change's pull request against its impact list.

## 6. Risks & mitigations

| Risk (classic + AI-introduced) | Human judgment that catches it | Mitigation |
|---|---|---|
| **Classic:** the matrix goes stale because rows are updated "later", and commits stop naming what they work on (about 40% did not, in Rath et al. 2018) | A reviewer who asks where the row changed | The row changes in the same pull request as the code; Build and Verify are checked at every use-case close |
| **AI-introduced:** asked to fill the matrix, the agent populates every cell, and some links are invented | Opening the document at the other end of a link you did not write | Blank cells stay blank; spot-check one row both ways per close; never let the agent's report be the only check |
| **AI-introduced:** a change request goes straight to the agent, which edits beyond what the requirement reaches and answers the open questions on its own | Writing the impact list before the agent starts, and taking its questions to the client | The issue carries the list; the review compares the diff with it |

## 7. Hands-on (studio + optional individual assignment)

**In class (Friday):** the two-week change from [4.6](#46-impact-analysis-what-a-change-touches-before-you-make-it), done in pairs from Project Pulse's live matrix: the list from the matrix, what a search adds, and the questions for the client. Then compare your list with the instructor's.

**Team, own project:**

- **Spine:** every use case and non-use-case FR has a row in table 3, with Build and Verify matching the code. Update the row in the pull request that changes its state.
- **Release plan:** by Checkpoint 2, every row has a Release value, revised by pull request at every use-case close. At Checkpoint 3, one forecast line under the calibration table.
- **Impact list:** the next time your client changes a requirement or a rule, the issue for the change carries its impact list (the IDs and files from the matrix, what a search added, and the questions you took to the client), and the pull request's description says which files outside the list it touched and why. Checked at [Checkpoint 2](../project.md#checkpoint-2-checklist).

**Individual assignment:** in *Add a use case* (assignment 3, due Fri Oct 30), the agent's use case gets its row in table 3, and its Verify cell names the tests that make it true.

## 8. Summary / key takeaways

- Keep the spine: use case → design → code → test, one row each, with Build and Verify kept apart.
- Forward finds what is missing; backward finds what nobody asked for. A requirement with no named test is not traced.
- Classify each divergence before repairing it, and register the ones you have not repaired. The dangerous one is the decision nobody wrote down.
- Before a requirement changes, list what it touches from the matrix and a search. That list is the agent's scope, the review's checklist, and the source of the client's questions.
- The agent does the upkeep, a tool does the checking, and the meaning stays human.
- A release plan is a Release column in your traceability matrix. Revise it at every close; when the forecast does not fit, change the scope with your client.

## 9. Key papers & further reading

- Gotel, O. C. Z., and Finkelstein, A. C. W. "An Analysis of the Requirements Traceability Problem." ICRE 1994. Why traceability fails in practice: the links nobody records at the time.
- Ramesh, B., and Jarke, M. "Toward Reference Models for Requirements Traceability." *IEEE Transactions on Software Engineering* 27(1), 2001.
- Cleland-Huang, J., Gotel, O., and Zisman, A., eds. *Software and Systems Traceability*. Springer, 2012.
- Bohner, S. A., and Arnold, R. S. *Software Change Impact Analysis*. IEEE Computer Society Press, 1996.
- ISO/IEC/IEEE 29148:2018. *Systems and software engineering: Life cycle processes, Requirements engineering.* The bidirectional traceability requirement.
- Beck, K., and Fowler, M. *Planning Extreme Programming*. Addison-Wesley, 2000. Release planning with stories and velocity.
- Cohn, M. *Agile Estimating and Planning*. Prentice Hall, 2005.
- Mäder, P., and Egyed, A. "Do Developers Benefit from Requirements Traceability When Evolving and Maintaining a Software System?" *Empirical Software Engineering* 20(2), 2015. The controlled experiment: faster, and more often right.
- Rempel, P., and Mäder, P. "Preventing Defects: The Impact of Requirements Traceability Completeness on Software Quality." *IEEE Transactions on Software Engineering* 43(8), 2017.
- Cleland-Huang, J., Gotel, O., Huffman Hayes, J., Mäder, P., and Zisman, A. "Software Traceability: Trends and Future Directions." Future of Software Engineering (FOSE), ICSE 2014. The case for traceability as a by-product of the work.
- Rath, M., Rendall, J., Guo, J. L. C., Cleland-Huang, J., and Mäder, P. "Traceability in the Wild: Automatically Augmenting Incomplete Trace Links." ICSE 2018.
- Fuchß, D., et al. "LiSSA: Toward Generic Traceability Link Recovery through Retrieval-Augmented Generation." ICSE 2025. Language models recovering trace links, and how far that is from practice.

## 10. Self-check

1. `ExportService.java` appears in no row of your matrix. Name the two things it could be, and who decides which.
2. A row reads `✅ Verified` and its Tests cell says `EvaluationServiceTest`. What do you open, and what has to be true for the cell to stand?
3. Your design says a deleted team's reports are kept; the code deletes them; nobody remembers deciding either way. Which drift shape is it, and what do you do first?
4. Your client changes a rule that one use case cites. What does the matrix give you, what does a search for the rule's ID add, and what does neither give you?
5. The agent's pull request for that change touches a file that is not on your impact list. What are the two possibilities, and what do you do about each?
6. Five unfinished use cases remain in `v1.0.0`; their estimate midpoints add up to 30 hours, your team's ratio is 1.5, and your team will have about 40 hours before the demo. Does the plan fit? What do you tell your client, and when?

## Related

- [Schedule](../schedule.md): when the traceability lectures land, and the weekly practice after them.
- [Senior Design Project](../project.md): the traceability matrix as a graded deliverable.
- [AI-Assisted Implementation](implementation.md#41-an-estimate-is-a-range-made-twice): the estimates and calibration ratio the release plan is built from.
- [Code Review](code-review.md): reviewing a change against its contract, which for a changed requirement includes its impact list.
- [SE and What AI Changes](se-and-ai.md): why the economics of rigor inverted, which is the argument this module rests on.
- [The Method](../method.md#the-traceability-model): the full traceability model this module teaches a subset of.
