---
title: Requirements as the Contract
module: spec-driven-requirements
week: 3
day: Wednesday
---

# Requirements as the Contract

Week 3 · You meet your client in about 24 hours

::: note
Labor Day took Monday, so this is the only lecture this week, and every team meets its client Thursday or Friday. Say that in the first thirty seconds: everything today is for a meeting that happens before the next time we are in this room.
:::

## "I just told you my requirements"

A manager asks for a system to track chemical containers. Chemists stop buying what is already down the hall. The safety office files its reports without a week of work.

Five months, before the compliance audit. Can you do it?

::: steps
- **Cynthia:** "Before I can commit to a schedule, we'll need to understand the requirements."
- **Gerhard:** "What do you mean? I just told you my requirements."
:::

::: note
Read it as two people, not as a slide. This is Wiegers' opening story and it is exactly the situation every team walks into on Thursday.

Then ask the room: did he give her requirements? Take two or three answers before advancing.
:::

## What he actually gave her

::: cols
**What he said**

Save money on chemicals.

Cut the safety office's reporting work.

Be ready in five months.
|||
**What nobody knows yet**

Who may request a hazardous chemical?

What happens to a half-empty container?

Is "the stockroom" one place or six?

What has to be in the report?
:::

::: key
Business objectives are not requirements. Both are necessary. The gap between them is your job.
:::

::: note
Be explicit that this is not a criticism of the client. Knowing the business and knowing what software to build are two different expertises, and only one of them is already in the room.

Your client is Gerhard. Yours has given you one page.
:::

## Then what is a requirement?

> Requirements are defined during the early stages of a system development as a specification of what should be implemented. They are descriptions of how the system should **behave**, or of a system **property** or **attribute**. They may be a **constraint** on the development process of the system.

::: steps
- **Behave:** what it does
- **Property or attribute:** what it must be, and what its data looks like
- **Constraint:** how you are allowed to build it
:::

::: key
"The requirements" is an umbrella over several kinds of information, not one list of features.
:::

::: note
Sommerville and Sawyer, 1997. Put it on screen and read the three nouns out loud. Stop on the third, because nobody expects it: a requirement can be about your development process rather than about the running system at all.

Project Pulse carries both of the unexpected kinds. CO-ferpa, comply with FERPA when storing student educational records. CO-vue-spring-stack, Vue on the front and Spring Boot on the back. Neither is a feature anyone would demo, and either one discovered in November is a rewrite.

Then the three reasons to write any of it down: understand, communicate, control. Control is the one that makes the word "contract" in the title honest.

Do **not** teach the nine types here. That is the Requirement Types page and week 4. All this slide has to do is stop them writing a feature list on Friday. Sixty seconds, then move.
:::

## This is what one page becomes

Project Pulse started as a complaint about spreadsheets.

`docs/requirements/` today:

- `project-glossary.md`
- `vision-and-scope.md` (7,500 words)
- `use-cases.md` (43,700 words)
- `business-rules.md`
- `software-requirements-specification.md`
- `OPEN-ISSUES.md`

::: note
Have the real folder open in a browser tab and show it: github.com/Washingtonwei/project-pulse, docs/requirements. Scroll the vision and scope for five seconds so they feel the length, then close it.

The folder is about 66,000 words in total. Say that number out loud; it is the whole point of the slide.

Name OPEN-ISSUES.md out loud. It comes back at the end of the hour.
:::

## Two of those are yours by Friday

::: cols
**Glossary**

One word, one concept.

Started in the first meeting, because your client hands you the vocabulary whether you ask or not.
|||
**Vision and scope**

Why this exists, what success looks like, who cares, and what is **not** in it.

You will not finish it Friday. You will start it.
:::

::: note
Third file too: OPEN-ISSUES.md, the questions you cannot answer yet. Writing "we do not know" is the correct state in week 3. What fails is knowing and not writing it down.

Templates: github.com/tcu-cosc-40943/course-templates. Copy the requirements folder into your team repo's docs/. Do not fork.
:::

## Thursday: three roles, agreed before you walk in

| | |
|---|---|
| **Lead** | Asks. One person, not four. |
| **Scribe** | Writes. Does not ask. Captures exact words, especially nouns. |
| **Observer** | Watches for what is not said. |

::: note
Six people and no roles produces an hour of interruptions and no notes. Assign these in Slack tonight.

Ask to record, and say why: so nobody is transcribing instead of listening. If they decline, fine, and the scribe now matters much more.

The observer is the role students think wastes a person. It is the one that catches the hesitation, the topic they keep circling back to, and who they look at before answering.
:::

## Shape of the hour

::: steps
- **10 min.** The business: why this, why now.
- **30 min.** The process as it works today, step by step.
- **10 min.** Scope: what is in, what is out.
- **10 min.** Read back what you heard.
:::

::: note
Thirty minutes on the current process sounds like a lot until they try it. It is where the requirements actually are.
:::

## The ten minutes teams skip

Say what you understood, in your own words. Watch for the correction.

