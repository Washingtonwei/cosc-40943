# Senior Design Project

Thirteen teams of five or six students, twelve of them working with a real external client on a real problem. This fall you specify, design, and prove the system, and deliver a working MVP. In COSC 40993 next spring you build it out and deliver it, in April 2027.

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

Clients write project briefs before the semester. **The instructor assigns students to teams and projects** from a short interest and skills survey given in week 1. There is no pitch-and-choose round: with thirteen teams it does not scale, and a written brief means your team has a real starting problem on day one rather than spending three weeks shopping.

!!! tip "If your client handed you existing code"
    The code is evidence, never authority. When the agent drafts your specification or a design from it, every statement it recovers is a guess about what the client meant until the client confirms it, and behavior that looks wrong goes into `OPEN-ISSUES`, not into a requirement. See [Starting from an existing codebase](method.md#starting-from-an-existing-codebase).

**[Teams, clients, and TAs are published here.](teams.md)** Each team is assigned a TA who stays with it all semester. **Your client brief is on TCU Online**, filed under your team's number.

Read it before Friday. Friday's studio is your team's first hour together, and you will spend it planning, not reading.

## What you deliver this fall

Your specification and design set lives as version-controlled Markdown in your team's GitHub repository, a public repository owned by one named member ([how to set it up](studio.md#where-your-repository-lives)). It is not a pile of documents produced for a grade; it is the contract your coding agent builds against, and it is the reason your agent's output can be reviewed at all.

Your team also keeps a **Google Drive** for everything that is not part of that contract. The split is worth understanding rather than memorizing, because it explains the whole method:

| Team GitHub repository | Team Google Drive |
|---|---|
| Glossary, vision and scope, use cases, business rules, SRS | Team and client meeting minutes |
| Architecture-of-record, design-of-record | Client-facing slides and demo decks |
| Traceability matrix | Shared working drafts and scratch |
| Source code and tests | |

Anything the agent must build against, or that a consistency check must resolve, is Markdown in the repository. A use case in a Google Doc cannot be cited by an ID, diffed in a pull request, or verified against the code, so it is not a specification, it is a note about one. Everything else, where six people co-writing matters more than machine-readability, belongs in Drive. Share the Drive with the instructor and your TA at kickoff. Weekly activity reports and peer evaluations go in neither; you submit them in Project Pulse (see [Weekly mechanics](#weekly-mechanics)).

**Your repository is public, so keep your client's material out of it.** The brief stays on TCU Online, and anything your client hands you or asks you to keep private stays in Drive. What goes in the repository is what your team writes: the specification, the design, the code.

| Deliverable | What it is |
|---|---|
| Project glossary | The canonical domain vocabulary. Fixes the words used in every other document, in code identifiers, and in UI text. No synonyms. |
| Vision and scope | Business objectives, risks, assumptions, and the major features. |
| Use cases | Behavioral specifications grouped by area. Each use case is a high-level functional requirement; its steps and associated information are its acceptance criteria. |
| Business rules | Cross-cutting policies and constraints, cited by use cases, never restated in them. |
| Software requirements specification | Non-use-case functional requirements, the domain model, quality attributes, constraints, operating environment. |
| Architecture-of-record | The breadth-complete, depth-shallow map: every component and integration named and placed, internals deferred. |
| Design-of-record | At least one use-case area taken through the design gate: component design, sequence diagrams, API contracts, schema deltas, the alternatives you rejected, and the test list, approved by pull request. |
| Traceability matrix | Specification to design to code to test, kept current, checked in both directions. |
| Source code | On GitHub. |
| MVP demo | Working software the client can actually test, released as `v1.0.0` with release notes. |

!!! danger "The MVP is not optional"
    Working software with limited features **must** be available for the client to test at the end of the fall semester. Failing to do so results in a letter grade reduction for the entire team.

## Checkpoints

Four times in the term, your team presents to its TA during the Friday studio hour. Checkpoint 0 is the exception: it is a verification you pass, not a presentation you give.

| Checkpoint | Date | What you present |
|---|---|---|
| **0**, kickoff gate | Fri Sep 4 | Verified in the room, not presented. Every member present. Your recurring meeting slot fixed and written into the contract. Team contract signed by every member and committed to your repository as [`docs/team-contract.md`](team-contract.md), each member signing in their own commit. GitHub repository, Projects board, and Slack channel standing, with your TA and the instructor on both. First client meeting requested, with a date proposed. **The client meeting itself, with minutes, is due Mon Sep 14.** |
| **1** | Fri Oct 2 | Glossary, vision and scope, use cases, business rules, and draft SRS, reviewed with your TA in the room. Architecture-of-record drafted in the same studio and merged by 11:59 pm: every use-case area, component, and external integration named. Your TA checks it over the weekend and replies by Sunday evening. See the [studio](studio.md#week-6-oct-2-checkpoint-1-and-your-architecture-of-record). |
| **2** | Fri Oct 23 | The architecture proven by one working vertical slice, demonstrated running, not described. See the [Checkpoint 2 checklist](#checkpoint-2-checklist) below. |
| **3** | Fri Nov 13 | Fan-out progress and production readiness, demonstrated from a tagged release (`v0.2.0`) with release notes. Multiple use cases built, tested, and traced, with the traceability matrix resolving. CI/CD pipeline with at least one quality gate, static analysis wired in, observability in place. The calibration table extended to every finished use case, with a ratio per person and for the team, and one forecast line under it: does `v1.0.0` still fit the hours left ([how](modules/traceability.md#from-estimates-to-a-release-plan))? At least one rule in your agent charter that came from a review, merged by pull request ([closing a use case](method.md#phase-c-fan-out-per-use-case)). One availability or performance requirement turned into a [measured objective](modules/reliability.md#7-hands-on-studio-optional-individual-assignment), and one test that makes an external dependency fail and checks the degradation your specification requires. Graded on completeness and honest interpretation, never on accuracy. |

Checkpoint 3 is the last one. After November 13 the next thing your client sees is the MVP demo, which means weeks 13 and 14 are hardening on your own schedule with no scheduled gate to catch you. Plan for that.

### Checkpoint 2 checklist

Your TA works through this list in the room on Fri Oct 23.

- [ ] **The slice runs.** Your highest-risk use case, taken through design-of-record, implementation, and tests, demonstrated running from a tagged release `v0.1.0` with release notes ([why a tag](modules/ai-augmented-team.md#410-knowing-exactly-what-you-built)).
- [ ] **The settings file.** `.claude/settings.json` merged by pull request, with `Read` deny rules covering where your secrets actually live ([the file](agent-setup.md#10-your-team-repository)).
- [ ] **The charter.** Its list of things the agent must not do includes the [dependency rule](modules/implementation.md#48-what-the-agent-may-read-and-run) and never removing the `Co-Authored-By` trailer. If you run more than one agent at a time, its workflow section has the [four parallel-agent lines](agent-setup.md#10-your-team-repository).
- [ ] **The calibration table.** Each finished use case: its estimate, its actual hours from your weekly activity reports, the ratio, and one sentence on the biggest miss ([how](modules/implementation.md#44-recording-and-calibrating)). Graded on completeness and honesty, never accuracy.
- [ ] **The release plan.** Every use case and FR row in `docs/traceability.md` has a Release value (`v0.1.0`, `v0.2.0`, `v1.0.0`, `Spring`, or `Out`), set by pull request ([how](modules/traceability.md#from-estimates-to-a-release-plan)).

You leave with Checkpoint 3's two reliability items: one measured SLO and one degradation test ([Reliability](modules/reliability.md#7-hands-on-studio-optional-individual-assignment)). Start them that week. The week 12 lecture builds on what you will already have begun.

## Weekly mechanics

These run every week once the project starts, and they are 40% of your grade between them.

You submit weekly activity reports and peer evaluations in **Project Pulse**. Its registration invitation and the Monday and Tuesday reminders come from `peer.evaluation.tool.senior.design@gmail.com`. Add that address to your safe senders: a reminder sitting in your junk folder does not extend a deadline.

**Weekly activity report (WAR)** is due in Project Pulse at the beginning of every Monday class. A line about a use case starts with its ID (`UC-<AREA>-<slug>: ...`), so its hours can be added up against [its estimate](modules/implementation.md#44-recording-and-calibrating). Inflating time or activities in a WAR is academic dishonesty, and so is shrinking them to make an estimate look accurate. Late WARs are not accepted, and a missing WAR is a zero for that week's evaluation.

**Meeting minutes** for both team and client meetings are due every Monday before class. Team members take turns preparing them from the provided template. A missing set costs the person responsible one weekly evaluation's worth, about 1.8%.

**Peer evaluations** of your teammates and yourself are due in Project Pulse every Tuesday at 10:00 AM, based on your own observation and on their WARs. Late peer evaluations are not accepted.

**Client evaluations** happen twice during the semester. Your client's assessment of your engagement is 10% of your grade, so be present and useful in client meetings.

**Team and client meetings** happen outside the class period. Advise the instructor well in advance of client meetings so he can attend as many as his schedule allows.

## Contribution expectations

Every team member contributes to **the writing**. Each document section has one main author; others review and comment, and only the main author accepts or rejects a suggestion. Track your authorship in your WAR.

Every team member contributes to **the code**. Commit history is monitored periodically. "I did the documentation" is not a defense, and neither is "I let the agent handle my part."

**Every team member is full stack.** Work is divided by use case, not by layer: one developer owns a use case end to end, front end, back end, tests, and the pipeline that ships it. There is no front-end person, no database person, and no designated tester on this team. Splitting the system by layer ("I'll take the front end") is the failure you saw in week 1: the defect that appears where two layers meet belongs to nobody, nothing is done until two people agree it is, and neither of them graduates able to build a system. Teams are staffed so that up to six use cases move at once, each with one owner who can answer for it.

## Conflict

Team conflict is normal and it is engineered for, not improvised. Your team contract, drafted in week 2, names **your recurring meeting time**, how you make decisions, what responsiveness you owe each other, and what happens when someone does not deliver. Fix the meeting time first: it is the clause the rest depend on, and the one teams regret leaving vague. When the contract is not enough, escalate to your TA, then to the instructor. Escalate early. A problem raised in week 5 is a conversation; the same problem raised in week 14 is a grade dispute.

How to run the conversation before it gets that far is [Professionalism](modules/professionalism.md); the standards, the accountability process, and the FAQ are in the [Professionalism handbook](professionalism.md).
