# Midterm Study Guide

**When:** Monday, October 19, 2026, in class (50 minutes)
**Weight:** 15% of your grade
**Allowed:** nothing. No notes, no devices, no agent.

## What the exam looks like

Short written answers. Most questions hand you something (a requirement, a use case step, a design excerpt, a few lines of Project Pulse code, a situation on a team) and ask you to judge it: what is wrong, what you would do, and why. A good answer names the specific defect and the specific fix. A paragraph of correct vocabulary that never commits to a judgment earns little.

There is no recall section. You will not be asked to reproduce a definition for its own sake, but you will need the definitions to answer.

## How to study

Every module ends with a **Self-check**. Those questions are the practice set, and they are the shape of the exam.

1. Answer each Self-check question **in writing, without the module open and without an agent**. A sentence or three is enough.
2. Then reread the section the question comes from and mark what you missed.
3. Where a question asks about "your project", answer it about your team's real specification and architecture. You wrote them; use them.

Asking an agent to answer the Self-checks for you is the one way to study that does not work, because the exam is the one room where you will not have it. Use the agent afterward instead: have it argue against your answer.

Your own work is study material too. [Assignment 2](assignments/spec-a-feature.md) and your team's specification and architecture-of-record exercise most of weeks 3 to 7.

## What to study, week by week

| Week | Topic | Read closely | Practice |
|---|---|---|---|
| 1 | What software engineering is, and what AI changed | [Reading](modules/se-and-ai.md): what software engineering is, what a requirement is, AI is an amplifier, the delegation boundary, agenda capture, the Napkin | [Self-check](modules/se-and-ai.md#9-self-check) |
| 2 | The AI-augmented team | [Reading](modules/ai-augmented-team.md): 4.1 to 4.9 and 4.11 (what the agent can see, well-formed issues, branches, pull requests, the traceability chain, onboarding the agent) | [Self-check](modules/ai-augmented-team.md#10-self-check) |
| 2 | Professionalism | [Reading](modules/professionalism.md): the four steps (observe, analyze, investigate, fix) and escalation. Expect at most one scenario question. | [Self-check](modules/professionalism.md#8-self-check) |
| 3 and 4 | Requirements as the contract | [Reading](modules/spec-driven-requirements.md): business objectives and success metrics, the glossary, the kinds of requirement, use cases (4.10 to 4.17), business rules, quality attributes. Also [Requirement Types](requirement-types.md). | [Self-check](modules/spec-driven-requirements.md#10-self-check) |
| 5 | Context engineering | [Reading](modules/context-engineering.md): all of section 4, especially 4.3 to 4.8 | [Self-check](modules/context-engineering.md#10-self-check) |
| 6 | Software architecture | [Reading](modules/architecture.md): 4.1 to 4.4, 4.6, 4.7, 4.9, 4.11 (quality attributes, architecturally significant requirements, decomposition by domain, one deployable or several, the trust boundary, writing a decision down) | [Self-check](modules/architecture.md#10-self-check) |
| 7 | Design-of-record | [Reading](modules/design-of-record.md): 4.1 to 4.7, 4.9, 4.11, 4.13, 4.14 (how much to write, finding the classes, sequence diagrams, the API contract, design decisions, the questions test, the design gate, the proving slice) | [Self-check](modules/design-of-record.md#10-self-check) |
| 8 | Traceability | [Reading](modules/traceability.md): section 3 and "Three ways the specification and the code drift apart" | The trace boxes in the requirements and design-of-record modules |

The slides for each week are on the [Schedule](schedule.md). They are the fast review; the readings are what the questions are written from.

## Not on the midterm

- **AI-assisted implementation** (week 8 Monday). It is examined on the final.
- **Traceability beyond what is listed above.** The rest of that module is on the final.
- Anything from week 9 on, including testing.

## Sample questions

These show the shape, not the content, of the real exam. No answers are posted: compare yours with a classmate, in Slack, or in office hours.

1. A teammate writes this requirement: "Students who haven't submitted their weekly activity report should be reminded." Name two decisions it leaves open that an agent would make for you, then rewrite it so a test could decide whether the system meets it.
2. Project Pulse's `getPeerEvaluationAverage` ends in `.average().orElse(0.0)`, so a student nobody evaluated gets an average of `0.0`. No business rule mentions the case. Which of the three ways the specification and the code drift apart is this? Say what your team does next, and which artifact changes first.
3. An agent's design-of-record for a new "export peer evaluations" use case includes a Strategy pattern with CSV and PDF exporters. The use case mentions only CSV. Its API contract lists one response, `200 OK`, while the use case has three extensions. You are the reviewer on the pull request. What do you ask for before you approve, and why?

## Related

- [Assignments](assignments.md): both exams, and the final's scope.
- [Syllabus](syllabus.md#exams): how exams fit the grade, and the academic integrity rule for exams.
- [Modules](modules.md): every reading in one place.
