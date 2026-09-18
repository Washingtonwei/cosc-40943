---
title: Writing the Specification
module: spec-driven-requirements
week: 4
---

# Writing the Specification

Week 4 · Requirements as the Contract, part 2

## Monday: from features to use cases {.center}

The unit your agent builds against

::: note
Thirty seconds of admin first. The first weekly activity report was due in Project Pulse at the start of this class. The first peer evaluation is due tomorrow, Tuesday, at 10:00 AM. Late submissions are not accepted, and the reminders come from peer.evaluation.tool.senior.design@gmail.com, which TCU's filter can junk: add it to your safe senders today.

Then the frame. Last week was what a client gives you. Today is the form you write it in, so that a teammate, a tester, and an agent all build the same thing.
:::

## From feature to use case

```mermaid
flowchart LR
  BO["BO-PERF-instructor-efficiency"] --> FEAT["FEAT-performance-tracking"]
  FEAT --> WAR["Area: WAR"]
  FEAT --> EVA["Area: EVA"]
  EVA --> UC["UC-EVA-submit-evaluation"]
  UC -.-> LATER["Design, code, test: week 8"]
```

::: key
Every arrow is a link you can follow, forward and backward. That is traceability.
:::

::: note
Every team has a feature list in its vision and scope. A feature is a capability a stakeholder can see, in value terms, with no behavior; Project Pulse has six. A feature is too coarse to build from, so it is broken into use case areas, and use cases live inside the areas.

This is Project Pulse's own chain. Point at UC-EVA-submit-evaluation: the room reviews it at the end of the hour.

Features and areas are many-to-many, never one-to-one. A feature that reads "create, edit, delete X" is a list of use cases in disguise; a feature that lands on exactly one area should be broadened.

Traceability is following these links forward to what realizes a requirement, and backward to why an artifact exists. Design, code, and tests arrive in week 8. Two minutes for this slide and the next, then the roleplay.
:::

## Your first trace

| Feature | Business objectives | Use case areas |
|---|---|---|
| `FEAT-performance-tracking` | `BO-PERF-instructor-efficiency`, `BO-PERF-student-participation` | `WAR`, `EVA` |

::: trace Trace: feature to use case area
- Every feature has at least one area.
- Every area is reached by a feature.
:::

::: note
This table goes in docs/traceability.md in the team repository, and it is part of Friday's work. Project Pulse's own traceability.md opens with exactly this table. Objectives attach at the feature; everything below inherits them.

The two checks. A feature with no area is a promise nobody has specified. An area no feature reaches is use cases no stakeholder asked for. The first time the second check ran on Project Pulse, it found two areas, the glossary and document authoring, that no feature pointed at.

Point at the pink box once. The three-node symbol marks every place the course adds a link to this chain, on slides and module pages alike, and it comes back in week 8.

Then the bridge: an area is only a name, and what fills it is use cases. Cast the volunteers.
:::

## Four volunteers

| ![The Shopper](img/shopper.svg){ height="150" } | ![The online store](img/web-store.svg){ height="84" } | ![The Fulfillment System](img/fulfillment.svg){ height="96" } | ![The Billing System](img/billing.svg){ height="76" } |
|:---:|:---:|:---:|:---:|
| **Shopper** | **The System** | **Fulfillment System** | **Billing System** |
| a person | the online store | ships the order | charges the card |

::: note
Cast four students before the next slide. Each reads their own lines and only their own lines. Whoever plays the System is the software today.

Give the room a job: count how many times the ball changes hands, and notice every time the System talks to someone who is not the Shopper.

This is a checkout everyone has done a hundred times. The content is not the point. The point is that it reads like a play.
:::

## Use Case 01: Place an order

| | |
|---|---|
| **Actors** | Shopper, Fulfillment System, Billing System |
| **Trigger** | The Shopper indicates to order the selected items. |
| **Precondition** | The Shopper has selected the items. |
| **Postconditions** | Placed, with a tracking ID and a delivery date. Or not placed, and the database is consistent. |

::: note
Read this one yourself; the cast reads the next three.

The full wording. Trigger: the Shopper indicates to order the items that have already been selected. Precondition: the Shopper has selected the items to be purchased. Postconditions: the order is placed in the system or canceled; if placed, the Shopper receives a tracking ID and knows the estimated delivery date; if not placed, the database should be consistent.

A registered Shopper has an existing account, possibly with billing and shipping information stored. A non-registered Shopper does not. The Fulfillment System processes orders for delivery; the Billing System bills customers for orders placed.

The trigger is the same as the first action step of the main success scenario. The postconditions cover both outcomes: a use case guarantees something even when the goal fails.
:::

## Main success scenario (1 of 2)

1. The **Shopper** indicates to order the items that have already been selected.
2. The **System** presents the billing and shipping information that the Shopper previously stored.
3. The **Shopper** verifies the information and confirms that the existing billing and shipping information should be used for this order.
4. The **System** presents the amount that the order will cost, including applicable taxes and shipping charges.
5. The **Shopper** verifies the information and confirms that the order information is accurate.
6. The **System** provides the user with a tracking ID for the order.
7. The **System** submits the order to the **Fulfillment System** for evaluation.
8. The **Fulfillment System** provides the System with an estimated delivery date.
9. The **System** presents the estimated delivery date to the Shopper.

::: note
Let the cast run. First stop after step 8: the System just talked to another system, and the Shopper was not in that exchange at all. A feature list never shows you that.
:::

## Main success scenario (2 of 2)

