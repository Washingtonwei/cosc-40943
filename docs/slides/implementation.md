---
title: Building With the Agent
module: implementation
week: 8
day: Monday
---

# Building With the Agent

Week 8 · From an approved design to code you can explain

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
Abridged from ExceptionHandlerAdvice; the module, 4.4, quotes it in full. Spring does not log an exception a handler has resolved. The fix is one line, LOGGER.error("Unhandled exception", ex), and dropping ex.getMessage() from the response. The full before and after is in the module, 4.4.
:::

## The logging rule, for your charter

::: steps
- One logger per class, one name.
- error: someone must act. warn: degraded. info: a business event. debug: development.
- Parameterized: "Sent {} of {} reminders", never concatenation.
- Every catch that does not rethrow logs the exception object.
- Never secrets, tokens, passwords, or student records.
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
From Project Pulse's WeeklyReminderScheduler today. It follows the rule, and it also writes student email addresses into the log. Whether that is acceptable is the client's privacy constraint to decide (CO-ferpa); asking is the reviewer's job.
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
Reading: module 4.6. Start both reminder leaves before the trunk merges and each agent writes its own SubmissionStatusService, with two definitions of "has not submitted". Never split one use case's layers across agents.
:::

## Before your agent builds the slice

::: steps
- Charter: the command that runs your tests.
- Charter: "write the test first and show it failing."
- Charter: your logging rule.
- Build trunk first; read it before the leaves.
:::
