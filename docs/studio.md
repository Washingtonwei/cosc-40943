# Friday Studio

Friday is not a lecture and not a lab on a toy problem. It is the hour your team works on **your own client project**, in the room, with a TA who knows your project.

## How it runs

- Same room, same time, whole class. Thirteen teams work in parallel, seated in three zones by TA. You sit in the same zone every Friday.
- **Each TA owns four or five teams for the entire semester.** You get the same TA every week, at every checkpoint. They know your project's history, which is the point.
- Every studio has **one scoped objective**, published on the [Schedule](schedule.md). It is the move you saw demonstrated on Project Pulse in Wednesday's lecture, now applied to your code.
- TAs circulate. They are there to unblock and to review, not to lecture.
- **On four Fridays, studio is your checkpoint presentation** to your TA. That week's objective moves to out-of-class team time.

Attendance in studio counts the same as lecture attendance: each absence is a 1% grade reduction.

## Teaching assistants

Led by **Hiep Nguyen**. Each TA takes four or five of the thirteen teams and keeps them all semester.

| TA | Email | Teams |
|---|---|---|
| Hiep Nguyen (lead) | HIEP.N.NGUYEN@tcu.edu | 1, 2, 5, 9, 13 |
| Ali Gasimli | A.GASIMLI@tcu.edu | 3, 6, 10, 12 |
| Yuv Raj Pant | YUV.RAJ.PANT@tcu.edu | 4, 7, 8, 11 |

Team numbers are on the [Teams page](teams.md).

## The first studio is different

Your team was formed on Wednesday and your project barely exists yet, so the first studio is guided onboarding rather than project work:

- **Week 2, Sep 4.** Your team's first hour together. Introduce yourselves, fix the recurring weekly meeting slot you will defend all term, read your client brief as a team, draft and sign your [team contract](team-contract.md), and stand up your GitHub repository, Projects board, Issues and Sub-issues, and Slack channel. The contract is committed to the repository as `docs/team-contract.md`, not kept in a document somewhere. Your TA verifies **Checkpoint 0** in the room while you work.

### Where your repository lives

**One member owns it, under their own GitHub account.** Name that person before you create anything, and write their name and the repository URL into your contract's header.

- The repository is **public**, named `cosc-40943-team-NN-<slug>` to match your brief on TCU Online. Create it with a README so it has a `main` branch from the start. Public means your client's material does not go in it: see [what belongs in the repository and what belongs in Drive](project.md#what-you-deliver-this-fall).
- The owner invites **nine collaborators**: the other members, all three TAs, and the instructor. A personal repository gives every collaborator write access, which is what you want.
- **A Project's access list is separate from the repository's.** Everyone can be on the repository and still be unable to move a card. After you create the Project and link it, the owner adds the team and your TA under the Project's own settings. This is the step teams forget, and your TA checks it from an account that is not the owner's.
- **The owner has to be someone continuing into COSC 40993 in the spring.** If they leave the course, transfer the repository before they go. Everyone clones on day one, so no single account is ever holding your history hostage.

Environment setup is not studio work. Getting Project Pulse running on your own machine is [assignment 1](assignments/hello-project-pulse.md), due that same day, so arrive with the [setup steps](resources.md) already done. With 77 students and three TAs, studio cannot absorb 77 cold installations.

From week 3 onward, studio is your project.

## The Napkin drill

On five non-checkpoint Fridays, studio opens with a twenty-minute warm-up before the main objective. You are handed a one-paragraph brief for a system you have never seen and asked to size it up on six points: shape, the hard part, the bottleneck, stack, three kill risks, and a verdict.

**[The frame, the rubric, and what separates a good answer from risk bingo are in the module](modules/se-and-ai.md#the-napkin-six-prompts).** Read it once before round 0; you will use it six times.

The one rule to remember in the room: **write yours alone and silently first, then reconcile as a team, then ask the agent, then diff.** Prompting first anchors you on the agent's answer and teaches nothing. The diff is where the learning happens.

**Round 0** napkins your own client project, before you have written a single requirement. It is sealed on the spot, not scored and not discussed. In the last full week of class you reopen it and score yourself against what actually happened, graded on **calibration, not correctness**. Being wrong in week 3 is expected. Not noticing you were wrong is the failure.

## What studio is not

- It is not a substitute for your team's working meetings. Fifty minutes a week does not build a product.
- It is not office hours for the exams.
- It is not a place to start the week's work from zero. Arrive having read the objective.