10. The **Shopper** indicates that the order shall be placed.
11. The **System** requests the **Billing System** to charge the Shopper for the order.
12. The **Billing System** confirms that the charge has been placed for the order.
13. The **System** submits the order to the **Fulfillment System** for processing.
14. The **Fulfillment System** confirms that the order is being processed.
15. The **System** indicates to the Shopper that she has been charged for the order.
16. The **System** indicates to the Shopper that the order has been placed.
17. The **Shopper** exits the System.

::: note
Ask the room for the count: how many times did the ball change hands? The exact number does not matter. That it changed hands at nearly every step does.
:::

## Extensions

- **3a.** The Shopper wants billing and shipping information different from what is stored. Also applies if nothing is stored, or the Shopper has no account.
    - 3a1. The Shopper indicates that this order shall use alternate billing or shipping information.
    - 3a2. The Shopper enters billing and shipping information for this order.
    - 3a3. The System validates the billing and shipping information.
    - 3a4. The use case continues.
- **5a.** The Shopper discovers an error in the billing or shipping information in her account.
    - 5a1. The Shopper indicates that the billing and shipping information is incorrect.
    - 5a2. The Shopper edits the billing and shipping information in her account.
    - 5a3. The System validates the billing and shipping information.
    - 5a4. The use case returns to step 2 of the normal flow.

::: note
Point at the numbering before anyone reads: 3a branches from step 3, and 3a1 is its first step. Where it rejoins is written down: 3a continues, 5a returns to step 2.
:::

## Run it again: the Shopper cancels

- **10a.** The Shopper determines that the order is not acceptable (perhaps the estimated delivery date) and cancels the order.
    - 10a1. The Shopper requests that the order be cancelled.
    - 10a2. The System confirms that the order has been cancelled.
    - 10a3. The use case terminates.

::: ask
Step 6 already issued a tracking ID. Step 7 already told the Fulfillment System. What does cancelling have to undo?
:::

::: note
Have the cast replay steps 1 to 10 quickly, then the Shopper takes 10a.

The question is the postcondition coming due: "if not placed, the database should be consistent." Nobody wrote how, and that is exactly the gap an agent would fill without telling you.
:::

## What is a use case?

The system's behavior under various conditions, as it responds to a request from one of the stakeholders, called the **primary actor**.

::: key
Use cases are fundamentally a text form. You just performed one.
:::

::: note
Thank the cast and let the room applaud them.

It was a conversation: four actors, one goal, and the software was one voice among four. Every use case has a primary actor who starts the interaction to reach a goal. A customer of Amazon places an order; a student searches for a course for spring.

Alistair Cockburn, Writing Effective Use Cases (2001).
:::

## Why use cases?

Ask users what they **do**, not what features they want.

Users can review a use case, because it is written in the words of their business.

::: note
Many business analysts have learned that elicitation focused on users and usage yields better results than an emphasis on features and functions.

I am a strong believer in use cases when the system has a lot of user interaction. They are an excellent way to structure the dialogue with users about the goals they need to accomplish with the system to be.

This is last week's "show me", written down: past behavior over a wish list.
:::

## You will meet user stories

"As a **student**, I want to **submit my weekly activity report**, so that **my instructor can see my work**."

::: steps
- **Card:** the sentence
- **Conversation:** where the detail lives
- **Confirmation:** the acceptance tests
:::

::: note
Ron Jeffries, "Essential XP: Card, Conversation, Confirmation" (2001). It is easy to mistake the card for the whole story. The card is short on purpose, because the detail is worked out in conversation.

Stories are the mainstream agile unit and they will be on your first employer's board. They are a good planning tool. Hold that for two slides.
:::

## INVEST

::: steps
- **I**ndependent
- **N**egotiable: *not an explicit contract; the details are co-created during development*
- **V**aluable
- **E**stimable
- **S**mall
- **T**estable
:::

::: note
Bill Wake, "INVEST in Good Stories, and SMART Tasks" (2003).

Read Negotiable's definition out loud and let the word "contract" land. This module is called Requirements as the Contract.
:::

## Your agent does not negotiate

::: ai
It builds what is written, and fills the gaps without asking.
:::

::: key
Plan with user stories. Build against use cases.
:::

::: joke
The product owner told the agent, "we'll work out the details later." The agent shipped before later arrived.
:::

::: note
A story's conversation happens between people who can say "what did you mean?" The agent never says it.

A use case carries what the card leaves to the conversation: preconditions, the steps, and above all the extensions, which is where the failure paths live.
:::

## Find the right level

::: ask
Which of these are valid use cases?
:::

- Get a student loan
- Set up a promotion for Black Friday
- Handle a return for a customer
- Log in
- Move a piece on the game board

::: note
Take hands on each. Then the answer: all of them can be use cases, at different levels, depending on the system, its boundary, the actors, and the goals. Which level you want is the next slide.
:::

## Three tests

| Test | Ask | Fails it |
|---|---|---|
| **Boss** | Is your boss happy you did this all day? | Log in |
| **Elementary business process** | One person, one sitting, a business event, value added? | Get a student loan: too big |
| **Size** | More than one step in a sequence? | Move a piece |

::: note
Craig Larman, Applying UML and Patterns (3rd edition, 2004). The boss test in full: "What have you been doing all day?" "Logging in!" Is your boss happy? The elementary business process in full: a task performed by one person in one place at one time, in response to a business event, which adds measurable business value and leaves the data in a consistent state. Good examples: approve a purchase order, handle a return request. Bad: delete a line item, print the document.

