# 2. Spec a feature

**Due Friday, October 2, at the beginning of class.** Individual work. 4% of your grade.

Project Pulse emails you a reminder every Monday telling you your weekly activity report is due. It emails you whether or not you already submitted it. If you filed on Sunday night, you still get the Monday email, because the code that sends it never asks.

This week you specify the feature that fixes that, and then you find out what an agent does with what you wrote.

You are not being asked to build it. You are being asked to write a use case precise enough that somebody else, or something else, could build the right thing from it without coming back to ask you a question.

## The gap, in the actual code

Open [`WeeklyReminderScheduler.java`](https://github.com/Washingtonwei/project-pulse/blob/347d48215e1d0770c09ef2d97648d1f553fbf908/backend/src/main/java/team/projectpulse/system/WeeklyReminderScheduler.java) in the real Project Pulse. That link is pinned to a commit so it keeps saying what this page says it says; Project Pulse is a live repository and `main` moves. The reminder loop is this:

```java
for (Student student : section.getStudents()) {
    String html = "Hello %s,<br><br>%s".formatted(student.getFirstName(), sharedBody);
    try {
        this.emailService.sendReminderEmail(student.getEmail(), "ProjectPulse Submission Reminder", html);
        sent++;
    } catch (RuntimeException e) {
        LOGGER.error("Could not send the weekly reminder to {} in section {}", student.getEmail(), section.getSectionName(), e);
    }
}
```

Every student in the course section, every time. The `try` handles an address the mail server rejects, and there is a comment above the loop explaining why. Nothing anywhere checks whether this student has already submitted anything.

Three things are missing, and they are one feature:

- Nobody can see **who has not submitted** this week.
- Nobody can send a reminder **to only those students**.
- The scheduled reminder itself does not skip the students who are already done.

No use case in `docs/requirements/use-cases.md` covers any of it. It is not in `OPEN-ISSUES.md` either. There is nothing to look up, which is the point.

## Your assignment repository

You do **not** work in the public [Project Pulse](https://github.com/Washingtonwei/project-pulse) repository. Fork this one:

**<https://github.com/tcu-cosc-40943/spec-a-feature>**

Same two settings as last time, and they still go wrong the same two ways.

!!! warning "1. Turn Issues on in your fork"
    A new fork has its **Issues tab disabled**. Switch it on: **Settings → General → Features → Issues**. Do not file on the class repository instead; your issue counts only in your fork.

!!! warning "2. Point your pull request at your own fork"
    GitHub sets the **base repository** to `tcu-cosc-40943/spec-a-feature`. Change it to **your own fork**, base branch `main`. Miss it and you have opened your pull request against the class repository, in front of everyone, and it is not your submission.

## What you submit

One pull request **in your own fork**, on a branch, linked to one issue you opened there. **Submit the pull request's URL to TCU Online** by the beginning of class on Friday, October 2.

Your pull request changes exactly two files:

| File | What you add |
|---|---|
| `docs/requirements/use-cases.md` | Your use case, written in the template every other use case in that file uses |
| `docs/requirements/business-rules.md` | Any new `BR-*` your use case needs, if it needs one |

Everything else, the build-context and your evaluation of the agent, goes in the **pull request description**.

## Part 1: Decide what the feature actually is

Before you write a line, make three decisions. They are the assignment; the writing is how you record them.

**Which use case is it?** "Nudge the non-submitters" could be one use case or three. The instructor seeing a list, the instructor sending a nudge, and the scheduler skipping the finished are not obviously the same actor doing the same thing at the same time. Larman's three tests from week 4 apply. Pick a scope and defend it in one sentence.

**Which area does it live in?** Every use case ID is `UC-<AREA>-<slug>`, and the area is baked in permanently. Read the areas already in use. `WAR`, `EVA`, `SEC`, `STU`, `TEA`, `INS`. None of them is obviously right for a notification, and there is no `UC-NOT` area, though the specification does carry `FR-NOT-weekly-reminder`. Choose, and say why in the pull request. There is no answer key here; there is a defensible choice and an undefensible one.

**What does "has not submitted" mean?** This is the decision the whole feature turns on, and the one an agent will get wrong quietly. A weekly activity report and a peer evaluation are different artifacts on different deadlines. Decide, precisely, and write it down.

## Part 2: Write the use case

Use the template that every use case in `docs/requirements/use-cases.md` already follows. Copy the shape from a neighbour, `UC-EVA-submit-evaluation` is a good one to read first. You need all of it: ID and name, primary actor, trigger, description, preconditions, postconditions, main success scenario, extensions, priority, frequency of use, business rules, associated information.

**Your extensions are where the grade is.** The main success scenario is the easy half and everybody writes it correctly. The edge cases are the specification. At minimum, decide what your use case does about each of these, because Project Pulse already has rules that bite:

- A student who is **not assigned to a team** cannot submit a peer evaluation at all (`BR-team-assignment-required`). Is she a non-submitter? Does she get nudged?
- The week's **submission window has closed**, so the nudge cannot help. Do you send it anyway?
- The week is **not one of the section's active weeks** (`BR-active-weeks`).
- The student **submitted, then deleted** what they submitted.
- The instructor nudges the same student **four times in one morning**.
- The mail server **rejects the address**, which the existing scheduler already handles by logging and stepping over.

**Cite business rules, do not restate them.** If your use case needs a rule that does not exist yet, write it in `business-rules.md` with a new `BR-<slug>` and cite it. A nudge that can be sent without limit is a policy decision, and policy lives in a business rule, not buried in a step.

**Respect the boundaries that already exist.** Who is allowed to see who has not submitted? Project Pulse scopes an instructor to her course section (`BR-section-scoped-access`) and a student to her own team (`BR-team-scoped-access`). Submission records are student records, and the course treats them under `CO-ferpa`. If your use case lets the wrong person see the list, it is wrong, and no amount of good prose fixes it.

## Part 3: Turn it into a build-context, and evaluate what you get

Now the week 5 move, on your own writing.

1. **Assemble the build-context.** Write it as your issue: the use case ID you just created, the `BR-*` rules it cites, the file paths you expect to change, and nothing else. **Cite, do not paste.** If you find yourself copying your use case into the issue, that is the defect week 5 warned you about.
2. **Hand it to an agent** and ask it, *before it writes any code*, to state every assumption it would have to make to build this. Plan mode does this for you if your agent has it.
3. **Read the list for what you never told it.** Every assumption you did not supply and did not intend is a gap in your specification.
4. **Fix the specification, not the agent.** Each gap goes back into the use case, into a business rule, or into the issue, whichever is its right home. Commit that fix. The commit history is the evidence you did this.

Then, in the pull request description, answer four things:

1. **Your three decisions from Part 1**, with the one-sentence defence of each.
2. **What the agent assumed that you had not told it.** Quote two of them. Say which of the three homes each gap belonged in, and why.
3. **What you deliberately left for the agent to derive**, and why guessing it wrong would not violate a requirement. This is the pinning litmus, and the answer "I specified everything" is a wrong answer.
4. **One thing the agent assumed that was better than what you wrote.** There will be one. Say what you changed.

## How it is graded

| | Points |
|---|---|
| **The use case.** Is it in the template, at a defensible scope, with a main scenario that is correct and unambiguous? | 25 |
| **The extensions and the rules.** Did you find the real edge cases, decide each one, and cite rather than restate the rules that bind them? | 30 |
| **The three decisions.** Scope, area, and the definition of "has not submitted", each defended rather than asserted. | 20 |
| **The gap analysis.** Did you actually run it, find real gaps, and route each to the right home, with commits that show it? | 20 |
| **Mechanics.** Branch, linked issue, clean commits, readable writing. | 5 |

!!! important "Not the bar: the agent produced something"
    An agent will write you a plausible use case for this in ninety seconds. It will have a clean main success scenario, no useful extensions, no cited business rules, and a definition of "has not submitted" that it invented and did not tell you about. That is the floor. The grade is for the decisions you made, the edge cases you found, and whether you can defend the area code you chose. Expect to be asked in class.

This is a **Writing Emphasis** course and this is the assignment where that is literal. A use case is technical writing with a reader who will build what it says. Ambiguity here is not a style problem, it is a defect that ships.

**Leave the pull request open. Do not merge your own.**

Your fork is public, and so is everyone else's. Read your classmates' work if you want, after you have filed your own. What you cannot do is submit a use case you did not write, or a gap analysis you did not run. That is the [explanation test](../ai.md), and it is asked in class.

Late work takes a 15% penalty per day and is not accepted more than two days late. See the [syllabus](../syllabus.md#late-work).

## Related

- [Context Engineering](../modules/context-engineering.md): the build-context, the questions test, and the pinning litmus in Part 3.
- [Requirements as the Contract](../modules/spec-driven-requirements.md): use cases, extensions, and business rules.
- [Use case style guide](https://github.com/Washingtonwei/use-case-style-guide): the standard your use case is reviewed against. Give it to your agent too.
- [All five Project Pulse assignments](../assignments.md)
- [Working with AI](../ai.md), which governs what individual work means when you have an agent.
