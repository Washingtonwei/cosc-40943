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

Gerhard, a senior manager at Contoso Pharmaceuticals, is meeting Cynthia, who manages the IT department. This conversation is read out loud in class, and it is worth reading again slowly.

> **Gerhard:** "We need to build a chemical tracking information system. The system should keep track of all the chemical containers we already have in the stockroom and in laboratories. That way, the chemists can get some chemicals from someone down the hall instead of always buying a new container. This should save us a lot of money. Also, the Health and Safety Department needs to generate government reports on chemical usage and disposal with a lot less work than it takes them today. Can you build this system in time for the compliance audit in five months?"
>
> **Cynthia:** "I see why this project is important, Gerhard. But before I can commit to a schedule, we'll need to understand the requirements for the chemical tracking system."
>
> Gerhard was confused. **"What do you mean? I just told you my requirements."**
>
> **Cynthia:** "Actually, you described some general business objectives for the project. That doesn't give me enough information to know what software to build or how long it might take. I'd like to have one of our business analysts work with some users to understand their needs for the system."
>
> Gerhard protested. **"The chemists are busy people. They don't have time to nail down every detail before you can start programming. Can't your people figure out what to build?"**
>
> **Cynthia:** "If we just make our best guess at what the users need to do with the system, we can't do a good job. We're software developers, not chemists. I've learned that if we don't take the time to understand the problem, nobody is happy with the results."
>
> Gerhard insisted. **"We don't have time for all that. I gave you my requirements. Now just build the system, please. Keep me posted on your progress."**
>
> Karl Wiegers and Joy Beatty, *Software Requirements*, 3rd edition, chapter 1.

Read Gerhard generously, because the scene collapses if you do not. He is not a fool and he is not a villain. He knows the business, the audit date is real, and every sentence he says is reasonable from where he is sitting. He also genuinely believes he gave her his requirements.

He did not. He described **business objectives**, which is a different thing and a valuable one. What nobody in that room yet knows: who is allowed to request a hazardous chemical, what happens when a container is half empty, whether "the stockroom" is one place or six, what the safety office's report has to contain, and which of those the system is responsible for.

Three things in the scene are worth naming, because you will meet all three this week.

**"Can't your people figure out what to build?"** You will hear a politer version of this on Thursday: *just do what you think is best*, or *you are the technical people*. It is an invitation to guess, and it always arrives sounding like trust.

**"We're software developers, not chemists."** Cynthia can say this out loud. An agent handed the same gap cannot. Ask it to build a chemical tracking system from Gerhard's paragraph and it produces something complete, confident, and plausible, with nothing in the output marking which parts came from him and which it invented. She declines to guess; it has no mechanism for declining.

**Gerhard wins the argument.** He is senior, he is paying, and he ends the conversation. Cynthia is right and still has to go and do the work without his blessing. That is the ordinary case, and it is why the rest of this module is about how to run the meeting rather than how to win it. Your leverage is not authority. It is a read-back your client cannot help correcting.

Your client is Gerhard. This is not a criticism of your client. Knowing the business and knowing what software to build are two different kinds of expertise, and only one of them is in the room already.

### 4.2 What "the requirements" actually means

So what did Cynthia want that Gerhard had not given her? The definition is deliberately broad:

> Requirements are defined during the early stages of a system development as a specification of what should be implemented. They are descriptions of how the system should **behave**, or of a system **property** or **attribute**. They may be a **constraint** on the development process of the system.
>
> Sommerville and Sawyer, *Requirements Engineering: A Good Practice Guide* (1997)

Read the three nouns. **Behavior** is what the system does, and it is the only one most teams write down. A **property or attribute** is what the system must *be*, and what its data has to look like: fast, available, auditable, five digits then an optional hyphen. A **constraint on the development process** is not about the running system at all. It restricts how you are permitted to build it.

That breadth is the point. **"The requirements" is not one kind of statement. It is an umbrella over several kinds of information that only mean something together**, which is why §4.9 lists nine of them and why they end up in four different documents. A team that hears only the first noun ships a feature list. Project Pulse's specification carries `CO-ferpa` (comply with FERPA when storing and transmitting student educational records) and `CO-server-side-llm-proxy` (every call to the language model routes through the server, so credentials never reach the browser). Neither is a behavior anyone would demo, and either one discovered in November is a rewrite.