The Black Friday promotion and handling a return pass all three: the boss is happy, it is one sitting, and the size is right.

A student loan, moved from a paper workflow online: apply for a loan, view the loan offer, accept some or all of it, e-sign the promissory note, then money to the university for tuition and to the student for living expenses. Each of those is nearer a user goal. Same for handling a car accident insurance claim.

User goal level use cases are the ones we care about. Litmus test: can the user go away happy after this use case, even if their larger goal is not done yet? "Customer orders products with a credit card" and "customer reserves a car online", yes. "Customer searches for a car on Priceline", not really: the real goal is to reserve a car and drive it, so searching is a subfunction.

On Project Pulse, UC-EVA-submit-evaluation passes all three: a student sits down once a week, does it, and leaves.
:::

## What is in a use case?

| Part | In Place an order |
|---|---|
| **Primary actor:** starts it, to reach a goal | The Shopper |
| **Actors:** anyone or anything with behavior | Fulfillment System, Billing System |
| **Scope:** the system under design | The online store |
| **Pre- and postconditions** | Items selected; placed, or database consistent |
| **Main success scenario:** nothing goes wrong | Steps 1 to 17 |
| **Extension:** a condition, then its handling | 10a, the Shopper cancels |

::: note
A use case is a contract for the behavior of the system under design. A stakeholder is someone with a vested interest in that behavior, whether or not they touch the system. Actors include other systems: the Fulfillment System and the Billing System were actors.

A use case holds many scenarios. Some succeed and reach the goal; some fail but still protect the interests of the stakeholders.

The table is Alistair Cockburn's annotated use case slide, with the labels moved onto the example the room just performed. His annotation on the steps: full sentences showing who takes the action, 3 to 9 of them. Place an order has seventeen. Guideline 4 comes back to that.
:::

## Every step is a subgoal

::: cols
![Each scenario step is a subgoal hiding a nested use case, drawn as striped trousers](img/striped-trousers.png)
|||
![A pair of trousers](img/trousers.png){ height="210" }

The goal is the belt. Each stripe is one scenario: success down one leg, failure down the other.
:::

::: note
Alistair Cockburn's striped trousers, from his Humans and Technology course slides.

A use case is a collection of scenarios for one goal. Each step is a subgoal (establish credit, check stock) that can succeed or fail, so scenarios multiply, and a step that hides a lot of work may be a smaller use case of its own.

Place an order has at least four stripes: the main path, 3a, 5a, and 10a.
:::

## Our template adds five things

- `UC-<AREA>-<slug>` identifier
- **Trigger**
- **Business Rules**, by `BR-*` identifier only
- **Associated Information:** data fields and validation
- **Frequency of Use**

::: note
The identifier survives reordering. The trigger is the event that starts the use case. Business Rules carries identifiers only, never the rule's text, which is Wednesday arriving early: one rule, one home. Associated Information holds the data fields and their validation rules. Frequency of Use tells your architecture which use cases carry the load.

The format is Wiegers and Beatty's, as adopted by the use case style guide. The field definitions are in use-cases.md in the course templates; do not lecture them field by field.
:::

## Writing use cases {.center}

::: joke
Robert Martin: "It shouldn't take longer than 15 minutes to teach someone how to write a use case." This lecture is fifty minutes. Writing a good one takes the rest of the semester.
:::

::: note
The quote heads Cockburn's own slide. The joke is honest: the format fits on an index card, and the skill is in the writing.
:::

## Save your energy

::: steps
- **1. Actors and goals:** the use case list
- **2. Main success scenario**, for the ones you pursue now
- **3. Failure conditions**, all of them, before handling any
- **4. Failure handling**
:::

::: key
Pause after each level. Each costs more than the last.
:::

::: note
Cockburn's four levels of precision.

Level 1: brainstorm the actors and their goals, one use case per user goal, named like the goal. Review the list for accuracy and completeness, prioritize, assign. That is the functional requirements at the first level of precision, and it is what every team brings to Friday's studio.

Level 2: sketch the main success scenario for the ones you pursue. Do not let the nice-to-haves hold the must-haves hostage: in Place an order, saved address and saved payment could wait. Simple, but not simpler.

Level 3: brainstorm every failure, and draft the whole list before handling any. People who start writing the handling immediately run out of energy before listing the failures.

Level 4: write the handling. Tiring and surprising work: an obscure business rule surfaces, or the handling reveals a new actor or a new goal.

The full writing process, if anyone asks: name the system scope and boundaries; brainstorm and list the primary actors; brainstorm and exhaustively list user goals for the system; pick one use case to expand; capture stakeholders and interests, preconditions and guarantees; write the main success scenario; brainstorm and exhaustively list the extension conditions; write the extension-handling steps; extract complex flows to sub use cases and merge trivial ones; readjust the set, adding, subtracting, and merging as needed.
:::

## Three kinds of action step

::: steps
- **Interaction** between two actors: "Clerk enters basic loss information."
- **Validation** protecting a stakeholder: "System confirms there are no competing claims."
- **Internal change** for a stakeholder: "System saves, and triggers acknowledgement be sent to agent."
:::

::: ask
Place an order has plenty of interactions and two validations. Where is its internal change?
:::

