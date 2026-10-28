# 3. Add a use case

**Due Friday, November 6, at the beginning of class.** Individual work. 4% of your grade.

A student withdraws in week 9. Her instructor wants her out of Project Pulse: no more logins, no more reminders, her teammates no longer asked to rate her. Her past weekly activity reports and peer evaluations should stay, because they are part of the record of how her team worked.

Project Pulse has a use case for exactly this, `UC-STU-deactivate-student`, and it is half built. This week you finish it with your agent, from the specification to a reviewed pull request: firm the use case, design it, build it trunk first, vet the tests the agent wrote, trace it, and review the agent's work before anyone else has to.

The build is the part the agent does well. The grade is for the parts it does not: the decisions the use case leaves open, the tests you refused to trust until you broke the code, and an honest review of a pull request you did not type.

## The gap, in the actual code

Every link below is pinned to commit [`b9d21b0`](https://github.com/Washingtonwei/project-pulse/tree/b9d21b0e59432abad2195d7d44fc35c686b24f42) so it keeps saying what this page says; Project Pulse is a live repository and `main` moves.

**Today, deactivation is a dropdown.** An instructor opens a student's edit form ([`EditStudentForm.vue`](https://github.com/Washingtonwei/project-pulse/blob/b9d21b0e59432abad2195d7d44fc35c686b24f42/frontend/src/pages/students/EditStudentForm.vue)), changes **Status**, and saves. There is no confirmation and no warning. The save lands in [`StudentService.updateStudent`](https://github.com/Washingtonwei/project-pulse/blob/b9d21b0e59432abad2195d7d44fc35c686b24f42/backend/src/main/java/team/projectpulse/student/StudentService.java), which flips one flag along with the name and email:

```java
// If the user is an admin, then the user can update all the fields
if (authentication.getAuthorities().stream().anyMatch(grantedAuthority -> grantedAuthority.getAuthority().equals("ROLE_instructor"))) {
    oldStudent.setEnabled(update.isEnabled());
}
```

The use case asks for more: a dedicated action, a warning that states the consequences, and a confirmation. Its traceability row reads `🟡 In progress`, Verify `🔎 None`.

**The use case has no extensions.** Read it in `docs/requirements/use-cases.md`. Its `**Extensions:**` field is empty, one of the 26 that `OPEN-ISSUES.md` lists under OI-40. The main scenario is fine. Everything that can go differently is unwritten.

**The code already disagrees with itself about what "deactivated" means.** Look at three places:

- [`SubmissionStatusService.findOwedItems`](https://github.com/Washingtonwei/project-pulse/blob/b9d21b0e59432abad2195d7d44fc35c686b24f42/backend/src/main/java/team/projectpulse/notification/SubmissionStatusService.java), the reminder you specified in assignment 2 and watched get built in week 8, skips a deactivated student, as `BR-submission-owed` says it must.
- [`EvaluationService.generateWeeklyPeerEvaluationReportForSection`](https://github.com/Washingtonwei/project-pulse/blob/b9d21b0e59432abad2195d7d44fc35c686b24f42/backend/src/main/java/team/projectpulse/evaluation/EvaluationService.java) keeps every student who is on a team, active or not.
- `EvaluationService.addPeerEvaluation`, in the same file, checks that the evaluator and the evaluatee share a team. It never asks whether the evaluatee's account is active.

Whether each of these is right is your call to make and defend. None of them is settled by the use case as written.

## Your assignment repository

You do **not** work in the public [Project Pulse](https://github.com/Washingtonwei/project-pulse) repository. Fork this one:

**<https://github.com/tcu-cosc-40943/add-a-use-case>**

It is a copy of Project Pulse at `b9d21b0`, with the `/design` and `/implement` commands under `.claude/commands/`. Same two settings as before, and they still go wrong the same two ways.

!!! warning "1. Turn Issues on in your fork"
    A new fork has its **Issues tab disabled**. Switch it on: **Settings → General → Features → Issues**.

!!! warning "2. Point every pull request at your own fork"
    GitHub sets the **base repository** to `tcu-cosc-40943/add-a-use-case`. Change it to **your own fork**, base branch `main`. This assignment has two pull requests, so check it twice.

!!! tip "Let your agent reach GitHub"
    `/design` and `/implement` both end by opening a pull request, so connect your agent this time: [Agent Setup](../agent-setup.md#6-get-an-assignment-repository-onto-your-laptop), step by step. Run `gh repo set-default <your-username>/add-a-use-case` first, or the agent's pull request lands in the class repository. Whatever the agent files under your name, you answer for in class.

!!! note "On Copilot CLI or another agent"
    `/design`, `/implement`, and `/code-review` are Claude Code commands. On Copilot CLI you run the same steps by hand ([Working with AI](../ai.md#getting-access)). For Parts 1 to 3, tell the agent to read `.claude/commands/design.md` or `.claude/commands/implement.md` and follow it one phase at a time, stopping where the file says to stop. In place of `/code-review` in Part 6, start a fresh session, give it the pull request's diff, the design, and the use case, and ask it to review the change against them. The deliverables and the grading are the same.

**Start early.** The backend test suite takes several minutes and needs Docker running (its integration tests start a MySQL container), the build needs the app running as it did in assignment 1, and Part 1 needs thinking time that the agent cannot shorten. This assignment also uses more agent time than the first two; on a metered plan, spread it over several days.

**Leave GitHub Actions off in your fork.** A new fork has them off, and nothing in this assignment needs CI on GitHub: you run the tests on your laptop.

## What you submit

In **your own fork**:

| | What it is | Merge it? |
|---|---|---|
| **One issue** | `UC-STU-deactivate-student` as the build-context, in the shape you practiced in assignment 2: the ID, the files you expect to change, nothing pasted | Not applicable. The design pull request says `Refs #N`, so merging it leaves the issue open; the build pull request says `Closes #N`. |
| **The design pull request** | From `/design`: the firmed use case, any new or changed `BR-*`, `docs/design/stu.md`, and the traceability row at `📐 Designed` | **Yes, you merge it.** That merge is the design gate. |
| **The build pull request** | From `/implement`: the code, the tests, the row updated, and your review in its description | **No. Leave it open.** |

**Submit the build pull request's URL to TCU Online** by the beginning of class on Friday, November 6. Link the issue and the design pull request from its description.

You review only the build pull request. Reviewing a design you wrote yourself proves little; the design gate's real test is whether the build matches it.

## Part 1: Firm the use case

Run `/design UC-STU-deactivate-student`. Its first beat challenges the use case before any design exists, and it will ask you questions. Answer them yourself. The agent will offer an answer to each, and some of those answers are wrong for Project Pulse.

Your extensions are where most of the grade is. At minimum, decide what the use case does about each of these, and write each decision as an extension, a business rule, or an Associated Information line, whichever is its right home:

- **The student is on a team.** Does deactivation take her off it? Look at what `BR-submission-owed` says about "every member of her current team whose account is active" before you decide. Removing her and keeping her both have consequences, and they are different consequences.
- **Her teammates' peer evaluations.** Do they still evaluate her? Can they? Does the section's peer evaluation report still show her, and for which weeks? Decide, then check your decision against the three places in [the code](#the-gap-in-the-actual-code).
- **She is logged in right now.** `FR-SEC-active-account` denies access to a deactivated account "regardless of otherwise-valid credentials". Find out what Project Pulse actually checks on each request after login, and decide whether the use case needs to say anything about it.
- **She is already deactivated.** The precondition says "at least one active student", which is a different condition from "this student is active".
- **The instructor is not hers.** `BR-student-lifecycle` lets a course admin, or an instructor assigned to the student's course section, deactivate her. What happens when anyone else tries?
- **The instructor changes her mind** at the warning in step 4.

**Cite business rules; do not restate them.** If a decision is policy, it belongs in `business-rules.md` under a `BR-<slug>`, and the use case cites it. If an existing rule turns out to be wrong, change the rule, and say so in the design pull request.

**Stay in scope.** `UC-STU-reactivate-student` is the mirror image and shares most of these questions. Do not build it. Where a decision you make constrains reactivation (a student taken off her team does not get her team back by herself), write it into the reactivate use case's Associated Information so the next person finds it.

**Each spec fix is its own commit.** The commits are the evidence that the challenge happened.

## Part 2: Design it, and pass the gate

The second beat of `/design` proposes a design and stops in plan mode for you to accept its shape. Read it against [Design-of-Record](../modules/design-of-record.md): the classes, the sequence for the main scenario, the new route and its rule in `SecurityConfiguration`, and the **test list**. Push back on anything that does not match your use case. Then let it write `docs/design/stu.md`, the first design-of-record for the STU area, and open the design pull request.

Read the test list before you merge. Every extension from Part 1 should have at least one row. A row that is missing here is a test nobody will write in Part 3.

**Merge the design pull request yourself.** Your fork has no other reviewer; in a team, a teammate does this.

## Part 3: Build it, trunk first

Run `/clear`, then `/implement UC-STU-deactivate-student`, in a fresh session that reads the merged design rather than your conversation about it.

**Trunk first.** If the use case changes code other paths depend on (a shared service, a query several features call, a security rule), the agent commits that change first, in a commit of its own, and you read it before it builds the rest. Required, not graded this term ([AI-Assisted Implementation 4.6](../modules/implementation.md#46-size-the-step-to-the-review)).

If `/implement` pauses to raise a contradiction, that is the command working. Settle it in the use case or the design, commit the fix, and continue.

## Part 4: Vet the tests the agent wrote

The agent will write tests, and they will pass. That is not evidence. Read each one with the five questions in [Testing 4.6](../modules/testing.md#46-reading-a-test-the-agent-wrote), and keep only the ones that answer them well. Fix or delete the rest, and say which.

In the build pull request's description, under the template's **The tests I kept** and **The code I broke**:

1. **For each test you keep, one line naming its oracle's source**: the use case step or extension, the business rule, or the test-list row its expected value comes from. "The code under test" is an honest answer and a reason to rewrite the test.
2. **Break the code once.** Pick the test you trust least, change one line of production code it should catch, and run it. Report the change and whether the test went red. If it stayed green, you found something; say what you did about it.

## Part 5: Trace it

`/implement` updates the use case's row in `docs/traceability.md`. Check it rather than trust it ([Traceability 4.1](../modules/traceability.md#41-the-spine-one-row-per-use-case)):

- **Build** says what the code does, and **Verify** says what the tests prove. They are set independently.
- The **Tests** cell names the tests that make Verify true, and which extensions each covers. An extension with no test is named as untested, and Verify is `🟡 Partial`, not `✅ Verified`.

A row that claims more than the tests show is the defect this whole week was about.

## Part 6: Review the pull request yourself

Before you submit, review the agent's build pull request as if a teammate had opened it ([Code Review 4.3 to 4.6](../modules/code-review.md#43-how-deep-trunk-security-rule-leaf)). Write it under **My review** in the pull request template:

1. **The triage line.** Which commit is the trunk, which is the security rule, which are leaves, and how deep you read each. One line.
2. **The test list, row by row.** Each row of `stu.md`'s test list marked covered (by which test) or not.
3. **At least one labeled comment** (Conventional Comments: `issue`, `suggestion`, `question`, each blocking or not) on something you changed or rejected. Put it on the line in GitHub's diff view, not only in the description.
4. **One `/code-review` run** (or a fresh session, on Copilot CLI) against the pull request. List its findings and what you did about each: fixed (with the commit), rejected (with the reason), or left as a follow-up issue.

"Not verified" is a section, and it is never penalized. A review that lists two things nobody checked is worth more than one that claims everything was.

## How it is graded

| | Points |
|---|---|
| **The firmed use case.** Are the extensions real, is each decision made rather than deferred, and is each one in its right home (extension, rule, or Associated Information), with rules cited rather than restated? | 30 |
| **The tests.** Does each kept test name an oracle from the specification, did you break the code and report the result honestly, and did you fix or drop the tests that did not hold up? | 20 |
| **The review.** Is the triage right, is the test-list check honest, and does each `/code-review` finding have a reasoned outcome? | 25 |
| **The design and the trace.** Does the test list cover the extensions, does the code match the merged design, and does the traceability row claim exactly what the tests show? | 15 |
| **Mechanics.** Linked issue, both pull requests in your fork, design merged, build left open, readable commits and writing. | 10 |

!!! important "Not the bar: the feature works"
    An agent will build this end to end in under an hour, with a confirmation dialog, a new endpoint, and a dozen green tests. That is the floor. The grade is for what you decided about the teammate who still has to rate her, for the test that stayed green when you broke the code, and for a review that says what nobody checked. Expect to be asked in class why your use case does what it does.

**Leave the build pull request open. Do not merge it.** It is reviewed and graded as submitted, the way it would be at work.

Your fork is public, and so is everyone else's. Read your classmates' work if you want, after you have filed your own. What you cannot do is submit decisions you did not make or a review you did not do. That is the [explanation test](../ai.md), and it is asked in class.

Late work takes a 15% penalty per day and is not accepted more than two days late. See the [syllabus](../syllabus.md#late-work).

## Related

- [The method](../method.md), Phase C: the per-use-case loop this assignment runs once, alone.
- [Design-of-Record](../modules/design-of-record.md): the design gate and the test list.
- [AI-Assisted Implementation](../modules/implementation.md): trunk-first commits.
- [Testing](../modules/testing.md): oracles and reading a test the agent wrote.
- [Traceability](../modules/traceability.md): the row, Build vs. Verify.
- [Code Review](../modules/code-review.md): the triage line, the checklist, and labeled comments.
- [Assignment 2, Spec a feature](spec-a-feature.md): the reminder this use case has to agree with.
- [All five Project Pulse assignments](../assignments.md)
- [Working with AI](../ai.md), which governs what individual work means when you have an agent.
