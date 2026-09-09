# Requirements as the Contract

**Slides:** [Requirements as the Contract](../slides/spec-driven-requirements.html) (the fast version).

> **Purpose (one line):** find out what your client actually needs, and write it down so that your team and your agent both build the same thing.

!!! note "This module is still being written"
    Week 3 is written: elicitation, business objectives and success metrics, the glossary, identifiers, and scope. Week 4 adds use cases, business rules, quality attributes, and the specification.

## 1. Learning objectives

By the end of week 3, a student can:

1. Run a first client meeting that produces business objectives, success metrics, and a scope line instead of a wish list.
2. Distinguish what a client says from what a client will commit to, and use a question that tells them apart.
3. Write a business objective and a success metric that someone else could verify a year later.
4. Build a project glossary that binds one word to one concept, and explain what breaks in a codebase without one.
5. Assign name-based identifiers to requirement items, and explain why numbered identifiers fail under an agent.

## 2. Where it fits

- **Prerequisites:** [The AI-Augmented Team](ai-augmented-team.md), whose thesis is that the repository is the team's shared memory and the only memory the agent has. Requirements are the first thing you put in it.
- **Leads into:** [Traceability](traceability.md). Every traceable node in this course is born here: if there is no specification, there is nothing to trace.
- **How it's taught:** two weeks. Week 3 has a single lecture day, Wednesday, on eliciting from a real client, and its studio drafts your glossary and vision and scope. Week 4 continues with use cases, business rules, quality attributes, and the specification. You keep both documents alive all term.
- **Course outcome it delivers:** [turning a client's problem into a specification that serves as the development contract](../syllabus.md#learning-outcomes) (outcome 1).

## 3. Motivation

**The problem, on Project Pulse.** Project Pulse began as a complaint: submitting weekly activity reports through shared spreadsheets and peer evaluations through uploaded Excel files was slow and error-prone. That complaint is a paragraph. What it became is [`docs/requirements/`](https://github.com/Washingtonwei/project-pulse/tree/main/docs/requirements): about 66,000 words across a vision and scope, a glossary, use cases, business rules, and a specification. The use cases alone run to 43,700. Nothing in that folder is decoration. It is what makes the difference between a team that builds the thing and a team that builds a thing.

You are holding a one-page brief. Your client is holding the rest, mostly without knowing they are holding it.

**A real failure it prevents.** On 29 October 2018 and 10 March 2019, two Boeing 737 MAX aircraft crashed, killing 346 people. The Maneuvering Characteristics Augmentation System read a single angle-of-attack sensor and pushed the nose down. **The software did what the requirements said.** The requirements were wrong: the hazard analysis understated the failure mode, the single-sensor dependency survived review, and pilots were not told the system existed.

Strip away the airplane and every link in that chain is an artifact this module owns.

| The failure | The artifact that should have caught it |
|---|---|
| The requirement was wrong | Vision and scope; the use case's failure paths |
| Hazard analysis understated the failure mode | Quality attributes, risk analysis |
| Single-sensor dependency survived review | Architecturally significant requirement; design review |
| Pilots were not told the system existed | Scope: is the operator inside the system boundary? |
| It shipped meeting its specification | Verification against validation |

A system can pass every test and still be the wrong system. Verification asks whether you built the thing right; validation asks whether you built the right thing. MCAS passed the first and failed the second.

Here is why that matters more now, not less. **An agent asked to implement MCAS from that specification would have implemented it faster, with better test coverage, and just as fatally.** Cheap generation does not touch a wrong requirement. It ships it sooner.

## 4. Core concepts

### 4.1 A brief is not a set of requirements

A manager at a pharmaceutical company asks for a system to track chemical containers, so chemists stop buying what is already down the hall and the safety office can file its reports without a week of work. Can it be ready in five months?

> "I see why this project is important," said Cynthia. "But before I can commit to a schedule, we'll need to understand the requirements for the chemical tracking system."
>
> Gerhard was confused. "What do you mean? I just told you my requirements."

He did not. He described **business objectives**, which is a different thing and a valuable one. What nobody in that room yet knows: who is allowed to request a hazardous chemical, what happens when a container is half empty, whether "the stockroom" is one place or six, what the safety office's report has to contain, and which of those the system is responsible for.

Your client is Gerhard. This is not a criticism of your client. Knowing the business and knowing what software to build are two different kinds of expertise, and only one of them is in the room already.

### 4.2 The first client meeting

You get an hour and roughly one first impression. Three roles, agreed before you walk in:

| Role | Does |
|---|---|
| **Lead** | Asks the questions and keeps the agenda moving. One person, not four. |
| **Scribe** | Writes. Does not ask. Captures the client's exact words, especially the nouns. |
| **Observer** | Watches for what is not said: hesitation, the topic the client keeps returning to, the person they defer to. |

Ask to record, and say why: so nobody is transcribing instead of listening. If the client declines, that is fine, and the scribe now matters more.

**Shape of the hour.** Ten minutes on the business, why this problem and why now. Thirty on the process as it works today, walked step by step. Ten on scope, what is in and what is out. Ten to read back what you heard.

**The read-back is the highest-value ten minutes and the part teams skip.** Say what you understood in your own words, and watch for the correction. A client who is nodding may be being polite; a client correcting you is engaged, and the correction is usually the single most useful sentence of the meeting. The vision statement table in [`vision-and-scope.md`](https://github.com/tcu-cosc-40943/course-templates/blob/main/requirements/vision-and-scope.md) is built for this: fill it in during the meeting, read the six rows aloud, and see what they fix. Ninety seconds.

**Within 24 hours**, send written notes and the open questions. This creates the record, and it gives the client a second chance to correct you while the meeting is fresh.

### 4.3 What people say versus what they take

Sony ran a focus group on a yellow sport Walkman. The room loved it: sporty, fresh, so much better than another black one. On the way out, participants were told to help themselves to a free Walkman, from two tables, black on one and yellow on the other. Everyone took a black one.

What people say in an interview is data about the interview. Asking "would you use this?" reliably produces yes, because agreeing is free and the person asking clearly wants it. The fix is not a better-worded question. It is a question whose answer costs the client something.

| Instead of | Ask |
|---|---|
| Would you use a dashboard? | Walk me through the last time you needed that number. What did you actually do? |
| Is this important? | If we can ship only one of these in December, which one? |
| Would this save time? | How long does it take today, and how do you know? |
| Do you like this? | Show me the spreadsheet you use now. |

Past behavior over hypothetical preference; a forced choice over a wish list; an artifact over a description. **"Show me" is the two most productive words in requirements engineering, and they cost nothing.** People describe the process they believe they follow; the spreadsheet shows the one they actually follow, and the difference is where the requirements are hiding.

Two more that pay for themselves:

**Ask why until you reach the need.** Much of what a client calls a requirement is a solution they have already picked. "I need a drop-down of states" is a solution; the need underneath might be that addresses have to validate against a shipping zone. Ask why three times and you usually get there. Then you are free to solve it a better way, which you were not before.

**Listen for the rule.** When a client says only certain people may do something under certain conditions, that is a business rule, and it usually comes with the word "must", "unless", or "only". Those sentences are gold, and they arrive unannounced in the middle of a story about something else.

### 4.4 Business objectives and success metrics

A **business objective** says what should improve, in numbers: "reduce the instructor's time to grade peer evaluations by 50%". Not "make grading better", which nobody can ever be wrong about.

A **success metric** tells you whether you are on track to get there, and can be measured much sooner. That gap is why they are separate things. An objective may not be measurable until long after your semester ends, and may depend on work beyond your project, but you still need to know in October whether you are pointed the right way. Sometimes the two are the same sentence, when the objective happens to be measurable early.

Every metric needs a **baseline**, and the question that produces it is the one students forget: not "how will you know this worked?" but the follow-up, **"what is that number today?"** If the client cannot say, you have found something worth writing down. A metric with no baseline cannot be met or missed.

Choose metrics that measure what matters rather than what is easy. "Reduce product development costs by 20 percent" is easy to measure and easy to hit by laying people off. Prefer the metric that gets **worse** if you build the wrong thing.

### 4.5 The glossary: one word, one concept

Write it from the first meeting, because your client hands you the vocabulary whether you ask or not.

The entries worth having are not the words your teammates already know. They are the words two stakeholders use differently. In airline statistics, one international body says **city-pair** and the other says **O and D** for the same thing, and the same two bodies say **traffic by flight stage** and **segment traffic** for another. A team that misses this ships a report that silently mixes them. Also worth entries: words that sound generic but are not ("active", "complete", "week"), your client's acronyms, and any term you invented that the client does not use.

If two words mean the same thing and nothing in the repository says so, your team will use both, and so will your agent. You get a `Team` class and a `Group` table, a `submitReport` endpoint and a `war_entry` row, and each of those pairs is a defect waiting for the day you join them. The agent cannot fix this by itself: asked to add a feature, it reads what is already there and imitates it, faithfully reproducing an inconsistency, and it will invent a plausible synonym for anything the repository never names.

The half that stays human is noticing. When your client says "cycle" in one sentence and "sprint" in the next, ask which they mean, in the room, while they are in front of you. An agent reading the transcript afterward cannot ask.

### 4.6 Identifiers: slugs, not numbers

Requirement items carry identifiers so that a design document, a test, a commit, and an issue can all point at the same thing. This course uses **name-based slugs**: `BO-grading-time`, `SM-submission-rate`, `RI-cloud-cost`, `AS-client-maintains-stack`, `FEAT-performance-tracking`.

Project Pulse did not always. An earlier version of its vision and scope numbered them `BO-1` through `BO-3` and `RI-1` through `RI-4`, and one of those four is missing its colon, which nobody noticed for years, because nothing ever read them.

Numbers fail in a specific way, and an agent makes it worse. Ask an agent to insert a new objective into a list running `BO-1` to `BO-6` and it has two options: renumber everything, silently breaking every citation in your use cases and specification, or append out of order so the numbering means nothing. No test you can write catches either one. A slug has neither failure mode, and it carries the gist at the place it is cited, so `BO-grading-time` tells a reader what it is and `BO-3` does not.

Rules: coin the slug from the concept, keep it short and unique within its space, **never rename or repoint one**, and cite by identifier rather than by position ("the third objective").

Numbers are not banned everywhere. `OPEN-ISSUES.md` uses `OI-1` upward, because that list only ever grows at the bottom and is cited lightly. The convention is not "slugs everywhere"; it is slugs wherever items get reordered or cited often.

### 4.7 Scope, and the line you will need in October

A business analyst is reviewing a specification when the marketing manager asks to add a "like this product" button. It sounds small. His argument is the one you will hear: the developers are going to be in the code anyway, so how hard is one tiny feature? Her analysis says it does not serve the objective the project exists for, and is not simple to build. The hard part is not the analysis. It is that the manager does not have the business objectives in mind and she has to be able to say why, out loud, without sounding obstructive.

That is what the scope section is for. It is not paperwork. It is the sentence you will need in October when your client, who likes you and is enthusiastic, suggests something genuinely good that will cost you the semester.

Write down what is **out** as explicitly as what is in, and ask the forcing question in the first meeting: *if we deliver only one of these in December, which one?* A client who cannot choose has not thought about it yet, and you need to know that now rather than in November.

### 4.8 The nine kinds of requirement

Everything a client says in a meeting is one of these. Sorting them as you hear them is most of the skill, and the right-hand column is what to listen for.

| Kind | What it is | Written down in | Sounds like |
|---|---|---|---|
| Business requirement | Why the organization is paying for this | Vision and scope | "We need to cut the time we spend on..." |
| User requirement | A goal a user must be able to accomplish | Use cases, user stories | "I need to print a mailing label." |
| Business rule | A policy, regulation, law, or formula that exists outside your software | Business rules catalog | "Must comply with...", "only managers may..." |
| Functional requirement | Observable behavior the system exhibits | Specification | "When X happens, the system shall Y." |
| Quality attribute | How well it does it | Specification | "fast", "easy", "secure", "reliable" |
| External interface | Where your system meets another one | Vision and scope, specification | "Must send messages to...", "must read files in..." |
| Constraint | A restriction on how you may build it | Specification | "Must be written in...", "cannot exceed..." |
| Data requirement | The structure, format, or values of the data | Specification | "An order consists of..." |
| Solution idea | A design the client has already chosen, wearing a requirement's clothes | Nowhere, until you find the need under it | "Then I select the state from a drop-down." |

The last row is the one to watch. Solution ideas arrive constantly and sound like requirements, and taking them at face value locks in a design chosen by someone who is not a software engineer.

**The full version, with definitions, sources, and worked examples for each kind, is in [Requirement Types](../requirement-types.md).** Read it once before week 4.

### 4.9 Knowing when to stop

You are never entirely done, particularly building incrementally. But you are at the point of diminishing returns when the client stops producing new use cases, proposes scenarios that turn out to be variations on ones you have, repeats issues already covered, or suggests things that are all out of scope or all low priority. Users tend to raise requirements in order of decreasing importance, so the tail is genuinely the tail.

The one signal that is not about the client: your own team and your reviewers stop asking questions when they read it.

## 5. The AI-native lens

- **Delegate to AI:** drafting document sections from the brief, the template, and your notes; generating a candidate interview script; producing a plain-language primer on the client's domain and acronyms before you walk in; turning a meeting recording into a first-pass glossary; listing every question it could not answer from what you gave it.
- **Keep human:** which of its thirty questions are worth your client's limited hour; telling enthusiasm from commitment; the scope line; deciding whose word wins when two stakeholders use different terms; noticing the thing the client did not say.
- **Context to supply:** the one-page brief, the template **including its instructions**, your meeting notes and recordings, the glossary as it grows, and the artifacts the client actually uses. The agent cannot infer your client's business, and it has never seen their spreadsheet.
- **How to verify:** every claim in the draft must trace to something the client said or a document you have. Hunt specifically for invented specifics, since numbers, names, and features nobody mentioned are where a fluent draft goes wrong. Then read it back to the client, which is the only check that matters.

The difference this makes is not speed. Without an agent, a team downloads a generic interview questionnaire, skims the brief, and shows up. With one, the same team arrives with a script built from their own brief, having already learned what the client's acronyms mean. That team asks better questions for the whole hour. The agent did not do the interview; it made the humans ready for it.

## 6. Risks and mitigations

| Risk (classic + AI-introduced) | Human judgment that catches it | Mitigation |
|---|---|---|
| A friendly client agrees with every feature proposed enthusiastically, so you build the yellow Walkman. The agent, handed the transcript, encodes the enthusiasm as a requirement, since it cannot tell agreement from commitment. | Watching what the client does rather than what they say. | Behavior questions, "show me", the forced MVP choice, and reading the vision statement back. |
| The specification has gaps. The agent fills them with a plausible guess, written in the same confident register as the parts that are true, so the guess is invisible. | Knowing which parts you were told and which you inferred. | Ask the agent for what it could not answer, and put those in `OPEN-ISSUES.md` rather than resolving them yourself. |
| Requirements are met and the product is still wrong, the MCAS failure. Cheap generation makes it faster to build the wrong thing correctly. | Validation: does this serve the business objective at all? | Trace every feature to an objective, and every objective to a metric with a baseline. |

## 7. Hands-on (studio + optional individual assignment)

**Studio (team, own project)**

- **Goal:** produce the first version of the two documents your project will be built from, and a written record of what you still do not know.
- **In studio (own project):** copy the [templates](https://github.com/tcu-cosc-40943/course-templates) into `docs/requirements/` in your team repository. Split the sections across the team, one owner each, one branch and one pull request per person. Draft the glossary from your client brief and your meeting, fill in Background, the business opportunity, business objectives with real slugs, and the vision statement, and record everything you could not answer in `OPEN-ISSUES.md`. Preceded by [Napkin](se-and-ai.md#the-napkin-six-prompts) round 0 on your own project, which is sealed unread.
- **Deliverable and assessment:** `docs/requirements/` on your `main` branch by end of studio, with commits from every member. Assessed on whether the objectives carry numbers, whether the open issues are real questions rather than placeholders, and whether the glossary contains terms you learned from the client rather than terms you already knew.

**Individual assignment (Project Pulse)**: none. The requirements skills are assessed on your own project, where there is a real client to be wrong about.

## 8. Summary

- Your client gives you business objectives and calls them requirements. Both are needed; they are not the same thing, and the gap between them is your job.
- What a client says in a meeting is weaker evidence than what they do. Ask about past behavior, ask for the artifact, and force a choice.
- A business objective carries a number. A success metric carries a number, a source, and a baseline, and can be measured before the project is over.
- One word, one concept, written in the repository, or your codebase will grow two names for everything and the agent will keep both.
- Identifiers are slugs, because numbered lists break silently when anything is inserted, and inserting things is what agents do.
- A system can meet its specification and still be the wrong system. That failure is not made rarer by faster code.

## 9. Key papers and further reading

- Karl Wiegers and Joy Beatty, *Software Requirements*, 3rd edition (2013). The source of the templates this course uses, the nine requirement kinds, and the business objectives and success metrics material. Chapters 5 and 6 cover the vision and scope document.
- Fred Brooks, *The Mythical Man-Month* (1975), on requirements: "The hardest single part of building a software system is deciding precisely what to build... No other part of the work so cripples the resulting system if done wrong."
- Nancy Leveson, *Engineering a Safer World* (2011), chapters 1 and 2, on failures as control-structure failures rather than component failures.
- Joint Authorities Technical Review, *Boeing 737 MAX Flight Control System* (2019), and the House Committee on Transportation and Infrastructure's final report (2020). The requirements and hazard-analysis sections are the relevant ones.
- Alexander Cowan, ["The Yellow Walkman"](https://www.alexandercowan.com/yellow-walkman-data-art-of-customer-discovery/), on what customer discovery data is worth.
- [Requirement Types](../requirement-types.md), this course's full reference for the nine kinds.

## 10. Self-check

1. MCAS met its specification. Where in the chain from business need to shipped code should it have been caught, and which artifact would have caught it?
2. Your client says "the system should be user-friendly." What kind of requirement is that, and what are the next two questions?
3. Write a success metric for the objective "reduce the time students spend submitting weekly reports by 25%". Include a source and a baseline. What would you have to ask the client to fill in the baseline?
4. Your teammate adds a new business objective to the middle of a numbered list. Name two things that break, and say why no test catches either.
5. Your client, in the same meeting, calls the same thing a "section" and a "class". What do you do, and when?

## Related

- [The AI-Augmented Team](ai-augmented-team.md): why these documents live in the repository rather than in a shared drive.
- [Traceability](traceability.md): what happens to these identifiers once code exists.
- [Requirement Types](../requirement-types.md): the nine kinds in full.
- [Studio](../studio.md): what your team does with this on Friday.
- [Schedule](../schedule.md): when this is taught.

---

## Drafting notes (raw, week 4, distribute when authored, then delete)

- **User stories are introduced, then critiqued** (`DECISION-user-stories-demoted`): teach them as the mainstream agile unit students will meet in industry, then show where they run out. A user story is a deliberately under-specified placeholder for a conversation, which is the wrong property when a coding agent builds precisely what the specification says. The use case (steps plus associated information) is the contract the agent builds against.
- Use case anatomy from the 2025 deck: name, summary, rationale, users, precondition, main success scenario, extensions, postconditions. The Search and Replace example (`UC-8`) is worked end to end and shows extensions properly.
- EARS templates for functional requirements (ubiquitous, event driven, state driven, optional, unwanted behavior, hybrid), from <https://alistairmavin.com/ears/>. Pairs naturally with the agent: an EARS-shaped requirement is far harder to misread than prose.
- Business rules as the origin of requirements: the table showing how one rule propagates into a business requirement, a user requirement, a functional requirement, and a quality attribute.
- Quality attributes list and the "how to find" listening cues; the training-room heating story (met every stated requirement, unusably loud) is the failure story for this section.
- Week 4 studio writes use cases and business rules and starts the specification.