::: note
The examples come from Register Loss, an insurance use case: 1. Clerk enters insured's policy number or else name and date of incident. 2. System populates available policy information and indicates claim is matched to policy. 3. Clerk enters basic loss information. 4. System confirms there are no competing claims and assigns a claim number. 5. Clerk continues entering loss information specific to claim line. 6. Clerk has System pull other coverage information from other computer systems. 7. Clerk selects and assigns an adjuster. 8. Clerk confirms they are finished. 9. System saves, and triggers acknowledgement be sent to agent. Steps 1, 3, and 5 to 8 are interactions, step 4 is a validation, and steps 2 and 9 are internal changes.

The answer for Place an order: nowhere. Its validations are 3a3 and 5a3, and no step records the order. That is why nobody could say what cancelling at 10a has to undo.

Once you can write the three kinds, your style is set. The same style serves every action step in any use case: main success scenario or extension, business or system use case, high level or low.
:::

## Guideline 1: simple grammar

Subject ... verb ... direct object ... prepositional phrase.

::: key
The system ... deducts ... the amount ... from the account balance.
:::

::: note
The sentence structure should be absurdly simple. That is all there is to it. It communicates across specialties, technical and non-technical, and it describes what the system will do.
:::

## Guideline 2: who has the ball?

At every step one actor has the ball, and that actor is the subject of the sentence.

::: ask
At the end of the sentence, who has the ball now?
:::

::: joke
"Kicked. Passed. Scored." Great match. Who won?
:::

::: note
Think of a soccer game. The ball is the message and data passed from actor to actor. About half the time, the step ends with another actor holding it.

Many people accidentally leave off the first noun. Leave it off and it is no longer clear who controls the action, and the story gets hard to follow.
:::

## Guideline 3: a bird's eye view

::: cols
**Not this**

Get ATM card and PIN.

Deduct amount from account balance.
|||
**This**

The customer puts in the ATM card and PIN.

The system deducts the amount from the account balance.
:::

::: note
Beginning writers, particularly programmers, write as the system looking out at the world and talking to itself. You are not a programmer right now: you are modeling the system's external behavior. Use cases summarize users' desires, not programmers' tasks.

Some people prefer a play style, which is exactly what the roleplay was. "Customer: puts in the ATM card and PIN. System: deducts the amount from the account balance."
:::

## Guideline 4: move the process forward

::: steps
- "User hits tab key." *Why?*
- To get to the address field. *Why?*
- She has to enter her name and address first.
- **"User enters name and address."**
:::

::: key
A main success scenario rarely needs more than nine steps.
:::

::: ask
Place an order had seventeen. Which would you merge?
:::

::: note
Draw a line on the board from zero to the goal: every step has to cover real distance along it. The common beginner mistake is writing interface operations.

To find the higher-level goal for a step, ask "why is the actor doing that?", several times if needed. It is last week's "ask why until you reach the need", applied to a single sentence.

A use case with 13 or 17 steps is likely made of sentences that barely move the goal forward. Merge them into steps that move it distinctly forward; the details can go in the specification.

Candidates in Place an order: 7 to 9 (get the delivery date), 11 and 12 (charge the Shopper), 13 and 14 (submit for processing), 15 and 16 (tell the Shopper). Do not settle it. The point is that they can see it now.
:::

## Guideline 5: intent, not movements

::: cols
**Before**

1. System asks for name.
2. User enters name.
3. System prompts for address.
4. User enters address.
5. User clicks "OK".
6. System presents user's profile.
|||
**After**

1. User enters name and address.
2. System presents user's profile.
:::

::: joke
Requirements that mention the OK button are how a voice assistant ends up with an OK button.
:::

::: note
Describing the user's movements in the interface is one of the most common and severe mistakes. It makes requirements longer, brittle, and over-constrained. Inventing an interface that serves the intent is the interface designer's job, in design, not in the functional requirements.

Typically, all the data passing in one direction goes into one step. Larry Constantine and Lucy Lockwood, Software for Use, call these essential use cases: they describe interface intentions.
:::

## Guideline 6: a reasonable set of actions

::: cols
**Too much in one step**

1. The customer enters the order number. The system detects a winning number, registers the winner, emails the sales manager, congratulates the customer, and explains how to collect the prize.
|||
**Split at the natural breaks**

1. The customer enters the order number.
2. The system detects that it matches the winning number of the month.
3. The system registers the winner, emails the sales manager, and congratulates the customer.
:::

::: note
The original wording. Version 1: "The customer enters the order number. The system detects that it matches the winning number of the month, registers the user and order number as this month's winner, sends an email to the sales manager, congratulates the customer and gives them instructions on how to collect the prize." Version 2 splits it into the entry, the detection, and the registration with its email, congratulations, and instructions.

Related actions can share a step when they are one transaction: the actor sends a request and data, the system validates them, alters its internal state, and replies with the result. Write each as its own step or combine them, depending on how complicated each piece is and where the natural breaks fall.
:::

## Guideline 7: "validates", not "checks whether"

::: cols
**Before**

2. The system checks whether the password is correct.
3. If it is, the system presents the available actions for the user.
4. If it is not, ...
|||
**After**

2. The system validates that the password is correct.
3. The system presents the available actions for the user.
:::

::: joke
The system checks whether the password is correct. The system is now very well informed, and nothing has happened.
:::

::: note
"Check" does not move the process forward, is not the goal, and leaves the result open, so programmers immediately write "if the check passes" and "if the check fails".

The second version describes the scenario succeeding, and it makes the reader ask at step 2, "but what if the password is not valid?" They turn to the extensions and find one starting "Password is not valid." That rhythm is what makes a use case easy to read and to review.
:::

## Guideline 8: mention timing only when it matters

