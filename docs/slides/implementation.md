---
title: Estimate, Then Build With the Agent
module: implementation
week: 8
day: Monday
---

# Estimate, Then Build With the Agent

Week 8 · From an approved design to an estimate you can defend and code you can explain

## Where we are

![The documents so far, and this week's code](img/document-map-week-08.svg){ height="520" }

::: note
One minute, left to right. Weeks 3 and 4 wrote the requirements, week 6 the one architecture, week 7 a design-of-record per use case area; Project Pulse's first is not.md, approved last week. This week is the code box: estimate it, then build it from not.md. Week 9 tests it.
:::

## When can I use it? {.center}

::: ask
The reminder's design is approved. The instructor asks: when can I use it? What do you answer?
:::

::: note
Take two or three numbers from the room and write them on the board. Do not comment on them yet; they come back at the end. The design is Project Pulse's docs/design/not.md from week 7.
:::

## The old answer: count the code

::: steps
- A controller, a `SubmissionStatusService`, a scheduler change, a dialog, their tests.
- Lines of code, times hours per line.
- That is COCOMO (Boehm, 1981).
:::

::: ai
The agent writes all of it in one session. By that arithmetic, the answer is "this afternoon."
:::

## It is not this afternoon

::: cols
**20**
rows in the test list. Each one is a behavior a person has to see pass.
|||
**6**
open risks. One (80 emails during one request) can only be settled by measuring on staging.
:::

::: key
The agent made the typing free and left everything else.
:::

## Your feeling of speed is not data

::: steps
- Before: developers expected AI to make them **24% faster**.
- Measured: they took **19% longer**.
- After: they still believed they had been **20% faster**.
:::

::: note
METR's randomized controlled trial, July 2025: 16 experienced open-source developers, 246 issues in their own repositories. METR's 2026 follow-up suggests newer tools probably do speed people up, but its confidence intervals include no change, and METR calls its own data very weak evidence. The point for estimation survives either way: felt speed was off by about 40 points, in the flattering direction.
:::

## The hours moved

::: cols
**Pull requests**
154% larger, 98% more of them.
|||
**Review time**
up 91%.
:::

::: note
Faros AI telemetry, more than 10,000 developers on 1,255 teams, June 2025. A vendor's correlational data, not an experiment. It points the same way as METR: generation got cheap, and the cost moved to the person reading the result.
:::

## Three things that sound alike

| | Who owns it | Sounds like |
|---|---|---|
| Estimate | You | "3 to 5 hours" |
| Target | The client | "Before the midterm" |
| Commitment | The team | "On staging by Friday" |

::: warn
When the target and the estimate do not fit, change the scope, not the estimate.
:::

::: note
McConnell, Software Estimation, 2006. An estimate is a range because it is uncertain; a commitment is one date because someone plans around it. The range narrows as decisions get made (the cone of uncertainty, Boehm 1981), so a use case is estimated twice: a coarse range when it is written, for ordering and the release plan, and the three-part estimate once its design is approved, for the commitment. Agile does the same with story points at backlog refinement and task hours at sprint planning.
:::

## Every classic model: size times a rate

| Model | Size | Rate |
|---|---|---|
| Function points | What it does for users | Hours per function point |
| COCOMO | Lines of code | Effort per line |
| Velocity | Story points | Points per iteration |

::: key
The rates were measured when people wrote the code. Keep the size. Measure your own rate.
:::

::: note
Function points: Albrecht, 1979. Velocity breaks for a second reason: it assumes a stable pace, and the agent changes every few months. Expert judgment is still the most used technique and no worse than the models on average (Jørgensen, 2004), but only if the expert's experience includes working with an agent. Planning poker survives untouched: independent estimates still beat one anchored voice.
:::

## Where the hours go now

::: steps
- **Specify:** closing the gaps the agent would guess at.
- **Build and review:** driving the agent, reading every line of the diff.
- **Verify:** seeing each test row pass, end to end.
:::

::: joke
The first 90 percent of the code takes the first 90 percent of the time. The remaining 10 percent takes the other 90 percent. (Tom Cargill, Bell Labs)
:::

::: note
The joke is now literally true: the agent does the first 90 percent of the code in minutes, and the other 90 percent of the time is review and verification. Each part maps onto weekly activity report categories: specify is DESIGN or DOCUMENTATION, build and review is DEVELOPMENT, verify is TESTING or BUGFIX.
:::

## Size it by the test list

::: steps
- Each row is one behavior a person has to see working.
- It counts what the software must do, like a function point. It is not yet hours.
- First estimate: by analogy to a finished change of the same size.
- After two or three use cases: your own hours per row.
- The open risks set the width of the range.
:::

## The reminder, estimated

| Part | Basis | Hours |
|---|---|---|
| Specify | Questions test already run | 0.5 to 1 |
| Build and review | Every diff read against the diagrams | 1.5 to 2 |
| Verify | 20 rows, latency on staging | 1 to 2 |
| **Total** | By analogy: #76, 3.5 h | **3 to 5** |

::: note
No measured rate yet, so this is an analogy. The reference class is Project Pulse pull request #76, the invitation hardening: 884 lines, 23 files, two review rounds, about 3.5 hours from first commit to merge. The reminder is the same size, so most likely about 3.5. Do this live before running /implement on not.md. Commitment: on staging by Friday with the latency measured, or a message to the instructor by Wednesday saying why not. Compare with the numbers the room gave on the first slide: those were the coarse estimate, made without the design, the job story points do in agile. This one is the sprint-planning estimate, made with it.
:::

## Write it down before you build

On the issue:

```text
Estimate: specify 0.5–1 h, build and review 1.5–2 h, verify 1–2 h
```

In every weekly activity report line about it:

```text
UC-NOT-remind-non-submitters: reviewed the agent's diff against the sequence diagram
```

::: note
Project Pulse already stores planned and actual hours on every activity line (the Activity entity). The use case ID at the start is what lets you add them up later.
:::

## Calibrate

::: key
Calibration ratio = actual hours ÷ midpoint of the estimate.
:::

::: steps
- Estimated 8 to 16, logged 18: ratio 1.5.
- Next use case you would call 4 to 8: say 6 to 12.
- A slip you see coming goes to the client at the next meeting, not on the date.
:::

::: joke
Hofstadter's Law: it always takes longer than you expect, even when you take into account Hofstadter's Law.
:::

::: note
The ratio is how you take Hofstadter's Law into account for real. Track it per person and per team: six ratios is how a team finds out that review, not building, is where its hours go.
:::

## Graded on honesty, not accuracy {.center}

::: key
A ratio of 2.3 with a reason earns the same as a ratio of 1.0.
:::

::: warn
Logging fewer hours to look accurate is inflating a weekly activity report, and it is academic dishonesty.
:::

## In your team meeting, by Sunday

::: steps
- Your build-context issue gets an estimate before the agent builds.
- Your weekly activity report lines carry the use case ID.
- Checkpoints 2 and 3: estimate, actual, ratio, and one sentence on the biggest miss.
:::

## The agent copies what it sees {.center}

::: key
4 of Project Pulse's 266 backend classes declare a logger.
:::

::: ai
Ask the agent for a feature there, and it writes code that does not log. Whatever your codebase does by habit, the agent does at speed.
:::

::: note
Two different logger names among the four, LOGGER and log. The catch-all exception handler logs nothing. Nothing near the new code logs, so the new code will not either. Same mechanism as week 2's reviewee example. This is why the rules in today's lecture go into the charter, not into a prompt.
:::

## First run the tests

```text
./mvnw test        (mvnw.cmd test on Windows)
```

::: steps
- The agent learns a suite exists, and how to run it.
- It sees how big the project is.
- Testing becomes the default for the session.
:::

::: note
From Simon Willison's "First run the tests", this week's reading. Put the command in your agent charter so every session starts there. Project Pulse's backend suite takes several minutes; in class we run one test class to show the habit.
:::

## Test first, and watch it fail

::: key
A test that passes before the change proves nothing about the change.
:::

::: warn
If the agent writes the test and the code, it can pass its own exam. The expected value comes from the use case, not from the code.
:::

::: note
Red/green: the agent writes the test from the use case's postcondition or extension outcome, runs it, sees it fail, then writes the code. Where the expected value comes from is week 9's question, the oracle. Today only plant it.
:::

## Cognitive debt {.center}

::: key
Code your team accepted without understanding it.
:::

::: note
Kosmyna et al. named it for essays written with an assistant; it fits code better, because an agent writes more than a person can read. It compounds like technical debt: the next session builds on code nobody can explain, and the first defect in it is debugged from scratch.
:::

## Size the step to the review

| Commit | What goes in it |
|---|---|
| **Trunk** | What many paths depend on, or existing users rely on, or is hard to undo |
| **Security rule or migration** | Alone |
| **Each leaf** | New code reached only through the new feature |

::: key
The agent pauses once, after the trunk. You read it before the leaves are built.
:::

::: note
Not a pause after every step: a wrong trunk found late means rebuilding every leaf; a wrong leaf does not. All the commits still go in one pull request, read commit by commit.
:::

## The pause check {.center}

::: ask
Can you say what changed and why, without asking the agent?
:::

::: note
If not, read until you can. That is cognitive debt paid while it is small.
:::

## The reminder, in four commits

::: steps
- Trunk: SubmittableItem, WeekKeys, SubmissionStatusService, ReminderService, two new queries. **Pause.**
- The two route rules in SecurityConfiguration, alone.
- ReminderController and the dialog.
- The moved WeeklyReminderScheduler.
:::

::: joke
The trunk commit message the agent wanted: "Add some stuff." The one you merge: "Add SubmissionStatusService: who owes what this week."
:::

::: note
From not.md's class diagram. Project Pulse's /implement commits this way and pauses after the trunk. This is what we build live today, after /clear, so the session reads only the merged design.
:::

## The team's settings file

```json
{
  "permissions": {
    "deny": [
      "Bash(git push --force *)",
      "Bash(gh pr merge *)",
      "Bash(gh repo delete *)",
      "Read(**/.env)",
      "Read(**/.env.*)",
      "Read(**/secrets/**)",
      "Read(**/*.pem)",
      "Read(**/*.key)"
    ]
  }
}
```

::: note
.claude/settings.json, committed once so every teammate's Claude Code picks it up. The full file, with the PowerShell twins and the short force-push spelling, is on the Agent Setup page, section 10. Open it as a pull request so the team reviews what the agent may not do. The Read rules are the new part this week: anything the agent reads goes to the model provider. Test it yourself: ask the agent to read your .env and see it refused. Your TA opens this file at Checkpoint 2.
:::

## Before Friday

::: steps
- `Read` deny rules for your secrets in the team's `.claude/settings.json`, by pull request.
- Ask the agent to read `.env`. Watch it refused.
- Charter line: no dependency without a person's check.
- Checked at Checkpoint 2.
:::

## Code you did not write

::: steps
- Asked to document existing code, the agent writes down what it does, bugs included.
- A missing check, read back, becomes a requirement nobody chose.
- The client calls each one intended, corrected, or a defect. Not you.
:::

::: key
The code is evidence, never authority.
:::

::: note
For teams whose client handed them a codebase. The method's section "Starting from an existing codebase" has the four steps; Project Pulse's /design calls its version "design-as-built". Defects go to OPEN-ISSUES.md, not into the specification.
:::

## The catch-all logs nothing

```java
@ExceptionHandler(Exception.class)
Result handleOtherException(Exception ex) {
    return new Result(false, INTERNAL_SERVER_ERROR,
        "A server internal error occurs.", ex.getMessage());
}
```

::: warn
A NullPointerException in production: the user sees one sentence, the operator sees nothing, and the browser gets the raw exception message.
:::

::: note
Abridged from ExceptionHandlerAdvice; the module, 4.10, quotes it in full. Spring does not log an exception a handler has resolved. The fix is one line, LOGGER.error("Unhandled exception", ex), and dropping ex.getMessage() from the response. The full before and after is in the module, 4.10.
:::

## The logging rule, for your charter

::: steps
- One logger per class, one name.
- error: someone must act. warn: degraded. info: a business event. debug: development.
- Parameterized: "Sent {} of {} reminders", never concatenation.
- Every catch that does not rethrow logs the exception object.
- Identifiers, never content: no secrets or passwords; a person's ID, not their email or scores.
:::

## Review what was logged, not only whether

```java
LOGGER.error("Could not send the weekly reminder to {} in section {}",
        student.getEmail(), section.getSectionName(), e);
```

::: ask
Right level, parameters, the exception object. And every failed student's email address in the log. Acceptable?
:::

::: note
From Project Pulse's WeeklyReminderScheduler today. It follows four of the rules and breaks the fifth: every failed student's email address goes into the log. Fix: `student.getId()`; the operator looks the address up. CO-ferpa. Catching this is the reviewer's job, because the agent copied it from the code around it.
:::

## Several agents at once

::: key
Safe exactly where the decisions they would make are already written down.
:::

::: steps
- Side task: it searches and reports; it edits nothing.
- Writer and reviewer: a fresh session reviews the diff.
- Fan-out by leaf: after the trunk merges.
:::

::: warn
No more agents than pull requests you will review well today.
:::

::: note
Reading: module 4.11. Start both reminder leaves before the trunk merges and each agent writes its own SubmissionStatusService, with two definitions of "has not submitted". Never split one use case's layers across agents.
:::

## Before your agent builds the slice

::: steps
- Charter: the command that runs your tests.
- Charter: "write the test first and show it failing."
- Charter: your logging rule.
- Build trunk first; read it before the leaves.
:::

## Checkpoint 2: Oct 23

::: steps
- The slice runs from a tagged release, `v0.1.0`, with release notes.
- `.claude/settings.json` denies reads of your secrets.
- The charter: the dependency rule, and never remove the `Co-Authored-By` trailer.
- The calibration table.
- The release plan: a Release value on every traceability row.
:::

::: note
The full checklist is on the Project page, under Checkpoint 2. The tag and the trailer rule come from week 2's "Knowing exactly what you built"; the settings file is on the Agent Setup page, section 10. Teams leave Checkpoint 2 with Checkpoint 3's two reliability items, one measured SLO and one degradation test, and start them that week.
:::
