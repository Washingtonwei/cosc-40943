# COSC 40943: Software Engineering

**Fall 2026, section 020. MWF 10:00 - 10:50 AM, SWR LH3.**
Instructor: Bingyang Wei, b.wei@tcu.edu, TUC 341D, office hours MW 11:00 - 12:00 or by appointment.

!!! important "Week 5: context engineering, and your TA checks last week's work"

    **Studio is back this Friday, Sep 25, and it opens with your TA checking the requirements work from week 4.** Have `docs/requirements/` populated and `traceability.md` copied from [`course-templates`](https://github.com/tcu-cosc-40943/course-templates) before you walk in. Teams that copied `requirements/` back in week 3 will not have `traceability.md` yet.

    **Napkin round 1 moved to Wednesday's lecture**, so Friday belongs to your own project. Bring nothing; you are handed the brief in the room.

    **Monday and Wednesday are context engineering:** the specification you spent two weeks writing is the context your agent needs, and the question the rest of the course keeps asking is how you know when you have supplied enough. The reading is [Context Engineering](modules/context-engineering.md).

    **Assignment 2, Spec a feature, is now due Friday, Oct 2** rather than Sep 25. It asks you to specify a feature Project Pulse does not have, turn it into a build-context, and judge what the agent did with it. The [assignments page](assignments.md) carries the details.

## What this course is

Software engineering assumed for fifty years that humans perform every engineering activity. That assumption no longer holds. AI can read requirements, generate design and code, write tests, review pull requests, and analyze logs.

So this course asks a harder question than the usual one: **what should software engineering become when AI is a permanent member of every development team?**

You will answer it by doing it. In a team of six, for a real external client, you will build real software using a method called **spec-driven, agent-assisted development**: write a specification the agent can build against, prove your architecture with one working slice, then fan out one use case at a time. The agent writes a great deal of the code. You remain responsible for all of it.

This is also where your Senior Design project starts. It continues into COSC 40993 in spring 2027.

## Start here

1. Read the [Syllabus](syllabus.md). It is your first course reading, and start with [what this course expects of your time](syllabus.md#what-this-course-expects-of-your-time). Plan your semester around this course rather than fitting it into the gaps.
2. Read [Working with AI](ai.md) before you touch the first assignment.
3. Work through the setup steps on [Resources](resources.md) early. Getting Project Pulse running is [assignment 1](assignments/hello-project-pulse.md), due Fri Sep 4; Friday's studio is your team's first working hour, not an install clinic.
4. Skim the [Schedule](schedule.md) so you know where the term is going.

## How the week works

| Day | What happens |
|---|---|
| **Monday, Wednesday** | Lecture. A software engineering topic, demonstrated live on [Project Pulse](https://github.com/Washingtonwei/project-pulse), a real Vue.js and Spring Boot application. |
| **Friday** | [Studio](studio.md). Same room, whole class, TA-led. Your team applies the week's move to your own client project. Four Fridays in the term are your checkpoint presentation. |
| **Outside class** | Team working meetings, client meetings, and building. |

See it on Project Pulse Wednesday. Do it on your project Friday.

## The through-lines

Four ideas recur in every topic. If you remember nothing else in five years, remember these.

- **Specification over conversation.** The durable artifact is the spec in your repository, not a chat transcript. When the code and the spec disagree, one of them is a defect.
- **The delegation boundary.** What goes to the agent, what stays human, and why the line moves by topic.
- **Context engineering.** The scarce skill is supplying what the agent cannot infer, and knowing when you have supplied enough.
- **Trust, then verify.** AI speeds up transformation. It does not lower the engineering bar.

## Quick links

- [Schedule](schedule.md) and [Friday Studio](studio.md)
- [Senior Design Project](project.md): teams, clients, deliverables, checkpoints
- [Assignments](assignments.md): the five individual Project Pulse assignments
- [Resources](resources.md): setup, tools, references
