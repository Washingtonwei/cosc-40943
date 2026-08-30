# Assignments

Two graded surfaces are individual: the **Project Pulse assignments** and the **exams**. Everything else is your team's work, covered on the [Senior Design Project](project.md) page.

## Individual Project Pulse assignments

Five assignments, 20% of your grade, done alone on [Project Pulse](https://github.com/Washingtonwei/project-pulse): the instructor's own Vue.js and Spring Boot application, and the codebase you watch in every Monday and Wednesday lecture.

Each one has the shape of real work on a codebase you did not write: **open a well-formed issue, make the change, submit a pull request.** Each is framed around the AI workflow.

!!! important "Graded on judgment, not on whether it ran"
    An agent can make almost any of these produce working output. That is not what earns the grade. The grade is for the quality of the issue you wrote, the changes you decided *not* to make, the findings you correctly dismissed, the test you added because you understood what could break, and your ability to explain in the pull request why the change is right. "It ran" is the floor, not the bar.

| # | Assignment | Due | Task |
|---|---|---|---|
| 1 | **[Hello, Project Pulse](assignments/hello-project-pulse.md)** | Fri **Sep 4** | Set up and run Project Pulse, read one package with the agent and catch a claim the code does not support, open a well-formed issue, and submit a small pull request. |
| 2 | **Spec a feature** | Fri **Sep 25** | Write a use case with acceptance criteria for a feature Project Pulse is missing, then turn it into an agent build-context and evaluate what the agent produced against what you wrote. |
| 3 | **Add a use case** | Fri **Oct 16** | Take one use case end to end with the agent, wire it into the traceability matrix, and add AI-generated tests that you have vetted. |
| 4 | **Triage the analyzers** | Fri **Nov 6** | Run linters, SpotBugs, and SonarQube on Project Pulse. Separate real findings from false positives, fix a set, and show them passing in CI. The triage is the assignment. |
| 5 | **Hunt the bug** | Fri **Nov 20** | Localize a planted bug using logs, traces, and the agent. Fix it and add the regression test that would have caught it. |

Each is due on the Friday of the week its topic is taught, roughly three weeks apart. That Friday's [studio](studio.md) then applies the same move to your team's project, so you do it once alone on Project Pulse and once with your team on your own code, in that order. Plan accordingly: Monday and Wednesday lecture is what you have behind you when the individual version is due. None lands during a break or on a checkpoint Friday except the first, which is deliberate: Checkpoint 0 is a lightweight kickoff gate and this assignment is small.

**You submit a link, and the pull request is the work.** Each assignment is done in **your own fork of a class copy of [Project Pulse](https://github.com/Washingtonwei/project-pulse)**, not in the public repository. Each assignment has its own repository to fork; the link is on that assignment's page. **Submit the pull request's URL to TCU Online** by the start of class on the due date. The issue you opened, the commits, and the pull request description are the artifact being graded; nothing else is uploaded. Late work takes a 15% penalty per day and is not accepted more than two days late.

## Exams

| Exam | When | Scope |
|---|---|---|
| **Midterm** | Mon Oct 19, in class | Weeks 1-8: what AI changes and the delegation boundary, the AI-augmented team and GitHub workflow, spec-driven requirements, context engineering, architecture and architecturally significant requirements, design-of-record, AI-assisted implementation, traceability. |
| **Final** | Mon Dec 14, 8:00 - 10:30 AM | Cumulative, weighted toward weeks 9-14: testing, static analysis, CI/CD, observability and debugging, maintainability and technical debt, ethics. The self-study open-source module is **not** examined. |

Exams assess whether *you* can reason about software engineering, which is the one thing the agent cannot do on your behalf in the room. Expect questions that give you an artifact and ask you to judge it: is this requirement testable, is this the right architectural decision and what did it cost, does this trace hold up, what would you have reviewed here.

## What "individual" means when you have an agent

Read [Working with AI](ai.md). The short version: using the agent on individual assignments is expected. Submitting work you cannot explain is not.
