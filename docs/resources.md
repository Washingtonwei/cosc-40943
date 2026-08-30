# Resources

## Setting up Project Pulse

Project Pulse is the codebase you read all term, and your [first assignment](assignments/hello-project-pulse.md) runs on it. Do this early in the week rather than the night before it is due. If something fails, post the exact command and the exact error text in Slack, in the help channel; setup problems are almost never unique to one person.

### 1. Install the toolchain

| Tool | Version | Notes |
|---|---|---|
| **Git** | any current | |
| **JDK** | **21** | Project Pulse targets Java 21 on Spring Boot 4. A newer JDK may work; 21 is what the build declares. |
| **Node.js** | **20 LTS or newer** | The frontend builds with Vite 5, which needs Node 18 at minimum. Use an LTS release. |
| **Docker Desktop** | any current | Runs MySQL 8.0 and Mailpit. |
| **Maven** | **do not install** | The repository ships the `mvnw` wrapper. Use it. |
| An editor | your choice | |

The README assumes this toolchain and does not name versions, which is why the table is here. A JDK other than 21 is the most common reason a first build fails.

### 2. Clone and run it

The [Project Pulse README](https://github.com/Washingtonwei/project-pulse#readme) is the procedure, and it is the one to follow: Docker for MySQL and Mailpit, the backend, the frontend, the ports, and the test student and instructor logins. It is not repeated here, because it moves with the code and a copy on this site would quietly fall behind it.

Two things differ for [assignment 1](assignments/hello-project-pulse.md). Clone **your own fork** rather than the repository the README names, and read the README **in your fork**, so the instructions match the code you actually have.

Getting it to start is the goal this week. Understanding it is not, yet.

### 3. Set up your AI coding agent

Confirm it can read the cloned repository. See [Working with AI](ai.md) for access.

### 4. Have a GitHub account

One you will use all year, with your real name on it. Your contribution history is part of how the project is assessed.

!!! tip "If you get stuck, write down exactly where"
    "It failed" is not a question anyone can answer. A pasted command and stack trace is. Post the text, not a description of the text.

## Project Pulse

[Project Pulse](https://github.com/Washingtonwei/project-pulse) is a Vue.js, Spring Boot, Maven, Docker, and Azure application. It plays two roles in this course:

- The **demonstration codebase**. Every software engineering move is shown on real code before you apply it to your own project.
- The **individual assignment vehicle**. All five [Project Pulse assignments](assignments.md) are graded per student on this codebase.

It is a real application with real history, real technical debt, and real bugs. That is why it is used instead of a toy example.

## If you have not taken Web Technologies

Studio assumes you can run a Spring Boot and Vue.js stack. Several later topics (CI/CD pipelines, Spring Boot Actuator, Spring Security) are taught here for the software engineering concepts and the lifecycle reasoning, not for the tooling setup, which would eat class minutes better spent elsewhere.

If you did not take that course, you are not stranded, but you do have a catch-up path to walk. Start with these two series, written by the instructor and free. Watch with the demo repository open beside you and type it along; reading it is not the same thing.

| Series | Code | Covers |
|---|---|---|
| [Learn Vue 3 with Bingyang](https://www.youtube.com/playlist?list=PLqq9AhcMm2oMvar6SRrKdCQsrBUbYicqA) | [learn-vue-3-with-bingyang](https://github.com/Washingtonwei/learn-vue-3-with-bingyang) | The frontend half. Project Pulse runs the same Vue 3 and Vite stack. |
| [Learn Spring Boot 3 with Bingyang](https://www.youtube.com/playlist?list=PLqq9AhcMm2oPdXXFT3fzjaKLsVymvMXaY) | [Hogwarts Artifacts Online](https://github.com/Washingtonwei/hogwarts-artifacts-online) | The backend half, built with the layering Project Pulse uses. The series teaches Spring Boot 3 and Project Pulse is on 4, so a few APIs moved; the structure and the practices carry over. |

Work through the parts you need rather than all of it. The goal is being able to read and run the stack, not mastery. Combine that with [assignment 1](assignments/hello-project-pulse.md) and the week 2 studio and you will keep up.


## Tools

Everything in this course is free to you, the coding agent included.

| Tool | Used for |
|---|---|
| Git and GitHub | Single source of truth: code, Issues as user stories, Sub-issues as tasks, Projects board, pull requests |
| Slack | Team and course communication |
| Markdown | Every specification and design document |
| Mermaid | Diagrams, in Markdown, version-controlled with everything else |
| A coding agent | Design and implementation, across the lifecycle. See [Working with AI](ai.md). |
| Google Drive | Your team's reports, minutes, and slides. See [Senior Design Project](project.md). |

No Jira. No Trello. Your GitHub repository is the project record, and it is what gets reviewed.

## Reading

Sources the course draws on, for anyone who wants the depth behind a lecture.

- Wiegers and Beatty, *Software Requirements*, 3rd edition. The SRS, use-case, vision-and-scope, and glossary shapes used in this course.
- Bass, Clements, and Kazman, *Software Architecture in Practice*. Quality-attribute-driven design and the utility tree.
- Starke and Hruschka, arc42, and Brown's C4 model. The architecture-of-record template.
- Nuseibeh, "Weaving Together Requirements and Architectures" (2001). Why requirements and architecture co-evolve rather than sequence.
- ISO/IEC/IEEE 29148. Requirements quality characteristics, and why traceability runs in two directions.

Per-topic reading is listed with each module as the term goes.

## Getting help

- **Your TA first**, for anything about your project. They know it.
- **Instructor office hours**, MW 11:00 - 12:00 in TUC 341D, or by appointment.
- **Slack**, for questions whose answers help everyone.
- **Email** b.wei@tcu.edu for anything private.
