# 1. Hello, Project Pulse

**Due Friday, September 4, at the beginning of class.** Individual work. 4% of your grade.

This is your first day on a codebase you did not write, which is what your first day at a job looks like. Nobody will explain the system to you. You will have an agent that answers every question instantly and is sometimes wrong, and you will be expected to produce something small, correct, and defensible by the end of the week.

You are not being asked to fix anything important. You are being asked to prove you can read unfamiliar code, catch your agent being confident and wrong about it, and file the kind of issue an engineer would act on.

## Your assignment repository

You do **not** work in the public [Project Pulse](https://github.com/Washingtonwei/project-pulse) repository. **Your own private copy of it** is created for you and appears in your GitHub account on Monday, August 31, alongside your team and client brief. It is a complete copy of the same code, and it is yours: your issue, your branch, and your pull request all live in it.

It is created from the GitHub username you gave in the interest and skills survey. If you did not give one, or gave the wrong one, email <b.wei@tcu.edu> on Monday.

You already have Project Pulse running from studio. Clone your own copy next to it and reuse the Docker containers and dependencies you have installed; the second setup costs a clone and a build, not another install.

## Before you start

- Project Pulse running on your machine, per the [setup steps](../resources.md). You did this in studio on August 28.
- Your assignment repository, cloned.
- Your AI coding agent, able to read the repository. See [Working with AI](../ai.md).

## What you submit

One pull request in your own assignment repository, linked to one issue you opened there. There is nothing to upload anywhere. The issue, the diff, and the pull request description are the artifact.

## Part 1: Read one package with the agent

Pick **one** backend package under `backend/src/main/java/team/projectpulse/` or one frontend feature under `frontend/src/`. Reasonable choices:

| Area | Packages |
|---|---|
| Performance tracking | `activity` (weekly activity reports), `evaluation` (peer evaluations), `rubric` |
| Org and enrollment model | `course`, `section`, `team`, `student`, `instructor` |
| Shared platform | `system` (the `Result` envelope, `StatusCode`, `ExceptionHandlerAdvice`), `security`, `user` |
| Requirements module | anything under `ram/`, for example `document`, `requirement`, `usecase`, `glossary`, `validation` |

Ask the agent to explain that package: what it is responsible for, how a request flows through it, what it depends on. Then **read the code and check the explanation against it.**

You are looking for one specific thing: **a claim the agent made that the code does not support.** It might be wrong, or too confident about something it could not have known, or true of the framework in general but not true of this code. It will not be flagged as uncertain. That is the point of the exercise.

Write down the claim, and write down the file and line that settles it. Both go in your pull request. If the first package you pick gives you nothing, say so and describe what you checked. A documented "I could not catch it here" beats a fabricated catch, and it is the only version of that answer that scores.

## Part 2: Open a well-formed issue

Checking the agent is also how you find something worth filing, because it forces you to read closely enough to notice where the code is not what it should be.

**What to look for.** Project Pulse states its conventions, and the most useful week-1 finding is a place that departs from one:

- The **`Result` envelope**: every API response is wrapped, and the frontend's shared Axios instance unwraps it. A response or a caller that does not follow this is a real finding.
- **`Converter<S, T>` DTO conversion**, written explicitly. There is no Lombok and no MapStruct in this codebase, on purpose.
- **`/api/v1` routing**, uniform across controllers.
- **Per-feature API clients** under `frontend/src/apis/<feature>/`, going through the shared Axios instance rather than calling the network directly.

Failing that: code whose name or comment disagrees with what it does, logic duplicated across two services that should share it, a literal that should be a named constant, or an error path that swallows the information a caller needs.

**What not to file.** Formatting and whitespace. Anything you found by asking the agent for "code smells" and did not verify yourself. Sweeping rewrites. Anything you cannot point at a line for.

!!! warning "Security findings do not go in a public issue"
    If you find something with security or privacy consequences, do not open an issue about it. Email <b.wei@tcu.edu> instead. Publishing a vulnerability where anyone can read it, before the owner can fix it, is how you get fired in your first month. A disclosure by email is graded the same as an issue.

**The shape of a good issue.** This is the shape, not a real finding, so do not file this one:

> **Title:** `ActivityController returns a raw list instead of the Result envelope`
>
> **Body:** `ActivityController.getActivitiesByTeam` returns `List<ActivityDto>` directly, while every other endpoint in the package returns `Result`. The frontend's shared Axios instance unwraps `Result`, so the client for this one call has to special-case the response shape.
>
> To see it: log in as a student, open the team activity view, and compare the network response for this call against any other `/api/v1` call.
>
> Suggested fix: wrap the return in `Result` with the matching `StatusCode`, and drop the special case in the frontend client.

Note what that does. It names the file and the method. It says what the code does and what the convention says. It gives a reason to care that is not "this is bad style." It tells the reader how to see it themselves. It proposes a fix without demanding one. Compare it to "the activity module has poor error handling and several code smells," which nobody can act on.

## Part 3: Make the change and open the pull request

Branch off `main` in your assignment repository, make the fix, and open a pull request that closes your issue.

**Keep it small.** One file is normal. If your diff runs past about fifty lines, you picked the wrong finding. Small is not a consolation prize here: choosing a change you can fully defend is the skill being assessed.

Your pull request description carries three things.

1. **What you changed and why it is right.** Argue for the change. Do not narrate the diff, which the reviewer can already read.
2. **What you deliberately did not change.** You will have noticed other things. Naming them and leaving them alone is a professional move, not an admission.
3. **What the agent got wrong**, from Part 1: the claim, and the file and line that disproves it.

Then say what you delegated and what you kept, in a sentence or two. "The agent drafted the fix and I rewrote the null handling because it silently returned an empty list" costs you nothing and is worth writing.

## How it is graded

| | Points |
|---|---|
| **The issue.** Does it name a real problem precisely enough to act on without asking you a question? | 35 |
| **The change and the argument for it.** Is the fix correct, appropriately small, and defended rather than described? | 35 |
| **Catching the agent.** Did you verify an explanation against the code, and can you show the line that settles it? | 20 |
| **Mechanics.** Branch, linked issue, clean commits, readable writing. | 10 |

!!! important "Not the bar: it ran"
    An agent can produce a passing version of every part of this in ten minutes. That is the floor. The grade is for the finding you chose, the changes you decided against, the claim you caught, and whether you can explain the diff to someone who did not write it. Expect to be asked in class.

**Leave the pull request open. Do not merge your own.** It is yours to merge, and merging it is not the assignment; it is reviewed and graded as submitted, the way it would be at work.

If your fix is genuinely good, you may be invited to open it against the real [Project Pulse](https://github.com/Washingtonwei/project-pulse) as an actual contribution. That is not part of the grade, and it is not something you should ask for. It is something a small number of these earn.

Late work takes a 15% penalty per day and is not accepted more than two days late. See the [syllabus](../syllabus.md#late-work).

## Related

- [All five Project Pulse assignments](../assignments.md)
- [Working with AI](../ai.md), which governs what individual work means when you have an agent
- [Setup steps and the toolchain](../resources.md)
