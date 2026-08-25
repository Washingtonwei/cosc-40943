# Schedule

August 24 to December 9, 2026. Monday and Wednesday are lecture, demonstrated on Project Pulse. Friday is [studio](studio.md), where your team applies the week's move to your own client project.

This calendar represents current plans. Changes will be announced in class and pushed to this page.

## No class on these days

| | |
|---|---|
| **Labor Day** | Monday, September 7 |
| **Fall break** | Thursday, October 8 and Friday, October 9. Classes recess Wed Oct 7 at 10:00 PM, resume Mon Oct 12 at 8:00 AM. |
| **Thanksgiving break** | Monday, November 23 through Friday, November 27. Classes recess Fri Nov 20 at 10:00 PM, resume Mon Nov 30 at 8:00 AM. |

Dates from the TCU Registrar's [Fall 2026 academic dates](https://registrar.tcu.edu/fall-academic-dates.php). The term runs **fifteen instructional weeks**.

## The arc

- **Weeks 1-2, setup.** Why software engineering, what AI changes, and standing up the team, GitHub, and Project Pulse. You use AI from day one.
- **Weeks 3-13, run the method.** Author the specification and a breadth-complete architecture, prove it with one vertical slice, then fan out one use case at a time.
- **Weeks 10-15, production readiness.** Gate, automate, observe, maintain, reflect. Overlaps the end of the fan-out.

## Week by week

| Wk | Dates | Mon + Wed lecture | Fri studio | Project milestone |
|----|-------|-------------------|------------|-------------------|
| 1 | Aug 24, 26, 28 | A real failure story; what software engineering is, and what AI changed about the job; the delegation boundary, the Napkin frame, and how an agent session goes wrong<br>[Story](slides/fifteen-weeks-to-demo-day.html){ .mat } [Slides](slides/se-and-ai.html){ .mat } [Reading](modules/se-and-ai.md){ .mat } | Onboarding: environment setup, run Project Pulse once, first AI-assisted task | Interest and skills survey, due Fri Aug 28 |
| 2 | Aug 31, Sep 2, 4 | The AI-augmented team and GitHub as single source of truth; professionalism, team contract, conflict protocol | **Checkpoint 0** (kickoff gate), after standing up your repo, board, and Slack | Teams and client briefs released Mon Aug 31; contract signed, board up, client meeting 1 |
| 3 | ~~Sep 7~~, 9, 11 | *Labor Day, no class Monday.* Requirements as the contract (1 of 2): glossary, vision and scope, use cases | Napkin **round 0** on your own project, then author your glossary and vision and scope | Requirements elicitation begins |
| 4 | Sep 14, 16, 18 | Requirements as the contract (2 of 2): business rules, quality attributes, the SRS | Write your use cases and business rules; draft the SRS | Draft specification underway |
| 5 | Sep 21, 23, 25 | Context engineering: the specification is the context, and when is it enough | Napkin **round 1**, then turn one use case into an agent build-context | Draft specification validated against build-contexts |
| 6 | Sep 28, 30, Oct 2 | Software architecture, just enough: breadth-complete and depth-shallow, architecturally significant requirements, security as a quality attribute | **Checkpoint 1** to your TA | Specification reviewed; architecture-of-record drafted |
| 7 | Oct 5, 7, ~~9~~ | Design-of-record and design decisions; the design gate; proving the architecture with one vertical slice | *Fall break, no studio.* Take one high-risk use case through design-of-record **out of class**, before week 8 | Proving slice built |
| 8 | Oct 12, 14, 16 | AI-assisted implementation, and the traceability anchor: forward and backward<br>[Reading](modules/traceability.md){ .mat } | Napkin **round 2**, then implement a use case with the agent and trace it design to code to first test | Fan-out begins |
| 9 | Oct 19, 21, 23 | **Mon Oct 19: midterm exam.** Wed: testing, the pyramid and AI-generated tests | **Checkpoint 2** to your TA | Architecture and proving slice demo |
| 10 | Oct 26, 28, 30 | Static analysis: linters, SpotBugs, ESLint, shift left, running in CI | Napkin **round 3**, then wire linters and run the tools on your repo | More use cases built and traced |
| 11 | Nov 2, 4, 6 | CI/CD: automating the gates, linters and tests in a pipeline | Napkin **round 4**, then build a pipeline with quality gates on your repo | Continuous deployment live |
| 12 | Nov 9, 11, 13 | Observability and debugging: logs, metrics, traces; dynamic analysis as a lens | **Checkpoint 3** to your TA | Fan-out plus production readiness |
| 13 | Nov 16, 18, 20 | Maintainability, readability, developer tooling; software metrics and technical debt as a lens | Run the traceability honesty check on your repo; refactor with the agent | Production hardening |
| | *Nov 23-27* | *Thanksgiving break, no class* | | |
| 14 | Nov 30, Dec 2, 4 | Ethics capstone and the graduate-profile reflection, including Napkin **round 5** | **MVP demos, teams 1-4** | Demo dry-runs |
| 15 | Dec 7, 9 | **MVP demos, teams 5-8** (Mon) and **teams 9-12** (Wed); team retrospective | *No studio, last day of class is Wed Dec 9* | MVP delivered to client |

