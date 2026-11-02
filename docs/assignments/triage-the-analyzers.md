# 4. Triage the analyzers

**Due Friday, November 13, at the beginning of class.** Individual work. 4% of your grade.

Project Pulse ran no static analyzer for two years. On November 1, [pull request #104](https://github.com/Washingtonwei/project-pulse/pull/104) added SpotBugs and PMD to the build, and recorded everything they found that day in two baseline files: 237 SpotBugs findings and 130 PMD findings, **untriaged**. The build now fails on anything new, and nobody has yet decided which of the old 367 are bugs.

That is your job this week, on a slice of the codebase. It is also the most likely first task of your internship: a team with an analyzer, a baseline nobody has read, and a new hire who is asked to "clean up the warnings".

An agent can make every warning disappear in minutes. Some of those changes will be right, some will hide a real bug, and a few will quietly change what the code does. The grade is for knowing which is which, and for leaving a record the next engineer can check.

## Before you start

Read [Static Analysis](../modules/static-analysis.md), especially [4.4](../modules/static-analysis.md#44-triage-real-false-positive-or-not-worth-it) (triage) and [4.6](../modules/static-analysis.md#46-an-existing-codebase-baseline-then-ratchet) (baselines). The five findings the module triages are worked examples; they are not in any slice.

## Your assignment repository

Fork this one:

**<https://github.com/tcu-cosc-40943/triage-the-analyzers>**

It is a copy of Project Pulse with #104 merged: the analyzers, the baselines, and the pull request workflow.

!!! warning "1. Turn Issues on in your fork"
    A new fork has its **Issues tab disabled**. Switch it on: **Settings → General → Features → Issues**.

!!! warning "2. Point your pull request at your own fork"
    GitHub sets the **base repository** to `tcu-cosc-40943/triage-the-analyzers`. Change it to **your own fork**, base branch `main`.

!!! warning "3. Turn GitHub Actions on in your fork"
    Unlike assignment 3, this one needs CI. Open your fork's **Actions** tab and enable workflows. Your pull request's checks are part of what you submit. The backend job takes about ten minutes, because the integration tests start a MySQL container.

**Run the gate locally first.** From `backend/`, `./mvnw verify` runs the tests, SpotBugs, and PMD (Docker must be running for the integration tests); `./mvnw verify -DskipTests` runs only the analyzers and takes about a minute. From `frontend/`, `npm ci`, then `npm run lint:check`, `npm run type-check`, and `npx prettier --check src/`.

**Find your slice's findings.** `./mvnw spotbugs:gui` opens SpotBugs' report; `target/pmd.xml` lists PMD's. Both reports are filtered by the baseline, so to see the baselined findings, empty the two baseline files in a scratch branch, run `./mvnw verify -DskipTests`, read the reports, and throw the branch away.

## What you submit

In **your own fork**:

| | What it is |
|---|---|
| **One issue** | "Triage slice N", naming your slice and the four project decisions. |
| **One pull request**, left open | Your decisions, your fixes and suppressions, the smaller baselines, and the template filled in. Its checks must be green, apart from the frontend steps, which only report. |

**Submit the pull request's URL to TCU Online** by the beginning of class on Friday, November 13. **Leave it open. Do not merge it.**

## Part 1: Four project decisions (everyone)

Some rules should not be triaged one finding at a time, because the question is whether the rule fits Project Pulse at all. Make these four decisions for the whole project:

| Decision | Rule | Findings |
|---|---|---|
| **D1** | SpotBugs `EI_EXPOSE_REP` and `EI_EXPOSE_REP2` | 219 |
| **D2** | PMD `UncommentedEmptyConstructor` and `UnnecessaryConstructor` | 40 |
| **D3** | PMD `ControlStatementBraces` | 30 |
| **D4** | PMD `GuardLogStatement` | 4 |

For each, choose one:

- **Enforce it.** Fix every baselined finding of that rule, and delete their baseline entries.
- **Turn it off.** Record the decision, with its reason, in `backend/config/spotbugs-exclude.xml` or `backend/config/pmd-ruleset.xml`, and delete that rule's baseline entries.
- **Narrow it.** Turn it off for part of the code (a package, a kind of class), with the reason, and enforce it everywhere else.

Read enough of the findings to know what the rule is objecting to before you decide. Then write a reason a teammate could check: what Project Pulse does that makes the rule right or wrong here. "Too noisy" is not a reason; why it is noisy is.

## Part 2: Triage your slice

Your slice is set by the **last digit of your TCU ID**. Every finding listed for your slice gets a verdict.

| Digit | Slice | Files | Findings |
|---|---|---|---|
| 0 | Students | `student/StudentSecurityService`, `StudentService`, `StudentSpecs` | 8 PMD |
| 1 | Instructors and courses | `instructor/InstructorSecurityService`, `InstructorService`, `InstructorSpecs`, `course/CourseSpecs` | 9 PMD |
| 2 | Sections | `section/SectionSecurityService`, `SectionService`, `SectionSpecs`, `section/dto/SectionDto` | 5 PMD |
| 3 | Teams and activities | `team/TeamSpecs`, `activity/ActivitySpecs`, `activity/ActivitySecurityService` | 5 PMD |
| 4 | Security | `security/AuthService`, `JwtProvider`, `SecurityConfiguration`, `system/StatusCode`, `user/UserController` | 3 SpotBugs, 6 PMD |
| 5 | Evaluations and rubrics | `evaluation/Rating`, `EvaluationService` (its `LiteralsFirstInComparisons` only), `rubric/CriterionSpecs`, `RubricSpecs` | 2 SpotBugs, 6 PMD |
| 6 | Requirements (RAM) | `ram/document/DocumentSectionLock`, `RequirementDocumentSpecs`, `ram/usecase/UseCaseLock`, `UseCaseService`, `UseCaseController`, `ram/requirement/ArtifactLinkSpecs`, `RequirementArtifactSpecs` | 8 PMD |
| 7 | Frontend: week pickers | `components/SearchPeriod.vue`, `SearchWeek.vue`, `TopNavigationBar.vue` | 8 `vue-tsc` errors |
| 8 | Frontend: reports and registration | `pages/activities/admin/SectionsActivities.vue`, `StudentActivities.vue`, `pages/evaluations/admin/StudentEvaluations.vue`, `pages/UserRegistration.vue`, and ESLint's unused imports in `pages/rubrics/` | 6 `vue-tsc` errors, 2 ESLint |
| 9 | Frontend: editor and teams | `pages/ram/RamDocumentEditor.vue`, `pages/teams/Teams.vue`, and ESLint's unused variables in `cypress.config.js` | 4 `vue-tsc` errors, 2 ESLint |

Backend slices are the findings left in those files after Part 1's four rules, except the `NP_NULL_ON_SOME_PATH_FROM_RETURN_VALUE` findings on `getAuthentication()` and `getAuthority()`, which the module triages (paths under `backend/src/main/java/team/projectpulse/`). Frontend paths are under `frontend/src/`, apart from `frontend/cypress.config.js`; the frontend has no baseline file, so for those slices "shrink the baseline" means the error count in the pull request's CI log.

For each finding, the three verdicts from [4.4](../modules/static-analysis.md#44-triage-real-false-positive-or-not-worth-it):

- **Real:** fix it. Make sure the fix is the right one, not just the one that silences the tool. Some fixes the tool suggests are wrong for a Spring or JPA class; find out before you apply one.
- **False positive:** suppress it at the site, with a reason someone can check.
- **Not worth it:** suppress it with the reason, or argue in the pull request that the rule belongs in Part 1.

Then **delete the finding's baseline entry**. The baselines only shrink. If your pull request adds a line to either baseline file, it is not accepted.

## Part 3: Show one bug

For at least one finding in your slice that you judged **real**, write a test that fails before your fix and passes after it. Commit the test first, then the fix, so the history shows it going from red to green. If no finding in your slice can be shown by a test, say why in the pull request; that is a legitimate answer for some slices, not for most.

## Part 4: The pull request

Use the template that opens with your pull request. Its sections:

- **Project decisions:** D1 to D4, each with your choice, the reason, and the file you changed.
- **My slice:** one row per finding: the file and line, the rule, your verdict, how you recorded it (the fix commit, or the suppression), and one line of reason.
- **The bug I showed:** the test, the failing run before the fix, the passing run after.
- **The baselines:** the count of entries in each baseline file before and after.
- **What the agent did:** which changes the agent proposed, and which you rejected or rewrote, and why. If you used no agent, say so.
- **Not verified:** what you did not check. An honest answer here is never penalized.

## How it is graded

| | Points |
|---|---|
| **The four decisions.** Is each choice defensible for Project Pulse, is the reason checkable, and does the configuration do exactly what the reason says? | 25 |
| **Your slice.** Does every finding have a verdict, is each verdict right for this code, is each real fix the right fix rather than the quietest one, and does each suppression carry a checkable reason? | 40 |
| **The bug.** Does the test fail before the fix and pass after, and does it show the bug the finding named? | 15 |
| **The gate.** Green checks, baselines that only shrank, every resolved finding's entry deleted, nothing new suppressed or baselined to make the build pass. | 10 |
| **Mechanics.** The issue, the pull request in your fork, readable commits and writing. | 10 |

!!! important "Not the bar: zero warnings"
    Zero warnings is easy. Suppress everything, or let an agent "fix" every finding the quickest way, and the build goes green in ten minutes. That earns little here. The grade is for the finding you correctly left alone, the fix the tool suggested that you refused, and the test that proves a warning was a bug. Expect to be asked in class why a finding in your slice is real.

Your fork is public, and so is everyone else's, including classmates with your slice. Read their work if you want, after you have filed your own. What you cannot do is submit verdicts you did not reach. That is the [explanation test](../ai.md), and it is asked in class.

Late work takes a 15% penalty per day and is not accepted more than two days late. See the [syllabus](../syllabus.md#late-work).

## Related

- [Static Analysis](../modules/static-analysis.md): the ladder, triage, and baselines.
- [Testing](../modules/testing.md): writing the test that shows the bug.
- [Code Review](../modules/code-review.md): reading a suppression the way you read code.
- [All five Project Pulse assignments](../assignments.md)
- [Working with AI](../ai.md), which governs what individual work means when you have an agent.
