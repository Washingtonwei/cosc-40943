# Process and Planning

**Slides:** [Estimating When the Agent Writes the Code](../slides/process-and-planning.html) (the fast version).

> **Purpose (one line):** estimate a use case in human hours before your agent builds it, make each next estimate better from the hours you actually logged, plan which release each use case ships in and whether the MVP still fits, and name the life-cycle model a team is running and what it bets on.

!!! note "This module is still being written"
    This page covers estimation and life-cycle models. The risk vocabulary (categories, impact and likelihood) is coming.

## 1. Learning objectives

By the end of this module, a student can:

1. Tell an estimate from a target and a commitment, and say which one a client is asking for.
2. Name the assumption behind each classical estimation technique and say whether it still holds when an agent writes the code.
3. Estimate a use case as a range of human hours, split into specify, build and review, and verify, sized from its design's test list.
4. Record the estimate before the build and the actual hours in the weekly activity report, and compute a calibration ratio from the two.
5. Use a calibration ratio to correct the next estimate, and tell the client early when a commitment no longer fits.
6. Place every use case in a release in the traceability matrix, and forecast from the remaining estimates and the calibration ratio whether the MVP fits.
7. Name what each major life-cycle model (waterfall, incremental, iterative, spiral, the Unified Process, agile) bets on, and say when each fits.
8. Place this course's method among those models, and map Scrum's vocabulary onto the units this course uses.

## 2. Where it fits