Week 1 gave you the test for whether one sentence qualifies: [a capability or a constraint, agreed with the people who can accept the system, and specific enough to verify](se-and-ai.md#what-a-requirement-is). This definition tells you what that sentence is allowed to be *about*. You need both.

**Why write any of it down.** Three reasons, and they are not the same reason:

- **Understand** precisely what the software has to do. Being told is not the same act as understanding.
- **Communicate** that understanding precisely to everyone who builds, tests, or accepts it. On your team that is five other people, three of whom were not in the meeting, and an agent that was in no meeting at all.
- **Control** production, so that what ships matches the specification, including after the specification changes. It will change.

The third is the one teams skip, and it is what makes the word *contract* in this module's title honest. A requirement nobody can hold you to is not a contract, and neither is one you can quietly edit in December to match what you happened to build.

### 4.3 The first client meeting

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

The questions themselves are not in this module. They are in [`client-interview-guide.md`](https://github.com/tcu-cosc-40943/course-templates/blob/main/requirements/client-interview-guide.md): fifteen sections of question with examples written for a different domain so you have to rewrite them in your client's vocabulary, a minute budget on each, and space under each one for what they said. It is your script going in and your meeting record coming out, and it is the file you customize with your agent in class on Wednesday. This module owns the technique; the guide owns the questions.

Its first rule is worth repeating here, because it is the mistake this room is most likely to make: **listen before you build.** Describing what you would build in the first twenty minutes ends the elicitation, because a client who has heard your idea starts reacting to it instead of describing their world. This is about order rather than silence. Some clients want to think out loud with you, and that is worth doing, after the read-back, once you can describe their current process back to them accurately. What is absolute is the other rule: **commit to nothing**, because five teammates are not in the room. "Let me write that down and bring it back to the team" is the whole sentence.

### 4.4 What people say versus what they take

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

### 4.5 Business objectives and success metrics

A **business objective** says what should improve, in numbers: "reduce the instructor's time to grade peer evaluations by 50%". Not "make grading better", which nobody can ever be wrong about.


Objectives come in two flavors, and the shapes are worth having in front of you while you write your own. Fill in the letters.

| Financial | Nonfinancial |
|---|---|
| Capture a market share of X% within Y months. | Achieve a customer satisfaction measure of at least X within Y months of release. |
| Increase market share in country W from X% to Y% within Z months. | Increase transaction-processing productivity by X% and reduce the data error rate to no more than Y%. |
| Reach a sales volume of X units or revenue of $Y within Z months. | Develop an extensible platform for a family of related products. |
| Achieve X% return on investment within Y months. | Develop specific core technology competencies. |
| Achieve positive cash flow on this product within Y months. | Be rated the top product for reliability in published reviews by a specified date. |
| Save $X per year currently spent on a high-maintenance legacy system. | Comply with specific federal and state regulations. |
| Reduce monthly support costs from $X to $Y within Z months. | Receive no more than X service calls and Y warranty calls per unit within Z months of shipping. |
| Increase gross margin on existing business from X% to Y% within one year. | Reduce turnaround time to X hours on Y% of support calls. |

Nearly every objective a senior design client has lives in the right-hand column. Your client is not selling the software you are building, so market share and revenue are rarely the point. Time, error rate, participation, compliance, and satisfaction are. A team that comes back with a financial objective has usually invented it.

Platitudes are the failure mode. "Become recognized as a world-class provider" and "provide a more rewarding customer experience" are not objectives, because no measurement could ever contradict them.

A **success metric** tells you whether you are on track to get there, and can be measured much sooner. That gap is why they are separate things. An objective may not be measurable until long after your semester ends, and may depend on work beyond your project, but you still need to know in October whether you are pointed the right way. Sometimes the two are the same sentence, when the objective happens to be measurable early.

Every metric needs a **baseline**, and the question that produces it is the one students forget: not "how will you know this worked?" but the follow-up, **"what is that number today?"** If the client cannot say, you have found something worth writing down. A metric with no baseline cannot be met or missed.

Choose metrics that measure what matters rather than what is easy. "Reduce product development costs by 20 percent" is easy to measure and easy to hit by laying people off. Prefer the metric that gets **worse** if you build the wrong thing.

### 4.6 The glossary: one word, one concept

Write it from the first meeting, because your client hands you the vocabulary whether you ask or not.

The entries worth having are not the words your teammates already know. They are the words two stakeholders use differently. In airline statistics, one international body says **city-pair** and the other says **O and D** for the same thing, and the same two bodies say **traffic by flight stage** and **segment traffic** for another. A team that misses this ships a report that silently mixes them. Also worth entries: words that sound generic but are not ("active", "complete", "week"), your client's acronyms, and any term you invented that the client does not use.

If two words mean the same thing and nothing in the repository says so, your team will use both, and so will your agent. You get a `Team` class and a `Group` table, a `submitReport` endpoint and a `war_entry` row, and each of those pairs is a defect waiting for the day you join them. The agent cannot fix this by itself: asked to add a feature, it reads what is already there and imitates it, faithfully reproducing an inconsistency, and it will invent a plausible synonym for anything the repository never names.

The half that stays human is noticing. When your client says "cycle" in one sentence and "sprint" in the next, ask which they mean, in the room, while they are in front of you. An agent reading the transcript afterward cannot ask.

### 4.7 Identifiers: slugs, not numbers

Requirement items carry identifiers so that a design document, a test, a commit, and an issue can all point at the same thing. This course uses **name-based slugs**: `BO-grading-time`, `SM-submission-rate`, `RI-cloud-cost`, `AS-client-maintains-stack`, `FEAT-performance-tracking`.

Project Pulse did not always. An earlier version of its vision and scope numbered them `BO-1` through `BO-3` and `RI-1` through `RI-4`, and one of those four is missing its colon, which nobody noticed for years, because nothing ever read them.

Numbers fail in a specific way, and an agent makes it worse. Ask an agent to insert a new objective into a list running `BO-1` to `BO-6` and it has two options: renumber everything, silently breaking every citation in your use cases and specification, or append out of order so the numbering means nothing. No test you can write catches either one. A slug has neither failure mode, and it carries the gist at the place it is cited, so `BO-grading-time` tells a reader what it is and `BO-3` does not.

Rules: coin the slug from the concept, keep it short and unique within its space, **never rename or repoint one**, and cite by identifier rather than by position ("the third objective").

Numbers are not banned everywhere. `OPEN-ISSUES.md` uses `OI-1` upward, because that list only ever grows at the bottom and is cited lightly. The convention is not "slugs everywhere"; it is slugs wherever items get reordered or cited often.

### 4.8 Scope, and the line you will need in October

A business analyst is reviewing a specification when the marketing manager asks to add a "like this product" button. It sounds small. His argument is the one you will hear: the developers are going to be in the code anyway, so how hard is one tiny feature? Her analysis says it does not serve the objective the project exists for, and is not simple to build. The hard part is not the analysis. It is that the manager does not have the business objectives in mind and she has to be able to say why, out loud, without sounding obstructive.

That is what the scope section is for. It is not paperwork. It is the sentence you will need in October when your client, who likes you and is enthusiastic, suggests something genuinely good that will cost you the semester.

Write down what is **out** as explicitly as what is in, and ask the forcing question in the first meeting: *if we deliver only one of these in December, which one?* A client who cannot choose has not thought about it yet, and you need to know that now rather than in November.

### 4.9 The nine kinds of requirement

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

**The full version is in [Requirement Types](../requirement-types.md)**: each kind with its definition, where it comes from, what it sounds like, and **one worked example from Project Pulse**, so you can read the same system sliced nine ways and feel where the lines fall. Read it once before week 4.

### 4.10 Knowing when to stop

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
- Ian Sommerville and Pete Sawyer, *Requirements Engineering: A Good Practice Guide* (1997). The source of the definition in §4.2, and still the clearest statement of why "the requirements" covers behavior, properties, and process constraints at once.
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
