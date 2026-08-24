# Working with AI

In most courses the AI policy tells you what you may not do. This one is different: **you are required to use an AI coding agent**, from week 1, across the whole lifecycle. The policy is about what that obligates you to.

## The one rule

> **You are responsible for everything submitted under your name, whoever or whatever typed it.**

Every other rule on this page follows from that one. "The agent wrote it" explains how a defect got there. It never excuses it.

## What you are expected to do

- **Use the agent across the lifecycle**, not just for code: requirements review, design alternatives, test generation, static-analysis triage, debugging, reading unfamiliar code.
- **Anchor it to a specification.** The method this course teaches exists because ad-hoc prompting drifts. Your specification is version-controlled Markdown in your repository. The agent builds against it, and you review the output *against* it.
- **Verify before you ship.** Run it, read it, test it. AI verifies first; a human verifies after. Never ship unreviewed AI output.
- **Be able to explain any line you submit.** Not "explain what it does" at a hand-wave, but why it is there, what it assumes, and what breaks if that assumption fails.
- **Disclose meaningfully when asked.** Several assignments ask what you delegated, what you kept, and what the agent got wrong. Answer honestly. "The agent produced this and I rewrote the error handling because it swallowed exceptions" is a good answer that costs you nothing.

## What is prohibited

- Submitting work you **cannot explain**. This is the operational test, and it is the one that gets applied.
- **Fabricated WARs or peer evaluations.** Inflating time or activities in a weekly activity report is academic dishonesty, agent-assisted or not.
- Using an agent **during exams**, or any other unauthorized resource.
- Letting an agent **do your teammates' share, or your own**. Every team member contributes to the writing and to the code. Commit history is monitored, and an agent-generated commit stream is recognizable.
- Passing off generated content as **client input, meeting minutes, or interview notes**. Those record what a human actually said.

## The delegation boundary

The interesting question is never "may I use AI." It is **what to hand over and what to keep**, and the line moves by topic. It comes up in every module of this course.

| Keep human | Delegate to the agent |
|---|---|
| Requirements quality, scope, and vocabulary | Turning an approved use case into a design-of-record |
| Business constraints and domain knowledge | Implementing an approved design into code and tests |
| Quality attributes and what "good enough" means | Cross-document consistency checks |
| High-level architectural decisions | Mechanical transformations between artifacts |
| Judgment calls, and "is this even a good idea" | Drafting, refactoring, and explaining unfamiliar code |

A rough test: **if guessing it wrong would violate a requirement, it stays human.** Otherwise the agent can derive it.

## Two failures to watch for in yourself

**Automation bias** is trusting output that is wrong. It has a tell: you approved something you did not read. The fix is mechanical, so build the habit now. Read the diff. Run the tests. Ask what it assumed.

**Agenda capture** is subtler and more common, and it has no error signal at all. After a dozen turns of conversation you are no longer directing the work. You are answering the agent's questions, following its reasoning, and building things that do not matter yet. Every individual step looks fine. The cost only appears at the end, when the thing you sat down to do is not done.

Why it happens: the agent always has a next move and never says "I do not know what matters here, you decide." Whoever asks the questions owns the frame, and you did not write the questions. The agent goes depth-first while seniority is breadth-first. And fifteen turns in, abandoning the thread feels wasteful even when abandoning is correct.

Three moves:

1. Answer the agent's question only if the answer changes what you would do next. Otherwise say so and return to the goal.
2. **Kill the session rather than redirect it.** The context that captured you is the same context you would be arguing against.
3. Write the goal down before opening the chat, so drift is checkable rather than a feeling.

The [Napkin drill](studio.md) exists partly for this. A napkin written before the session gives you something external to check the conversation against.

## Getting access

**The baseline for this course is [GitHub Copilot CLI](https://docs.github.com/en/copilot), free to verified students through the [GitHub Student Developer Pack](https://education.github.com/pack).** Everyone can get it, so nobody is blocked by cost.

**Do this in week 1, not the night before an assignment.** Verification requires a school-issued email or dated proof of enrollment, and activation can take several days after you are approved. GitHub also re-checks eligibility monthly, so keep your student status current.

1. Apply for the Student Developer Pack at [education.github.com/pack](https://education.github.com/pack).
2. Once verified, activate Copilot from your GitHub education benefits settings.
3. Install the Copilot CLI and confirm it can read your cloned Project Pulse repository.

Two things to know about the student plan. Code completions are unlimited, but **chat and agent usage draw on a metered allowance of AI credits**, and model choice is automatic rather than yours. This course leans on *agent* usage, not completions, so budget it: do the thinking before you open the session, and do not burn credits letting an agent wander. That habit is the [agenda capture](#two-failures-to-watch-for-in-yourself) lesson with a price tag attached.

**Already paying for your own agent?** Keep using it. Claude Code, Cursor, Codex, or anything else with real agentic capability is fine, and if you have one you will hit fewer limits. **If your client offers to sponsor licenses for your team, take it** and tell the instructor. Not every client can afford six or seven seats, which is exactly why the Copilot student baseline exists.

The method this course teaches is deliberately tool-agnostic. Artifacts, approval gates, the challenge loop, and traceability are the point; the agent is interchangeable and will change again before you graduate.

## Skill atrophy, honestly

A fair objection: if the agent writes the code, do you learn to write code? The course's answer is that the scarce skill has moved, not vanished. Reading code critically, deciding what should exist, judging whether a design is sound, and noticing that a plausible answer is wrong are all harder than producing syntax, and all of them are what this course grades. But the objection is not silly, and you should watch yourself for it. If you cannot write a method without asking, that is information about you worth acting on.

## TCU academic conduct

This course policy operates within TCU's [Academic Conduct Policy](http://tcu.smartcatalogiq.com/current/Undergraduate-Catalog/Student-Policies/Academic-Conduct-Policy-Details) and Section 3.4 of the Student Code of Conduct. Where they conflict, the university policy governs.

TCU's university-wide statement on AI use:

> Course syllabi include information about when, how, and which forms of AI are required, permitted, restricted, or prohibited in courses. When AI use varies from the general course expectations for specific activities, you can expect activity-level instructions. If in doubt, you, as a student, should ask the instructor before submitting work. If you use AI in any course, you are responsible for the accuracy, quality, and integrity of the coursework you submit including any errors, fabrications, or biases the AI may produce. Your critical judgment is crucial in determining how you use AI. Once included in your coursework, you are responsible for any misinformation. AI technology is not responsible.

That last line is this page's one rule, in the university's words. Everything above is what it means for a course where the agent writes production code.

**Activity-level summary**, since TCU's statement anticipates that use varies by activity:

| Activity | AI use |
|---|---|
| Team project: specification, design, code, tests | **Required.** This is the course. |
| Individual Project Pulse assignments | **Required**, and you disclose what you delegated. |
| Exams | **Prohibited**, along with all other outside resources. |
| Weekly activity reports, peer evaluations, meeting minutes | **Prohibited as a source of content.** These record what actually happened. |