- **Prerequisites:** [Design-of-Record](design-of-record.md), whose test list is the size measure this module uses.
- **Leads into:** the fan-out, where every use case your team builds gets an estimate first, and [Checkpoint 2](../project.md#checkpoints) and Checkpoint 3, where your team shows its estimates beside its actual hours, its release plan, and at Checkpoint 3 a forecast.
- **How it's taught:** life-cycle models are introduced in week 1 and read here in full; estimation is one lecture segment in week 8, before the first use case of the fan-out is built; whatever the lecture does not reach, read here. From then on it is practiced, not lectured: an estimate on every use-case issue, the use case ID on every weekly activity report line, and a calibration table at each checkpoint.
- **Course outcome it delivers:** [sizing up a problem and judging whether it is feasible for this team in this time](../syllabus.md#learning-outcomes) (outcome 10), carried from the first week's Napkin drill into a number your client can plan around.

## 3. Motivation

**The client's question.** Project Pulse's instructors asked for a reminder that emails only the students who have not submitted. Its design, [`not.md`](https://github.com/Washingtonwei/project-pulse/blob/main/docs/design/not.md), is approved. Before anyone runs `/implement`, the instructor asks the question every client asks: *when can I use it?*

The old way to answer counts the code: a controller, a new `SubmissionStatusService`, changes to the scheduler, a dialog, their tests, then hours per unit of code. An agent will write all of that in one session. If the code were the cost, the answer would be "this afternoon."

It is not this afternoon. The design's [test list](https://github.com/Washingtonwei/project-pulse/blob/main/docs/design/not.md#tests) has 18 rows, and each one is a behavior a person has to see pass: a student who reported is not emailed, an unassigned instructor gets `403`, a first name containing `<b>` is escaped. Its open-questions list carries five risks, one of which (whether 80 emails over Gmail sent during the request finish in a comfortable time) cannot be settled until it is measured on staging. The hours are in specifying, reviewing, and verifying. The agent made the typing free and left everything else.

**Your feeling of speed is not data.** In 2025, METR ran a randomized controlled trial with 16 experienced open-source developers on 246 issues from their own repositories. Before starting, they expected AI tools to make them 24% faster. With the tools they took 19% longer. Afterward, they still believed the tools had made them 20% faster. METR's 2026 follow-up suggests later tools probably do speed developers up, but its confidence intervals include no change at all, and METR calls its own data "very weak evidence" for the size of the effect. Either way, the lesson for estimation holds: a developer's sense of how long agent-assisted work took was wrong by about 40 points, in the flattering direction.

**The hours moved; they did not vanish.** Faros AI's telemetry from more than 10,000 developers on 1,255 teams (June 2025) found that teams with high AI adoption merged 98% more pull requests, while pull requests grew 154% larger and review time rose 91%. It is a vendor's correlational data, not an experiment, but it points the same way: generation got cheap, and the cost moved to the person reading the result.

## 4. Core concepts

### 4.1 Estimate, target, commitment

Three different things share one sentence ("it'll take two weeks"), and confusing them is the oldest failure in planning (McConnell 2006):

| | What it is | Who owns it | Example |
|---|---|---|---|
| **Estimate** | A prediction, with a range | The person doing the work | "3 to 5 hours of work, most likely about 3.5" |
| **Target** | A wish about the date | The client or the business | "We'd like it before the midterm" |
| **Commitment** | A promise to deliver by a date | The team, after comparing the two | "It will be on staging by Friday, Oct 23" |

An estimate is a range because it is uncertain. A commitment is a single date because someone will plan around it. When the target and the estimate do not fit, you change the scope, not the estimate.

The range narrows as decisions get made. Boehm (1981) measured it: at the concept stage an estimate can be off by a factor of four in either direction, and the spread shrinks as requirements, then design, are settled; McConnell (2006) named the shape the *cone of uncertainty*. This is why you estimate a use case *after* its design-of-record is approved, not before: the design is what turned "how hard is a reminder?" into 18 named tests and five named risks.

### 4.2 The classical techniques, and what each one assumed

| Technique | Origin | What it sizes | The assumption | With an agent writing the code |
|---|---|---|---|---|
| **Expert judgment** | The oldest; the most used in practice (Jørgensen 2004) | Whatever the expert compares it to | The expert has done comparable work | Holds only if "comparable" includes doing it *with an agent*; experience from before agents is the wrong reference |
| **Wideband Delphi**, then **planning poker** | Boehm 1981; Grenning 2002 | Same, but several people estimate independently, then discuss the gap | Independent estimates beat one anchored voice | Holds. Nothing about agents makes anchoring less dangerous |
| **Story points and velocity** | Extreme Programming, popularized by Cohn 2005 | Relative size, converted to time by the team's measured pace | The pace is stable from one iteration to the next | Breaks while the tools are changing every few months; a velocity measured in September describes September's agent |
| **Function points** | Albrecht 1979 | What the software does for its users: inputs, outputs, inquiries, files, interfaces | Effort per function point is stable for a team | The *size* still holds; the hours per function point, measured when people wrote the code, do not |
| **COCOMO** | Boehm 1981 | Effort as a function of thousands of lines of code, scaled by cost drivers | A line of code costs roughly the same to produce | Breaks. An agent produces lines at almost no cost; the cost is in reading them |

Read down the last column and one pattern appears: every model converts a **size** into **hours** through a **rate measured when people wrote the code**. The size measures mostly survive. The rate is what agents changed. So the course keeps a size measure (the test list), throws away the borrowed rate, and measures its own (4.5).

### 4.3 Where the hours go now

Estimate a use case in three parts, each as a range of human hours:

| Part | What the hours buy | Weekly activity report categories |
|---|---|---|
| **Specify** | Closing the gaps the agent would otherwise guess at: fixing the use case, the design, or the build-context when the questions test or the build exposes a hole | `DESIGN`, `DOCUMENTATION` |
| **Build and review** | Driving the agent, reading every line of its diff against the design, sending it back | `DEVELOPMENT` |
| **Verify** | Making each row of the test list pass and seeing it pass, running the flow end to end, fixing what that finds | `TESTING`, `BUGFIX` |

**Size it from the test list.** Each row is one behavior a person has to see working, so the row count is the closest thing the course has to a function-point count: it measures what the software must do, and it is already written. The open-questions list sets the width of the range: a risk that can only be settled by measuring (like the reminder's email latency) widens the high end.

What the agent does not change is how long it takes *you* to understand a diff and know it is right. That is the term to estimate carefully.

### 4.4 Worked example: the reminder

The estimate for `UC-NOT-remind-non-submitters` and `FR-NOT-weekly-reminder`, made from `not.md` before `/implement` runs:

| Part | Basis | Estimate (hours) |
|---|---|---|
| Specify | Design approved; the questions test already closed its three contradictions and sixteen guesses. Allow for holes the build exposes | 0.5 to 1 |
| Build and review | Every diff read against the sequence diagrams | 1.5 to 2 |
| Verify | 18 agent-written test rows: trunk rows read line by line, leaf rows checked by running them. The email-latency risk can only be measured on staging, and it sets the high end | 1 to 2 |
| **Total** | The same size as the reference change below, which took about 3.5 hours end to end | **3 to 5, most likely about 3.5** |

**The reference.** [Project Pulse pull request #76](https://github.com/Washingtonwei/project-pulse/pull/76), which hardened student invitations, is the closest change already built with an agent: 884 lines added across 23 files, a new endpoint and dialog, a scheduler change, and two review rounds that each caught real defects. It took about 3.5 hours from first commit to merge, so the reminder, a change of the same size, should take about the same. A reference class is your own past work, not someone else's; your first ones will be slower than the instructor's in a codebase the instructor wrote, and the calibration ratio in 4.5 is what corrects for that.

The commitment that follows: on staging by the Friday of the build week, with the latency measured, or a message to the instructor by Wednesday saying why not.

The actual hours are recorded after the build, and this table gains an *Actual* column.

<!-- DRAFTING NOTE: fill in the Actual column from the build. -->

### 4.5 Recording and calibrating

An estimate nobody checks teaches nothing. The course already records the other half: every line of your weekly activity report in Project Pulse carries **planned hours** and **actual hours** (the `Activity` entity, [`Activity.java`](https://github.com/Washingtonwei/project-pulse/blob/main/backend/src/main/java/team/projectpulse/activity/Activity.java)). Three habits connect the two:

1. **Before building**, the use case's owner writes the estimate on its issue: `Estimate: specify 0.5–1 h, build and review 1.5–2 h, verify 1–2 h.`
2. **Every week**, each weekly activity report line about that use case starts with its ID (`UC-NOT-remind-non-submitters: reviewed the agent's diff against the sequence diagram`) and uses the category from the table in 4.3.
3. **When the use case is done**, sum the actual hours across weeks and compute the **calibration ratio**: actual hours divided by the midpoint of the estimate.

A ratio of 1.5 means you take half again as long as you think. Multiply your next midpoint by it, and keep the range. Track it per person and per team: six ratios on a team is how you find out that review, not building, is where your team's hours go.

When the ratio says a commitment will slip, tell the client at the next meeting, not on the date. A slipped commitment reported early is planning; reported late, it is a broken promise.

### 4.6 From estimates to a release plan

An estimate answers "when can I use this one?" The client's next question is "what will I have in December?" Answering it takes a **release plan**: every use case placed in the release it ships in. Agile planning has always done this with stories and velocity (Beck and Fowler 2000; Cohn 2005). The course keeps the idea and changes the units.

**It is a column, not a document.** Your `traceability.md` already has one row per use case (and per non-use-case FR) with its Build and Verify state. The plan is one more column, **Release**: `v0.1.0` (the proving slice), `v0.2.0` (Checkpoint 3), `v1.0.0` (the December MVP), `Spring`, or `Out`. Plan and progress share a row, so they cannot disagree, and an empty cell is work nobody has planned. Your client agrees to scope by feature in vision and scope's MVP Scope section; the column carries that agreement down to use cases.

**Placing the rows.** Risk first, for the reason your proving slice went first ([4.11](#411-spiral-let-risk-choose-the-next-step)): a wrong decision found in week 9 is cheap, and in week 14 it is not. Then what the client needs first, then dependencies. When something goes ahead of risk, the pull request that changes the column says why: the column holds the decision, and git holds the reason.

**Project Pulse's plan.** Project Pulse shipped up to `v1.5.0` without a release plan. Its [Release column](https://github.com/Washingtonwei/project-pulse/blob/main/docs/traceability.md#release-legend) starts with the work that is left:

| Release | What ships | Why there |
|---|---|---|
| `v1.6.0` | The reminders: on-demand (`UC-NOT-remind-non-submitters`), and the scheduled one brought in line with `BR-submission-owed` | Designed; built in week 8 |
| `v1.7.0` | The rest of the requirements editor: artifact and link screens, comments, review, export | Backends built and tested; the client wants the editor finished first |
| `v1.8.0` | The first AI assistant end to end: `UC-AI-critique`, the proposal loop, its settings, the model proxy | The riskiest work: the first model call, with the outage scenario measured |
| `v1.9.0` | ReqLint and the tutor | The tutor explains ReqLint's findings, so it follows ReqLint |
| `v2.0.0` | The other six assistants | The Fall 2027 classroom deployment |

Risk alone would put `v1.8.0` before `v1.7.0`. The client chose otherwise, and the plan records that trade instead of hiding it. Writing the column also exposed a disagreement: the vision listed real-time co-editing as out of the MVP, while traceability showed it as unstarted work. The use case's own Status line already said Deferred, so that line settles it, and its Release cell stays empty: one fact, one owner.

**The forecast.** A use case that is not designed yet has no test list, so size it from what it has, its main scenario and extensions, as a range wider than 4.3's: it sits earlier in the cone of uncertainty (4.1). Write that range on the use case's issue; when its design is approved, the three-part estimate replaces it. Then:

> **Hours still needed** = the sum of the estimate midpoints of every unfinished `v1.0.0` row × your team's calibration ratio

Compare that with the hours your team will have before the MVP demo, judged from what your weekly activity reports show you actually work. If the plan does not fit, move rows out of `v1.0.0` with your client at the next meeting. This is 4.1's rule in practice: when the estimate and the target disagree, change the scope, not the estimate. Write the result as one line under your calibration table:

`Forecast: 6 rows left in v1.0.0, 38 to 60 h at ratio 1.4; about 70 h available. Fits, with no slack for the high end.`

Revise the column at every use-case close ([the method, Phase C](../method.md#phase-c-fan-out-per-use-case)), and recompute the forecast whenever the ratio moves.

### 4.7 What an estimate is not for

An estimate is not a performance score. Once estimates are used to pressure people, they stop being honest, and a dishonest estimate is worse than none (Jeffries 2021). The course grades whether you **recorded** and **interpreted** your estimates, never whether they were accurate: a team that reports a ratio of 2.3 and says why earns the same credit as a team at 1.0. Inflating the actual hours in a weekly activity report to make a ratio look good is academic dishonesty, as any inflated report is.

### 4.8 Life-cycle models: each one is a bet on what is expensive

[Week 1](se-and-ai.md#the-software-development-life-cycle-sdlc) drew the life cycle as eight activities in a loop. A **life-cycle model** (or *process model*) decides how a team moves through them: once, in order, or many times, in slices. Every model is a bet on what costs the most, and each was right for the costs of its time:

| Model | Its bet | Fits when |
|---|---|---|
| **Waterfall** | Change is expensive late, so decide everything first | Requirements are known and stable: regulated systems, fixed hardware, fixed-price contracts |
| **Incremental** | Value should arrive early, one complete piece at a time | The core is clear, but not all of it is needed at once |
| **Iterative** | You learn what to build by building a rough version | The product's shape is uncertain |
| **Spiral** | Risk, not a schedule, should choose the next step | Some decision could sink the project if it is wrong |
| **Unified Process** | Use cases drive the work, and architecture is proven early | A system big enough to need an architecture, with requirements that keep moving |
| **Agile (Scrum, Kanban)** | Requirements will change, so deliver working software often and adjust | A customer close enough to give feedback every week or two |

### 4.9 Waterfall, and what Royce actually wrote

Waterfall runs the activities once, each signed off before the next begins. Real projects do not flow one way, clients cannot state every requirement up front, and nobody sees working software until the end, when change costs most.

It is usually traced to Winston Royce's 1970 paper, which drew the phases in sequence and then wrote under the figure: "I believe in this concept, but the implementation described above is risky and invites failure." The rest of the paper adds what the single pass lacks: feedback between steps, early simulation, the customer involved throughout, and building the program twice. The word "waterfall" is not in it. Later standards and contracts adopted the figure and dropped the corrections (Larman and Basili 2003).

### 4.10 Incremental and iterative

- **Incremental:** build one feature at a time, each to full quality, and ship as you go. Your fan-out is incremental: one use case at a time, each designed, built, tested, and traced before it counts as done.
- **Iterative:** build everything roughly, then improve all of it in passes. Your specification is iterative: the first draft for Checkpoint 1, then revised every time the design or the build exposes a gap.

Jeff Patton's illustration: an incremental painter finishes the Mona Lisa one square at a time; an iterative one sketches the whole portrait, then refines it. Working teams do both.

### 4.11 Spiral: let risk choose the next step

In Boehm's spiral model (1988), every cycle starts by asking what could sink the project now, then spends the cycle reducing that risk with a prototype, a simulation, or a measurement. Your proving slice is a spiral cycle: of all your use cases, you build first the one that exercises the riskiest architectural decisions, because finding out it is wrong in week 9 is cheap and in week 14 is not.

### 4.12 The Unified Process, and this course's method

The Unified Process (Jacobson, Booch, and Rumbaugh 1999; IBM's commercial version was the Rational Unified Process) describes itself in three phrases: **use-case driven, architecture-centric, iterative and incremental**. It runs in four phases, each made of iterations. The course's [method](../method.md#the-lifecycle) is closest to it:

| Unified Process | The course's method |
|---|---|
| **Inception**: vision, scope, the main use cases | Phase A: vision and scope, use cases, business rules (weeks 3 to 5) |
| **Elaboration**: most use cases, and an executable architecture baseline that proves the risky decisions | Phase A's architecture-of-record (week 6), then Phase B's proving slice, chosen by risk (weeks 7 to 9) |
| **Construction**: build the remaining use cases, iteration by iteration | Phase C: fan out, one use case at a time (weeks 9 to 14) |
| **Transition**: hand the system to its users | The MVP your client receives |

The method's life cycle is not new: its phases are the Unified Process's, with a spiral's risk-first slice. What is new is what moves through them. The specification is written for an agent to build from, complete where guessing is unsafe and silent where the agent may derive. The agent challenges the specification before it builds, and the questions test measures whether the specification is enough. Humans own some levels and the agent builds others, behind approval gates. Traceability is kept true by tooling rather than by discipline. And the work flows one use case at a time instead of in time-boxed iterations.

### 4.13 Agile, Scrum, and Kanban: the vocabulary you will meet

The *Manifesto for Agile Software Development* (Beck et al. 2001) values working software, customer collaboration, and responding to change over documentation, contracts, and following a plan, while granting that the second list still has value. Two practices dominate industry:

- **Scrum** (Schwaber and Sutherland 2020): work happens in **sprints** of a month or less. A **product backlog** is ordered by the **Product Owner**; the team pulls a **sprint backlog** from it at **sprint planning**, meets briefly every day, shows the result at the **sprint review**, and improves its process at the **retrospective**. An item counts only when it meets the team's **definition of done**.
- **Kanban** (Anderson 2010): no sprints. Work flows across a board, and each column has a limit on how many items it may hold, so the team pulls new work only when something finishes.

This course uses parts of both under its own units. Your board, backlog, and weekly iteration are [week 2's vocabulary](ai-augmented-team.md#411-the-boards-vocabulary); your definition of done is a merged pull request that meets the use case's acceptance criteria. The use case replaces the user story, a use-case area is a milestone, and your client, not a teammate, owns what gets built.

### 4.14 What agents change

Agents make code cheap and iteration cheaper. Royce's "build it twice" used to double the cost; now a throwaway first version takes an afternoon, and Brooks's advice to "plan to throw one away" (1975) costs almost nothing to follow. What did not get cheaper is deciding what to build and checking what was built ([4.3](#43-where-the-hours-go-now)). So the bet shifts: spend human effort on specification and verification, and let the agent do the iterating, each use case built and rebuilt as often as review allows.

## 5. The AI-native lens

- **Delegate to AI:** the counting. Give the agent the design-of-record and it can list the test rows, the files the sequence diagrams touch, and the open risks, and draft the three-part breakdown. Give it your weekly activity report lines and it can sum the actual hours by use case ID. Give it the traceability matrix and the ranked quality attributes and it can draft the Release column and add up the forecast.
- **Keep human:** the hours and the commitment. An agent asked "how long will this take?" answers from text written about teams that wrote their own code; it has no record of your hours, your review speed, or this term's agent. The commitment to a client is a promise, and only a person can make one. So is the cut line: which use cases leave `v1.0.0` is agreed with the client, never decided by the agent.
- **Context to supply:** the approved design, its test list and open questions, and your team's current calibration ratio.
- **How to verify:** check the agent's breakdown against the design (every test row counted, every open risk reflected in the range). Never accept an hour figure from it, including one it presents as a range.

## 6. Risks & mitigations

| Risk (classic + AI-introduced) | Human judgment that catches it | Mitigation |
|---|---|---|
| **Classic:** an estimate given as a single number becomes a commitment nobody made | Hearing "two weeks" and asking "is that an estimate or a promise?" | Always state a range; make the commitment a separate, explicit sentence |
| **AI-introduced:** estimating how long the agent takes to write the code, and forgetting review and verification | Noticing that the estimate has no line for reading the diff | Estimate in the three parts of 4.3; size from the test list, not the code |
| **AI-amplified:** trusting your felt speed with an agent, which runs fast and flattering | Comparing the estimate with the logged hours, not with memory | The calibration ratio, computed from weekly activity reports, at every checkpoint |
| **Classic:** a release plan written once and never revised, so the December demo is a surprise | Asking at every use-case close whether the forecast still fits | Revise the Release column at every close; show the forecast at Checkpoint 3 |

## 7. Hands-on (studio + optional individual assignment)

**Studio (team, own project)**

- **Goal:** every use case in the fan-out is estimated before it is built, and the team learns its own rate.
- **In studio (own project):** before the first fan-out use case is built, each owner writes the three-part estimate on its issue, sized from the design's test list. From then on, weekly activity report lines carry the use case ID.
- **Release plan:** by Checkpoint 2, every row of your traceability matrix has a Release value, revised by pull request at every use-case close. At Checkpoint 3, one forecast line under the calibration table ([4.6](#46-from-estimates-to-a-release-plan)).
- **Deliverable & assessment:** at Checkpoints 2 and 3, one table: each finished use case, its estimate, its actual hours, its ratio, and one sentence on the biggest miss. Assessed on completeness and honest interpretation, never on accuracy.

**At the final retrospective (week 15):** name the life-cycle model your team actually ran, where it departed from the method, and why. A team that ran waterfall in practice (all specification, then a scramble to build) should be able to say so, and say what it would change.

**Individual assignment (Project Pulse):** none.

## 8. Summary / key takeaways

- An estimate is a range you own; a commitment is a date you promise; a target is what the client wishes. Keep the three apart.
- Classical models convert size to hours through a rate measured when people wrote the code. Keep the size; measure your own rate.
- With an agent, the hours are in specifying, reviewing, and verifying. Size a use case by its test list.
- Your sense of how fast you work with an agent is unreliable. Your weekly activity reports are not.
- Estimates are graded on honesty, never on accuracy.
- A release plan is a Release column in your traceability matrix. Revise it at every close; when the forecast does not fit, change the scope with your client.
- Every life-cycle model is a bet on what is expensive. Royce never recommended the single pass that bears the waterfall name.
- This course's life cycle follows the Unified Process with a spiral's risk-first slice. What is new is the specification written for an agent to build from, and the checks around it.

## 9. Key papers & further reading

- Albrecht, A. J. "Measuring Application Development Productivity." *Proceedings of the Joint SHARE/GUIDE/IBM Application Development Symposium*, Monterey, CA, October 1979, 83–92. The origin of function points.
- Boehm, B. W. *Software Engineering Economics*. Prentice-Hall, 1981. COCOMO, Wideband Delphi, and the measurements behind the cone of uncertainty.
- Grenning, J. "Planning Poker, or How to Avoid Analysis Paralysis While Release Planning." 2002.
- Cohn, M. *Agile Estimating and Planning*. Prentice Hall, 2005.
- Beck, K., and Fowler, M. *Planning Extreme Programming*. Addison-Wesley, 2000. Release planning with stories and velocity.
- Jørgensen, M. "A Review of Studies on Expert Estimation of Software Development Effort." *Journal of Systems and Software* 70, no. 1–2 (2004): 37–60. Expert judgment is the most used technique, and no worse on average than the models.
- McConnell, S. *Software Estimation: Demystifying the Black Art*. Microsoft Press, 2006. Estimates, targets, and commitments; the cone of uncertainty.
- Jeffries, R. "Estimation Is Evil." 2021. <https://ronjeffries.com/articles/021-01ff/estimation-is-evil/>
- METR. "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity." July 10, 2025. <https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/>
- METR. "We Are Changing Our Developer Productivity Experiment Design." February 24, 2026. <https://metr.org/blog/2026-02-24-uplift-update/>
- Faros AI. "The AI Productivity Paradox." July 23, 2025. <https://www.faros.ai/blog/ai-software-engineering>
- Royce, W. W. "Managing the Development of Large Software Systems." *Proceedings of IEEE WESCON*, August 1970, 1–9.
- Brooks, F. P., Jr. *The Mythical Man-Month*. Addison-Wesley, 1975. Chapter 11, "Plan to Throw One Away."
- Boehm, B. W. "A Spiral Model of Software Development and Enhancement." *IEEE Computer* 21, no. 5 (1988): 61–72.
- Jacobson, I., Booch, G., and Rumbaugh, J. *The Unified Software Development Process*. Addison-Wesley, 1999.
- Beck, K., et al. *Manifesto for Agile Software Development*. 2001. <https://agilemanifesto.org/>
- Larman, C., and Basili, V. R. "Iterative and Incremental Development: A Brief History." *IEEE Computer* 36, no. 6 (2003): 47–56.
- Anderson, D. J. *Kanban: Successful Evolutionary Change for Your Technology Business*. Blue Hole Press, 2010.
- Schwaber, K., and Sutherland, J. *The Scrum Guide*. November 2020. <https://scrumguides.org/>

## 10. Self-check

1. Your client says, "Can you have the export feature by next Friday?" Is that an estimate, a target, or a commitment? What do you need before you can turn it into a commitment?
2. COCOMO and function points both convert size to effort. Which half of each still works when an agent writes the code, and which half does not?
3. A use case's design has 12 test rows and one open risk that can only be measured in production. Which part of the three-part estimate does the risk widen, and why?
4. Your estimate was 6 to 10 hours; your weekly activity reports show 14. What is your calibration ratio, and what is your next estimate for a use case you would otherwise have called 4 to 8 hours?
5. A teammate logs fewer actual hours than they worked so the team's ratio looks better. What has the team lost?
6. Five unfinished use cases remain in `v1.0.0`; their estimate midpoints add up to 30 hours, your team's ratio is 1.5, and your team will have about 40 hours before the demo. Does the plan fit? What do you tell your client, and when?
7. Your team's fan-out builds one use case at a time to full quality, while the specification keeps being revised. Which part of your process is incremental, which is iterative, and why do you need both?
8. A classmate says this course "does waterfall, because the specification comes first." Using Royce's paper and the Unified Process, explain what they have right and what they have wrong.

## Related

- [Design-of-Record](design-of-record.md): the test list and open questions this module sizes from.
- [Project](../project.md): the checkpoints where the calibration table is shown, and the weekly activity reports it is built from.
- [Schedule](../schedule.md): when this is taught.

<!--
## Drafting notes (raw: distribute into template sections, then delete before `stable`)

### Still to author in this module

- **Risk vocabulary** (categories, impact and likelihood, a risk-management plan), the one light touch the risk thread assigns to this module, about 20 minutes and not graded.

### Sources to check before `stable`

- Jørgensen 2004: confirm volume, issue, and pages against the published version.
- Boehm 1981: confirm the factor-of-four figure and the chapter on Wideband Delphi against the book.
- Grenning 2002: find the primary copy and confirm the exact title.
- McConnell 2006: confirm the estimate/target/commitment chapter.
- METR and Faros figures were checked against the primary posts on 2026-10-10.
- Royce 1970: confirm the "risky and invites failure" quotation and the do-it-twice recommendation against the paper; confirm that "waterfall" does not appear in it.
- Patton's Mona Lisa illustration: find the original (Patton, "Don't Know What I Want, But I Know How to Get It," 2008) and confirm the attribution.
- Week numbers in 4.12's mapping follow the published schedule as of 2026-10-10.
- Project Pulse facts (`Activity.java`, `not.md`'s 18 test rows and five open risks) checked against `main` at `8768a1d` on 2026-10-10.
- 4.6's Project Pulse release plan is from the handoff drafted 2026-10-11 against `main` at `31cd1a1`; check the Release column and its `#release-legend` anchor on `main` once committed.
- Beck and Fowler 2000: confirm title and publisher.
-->