::: key
A client who is nodding may just be polite. A client correcting you is engaged.
:::

::: note
The correction is usually the most useful sentence of the hour.

The vision statement table is built for this. Fill it in during the meeting, read the six rows aloud, watch what they fix. Ninety seconds.

Then: written notes and open questions to the client within 24 hours. It creates the record and gives them a second chance to correct you while it is fresh.
:::

## Everyone said yellow. Everyone took black.

Sony ran a focus group on a yellow sport Walkman. The room loved it.

On the way out, free Walkman, two tables. Black on one, yellow on the other.

::: key
What people say in an interview is data about the interview.
:::

::: note
Thirty seconds, do not linger. Full version is in the module.

The point: "would you use this?" reliably produces yes, because agreeing is free and the person asking clearly wants it. The fix is not a better-worded question. It is a question whose answer costs something.
:::

## Ask the question that costs something

| Instead of | Ask |
|---|---|
| Would you use a dashboard? | Walk me through the last time you needed that number. What did you do? |
| Is this important? | If we ship only one thing in December, which one? |
| Would this save time? | How long does it take today, and how do you know? |
| Do you like this? | **Show me the spreadsheet you use now.** |

::: note
Past behavior over hypothetical preference. A forced choice over a wish list. An artifact over a description.

"Show me" is the two most productive words in requirements engineering, and they cost nothing. People describe the process they believe they follow. The spreadsheet shows the one they actually follow, and the difference is where the requirements are hiding.

Every team should leave today intending to ask for an artifact.
:::

## Ask why until you reach the need

"I need a drop-down of states."

That is not a requirement. That is a solution, already chosen, wearing a requirement's clothes.

::: joke
The client asked for a faster horse, so we shipped a horse with a spoiler. It tested green.
:::

::: note
Ask why three times and you usually reach the need: addresses have to validate against a shipping zone. Now you are free to solve it a better way, which you were not before.

Say the stakes plainly: taking a solution idea at face value locks in a design chosen by someone who is not a software engineer.
:::

## Listen for the rule

::: steps
- "Only lab managers may..."
- "Must comply with..."
- "Unless it's been more than a year."
:::

Business rules exist whether or not your software does. Write them down the second you hear one.

::: note
They arrive unannounced, in the middle of a story about something else, which is why the scribe is capturing exact words.

You will not remember these on Friday. Nobody does.
:::

## Business objectives carry a number

`BO-grading-time`: reduce the instructor's time to grade peer evaluations by 50%.

::: ask
"Make grading better." Is that a business objective?
:::

::: note
No, because nobody can ever be wrong about it. An objective carries a number so that someone can tell, a year later, whether it was met.

The other identifier shapes live in the same document: RI- for risks, AS- for assumptions, FEAT- for features. State a risk as a mechanism, not a category.
:::

## Objectives come in two flavors

| Financial | Nonfinancial |
|---|---|
| Save $X per year spent on a legacy system. | Cut the data error rate to no more than X%. |
| Reduce monthly support cost from $X to $Y in Z months. | Comply with specific federal and state regulations. |
| Reach revenue of $X within Y months. | Reduce turnaround to X hours on Y% of requests. |
| Achieve X% return on investment within Y months. | Raise satisfaction to at least X within Y months. |

::: key
Your client's objectives are almost all in the right-hand column.
:::

::: note
Point at the right column and say why: your client is not selling the software you are building, so market share and revenue are rarely the point. Time, error rate, participation, compliance, and satisfaction are. A team that comes back Friday with a financial objective has usually invented it.

Every row has a letter in it. That is the shape, not decoration.

The full sixteen shapes are in the module, section 4.5. If you are behind, show this slide and say only the right-column line. Do not read the table.
:::

## The follow-up nobody asks

"How will you know this worked?"

Good question. Not the hard one.

::: key
"What is that number today?"
:::

::: note
Baseline. If they cannot say, you have found something worth writing down, and it goes straight into OPEN-ISSUES.

Success metrics are a separate thing from objectives because objectives often cannot be measured until long after your project ends. Metrics can be read during testing.

Then the warning: pick metrics that measure what matters, not what is easy. "Cut development costs 20%" is easy to measure and easy to hit by firing people. Prefer the metric that gets worse if you build the wrong thing.
:::

## One word, one concept

Your client says "cycle" in one sentence and "sprint" in the next.

::: key
Ask which they mean, in the room, while they are in front of you.
:::

::: joke
There are two hard problems in computer science: cache invalidation, naming things, and off-by-one errors.
:::

::: note
The glossary is the cheapest document to start and the one that keeps paying, because every later document cites it instead of redefining things.

The entries worth having are not words your teammates already know. They are the words two stakeholders use differently, the words that sound generic but are not ("active", "complete", "week"), and your client's acronyms.

Ask directly: "is there a word your team uses here that I would not guess the meaning of?"
:::

## What happens without one

Two words for one concept, and nothing in the repository says so.