Usually the timing is obvious. Say it only when the requirement depends on it.

::: note
Feel free to put timing in, but only when you need to.
:::

## Guideline 9: "user has System A kick System B"

::: cols
**Not good**

User hits FETCH, at which time the system fetches the data from system B.
|||
**Better**

4. User has the system fetch the data from system B.
:::

::: note
The acceptable middle version is two steps: "4. User signals to the system to fetch data from system B. 5. The system fetches the background data from system B." It works, but it is awkward and redundant.

The better version says that the user controls the timing, that the ball passes from the user to the system to system B, and what each of the three is responsible for. How the user starts it stays unspecified, as it should.
:::

## Guideline 10: "do steps x-y until condition"

3. User selects an item to buy, marks it for purchase.
4. System adds the item to the customer's shopping cart.

Customer repeats steps 3-4 until indicating that they are done.

5. Customer purchases the items in the shopping cart.

::: note
The full example: 1. Customer supplies either account identifier or name and address. 2. System brings up the customer's preference information. 3. User selects an item to buy, marks it for purchase. 4. System adds the item to the customer's shopping cart. Customer repeats steps 3-4 until indicating that they are done. 5. Customer purchases the items in the shopping cart.

When only one step repeats, put the repetition in the step: "The user selects one or more products." When several repeat, write the repetition after them. Do not number the repetition statement, and do not open the loop with a statement of its own; both clutter the scenario.

The same idiom covers order: 1. Customer logs on. 2. System presents available products and services. Steps 3-5 can happen in any order. 3. User selects products to buy. 4. User specifies preferred form of payment. 5. User gives destination address. 6. User indicates shopping spree is complete. 7. System initiates order, with selected products to be charged against the form of payment and sent to the destination address.
:::

## Standard mistakes: "Register for Courses"

1. Display a blank schedule.
2. Display a list of all classes in the following way: The left window lists all the courses in the system in alphabetical order. The lower window displays the times the highlighted course is available. The third window shows all the courses currently in the schedule.
3. Do
4. Student clicks on a course.
5. Update the lower window to show the times the course is available.
6. Student clicks on a course time and then on the "Add Course" button.
7. Check if the Student has the necessary prerequisites and that the course offering is open.
8. If the course is open and the Student has the necessary prerequisites, add the Student to the course. Display the updated schedule showing the new course. If no, put up a message, "You are missing the prerequisites. Choose another course."
9. Mark the course offering as "enrolled" in the schedule.
10. End do when the Student clicks on "Save Schedule."
11. Save the schedule and return to the main selection screen.

::: ask
How many of the ten guidelines does this break?
:::

::: note
Steve Adolph and Paul Bramble, Patterns for Effective Use Cases (2002), UC 1.1, as shown on Alistair Cockburn's slides.

Let the room call out breaks for a minute before advancing. Expect: no subject in steps 1, 2, 5, 9, and 11 (guideline 2); window layout and button clicks (guideline 5); "check if" and "if no" in 7 and 8 (guideline 7); a programming loop in "Do" and "End do" (guideline 10); steps that move nothing forward (guideline 4). And no extensions at all: the missing-prerequisites failure is buried inside step 8.
:::

## Corrected: "Register for Courses"

**System:** Course Enrollment System · **Goal level:** User Goal

1. Student requests to construct a schedule.
2. The system prepares a blank schedule form.
3. The system gets available courses from the Course Catalog System.
4. Student selects up to 4 primary and 2 alternate course offerings.
5. For each course, the system verifies that the Student has the necessary prerequisites, adds the Student to the course, marking Student as "enrolled" for that course in the schedule.
6. When the Student indicates the schedule is complete, the system saves it.

**Extensions**

- **1a.** *Student already has a schedule:* System brings up the current version of the Student's schedule for editing instead of creating a new one.
- **1b.** *Current semester is closed and next semester is not yet open:* System lets Student look at existing schedules, but not create new ones.
- **3a.** *Course Catalog System does not respond:* The system notifies the Student and the use case ends.
- **5a.** *Course full or Student has not fulfilled all prerequisites:* System disables selection of that course and notifies the Student.

::: note
Adolph and Bramble, UC 1.3. Eleven steps became six. The failure buried in step 8 became extension 5a. The Course Catalog System turned out to be an actor, and its failure to respond became 3a.
:::

## Extensions: where the defects live {.center}

::: joke
An agent handed a use case with no extensions: "Understood. Nothing can go wrong."
:::

::: note
A use case with no extensions is not finished. An agent building from one invents the error handling silently, and you find out in a demo.
:::

## A checklist for extensions

::: steps
- Another way to succeed: "Clerk uses a shortcut code"
- The actor does it wrong: "Invalid password"
- The actor does nothing: "Password time-out"
- Every "validates": "Invalid account number"
- A supporting actor fails: "Response time-out"
- An expected internal failure: "Cash dispenser jams"
- An unexpected internal failure: "Corrupt transaction log"
- Too slow: "No response within 5 seconds"
:::

::: note
The full checklist. Alternative success paths ("Clerk uses a shortcut code"). The primary actor behaves incorrectly ("Invalid password"). Inaction by the primary actor ("Time-out waiting for password"). Every occurrence of "the system validates" implies an extension to handle failure of the validation ("Invalid account number"). Inappropriate or lack of response from a supporting actor ("Time-out waiting for response"). Internal failure within the system under design, which must be detected and handled as part of normal business ("Cash dispenser jams"). Unexpected and abnormal internal failure, which must be handled and will have an externally visible consequence ("Corrupt transaction log discovered"). Critical performance failures of the system that you must detect ("Response not calculated within 5 seconds").