**Final exam:** Monday, December 14, 8:00 - 10:30 AM.

Each week's materials are linked at the end of its lecture cell. **Slides** is that week's deck, **Story** is a narrated set piece where there is one, and **Reading** is the full written module behind the lecture, for when you want more than the deck. Reading is optional unless a row says otherwise. Links appear as material is written, so weeks further out are still bare.

<!-- Materials chips: end the lecture cell with <br> then one chip per item. Week 1 is the
     worked example. Styles are in docs/assets/extra.css.

       [Slides](slides/<module-slug>.html){ .mat }
       [Story](slides/<deck-name>.html){ .mat }
       [Reading](modules/<module-slug>.md){ .mat }

     Decks are authored at docs/slides/<module-slug>.md and compiled by decks/hook.py during the
     build (DECISION-html-slides). Do not link to Google Slides or .pptx. -->

## Checkpoints

Four times in the term, the Friday studio hour is your team's checkpoint presentation to its TA. That week's own-project objective moves to out-of-class team time.

**Fri Sep 4** (kickoff gate) · **Fri Oct 2** · **Fri Oct 23** · **Fri Nov 13**. They are marked in the grid above.

**What each checkpoint requires is on the [Senior Design Project](project.md#checkpoints) page**, which is the page to read before you prepare one. After Checkpoint 3 the next thing your client sees is the MVP demo, so weeks 13 and 14 are hardening on your own schedule.

## Threaded through every week

Some topics get no row of their own because they are practiced continuously rather than taught once.

- **Code review.** Every studio reviews AI output. This is the highest-leverage human skill in the course.
- **Traceability.** Practiced weekly after the week 8 anchor, on your growing codebase.
- **Risk.** Every topic carries the classic failure and the one AI introduces or amplifies.
- **The delegation boundary.** Revisited at each new topic: what do we hand the agent here, and what stays human?
- **Security.** Enters in week 6 as an architecturally significant requirement, then threads through implementation, static analysis, and CI/CD.
- **Ethics.** Surfaces as real cases arise, and is capstoned in week 14.

## Self-study this term

**Open source: dependencies and supply chain, contributing to code you do not own, reading an unfamiliar codebase with an agent.** Fifteen weeks do not hold every topic worth knowing, and this is the one taught as reading rather than in class. The written module stands on its own and is worth your time before you start interviewing; it is not examined.

## The Napkin drill

Six times across the term, studio opens with a twenty-minute warm-up: size up an unfamiliar problem brief, naming its shape, the hard part, the bottleneck, a plausible stack, three kill risks, and a feasibility verdict. You write yours alone first, then reconcile as a team, then compare against the agent's version. The comparison is where the learning is.

| Round | When |
|---|---|
| 0, your own client project, sealed | Fri Sep 11 |
| 1 | Fri Sep 25 |
| 2 | Fri Oct 16 |
| 3 | Fri Oct 30 |
| 4 | Fri Nov 6 |
| 5, round 0 reopened and scored | Week of Nov 30, in lecture |

Round 0 napkins **your own client project** before the specification exists. It is sealed on the spot, and reopened in week 14 to be scored against what actually happened. Rounds 0 through 4 are ungraded; the closing reflection is graded on how well-calibrated you were, not on having been right.
