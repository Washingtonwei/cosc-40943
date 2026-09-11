# COSC 40943: Software Engineering

**Fall 2026, section 020. MWF 10:00 - 10:50 AM, SWR LH3.**
Instructor: Bingyang Wei, b.wei@tcu.edu, TUC 341D, office hours MW 11:00 - 12:00 or by appointment.

!!! important "Week 3: meet your client, then start your requirements"

    **Every team meets its client this Thursday or Friday.** Commit your filled-in interview guide the same day, as `docs/requirements/client-interview-YYYY-MM-DD.md`. It is the record everything else this week is drafted from.

    Friday's [studio](studio.md) opens with [Napkin round 0](studio.md#the-napkin-drill) on your own project, sealed. Then your team drafts the glossary, the first sections of vision and scope, and `OPEN-ISSUES.md`: one section per person, each on its own branch and pull request. Before you arrive, the repository owner turns on [branch protection](git-workflow.md#repository-settings) with status checks left off.

    The reading for the week is [Requirements as the Contract](modules/spec-driven-requirements.md). Use cases are Monday.

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