::: ai
You get a `Team` class and a `Group` table. A `submitReport` endpoint and a `war_entry` row. The agent reads what is already there and imitates it, faithfully reproducing the inconsistency, and invents a plausible synonym for anything the repository never names.
:::

::: note
This is week 2's thesis paying out again: the repository is the only memory the agent has.

The half that stays human is noticing, in the meeting. An agent reading the transcript afterward cannot ask which word the client meant.
:::

## `BO-3` or `BO-grading-time`?

::: cols
**How Project Pulse used to do it**

`BO-1`, `BO-2`, `BO-3`

`RI-1` … `RI-4`
|||
**How it does it now**

`BO-grading-time`

`RI-cloud-cost`
:::

::: joke
We renumbered the requirements. Good news: `BO-1` through `BO-7` are all still there. Bad news: they are not the same seven.
:::

::: note
This is my own document, three years apart. Show the old one if the tab is handy.

Ask an agent to insert an objective into BO-1 through BO-6 and it either renumbers everything, breaking every citation in your use cases, or appends out of order. No test catches either.

One more tell: in the old file, RI-3 is missing its colon. Nobody noticed for years, because nothing ever read those identifiers.

The exception, so they do not over-apply it: OPEN-ISSUES uses OI-1, OI-2, because that list only grows at the bottom and is cited lightly.
:::

## The sentence you will need in October

A marketing manager wants one small button added. "The developers are going to be in the code anyway. How hard is one tiny feature?"

::: key
Write down what is **out** as explicitly as what is in.
:::

::: note
The hard part is not the analysis. It is that he does not have the business objectives in mind, and she has to say why, out loud, without sounding obstructive.

Your client is enthusiastic and likes you, and in October they will suggest something genuinely good that costs you the semester.

The forcing question, ask it Thursday: if we deliver only one of these in December, which one? A client who cannot choose has not thought about it yet, and you need to know that now rather than in November.
:::

## Your turn: build Thursday's script

**Twelve minutes. Laptops open, one per team.**

::: steps
- Open the guide, select all, copy: `raw.githubusercontent.com/tcu-cosc-40943/course-templates/main/requirements/client-interview-guide.md`
- Give your agent that, your one-page brief, and the role. "You are an experienced business analyst."
- Ask for two things: your domain's version of every question in the guide, and a plain-language primer on this client's acronyms.
- It will give you about thirty questions.
:::

::: ai
Then do the part it cannot do.
:::

::: note
The raw URL is the whole file as plain text, so it is select-all and paste, no cloning. Have it on the board before you start; nobody types that from a slide.

Say what the guide is: fifteen sections of question with a minute budget on each, examples written for a recruiting client so they cannot be used unchanged, and a place to write what was said. It is the script tomorrow and the meeting record afterward. Tell them to commit it to docs/requirements/ as client-interview-YYYY-MM-DD.md, one file per meeting.

Walk the room, all three TAs too. Watch for teams that paste the brief and nothing else; the guide's instructions are the context that makes the difference.

The primer is the half nobody thinks to ask for. A team that walks in already knowing what their client's acronyms mean asks better questions for the whole hour.

If a team finishes early, send them to section 11: who runs this after we graduate, and what do they already know how to run. Almost nobody asks it and it constrains the whole stack.
:::

## Thirty questions. Forty-five minutes.

::: key
Which ten do you take, and why?
:::

::: joke
A requirements analyst walks into a bar and orders a beer, 0 beers, 999999999 beers, a lizard, and −1 beers. The bar ships flawlessly. The first real customer walks in and asks where the bathroom is.
:::

::: note
The joke is the slide's argument, so land it and then say it plainly: you can cover every edge case you thought of and still miss the thing the customer actually came in for. Only the customer can tell you that, and only if you ask.

The agent does not know what this client will tolerate, which questions are cheap to answer by reading a document, or which ones cost you a month if you guess wrong.

Sort by what it costs to stay wrong, not by what is easy to ask.

Take three teams' answers out loud. Ask one of them to name a question they cut and why.
:::

## Before you walk in

::: steps
- Listen before you build. Brainstorm after the read-back, not in minute five.
- Assign the three roles tonight.
- Send your client the shortlist the day before. They arrive with answers instead of promises.
- Copy the templates into `docs/requirements/` in your team repo.
- Scribe has `client-interview-guide.md` open in the meeting. Commit it the same day.
- Everything you could not answer goes in `OPEN-ISSUES.md`.
:::

::: warn
No requirements document has ever survived contact with a client unchanged. That is not failure, that is the process working.
:::

## Friday

Studio: Napkin round 0 on your own project, sealed. Then draft the glossary and vision and scope, on branches, one section each.

Repository owner: turn on branch protection before Friday.

::: note
Napkin round 0 is sealed and unread until the last full week of class, when they score themselves on calibration rather than correctness. Being wrong in week 3 is expected; not noticing you were wrong is the failure.

Reading is the module. The nine kinds of requirement are in the Requirement Types reference page. Use cases are Monday.
:::
