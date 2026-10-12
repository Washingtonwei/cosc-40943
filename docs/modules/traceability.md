# Requirements traceability

> **Purpose (one line):** a student can keep a use case honest end to end, tracing it forward (is it built and tested?) and backward (why does this code exist?), can explain why this matters more, not less, when an AI writes the code, and can place every use case in the release it ships in and forecast whether the MVP still fits.


!!! note "This module is still being written"
    The course is being revamped this term, so modules go up as they are written rather than all at once. What is here is usable; the rest is coming. Lectures and studio do not depend on the missing parts.

<!--
DRAFT SEED. This file exists to park decided content (`DECISION-traceability-thread`) and the motivation paragraph the instructor
wants preserved; it is NOT a fully authored module yet. Sections 4, 6, 7, 8, 9 are still template
placeholders. Author to publication grade. See the planning repo's course-design/module-catalog.md
("The traceability thread") for how this threads through the other modules, and notes/methodology.md
for the full traceability model (two axes, off-spine overlays) that this module teaches a subset of.

Section 4's "Three ways the specification and the code drift apart" is authored. Its code facts were
verified against https://github.com/Washingtonwei/project-pulse (branch main): addPeerEvaluation
guards on active weeks and on the previous-week window, updatePeerEvaluation guards on neither, and
getPeerEvaluationAverage ends in .average().orElse(0.0). Re-check before this module goes stable;
the running example is a live repository, and OI-24 in particular is code-deferred, so the first
example disappears the day it is fixed.

The release-plan subsection's Project Pulse plan is from the handoff drafted 2026-10-11 against `main` at
`31cd1a1`, merged as Project Pulse #95 at `81b5a97`; re-check the Release column and its `#release-legend`
anchor before stable. Beck and Fowler 2000: confirm title and publisher.
-->

## 2. Where it fits

