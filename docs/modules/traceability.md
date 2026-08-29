# Requirements traceability

> **Purpose (one line):** a student can keep a use case honest end to end, tracing it forward (is it built and tested?) and backward (why does this code exist?), and can explain why this matters more, not less, when an AI writes the code.


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
-->

## 2. Where it fits

- **Prerequisites:** requirements as the contract (the spec is where traceable nodes get their stable IDs), AI-assisted implementation, and testing.
- **Leads into:** maintainability, which is where the payoff and the honesty rule land.
- **How it's taught:** one anchor lecture in week 8, when fan-out begins and the matrix first earns its keep, then practised every week on your growing codebase. You are required to keep the single-axis spine current; the fuller two-axis matrix is shown so you recognise it, not so you maintain it.
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

## 5. The AI-native lens

- **Delegate to AI:** generating the design and code for a use case and updating its trace row; mechanically checking that every link resolves and every requirement has a verifying test.
- **Keep human:** deciding what *should* trace to what, and judging whether a backward-orphan is dead code or a missing requirement. The graph's meaning is a human call.
- **Context to supply:** the stable IDs and the spec they come from; the agent cannot invent a consistent handle space, it must be given the glossary and the use-case/FR/BR IDs.
- **How to verify:** run the consistency check (`/spec-build`-style) and read its report; spot-check a random use case both directions by hand to confirm the tooling is telling the truth.

## 6. Hands-on (studio)

<!-- To author. Sketch: in studio, take one of the team's own use cases through design to code to test, then update the traceability matrix; introduce a spec change and show the forward/backward checks catching what must change. The same move is demoed on Project Pulse in lecture first. Free tools only (`DECISION-free-tools`). -->

- **Goal:** …
- **In studio (own project):** …
- **Deliverable & assessment:** …

## 7. Summary / key takeaways

<!-- To author. -->

- …

## 8. Key papers & further reading

<!-- To author. Candidates: ISO/IEC/IEEE 29148 (traceability requirement); Gotel & Finkelstein on the traceability problem; the methodology's own traceability model in notes/methodology.md. -->

- …

## 9. Self-check

<!-- To author. -->

1. …

## Related

- [Schedule](../schedule.md): when the traceability anchor lands, and the weekly practice after it.
- [Senior Design Project](../project.md): the traceability matrix as a graded deliverable.
- [SE and What AI Changes](se-and-ai.md): why the economics of rigor inverted, which is the argument this module rests on.
- [The Method](../method.md): the full traceability model this module teaches a subset of, including the second axis and the off-spine overlays.