Brainstorm from the first step of the scenario to the last, for the best coverage. They will be amazed at how many things can go wrong.

This is where the agent earns its keep: ask it for extensions and it proposes more than you thought of. Some are real paths in your client's business and some are generic ones it has seen elsewhere. Only someone who met the client can tell which.
:::

## Guideline 11: the condition says what was detected

::: cols
**Not this**

Customer forgets PIN.
|||
**This**

PIN entry time-out.
:::

Invalid PIN · Network is down · The customer walked away (time-out) · Cash did not eject properly

::: joke
The system has no sensor for regret.
:::

::: note
The system cannot detect that they forgot their PIN. Perhaps they walked away, had a heart attack, or are busy quieting a crying baby. What it detects is inaction: a time limit exceeded.

A condition the system can detect is one a developer can implement and a tester can trigger.
:::

## An extension is a miniature use case

::: steps
- **Trigger:** the extension condition
- **Goal:** complete the use case goal, or recover from the failure just encountered
- **Body:** action steps, and possibly extensions of its own
:::

::: note
Start writing the handling with the action step that follows detection. No need to repeat that the condition was detected. Continue the story exactly as in the main success scenario.
:::

## Guideline 12: indent condition handling

**Extensions**

- **2a.** Insufficient funds:
    - 2a1. System notifies customer, asks for a new amount.
    - 2a2. Customer enters new amount.

::: note
Indent the steps that handle the condition, and start the numbering again at 1 after the letter. The handling steps follow every guideline above. The course template and Project Pulse number extensions exactly this way.
:::

## Our style guide

<https://github.com/Washingtonwei/use-case-style-guide>

::: key
Your use cases are reviewed against it. Give it to your agent when you ask for a review.
:::

::: note
Senior design use cases follow this style. An agent reads the raw file best: raw.githubusercontent.com/Washingtonwei/use-case-style-guide/main/README.md.
:::

## Your turn: review a real use case

Project Pulse, `UC-EVA-submit-evaluation` (link in Slack)

::: steps
- **Alone, 5 minutes:** list every defect.
- **With your agent, 4 minutes:** give it the use case and the style guide.
- **Compare the two lists.**
:::

::: note
Students without Slack open can search docs/requirements/use-cases.md on Project Pulse main for the identifier. The pinned link stays valid after the use case is fixed: github.com/Washingtonwei/project-pulse/blob/347d48215e1d0770c09ef2d97648d1f553fbf908/docs/requirements/use-cases.md?plain=1#L2186-L2250

The alone half uses today's guidelines, the extension checklist, and the checklist at the end of the use-cases.md template. Laptop lid down if they have the use case on a phone.

Yes, it is mine, and it has at least six defects. The answer key is in the lecture plan; do not put it on screen.

Alone first, for the same reason the Napkin is done before the agent sees the brief: a review that starts from the agent's list anchors on it.
:::

## Two lists

::: ask
What did you find that the agent missed? What did it find that you missed?
:::

::: key
Where your review and the agent's disagree is where to look.
:::

::: note
Take three answers. Make sure the precondition contradiction comes out: PRE-2 says the student is assigned to a team, and extension 1c handles the student who is not. One of them is wrong, and deciding which is a question about the business, not about grammar.
:::

## They are requirements. They are not all of the requirements.

::: cols
**Use cases specify**

What the system does, including when it fails.
|||
**They do not specify**

Interfaces, data formats, business rules, formulas, constraints, quality attributes.
:::

::: note
Written properly, use cases really are requirements: you should not have to convert them into another form before a developer builds from them. But they are a fraction of what you need to collect. An important fraction, and still a fraction. Wednesday is the rest.
:::

## Before Friday

::: steps
- **No class Wednesday.**
- **Friday:** the rest of the specification, in this room. There is no studio this week.
- **Bring:** your use case list (actors and goals only) and your feature-to-area table.
- **Tomorrow, 10:00 AM:** peer evaluation, in Project Pulse.
:::

::: note
The list goes in section 3 of docs/requirements/use-cases.md, one row per use case under its area code, built from the team's feature list. It is the cheapest thing to review with your client, so send it to them once it is committed. The feature-to-area table goes in docs/traceability.md, with both checks run.

Say clearly that Friday is a lecture, not a studio, and that the team work moves to each team's own weekly meeting slot. Their TA checks it at the start of studio on Friday Sep 25.
:::

## Friday: the rest of the specification {.center}

Everything a use case does not say

::: note
Monday gave you the unit your agent builds against. Today is everything that is not in it, plus the document that holds the set together.

Remind them there was no class Wednesday, so this hour is carrying two days of material. It moves fast and the reading carries the detail.
:::

## A pile of information

Sixty employees. One day-long workshop. A hundred pages.

::: note
A senior manager at a software company convened about sixty employees for a day-long "voice-of-the-customer" workshop on the company's next flagship product. Facilitators, brainstorming, ideas everywhere. He compiled the results into a hundred-page document and called it a requirements specification.

It was nothing more than a pile of information. Nothing in it had been classified, organized, analyzed, or processed into anything describing a proposed solution. There were nuggets of real requirements buried in the chaff, and no developer could have found them.

Ask the room: what does he have that a specification does not, or what does a specification have that he does not? Take one answer, then move.
:::

## Collecting is not specifying

::: cols
**A pile**

