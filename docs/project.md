# Senior Design Project

Twelve teams of six students, each working with a real external client on a real problem. This fall you specify, design, and prove the system, and deliver a working MVP. In COSC 40993 next spring you build it out and deliver it, in April 2027.

## The year at a glance

Senior design is one project across two semesters and two course numbers. What you do this fall determines what spring costs you.

| When | Course | What happens |
|---|---|---|
| Aug - Sep 2026 | COSC 40943 | Teams and clients assigned. Specification authored: glossary, vision and scope, use cases, business rules, SRS. |
| Oct 2026 | COSC 40943 | Architecture-of-record drafted, then proven by one working vertical slice. Midterm Oct 19. |
| Oct - Nov 2026 | COSC 40943 | Fan-out one use case at a time. Testing, static analysis, CI/CD, observability wired in. |
| Dec 2026 | COSC 40943 | **MVP demoed to your client** (Dec 4, 7, 9). Final exam Dec 14. |
| Jan - Apr 2027 | COSC 40993 | Build out the remaining use cases against the specification you already own. |
| April 2027 | COSC 40993 | Final delivery to the client. |

The MVP in December is not a course exercise that ends with a grade. It is the halfway point of a real delivery, and the specification, architecture, and pipeline you build this fall are what you work from in the spring.

## Before anything else: what this costs you

A real organization is going to depend on what your team ships in December. That is the point of the course and it is also the obligation it creates.

