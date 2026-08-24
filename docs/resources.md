# Resources

## Before Friday, August 28

Friday studio is for unblocking, not for installing. There are 72 of you and three TAs. Attempt all of this beforehand and bring your specific error message.

### 1. Install the toolchain

| Tool | Version | Notes |
|---|---|---|
| **Git** | any current | |
| **JDK** | **21** | Project Pulse targets Java 21 on Spring Boot 4. A newer JDK may work; 21 is what the build declares. |
| **Node.js** | **20 LTS or newer** | The frontend builds with Vite 5, which needs Node 18 at minimum. Use an LTS release. |
| **Docker Desktop** | any current | Runs MySQL 8.0 and Mailpit. |
| **Maven** | **do not install** | The repository ships the `mvnw` wrapper. Use it. |
| An editor | your choice | |

### 2. Clone and run [Project Pulse](https://github.com/Washingtonwei/project-pulse)

```bash
git clone https://github.com/Washingtonwei/project-pulse.git
cd project-pulse

# MySQL on 3306, Mailpit on 1025 (SMTP) and 8025 (web)
docker compose up -d

# Backend, serves on http://localhost:80
cd backend && ./mvnw spring-boot:run

# Frontend, in a second terminal, serves on http://localhost:5173
cd frontend && npm install && npm run dev
```

Then open <http://localhost:5173>. The README lists test student and instructor logins. Getting it to start is the goal this week; understanding it is not, yet.

### 3. Set up your AI coding agent

Confirm it can read the cloned repository. See [Working with AI](ai.md) for access.

### 4. Have a GitHub account

One you will use all year, with your real name on it. Your contribution history is part of how the project is assessed.

!!! tip "If you get stuck, write down exactly where"
    "It failed" is not a question a TA can answer in a fifty-minute studio. A pasted command and stack trace is. Bring the text, not a description of the text.

## Project Pulse

[Project Pulse](https://github.com/Washingtonwei/project-pulse) is a Vue.js, Spring Boot, Maven, Docker, and Azure application. It plays two roles in this course:

- The **demonstration codebase**. Every software engineering move is shown on real code before you apply it to your own project.
- The **individual assignment vehicle**. All five [Project Pulse assignments](assignments.md) are graded per student on this codebase.

It is a real application with real history, real technical debt, and real bugs. That is why it is used instead of a toy example.

## If you have not taken Web Technologies

Studio assumes you can run a Spring Boot and Vue.js stack. Several later topics (CI/CD pipelines, Spring Boot Actuator, Spring Security) are taught here for the software engineering concepts and the lifecycle reasoning, not for the tooling setup, which would eat class minutes better spent elsewhere.

If you did not take that course, you are not stranded, but you do have a catch-up path to walk. Start with these, both written by the instructor and both public:

| Resource | Covers |
|---|---|
| [Learn Vue 3 with Bingyang](https://github.com/Washingtonwei/learn-vue-3-with-bingyang) | The frontend half. Demo code for the free YouTube tutorial series; work through it alongside the videos. |
| [Hogwarts Artifacts Online](https://github.com/Washingtonwei/hogwarts-artifacts-online) | The backend half. A Spring Boot sample application demonstrating typical use cases and practices, including the layering Project Pulse uses. |

Work through the parts you need rather than all of it. The goal is being able to read and run the stack, not mastery. Combine that with the week 1 and 2 studio onboarding and you will keep up.


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