Everything anyone said, in the order they said it.
|||
**A specification**

The functions the system must provide, its characteristics, and the constraints it must respect.
:::

::: note
The definition matters: completely enough to say how the system behaves under various conditions, and how well it behaves. Behavior and quality, both.
:::

## It is not written for you

| Reader | Takes |
|---|---|
| Project managers | Schedule, effort, resources |
| Developers | What to build |
| Testers | Test plans and procedures |
| Maintenance | What each part is supposed to do, years later |
| Doc writers | Manuals and help screens |
| Training | Course material |
| Legal | Whether it complies with the law |

::: note
Do not read the table. Point at three rows.

The tester, who derives cases from it and will find your ambiguities the expensive way. The maintainer, who reads it in three years with nobody left to ask, and who is what most of this room will be within two years of graduating. And legal, which is not a joke on a contract: subcontractors are an eighth reader and can be held legally to what the document says.
:::

## The eighth reader

::: ai
It reads the specification as its instructions. It is the only reader that cannot walk down the hall.
:::

::: key
Good enough for a teammate is not good enough for an agent.
:::

::: note
Every other reader on that table, meeting a sentence that could mean two things, asks somebody. The agent picks one meaning, silently, and writes it up in exactly the same confident prose as the parts that are true. You find out when you read the code. Or later.

The line to land, slowly: the questions your teammate would have asked were doing work you never noticed, because you never saw the questions they did not need to ask.
:::

## "It says I haven't taken a training class in over a year."

::: note
Jackie, a chemist, calling Tim, the product owner of the chemical tracking system. She needs more phosgene for her dyes and the system will not accept the request.

Tim: Contoso requires an annual refresher class in the safe handling of hazardous chemicals. Corporate policy, based on OSHA regulations. The system just enforces it. The stockroom used to hand you whatever you asked for. They cannot anymore.

Ask the room, and wait for it: is that a requirement of the software?
:::

## No. It is a property of the business.

Corporate policies · government regulations · laws · industry standards · computational algorithms

::: key
The rule existed before the software, and survives the software being switched off.
:::

::: note
So a business rule is not a software requirement as it stands. It is the origin of requirements, usually several, of different kinds: a business objective, a user requirement, a functional requirement that enforces it, a quality attribute. The propagation table is on the Requirement Types page.
:::

## Whose rule is this?

::: cols
**`BR-evaluation-submission-window`**

A student may submit a peer evaluation only for the previous week, and has that one week to complete it. Later edits included.
|||
**The course's.**

Project Pulse enforces it. Change the syllabus and the software is wrong.
:::

::: note
Worth saying out loud: this is the rule they are all living under right now, and the peer evaluation due yesterday was governed by it. Their own project has rules exactly like this, and most of them have not been written down.
:::

## Every rule has a source

::: steps
- Who says so, and where it is written down.
- A syllabus section. A policy number. A regulation with a citation. A sentence your client said, with the date.
- No source? It is not a rule yet. It is an `OPEN-ISSUES.md` entry.
:::

::: note
This is not bureaucracy, and here is why. In November somebody questions the rule and you need to check it against something. And a rule with no source cannot be told apart from one a teammate assumed, or one your agent supplied because it is the kind of rule a business like this usually has.
:::

::: joke
"Must comply with all applicable regulations." Which ones? "The applicable ones."
:::

## "I'm practically shouting over the fan and I'm getting hoarse."

::: note
Clarice, teaching in the new training room, calling Sam, the maintenance supervisor. Is the heating system broken?

Sam: it is working normally. It meets the requirements the engineers gave me. It circulates the right amount of air per minute, it controls temperature to within half a degree from 60 to 85, and it has every profile-programming capability that was requested. Nobody said anything about noise, so I bought the cheapest system that satisfied the requirements.

Clarice: the temperature control is fine. But this is a training room.
:::

## Every requirement met. Room unusable.

::: key
Quality attributes are how *well* the system does what it does.
:::

::: note
Nobody lied and nobody was lazy. Sam did exactly what he was asked. And the unit cannot be replaced now, because it was cheap for a reason.

This is where a system that passes every functional test still fails the people using it, which makes section 9 the section you cannot treat as a formality.
:::

## An adjective is not a requirement

::: cols
**What they say**

"The dashboard should be fast."
|||
**`PER-report-load`**

Return the dashboard and report views within 500 ms at the 95th percentile, under peak near-deadline concurrency.
:::

::: note
Same wish. The left one cannot be tested, cannot be designed against, and cannot be argued about in November, because there is nothing there to argue with.

Fast, easy, reliable, secure, user-friendly. Every one is the start of a conversation. Your job is to sit with the client until the verifiable goal underneath comes out.
:::

## A number and a way to measure it

::: key
Both halves.
:::

::: note
A threshold nobody can measure is a threshold nobody checks, and you discover that in the week you planned to demonstrate it. "500 ms at p95" still needs somebody to say how p95 is measured, and under what load.

Their section 9 entries are graded on both halves.
:::

## Where did this number come from?

::: ai
Ask an agent for quality attributes and you get 99.9% uptime and a 200 ms response. Plausible, well-formed, conventional, traceable to nothing.
:::

::: steps
- Your client said it.
- You measured it.
- Your team decided it, and can defend it.
:::

::: key
There is no fourth source.
:::

## Say "not applicable" out loud

`SAF-not-applicable`: this system controls nothing physical and stores no data whose disclosure could injure someone.

::: note
One sentence with a reason is information. Silence cannot be told apart from not having thought about it, and the reviewer cannot tell which one you did.