**Expect 6 to 9 hours per week outside of class**, on a schedule your team sets rather than one you pick. See [the syllabus](syllabus.md#what-this-course-expects-of-your-time) for how attendance, peer evaluation, and client evaluation turn that expectation into 50% of your grade.

The single most reliable predictor of a struggling senior design team is not weak technical skill. It is a team that never found a time to meet. Teams that lock a recurring slot in week 2 and defend it tend to do well; teams that schedule week to week around whoever is busiest tend to drift, miss checkpoints, and discover in November that nobody owns anything. Your team contract fixes that time, and the whole team signs it.

## Teams and clients

Clients write project briefs before the semester. **The instructor assigns students to teams and projects** from a short interest and skills survey given in week 1. There is no pitch-and-choose round: with twelve teams it does not scale, and a written brief means your team has a real starting problem on day one rather than spending three weeks shopping.

That survey is **[here](https://forms.gle/m3vzou8VhPJ2pBTz6)**, and it closes Friday, Aug 28. It is the only input to who you work with and what you build, so it is worth ten unhurried minutes. If you cannot commit to at least four meeting blocks a week, say so in the survey and email the instructor before Friday.

**Teams, clients, and project briefs are announced Wednesday, September 2.** Each team is assigned a TA who stays with it all semester. Read your brief before Friday: Friday's studio is your team's first hour together, and you will spend it planning, not reading.

<!-- TODO(instructor): link the client briefs and publish the team roster once assignments are made. -->

## What you deliver this fall

Your specification and design set lives as version-controlled Markdown in your team's GitHub repository. It is not a pile of documents produced for a grade; it is the contract your coding agent builds against, and it is the reason your agent's output can be reviewed at all.

Your team also keeps a **Google Drive** for everything that is not part of that contract. The split is worth understanding rather than memorizing, because it explains the whole method:

| Team GitHub repository | Team Google Drive |
|---|---|
| Glossary, vision and scope, use cases, business rules, SRS | Weekly activity reports |
| Architecture-of-record, design-of-record | Team and client meeting minutes |
| Traceability matrix | Client-facing slides and demo decks |
| Source code and tests | Shared working drafts and scratch |

Anything the agent must build against, or that a consistency check must resolve, is Markdown in the repository. A use case in a Google Doc cannot be cited by an ID, diffed in a pull request, or verified against the code, so it is not a specification, it is a note about one. Everything else, where six people co-writing matters more than machine-readability, belongs in Drive. Share the Drive with the instructor and your TA at kickoff.

| Deliverable | What it is |
|---|---|
| Project glossary | The canonical domain vocabulary. Fixes the words used in every other document, in code identifiers, and in UI text. No synonyms. |
| Vision and scope | Business objectives, risks, assumptions, and the major features. |
| Use cases | Behavioral specifications grouped by area. Each use case is a high-level functional requirement; its steps and associated information are its acceptance criteria. |
| Business rules | Cross-cutting policies and constraints, cited by use cases, never restated in them. |
| Software requirements specification | Non-use-case functional requirements, the domain model, quality attributes, constraints, operating environment. |
| Architecture-of-record | The breadth-complete, depth-shallow map: every component and integration named and placed, internals deferred. |
| Design-of-record | At least one use-case area taken through the design gate: component design, sequence diagrams, API contracts, schema deltas, and the alternatives you rejected. |
| Traceability matrix | Specification to design to code to test, kept current, checked in both directions. |
| Source code | On GitHub. |
| MVP demo | Working software the client can actually test. |

!!! danger "The MVP is not optional"
    Working software with limited features **must** be available for the client to test at the end of the fall semester. Failing to do so results in a letter grade reduction for the entire team.

## Checkpoints

Four times in the term, your team presents to its TA during the Friday studio hour. Checkpoint 0 is the exception: it is a verification you pass, not a presentation you give.

| Checkpoint | Date | What you present |
|---|---|---|
| **0**, kickoff gate | Fri Sep 4 | Verified in the room, not presented. Every member present. Your recurring meeting slot fixed and written into the contract. Team contract signed by all six and committed to your repository as `docs/team-contract.md`. GitHub repository, Projects board, and Slack channel standing. First client meeting requested, with a date proposed. **The client meeting itself, with minutes, is due Mon Sep 14.** |
| **1** | Fri Oct 2 | Glossary, vision and scope, use cases, business rules, and draft SRS, reviewed. Architecture-of-record drafted: every use-case area, component, and external integration named. |
| **2** | Fri Oct 23 | The architecture proven by one working vertical slice: the highest-risk use case taken through design-of-record, implementation, and tests. Demonstrated running, not described. |
| **3** | Fri Nov 13 | Fan-out progress and production readiness. Multiple use cases built, tested, and traced, with the traceability matrix resolving. CI/CD pipeline with at least one quality gate, static analysis wired in, observability in place. |

Checkpoint 3 is the last one. After November 13 the next thing your client sees is the MVP demo, which means weeks 13 and 14 are hardening on your own schedule with no scheduled gate to catch you. Plan for that.

## Weekly mechanics

These run every week once the project starts, and they are 40% of your grade between them.

**Weekly activity report (WAR)** is due at the beginning of every Monday class. Inflating time or activities in a WAR is academic dishonesty. Late WARs are not accepted, and a missing WAR is a zero for that week's evaluation.

**Meeting minutes** for both team and client meetings are due every Monday before class. Team members take turns preparing them from the provided template. A missing set costs the person responsible 2.2%.

**Peer evaluations** of your teammates and yourself are due every Tuesday at 10:00 AM, based on your own observation and on their WARs. Late peer evaluations are not accepted.

**Client evaluations** happen twice during the semester. Your client's assessment of your engagement is 10% of your grade, so be present and useful in client meetings.

**Team and client meetings** happen outside the class period. Advise the instructor well in advance of client meetings so he can attend as many as his schedule allows.

## Contribution expectations

Every team member contributes to **the writing**. Each document section has one main author; others review and comment, and only the main author accepts or rejects a suggestion. Track your authorship in your WAR.

Every team member contributes to **the code**. Commit history is monitored periodically. "I did the documentation" is not a defense, and neither is "I let the agent handle my part."

**Every team member is full stack.** Work is divided by use case, not by layer: one developer owns a use case end to end, front end, back end, tests, and the pipeline that ships it. There is no front-end person, no database person, and no designated tester on this team. Splitting the system by layer ("I'll take the front end") is the failure you saw in week 1: the defect that appears where two layers meet belongs to nobody, nothing is done until two people agree it is, and neither of them graduates able to build a system. Teams are staffed so that up to six use cases move at once, each with one owner who can answer for it.

## Conflict

Team conflict is normal and it is engineered for, not improvised. Your team contract, drafted in week 2, names **your recurring meeting time**, how you make decisions, what responsiveness you owe each other, and what happens when someone does not deliver. Fix the meeting time first: it is the clause the rest depend on, and the one teams regret leaving vague. When the contract is not enough, escalate to your TA, then to the instructor. Escalate early. A problem raised in week 5 is a conversation; the same problem raised in week 14 is a grade dispute.