- **Prerequisites:** requirements as the contract (the spec is where traceable nodes get their stable IDs), AI-assisted implementation, and testing.
- **Leads into:** maintainability, which is where the payoff and the honesty rule land.
- **How it's taught:** one anchor lecture in week 8, when fan-out begins and the matrix first earns its keep, ending on the release plan (a column in the same matrix), then practised every week on your growing codebase. You are required to keep the single-axis spine current; the fuller two-axis matrix is shown so you recognise it, not so you maintain it.
- **Course outcome it delivers:** [maintaining living traceability from specification to design to code to test, and keeping it honest with tooling](../syllabus.md#learning-outcomes) (outcome 8).

## 3. Motivation

- **The problem, on Project Pulse:** an agent can turn an approved use case into working code in minutes, so the codebase grows faster than anyone's memory of what maps to what. Without a durable map, "which code satisfies UC-X?" and "why does this module exist?" become unanswerable, exactly the questions maintenance depends on.

- **Why it matters more with AI (the paragraph to keep):**

Traceability is the antidote to the specific way AI-generated code rots. A human who writes code carries the "why" in their head; that tacit memory is what lets them maintain it later. An agent doesn't carry that memory across sessions, and it generates plausible code faster than any human, so unmapped code accumulates faster than on any human team. The traceability matrix is that lost memory, externalized into a durable artifact. So traceability isn't just as important for vibe-coded projects, it's arguably more important than it ever was for hand-written code, precisely because AI removed the natural friction that used to cap how fast un-understood code piled up. In ISO-25010 terms it buys you analysability (locate what a change affects) and testability (every requirement has a verifying test), the two maintainability sub-characteristics vibe coding destroys first.

- **Why we can finally afford it (the economics inverts):** traceability is not a new idea. The SE literature always prescribed it; real teams always skipped it or let it rot. The reason was never doubt about its value, it was that maintaining the matrix was tedious, error-prone, unrewarding human labor, and humans lose patience with clerical upkeep (writing code was more fun than updating a matrix). AI removes exactly that cost: an agent works tirelessly with text and does not lose patience. So the old objection "a stale matrix is worse than none" flips, from a reason to skip traceability into a reason to *delegate its upkeep*. This is one instance of a general move ("AI inverts the economics of rigor"): once the human cost collapses, discarded rigor becomes worth reinstating.

- **The honesty rule, now the guardrail (not a retreat):** cheap to maintain is not the same as safe to trust. An agent can silently corrupt the matrix and produce plausible-but-wrong links faster than any human, so *unverified* traceability rots faster than the hand-drawn kind ever did. What makes reinstatement safe is a split verification: delegate the tedious maintenance to the agent; delegate the *checking* to **deterministic tooling** (`/spec-build`: do the IDs resolve? does every requirement have a verifying test?); keep the *meaning* judgment human (what should trace to what; is this backward-orphan dead code or a missing requirement). The failure mode to name for students: letting the LLM judge its own links (LLM-as-judge) reintroduces drift as automated, confident, false assurance. "A stale matrix is worse than none" survives the inversion, it just moves up one level, from the artifact to the verification of the artifact. That split is the delegation through-line in miniature.

## 4. Core concepts

<!-- To author (`MODULE-traceability` build). Required subset: the single-axis spine (use case to design to code to test), forward = coverage, backward = justification; the verification edge (a requirement with no test is not traced). Exposed: the second (NFR) axis, off-spine overlays (BO, ASR-to-KD, business rules as constraints), cite-don't-restate invariants. Pull the full model from notes/methodology.md ("The traceability model"). The subsection below is authored; the rest of section 4 still needs writing around it. -->

…

### Three ways the specification and the code drift apart

The backward edge asks which requirement authorized a given piece of code. On a real codebase the answer is often "none", and that answer comes in three shapes, repaired three different ways.

| Shape | What you see | Repair |
|---|---|---|
| Specification right, code behind | A rule is written down and the code does not enforce it | Conform the code |
| Code right, specification stale | The document describes behavior the system no longer has | Amend the document |
| Neither says anything | The code made a decision no document records | Decide it, then write it down |

**Specification right, code behind.** `BR-evaluation-submission-window` binds both the initial submission and any later edit to a one-week window. `EvaluationService.addPeerEvaluation` enforces it twice over: the week must be one of the section's active weeks, and it must be the previous week. `updatePeerEvaluation` checks neither, so an evaluation stays rewritable forever. Trace forward from the rule and you land on `addPeerEvaluation` and stop, because the edit path was never linked to it.

**Neither says anything.** `getPeerEvaluationAverage` ends in `.average().orElse(0.0)`, so a student nobody evaluated is reported with an average of `0.0`, the same number as a student her teammates all rated zero. No business rule covers the empty case. Trace backward from that `0.0` and you arrive nowhere. It is not a violation, because there is nothing to violate. Someone decided in code that "not evaluated" and "rated zero" are the same value, and no document records the decision or what it does to the section's weekly report.

The third shape is the one that scales badly once an agent is writing the code. The first two are inconsistencies, and an inconsistency can be found by machine, because two artifacts exist and they disagree. The third produces no inconsistency at all: only one artifact ever spoke. An agent handed an under-specified use case always picks something, picks it in seconds, and emits code indistinguishable from code implementing a decision you actually made. That is how an implementation quietly becomes the specification, and it is the reason to ask the backward question out loud rather than assume the forward map covers you.

You will meet the opposite advice, and it is good advice. Guidance on reading an unfamiliar codebase tells you to treat documentation as a starting point rather than truth, because it is often out of date. That is not the opposite of this course's position, it is the other half of it. Neither artifact is true by default: a contract can be behind the system, and a system can be wrong about the contract. Which of the two is wrong is decided per item, and deciding it is what a register is for.

**Keep a register.** Project Pulse reconciles the two in [`docs/requirements/OPEN-ISSUES.md`](https://github.com/Washingtonwei/project-pulse/blob/main/docs/requirements/OPEN-ISSUES.md), under a "Doc ↔ Code Gap Analysis" heading. Each entry names the rule, the `file:method` that diverges from it, and the direction the divergence will be resolved. Read it: a working register is worth more than the definition. And note what it is not. It is not a bug list. Each entry is a claim about *which of the two artifacts is currently wrong*, decided per item rather than assumed, which is why several of them resolve by changing the document. A divergence you have decided not to fix yet is traced. A divergence nobody noticed is not, and that is the whole difference the register buys.

### From estimates to a release plan

An estimate answers "when can I use this one?" The client's next question is "what will I have in December?" Answering it takes a **release plan**: every use case placed in the release it ships in. Agile planning has always done this with stories and velocity (Beck and Fowler 2000; Cohn 2005). The course keeps the idea and changes the units.

**It is a column, not a document.** Your `traceability.md` already has one row per use case (and per non-use-case FR) with its Build and Verify state. The plan is one more column, **Release**: `v0.1.0` (the proving slice), `v0.2.0` (Checkpoint 3), `v1.0.0` (the December MVP), `Spring`, or `Out`. Plan and progress share a row, so they cannot disagree, and an empty cell is work nobody has planned. Your client agrees to scope by feature in vision and scope's MVP Scope section; the column carries that agreement down to use cases.

**Placing the rows.** Risk first, for the reason your proving slice went first ([the spiral model](se-and-ai.md#spiral-let-risk-choose-the-next-step)): a wrong decision found in week 9 is cheap, and in week 14 it is not. Then what the client needs first, then dependencies. When something goes ahead of risk, the pull request that changes the column says why: the column holds the decision, and git holds the reason.

**Project Pulse's plan.** Project Pulse shipped up to `v1.5.0` without a release plan. Its [Release column](https://github.com/Washingtonwei/project-pulse/blob/main/docs/traceability.md#release-legend) starts with the work that is left:

| Release | What ships | Why there |
|---|---|---|
| `v1.6.0` | The reminders: on-demand (`UC-NOT-remind-non-submitters`), and the scheduled one brought in line with `BR-submission-owed` | Designed; built in week 8 |
| `v1.7.0` | The rest of the requirements editor: artifact and link screens, comments, review, export | Backends built and tested; the client wants the editor finished first |
| `v1.8.0` | The first AI assistant end to end: `UC-AI-critique`, the proposal loop, its settings, the model proxy | The riskiest work: the first model call, with the outage scenario measured |
| `v1.9.0` | ReqLint and the tutor | The tutor explains ReqLint's findings, so it follows ReqLint |
| `v2.0.0` | The other six assistants | The Fall 2027 classroom deployment |

Risk alone would put `v1.8.0` before `v1.7.0`. The client chose otherwise, and the plan records that trade instead of hiding it. Writing the column also exposed a disagreement: the vision listed real-time co-editing as out of the MVP, while traceability showed it as unstarted work. The use case's own Status line already said Deferred, so that line settles it, and its Release cell stays empty: one fact, one owner.

**The forecast.** A use case that is not designed yet has no test list, so size it from what it has, its main scenario and extensions, as a range wider than the [three-part estimate](implementation.md#42-where-the-hours-go-now), because [nothing is designed yet](implementation.md#41-estimate-target-commitment). Write that range on the use case's issue; when its design is approved, the three-part estimate replaces it. Then:

> **Hours still needed** = the sum of the estimate midpoints of every unfinished `v1.0.0` row × your team's calibration ratio

Compare that with the hours your team will have before the MVP demo, judged from what your weekly activity reports show you actually work. If the plan does not fit, move rows out of `v1.0.0` with your client at the next meeting. This is the [estimate's rule](implementation.md#41-estimate-target-commitment) in practice: when the estimate and the target disagree, change the scope, not the estimate. Write the result as one line under your [calibration table](implementation.md#44-recording-and-calibrating):

`Forecast: 6 rows left in v1.0.0, 38 to 60 h at ratio 1.4; about 70 h available. Fits, with no slack for the high end.`

Revise the column at every use-case close ([the method, Phase C](../method.md#phase-c-fan-out-per-use-case)), and recompute the forecast whenever the ratio moves.

## 5. The AI-native lens

- **Delegate to AI:** generating the design and code for a use case and updating its trace row; mechanically checking that every link resolves and every requirement has a verifying test; drafting the Release column from the matrix and the ranked quality attributes, and adding up the forecast.
- **Keep human:** deciding what *should* trace to what, and judging whether a backward-orphan is dead code or a missing requirement. The graph's meaning is a human call. So is the cut line: which use cases leave `v1.0.0` is agreed with the client, never decided by the agent.
- **Context to supply:** the stable IDs and the spec they come from; the agent cannot invent a consistent handle space, it must be given the glossary and the use-case/FR/BR IDs.
- **How to verify:** run the consistency check (`/spec-build`-style) and read its report; spot-check a random use case both directions by hand to confirm the tooling is telling the truth.

## 6. Hands-on (studio)

<!-- To author. Sketch: in studio, take one of the team's own use cases through design to code to test, then update the traceability matrix; introduce a spec change and show the forward/backward checks catching what must change. The same move is demoed on Project Pulse in lecture first. Free tools only (`DECISION-free-tools`). -->

- **Goal:** …
- **In studio (own project):** …
- **Release plan:** by Checkpoint 2, every row of your traceability matrix has a Release value, revised by pull request at every use-case close. At Checkpoint 3, one forecast line under the calibration table.
- **Deliverable & assessment:** …

## 7. Summary / key takeaways

<!-- To author. -->

- …
- A release plan is a Release column in your traceability matrix. Revise it at every close; when the forecast does not fit, change the scope with your client.

## 8. Key papers & further reading

<!-- To author. Candidates: ISO/IEC/IEEE 29148 (traceability requirement); Gotel & Finkelstein on the traceability problem; the methodology's own traceability model in notes/methodology.md. -->

- …
- Beck, K., and Fowler, M. *Planning Extreme Programming*. Addison-Wesley, 2000. Release planning with stories and velocity.
- Cohn, M. *Agile Estimating and Planning*. Prentice Hall, 2005.

## 9. Self-check

<!-- To author. -->

1. …
2. Five unfinished use cases remain in `v1.0.0`; their estimate midpoints add up to 30 hours, your team's ratio is 1.5, and your team will have about 40 hours before the demo. Does the plan fit? What do you tell your client, and when?

## Related

- [Schedule](../schedule.md): when the traceability anchor lands, and the weekly practice after it.
- [Senior Design Project](../project.md): the traceability matrix as a graded deliverable.
- [AI-Assisted Implementation](implementation.md#41-estimate-target-commitment): the estimates and calibration ratio the release plan is built from.
- [SE and What AI Changes](se-and-ai.md): why the economics of rigor inverted, which is the argument this module rests on.
- [The Method](../method.md): the full traceability model this module teaches a subset of, including the second axis and the off-spine overlays.