Most projects in this room have no safety requirements. Saying so, with the reason, is the deliverable.
:::

## Constraints

::: cols
**`CO-vue-spring-stack`**

Vue.js on the client. Spring Boot on the backend.
|||
**`CO-ferpa`**

Comply with FERPA when storing and transmitting student educational records.
:::

::: key
Not a feature. It removes an option you would otherwise have had.
:::

## Where constraints come from

Mandated or banned technologies · the operating environment · required conventions and standards · backward compatibility · regulation · hardware limits · systems that already exist

::: note
The full list is on the Requirement Types page. The point here is that constraints arrive from outside, and you do not get to negotiate most of them. They go in section 2.4.
:::

## The one nobody asks

::: key
Who maintains this after you graduate, and what do they already know how to run?
:::

::: note
A client whose entire technical staff is one part-time student worker cannot inherit a Kubernetes cluster, however correct it is. That is a constraint on your architecture, and it stays invisible until somebody asks the question.

Tell them to ask it at their next client meeting, and to write the answer down as a `CO-` entry.
:::

::: joke
Constraint discovered in week 14: the client's laptop cannot run Docker.
:::

## Data requirements

A requirement document's status is `DRAFT`, `SUBMITTED`, `RETURNED`, or `ACCEPTED`.

Submitted goes to returned or accepted. Accepted is read-only.

::: note
Entities, fields, allowed values, defaults, formats, and the reports built from them. Section 7.

The allowed values and the legal transitions between them are the data requirement. Get them wrong and you have built a workflow your client does not have, which is worse than building nothing, because it looks finished.
:::

## Invented precision

::: ai
A plausible field list reads exactly like a real one.
:::

::: note
A ZIP code has five digits, an optional hyphen, and four more that default to 0000. Anyone can check that against the world. A status enumeration has whatever values your client's process actually has, which is not the set that appears most often in the training data.

This is the hardest kind of hallucination to catch, because there is nothing wrong with the shape of it. Only with the content, and only someone who met the client can tell.
:::

## Not everything is a use case

::: steps
- A session expires after a period of inactivity.
- Every write to a student record is audited.
- Every night, a reminder goes to each student with an unsubmitted evaluation.
:::

::: note
None of those is a user's goal. Forcing them into use case shape produces bad use cases with imaginary actors, and everyone has seen the "Actor: System" use case that results.

They go in section 5.2, and they are still requirements.
:::

## EARS: five shapes

| Shape | Opens with |
|---|---|
| **Ubiquitous** | The `<system>` shall `<response>` |
| **Event driven** | **When** `<trigger>` |
| **State driven** | **While** `<in a state>` |
| **Optional** | **Where** `<feature is included>` |
| **Unwanted behavior** | **If** `<precondition>`, then |

::: note
Do not read the table. Read the four keywords: When, While, Where, If. All five with worked examples are on the Requirement Types page.

A requirement written in one of these is markedly harder for a human or an agent to misread than the same requirement in prose.
:::

## The shape teams skip

::: key
**If.**
:::

::: note
Which is why so many specifications describe a system in which nothing ever goes wrong. It is the same failure as a use case with no extensions, one document further down.

Converting prose into EARS is worth handing to your agent. Deciding which shape a requirement belongs in is a decision about what you meant, and that one is yours.
:::

## The specification is a hub, not a book

::: cols
**Tempting**

Paste the use cases into section 5 so the document is complete on its own.
|||
**Right**

5.1 points at `use-cases.md`. 6 points at `business-rules.md`. 4 points at vision and scope.
:::

::: key
A fact in two documents means one of them is wrong, and it is the one you are reading.
:::

::: note
This is the same rule the repository runs on, and it is what the identifiers have been for since week 3. A link you can follow is only possible if the thing at the other end has a name.
:::

## One more link in the chain

::: trace Trace: business rule to what enforces it
- Every rule is enforced by something.
- Every requirement that cites a rule cites one that exists.
:::

::: note
A second table in docs/traceability.md: rule, source, enforced by. For example BR-evaluation-submission-window, sourced to the syllabus, enforced by UC-EVA-submit-evaluation step 2 and extension 4a.

The two checks fail in opposite directions. The first catches a policy your software quietly ignores. The second catches a draft citing BR-late-penalty because a late penalty is the kind of thing a course usually has, which is aimed squarely at generated text.
:::

## Your turn: where did this number come from?

::: steps
- Your agent drafts section 9 of your specification, from your brief and your notes.
- Label every number **client**, **measured**, **decided**, or **nobody knows**.
- Every "nobody knows" becomes an `OPEN-ISSUES.md` entry, or gets deleted.
:::

::: note
Ten minutes, in teams, one screen per team is fine. Walk the room.

What they will find is that most of the numbers are in the fourth category, and that is the whole lesson. Much better felt than told. Ask two teams to read out one number they deleted and one they kept, and why they could defend the one they kept.
:::

## Before your next team meeting

::: steps
- **Agree your use case list**, then split: four write one use case in full, one owns `business-rules.md`, one owns constraints and quality attributes.
- **Both tables** in `docs/traceability.md`, with their checks.
- **Send the use case list to your client.**
- **Your TA checks all of it** at the start of studio, Friday Sep 25.
:::

::: note
No studio this week, so this happens in the team's own weekly meeting slot. One branch and one pull request each, as always.

Last thing: Monday is context engineering, which is where the specification they just started gets handed to an agent on purpose.
:::
