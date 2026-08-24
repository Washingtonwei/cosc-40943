# SE and What AI Changes

> **Purpose (one line):** decide what to hand an agent and what to keep, and defend a twenty-minute judgment about an unfamiliar problem against the agent's version of it.

**Slides:** [SE and What AI Changes](../slides/se-and-ai.html) (the fast version) and [Fifteen Weeks to Demo Day](../slides/fifteen-weeks-to-demo-day.html) (the week-1 failure story).

## 1. Learning objectives

By the end of this module, a student can:

1. State what software engineering is responsible for beyond writing code, and name which of those responsibilities AI has and has not absorbed.
2. Place a given task on the delegation boundary and justify the placement using the reversibility test (if guessing it wrong would violate a requirement, it stays human).
3. Produce a Napkin for an unfamiliar one-paragraph brief in twenty minutes: shape, the hard part, the bottleneck, stack, three kill risks as mechanisms, and a feasibility verdict.
4. Distinguish automation bias from agenda capture, name the tell for each, and apply a recovery move.
5. Explain how a project fails completely with no defective code in it, and identify which decisions in that failure an agent cannot own.
6. State the three constraints that define project success and explain why failing to renegotiate them, rather than failing to build, is the common cause of missed delivery.

## 2. Where it fits

- **Prerequisites:** none. This is the course opener.
- **Leads into:** The AI-Augmented Team in week 2 (onboarding the agent as a teammate), then requirements as the contract in weeks 3-4, and architecture in week 6, where the Napkin's six questions get the slow, derived treatment.
- **How it's taught:** two lecture days in week 1, then revisited at every new topic all term. It owns the [Napkin drill](../studio.md#the-napkin-drill) you will run six times in studio.
- **Course outcome it delivers:** [sizing up an unfamiliar problem and defending that judgment against the agent's version](../syllabus.md#learning-outcomes) (outcome 10), and it opens [collaborating with AI across the lifecycle](../syllabus.md#learning-outcomes) (outcome 6).

## 3. Motivation

**The problem, on Project Pulse.** Ask an agent to add a feature to Project Pulse with a one-line prompt and it will produce plausible, running code in under a minute. Ask it twice and you get two different designs. Neither one knows that instructors are the only actors permitted to publish a rubric, because nothing in the repository says so in a form the agent must honor. The code compiles, the tests it wrote pass, and the feature is wrong. There is nothing to review it *against*.

That is the whole course in one observation. The scarce thing is not the code. It is the contract.

**The failure this module is arranged against.** Not a spectacular one. The ordinary one, which is the one that will happen to you: six competent people, a real client, fifteen weeks, and nothing usable at the end. Nobody writes bad code. The requirements are a mood rather than a contract, so the agent fills the gaps silently and six people build six different products at speed. "Almost done" is never checked against anything, integration waits until week ten, and when time runs out the only thing left to spend is quality. [Fifteen Weeks to Demo Day](../slides/fifteen-weeks-to-demo-day.html) walks that failure end to end.

Every decision in that chain (what "done" means, which architecture survives contact with the other five, whether a generated feature was ever asked for) is a human responsibility. An agent given that specification will implement it, faster, with better test coverage, and just as wrongly.

## 4. Core concepts

### What software engineering was always responsible for

Programming is producing code that works. Software engineering is everything that makes that code the right code, keeps it right as it changes, and lets a team of people who do not share a brain build it together: deciding what to build, agreeing what the words mean, choosing structures that survive the second year, verifying behavior, and keeping the record honest.

AI has become excellent at the transformations between artifacts (requirements to design, design to code, code to test). It has not absorbed the decisions on either end.

### What the market pays for

That claim is testable against what companies actually hire for. Read a senior engineering posting at Amazon, Google, or any mid-size product company and count how much of it is about producing code. Very little. What recurs instead:

- Code review, coding standards, source control, build processes, testing, and operations, named as "the full software development life cycle"
- Taking a project from scoping requirements through launch
- Communicating with users, other technical teams, and senior management to collect requirements and describe designs
- Mentoring, and influencing engineering practice across a team
- Knowing when to use an existing technology and when to build a tailored one
- Disagreeing constructively

Every one of those is a responsibility from the list above, and not one of them is typing. These postings were written before agents could code well, which is what makes them useful now: the industry was already paying a premium for the part that AI has not absorbed. The premium got larger.

### What "success" means, and how teams fail at it

Success on a software project is conventionally three constraints: **scope** (what must be built), **schedule** (when by), and **resources** (how much it costs, including how many people). They trade against each other. Fix all three and you have fixed quality too, because quality is the only thing left to spend.

The interesting part is the failure mode. Projects rarely fail because a team could not build the thing. They fail because the three constraints were set unrealistically at the start and **the team never renegotiated them**, so it tried to deliver under constraints that stopped being achievable in week three. Nobody wanted to be the one to say so. The MVP demo shrinks quietly instead, and the client finds out in December.

This is why the course has four checkpoints and a scoped MVP rather than one deadline. A checkpoint is a scheduled opportunity to renegotiate while renegotiating is still cheap. Use them for that, not just to report that things are fine.

### What actually changed

Three things, and they pull in different directions.

**Transformation got cheap.** The cost of turning an approved design into code fell by an order of magnitude. Anything whose difficulty was mostly typing is now nearly free.

**The cost of being wrong went up.** When code took a week, a bad requirement was caught by the friction of building it. When code takes a minute, the wrong thing gets built completely, tested, and merged before anyone notices the premise was wrong. Speed removes the accidental checkpoints that slow work used to provide.

**The economics of rigor inverted.** Teams skipped living traceability, current design documents, and consistent glossaries because the *upkeep* cost human hours, not because the practices lacked value. That cost has collapsed. So the question is no longer "is this rigor worth the effort?" but "now that upkeep is cheap, which discarded rigor is worth reinstating?" This is the reasoning behind several choices later in the course that would have looked like bureaucratic overhead in 2019.

The guardrail: cheap generation is not cheap trust. A practice is worth reinstating when it has value, was skipped for labor reasons, and a check can keep it honest. Practices failing that last test are reinstated only behind human sign-off, and that is exactly where judgment gets taught.

### The delegation boundary

The recurring question of this course, asked fresh at every topic: **what do we hand the agent here, and what stays human?**

| Stays human | Goes to the agent |
|---|---|
| Requirements quality, scope, vocabulary | Use case to design-of-record |
| Business constraints, domain knowledge | Approved design to code and tests |
| Quality attributes, and what "good enough" means | Cross-document consistency checks |
| Architectural decisions that are hard to reverse | Mechanical artifact transformations |
| "Is this even a good idea?" | Drafting, refactoring, explaining unfamiliar code |

The test: **if guessing it wrong would violate a requirement, the human pins it. Otherwise the agent derives it.** Both extremes are wrong answers. "Delegate everything" produces a fast, well-tested implementation of a question nobody answered; "keep everything human" throws away the one advance that makes the rigor affordable.

### The Napkin: six prompts

Given an unfamiliar problem, produce a defensible rough judgment in twenty minutes. This is the delegation boundary at project scale: an agent will produce a fluent plan, stack, and risk list for any prompt in seconds, so the human differentiator is judging whether it is any good.

1. **Shape.** What kind of system is this really (CRUD app, pipeline, real-time, integration glue, ML)? One sentence, then three to five boxes.
2. **The hard part.** The one thing that makes this not a weekend project. Every project has one that dominates, and naming it is most of the skill.
3. **Bottleneck.** Where it breaks first: under load, under scale, or under a five-person team.
4. **Stack.** What you would build it with, one sentence of why. Boring default unless there is a reason.
5. **Kill risks.** Top three, each stated as a mechanism, not a category.
6. **Verdict.** Feasible for this team in this time, yes or no, and what you would cut first.

A seventh prompt, **Delegate** (what goes to the agent, what stays human), is held in reserve until the first six run smoothly.

**The sequence is fixed:** individual silently (about 5 minutes), team reconcile (about 10), then the agent's napkin, then diff (about 5). Students who prompt first anchor on the agent's answer and learn nothing. The diff step is where the learning happens; protect it when time runs short.

**What scores.** Credit goes to naming a mechanism over naming a category. "Scope creep, integration issues, communication problems" is risk bingo and scores nothing. "The client's system exports CSV nightly, so nothing is real-time and the dashboard requirement is dead on arrival" is the target.

**Honest framing for students.** One semester does not manufacture ten years of pattern library. What the drill offers is the frame, six calibrated rounds with fast feedback, and the habit of noticing when your own estimate was wrong.

### Agenda capture: losing control of the conversation

**The failure.** After several turns of dialogue the engineer is no longer directing the work. They are answering the agent's questions, following its reasoning, and building things that do not matter yet. Plain-language version: you lost the wheel.

**Distinguish it from automation bias.** Automation bias is trusting output that is wrong. Agenda capture is competent output on the wrong problem. There is no error signal anywhere, which is why it is hard to catch: every individual step looks fine, and the cost only shows up at the end, when the thing you sat down to do is not done.

**Why it happens.**

1. *The agent always has a next move.* It never stalls or says "I do not know what matters here, you decide." Every turn ends in a proposal, and a proposal is a default. The human's role degrades from choosing the work to approving it, and approving is cheap.
2. *Whoever asks the questions owns the frame.* Answering clarifying questions feels productive and each answer is locally reasonable, but the set of questions defines the problem, and the human did not write it. Novices are the most exposed: an expert has a prior about what matters and resists the pull, a student has none, so the agent's agenda becomes theirs by default.
3. *The agent goes depth-first; seniority is breadth-first.* Survey, size, prune, then dig. The model picks a thread and pulls, because it holds no cost model, no deadline, and no stake. "Interesting" and "important right now" are indistinguishable to it.
4. *Accumulated context is a commitment device.* Fifteen turns in, abandoning the thread feels wasteful even when abandoning is correct. The sunk cost is real and it is inside the session.

**Not unique to AI, but worse with it.** A dominant pair-programming partner does the same. What is new: no fatigue, no social friction to signal a redirect, and an inexhaustible supply of plausible next steps. There is no natural stopping point, so the human has to supply one.

**What the human has to bring.** Two things, and the second is the trainable one. First, a clear and strongly held motivation for what this session is for. Second, the capability to steer: to notice drift, to stop, and to change the subject. Without the first there is nothing to steer toward, and the rabbit hole is not really the agent's doing.

**The tell, and the moves.**

- *Tell:* watch the ratio of questions you ask to questions you answer. When it inverts, you have lost the wheel.
- *Move 1:* answer the agent's question only if the answer changes what you would do next. Otherwise say so and return to the goal.
- *Move 2:* kill the session rather than redirect it. The context that captured you is the same context you would be arguing against.
- *Move 3:* write the goal down before opening the chat, so drift is checkable rather than a feeling.

**The Napkin is the pre-commitment device.** A napkin written before the session gives an external thing to check the conversation against ("does this thread touch the hard part or the bottleneck I named?"). The drill therefore has two uses: sizing an unfamiliar problem, and making agenda capture visible in a familiar one. The second is probably the more frequent use in practice.

## 5. The AI-native lens

- **Delegate to AI:** producing a first napkin for comparison, summarizing an unfamiliar domain, enumerating candidate risks, drafting the boring parts of any artifact.
- **Keep human:** which risks actually matter for *this* client, whether the problem is worth solving, the feasibility verdict, and what to cut first. These require a stake in the outcome, which the model does not have.
- **Context to supply:** the client's real constraints (budget, incumbent systems, deadline, who will operate it), the team's actual skills, and the definition of done. An agent asked to plan a project will invent all three plausibly and silently.
- **How to verify:** diff its napkin against yours and interrogate the differences in both directions. Where it named something you missed, ask whether the mechanism is real. Where you named something it missed, ask why it did not: usually because you hold context that never made it into the prompt, which is the context-engineering lesson arriving early.

## 5.5. Risks and mitigations

| Risk (classic + AI-introduced) | Human judgment that catches it | Mitigation |
|---|---|---|
| Building the wrong thing correctly. AI amplifies it: the wrong thing now gets built completely and tested before anyone questions the premise. | Asking what problem this solves for whom, before asking how to build it. | The Napkin before the session; the specification before `/implement`; the approval gate. |
| Risk bingo. Naming risk categories that apply to every project and therefore inform no decision. | Can I state the mechanism, and would a reader who knows this domain agree it is the top-three concern? | Rubric credits mechanisms over categories; briefs are specific enough that generic answers are visibly wrong. |
| Skill atrophy. Delegating the parts that build judgment, not just the parts that cost time. | Noticing you cannot evaluate the output you just accepted. | Individual Pulse assignments graded on judgment; exams without an agent; the diff step run before prompting, never after. |

## 6. Hands-on (studio + individual assignment)

**Studio (team, own project)**

- **Goal:** every student has a running Project Pulse and has completed one AI-assisted task on real code.
- **In studio (own project):** week 1 is guided onboarding, not own-project work, because teams are still being assigned. Environment setup, run Project Pulse once, first AI-assisted task with a TA watching.
- **Deliverable and assessment:** Pulse running locally, shown to a TA. Ungraded; it gates the week 2 work.

**Individual assignment (Project Pulse)** — Hello, Project Pulse

- **Task (AI-workflow-framed):** set up and run Pulse, explore it with the agent, open a well-formed issue for a real smell you found, and submit a small pull request.
- **Deliverable and assessment (per student):** the issue and the pull request. Graded on whether the issue names a real problem precisely enough to act on, and whether the pull request explains why the change is right. Not on size.

## 7. Summary / key takeaways

- Software engineering owns the decisions on both ends of the transformations AI now performs. Those ends got more valuable, not less. Senior engineering job postings were already paying for that half before agents could code.
- Scope, schedule, and resources trade against each other, and quality is what gets spent when a team will not renegotiate them. Checkpoints exist to make that renegotiation cheap and scheduled.
- The delegation test: if guessing it wrong would violate a requirement, it stays human.
- The economics of rigor inverted. Ask which discarded practice is now worth reinstating, not whether rigor is affordable.
- Automation bias is wrong output you trusted; agenda capture is right output on the wrong problem. The second has no error signal, so you need an external checkpoint.
- A project fails completely with no defective line of code in it, when the specification was a mood and nobody was at the wheel. That is the failure mode this whole course is arranged against.

## 8. Key papers and further reading

- Fred Brooks, "No Silver Bullet: Essence and Accidents of Software Engineering" (1987). The essence/accident distinction is the sharpest available tool for asking what AI actually removed.
- Nancy Leveson, *Engineering a Safer World* (2011), chapters 1-2. Why failures are control-structure failures rather than component failures, which is this module's thesis in a different vocabulary.
- CMU 17-313, *Foundations of Software Engineering*: the introductory lecture.

## 9. Self-check

1. Name three responsibilities of software engineering that an agent cannot discharge, and say why for each.
2. A teammate says "the agent wrote it, so the bug is not mine." What is wrong with that claim, precisely?
3. You are twelve turns into a session and have written a lot of working code. What two checks tell you whether you are still working on what you sat down to do?
4. Rewrite this kill risk as a mechanism: "there is a risk of integration problems with the client's system."
5. A feature appears in your demo that the client never asked for, and nobody on the team remembers deciding to build it. Where in the chain from business need to shipped code should that have been caught, and what artifact would have caught it?

## Related

- [Schedule](../schedule.md): when this module is taught, and what follows it.
- [Friday Studio](../studio.md): the Napkin drill as you will actually run it.
- [Working with AI](../ai.md): the delegation boundary and these two failure modes, stated as course policy.
