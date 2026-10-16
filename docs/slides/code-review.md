---
title: Reviewing What the Agent Built
module: code-review
week: 8
day: Friday
---

# Reviewing What the Agent Built

Week 8 · Review the change, not the diff

::: note
Good morning. On Monday we watched an agent build. Today we learn to read what it built, and I will warn you now: reading is becoming the bigger half of the job.

The subtitle is the whole lecture in five words. Review the change, not the diff.

Two housekeeping items. The midterm is Monday and covers weeks one to seven. Today is not on it, so you are free to actually enjoy this. And your build-context is due in your team meeting by Sunday. With the midterm on Monday, meet early in the weekend.
:::

## Approved, merged, shipped {.center}

![xkcd 1354, Heartbleed Explanation, its six panels in three columns](img/xkcd-heartbleed.png)

Randall Munroe, [xkcd 1354](https://xkcd.com/1354/), CC BY-NC 2.5, rearranged.
{: .small }

::: key
A diff shows what was added, never what was left out.
:::

::: note
New Year's Eve, twenty eleven. A developer commits a new feature to OpenSSL, the library that encrypts a large share of the web. It is called heartbeat. A core maintainer reviews it and merges it. So far, this is exactly the process we teach.

Here is what heartbeat is for. Two computers on an encrypted connection go quiet for a while. One of them wants to know: are you still there? So it sends a little message, and the other side echoes it back.

Point at the first column. "Server, are you still there? If so, reply POTATO, six letters." The server finds POTATO in its memory and sends back six letters. POTATO. Perfect.

Second column. "Reply BIRD, four letters." Back comes BIRD. Look at her face in the bottom panel. She is thinking.

Third column. "Reply HAT. Five hundred letters." HAT is three letters. But the server never checks. It was told five hundred, so it starts at HAT and keeps copying: HAT, and then whatever happens to sit next to it in memory. Someone's password change. A master key. Four hundred and ninety-seven letters of other people's secrets, handed to a stranger who asked nicely.

That is the whole bug. The real thing was the same: send three bytes, claim sixty-four thousand, and get back sixty-four kilobytes of the server's memory, private keys included. Over and over, and nothing in the logs.

It shipped in March twenty twelve. It was found in April twenty fourteen and named Heartbleed. Two years.

The fix was about one line: if the claimed length is bigger than what actually arrived, throw the message away.

Now, the question I want you to sit with. What should the reviewer have spotted in that diff?

Pause. Then say: nothing. That one line was never written, so it was never in the diff. The reviewer read every line that was there. The bug was a line that wasn't. A diff shows what was added, never what was left out.
:::

## What review actually finds

::: cols
**Expected**

Finding defects.
|||
**Delivered**

Fewer defects than expected. Knowledge of code you did not write. Findings that are about 75% style and structure.
:::

::: note
So what does review find? Researchers at Microsoft asked developers what they expect from code review. Number one answer: finding defects. Then they looked at what reviews actually deliver. Fewer defects than people expect. Something else instead: knowledge of code you did not write.

A second study found that about three quarters of what reviews catch is style and structure. Naming, readability, layout. Not behavior.

Two things follow. First, style is a job for a machine. In week ten, linters take it over, and your attention goes to behavior and the contract. Second, on a team of six, review is how anyone learns the parts they did not write. If you only ever read your own code, you know one sixth of your product.
:::

## The rubber stamp has a price

::: steps
- Low review participation: up to **5 more** post-release defects per component.
- Past about **400 lines** in a session, review stops finding things.
- With an AI assistant: **less** secure code, **more** confidence that it was secure.
:::

::: joke
Ask a programmer to review 10 lines of code and they will find 10 issues. Ask them to review 500 lines and they will say it looks good.
:::

::: note
What happens when review is a rubber stamp? Three numbers.

A study of three open-source projects found that components with low review participation had up to five more defects after release.

An industry study at Cisco found that past about four hundred lines in one session, reviewers stop finding things. That one is a vendor study, not peer reviewed, so hold it loosely. But it matches everyone's experience.

And a Stanford study: people with an AI assistant wrote less secure code, and were more confident it was secure. Less safe, more sure. That is the worst combination.

Read the joke. Ask a programmer to review ten lines of code and they will find ten issues. Ask them to review five hundred lines, and they will say it looks good.

That joke is the four hundred line finding in one sentence. And the last pull request of this size on Project Pulse was eight hundred and eighty-four lines. That is not one sitting.
:::

## Every layer has holes {.center}

![Five slices of Swiss cheese: the agent, its tests, the linters, and CI let a missing extension through aligned holes; you, checking against the use case, stop it](img/swiss-cheese-review.svg)

::: key
Your slice is the only one holding the use case.
:::

::: note
Here is a picture from safety engineering, James Reason's Swiss cheese model. Every defense is a slice of cheese, and every slice has holes. Accidents happen when the holes line up.

Count the slices on your pull request. The agent. Its tests. The linters. Continuous integration. Notice what they all have in common. They check the code against itself. The agent wrote the tests from the code it wrote.

Point at the red line. That is a missing extension, like Heartbleed's missing check. It goes straight through all four, because their holes line up: none of them knows the extension was supposed to exist.

There is one slice that checks the code against what the client actually asked for. The purple one. That slice is you.

Your slice is the only one holding the use case.
:::

## Two questions every review answers

::: steps
- Does this change do what the **contract** says?
- How deep must I read **this part**, given where it lands?
:::

::: note
So every review answers two questions.

One. Does this change do what the contract says? By contract I mean the use case, every extension included, its business rules, and the design's API table and test list. Notice you cannot answer this question from the diff alone. You need the contract open beside it.

Two. How deep must I read this part, given where it lands? Not every line deserves the same attention. We will get to that in a minute.
:::

## Open the test list beside the diff

| Row | Asserts | Test? |
|---|---|---|
| UC-NOT main, WAR | Only students with no activity are emailed | |
| UC-NOT 4a | Inactive week: `400`, no email | |
| UC-NOT 6a | One send fails: the others still go | |
| UC-NOT authorization | Unassigned instructor, student: `403` | |

::: ask
A missing extension: where would you see it, in the diff or here?
:::

::: note
Here are four rows from the reminder's test list, in its design file, not dot m d. The full list has twenty. Each row says what has to be true. The main scenario: only students with no activity get emailed. Extension four a: the week is inactive, so the answer is a four hundred and no email. Six a: one email fails and the others still go. And authorization: an unassigned instructor or a student gets a four oh three.

Read the question. A missing extension: where would you see it, in the diff or here?

Take two or three answers before moving on.

Then say: here. If nobody handled four a, there is no code for it, so there is nothing in the diff to look at. That is the Heartbleed shape. But in this table, the row is sitting right there with an empty Test column. The test list is how you see what is not there.

If the seeded pull request is up, fill the Test column with the room now: for each row, name the test that covers it, or say that none does. If it is not up, take the question alone and move on.
:::

## How deep

| Commit | Read |
|---|---|
| **Trunk** | Every line |
| **Security rule or migration** | Every line, and where it sits |
| **Leaf** | Its tests against the test list; skim the rest |

::: note
Now the second question. How deep?

On Monday the agent built in commits, and it stopped after the first one so we could read it. That was not politeness. The commits tell you how deep to read.

The trunk is code that many paths depend on, that changes behavior users rely on, or that is hard to undo. Read every line.

A security rule or a database migration. Read every line, and also where it sits. You will see why on the next slide.

A leaf is new code reached only through the new feature. Check its tests against the test list, and skim the rest. Skimming a leaf is allowed. Skimming the trunk is not.
:::

## One word

```java
// The design:
.requestMatchers(POST, base + "/sections/{sectionId}/reminders")
    .access(anyOf(sectionInstructor, sectionOwnership))
// The quickest way to make a 403 test pass:
.requestMatchers(POST, base + "/sections/{sectionId}/reminders")
    .authenticated()
```

::: warn
Any logged-in student can now email an entire course section.
:::

::: note
Here is the design's security rule for sending reminders. A POST to the section's reminders route, and access goes to the section's instructor or the course owner.

Below it is the quickest way to make a failing four oh three test pass. Same route. Dot authenticated.

One word changed. Here is what it means.

Read the warning. Any logged-in student can now email an entire course section.

How does this happen? Project Pulse's security configuration ends with a rule that denies everything, so a new route fails closed until someone writes its rule. The agent writes an integration test, gets a four oh three, and the fastest path to green is a looser rule. Nobody intended harm. The test passed. The tests always pass.

What catches it? The test-list row for authorization: a student must get a four oh three. And this is why the security rule goes in a commit of its own, where one word cannot hide among eight hundred lines.
:::

## Write the triage down

```text
Trunk: SubmissionStatusService, read in full.
Security: the two route rules, read in full.
Leaves: controller and dialog; tests checked against rows 1 to 11; skimmed the rest.
```

::: key
A skim you wrote down is a decision. A skim you did not is a rubber stamp.
:::

::: note
So you decided what to read deeply and what to skim. Write it down. One line, at the top of your review. Something like this.

Read the three lines. Trunk: Submission Status Service, read in full. Security: the two route rules, read in full. Leaves: controller and dialog, tests checked against rows one to eleven, skimmed the rest.

Read the key line. A skim you wrote down is a decision. A skim you did not is a rubber stamp.

The written skim is honest, and a teammate can challenge it. Maybe they say: wait, the controller does the recount at send time, read that part too. Good. That is review working.
:::

## Checklists save lives {.center}

::: key
Five steps for central lines. Infections: 11% to zero.
:::

::: note
A story from medicine. Peter Pronovost at Johns Hopkins gave intensive care staff a checklist for inserting central lines. Five steps. The line infection rate fell from eleven percent to zero.

Here is the part I love. Every doctor already knew all five steps. Nobody learned anything new. The checklist caught the steps people skip when they are busy and tired and confident.

That is what a review checklist is for. Not to teach you something. To catch what you skip when a pull request looks fine.
:::

## The review checklist

::: steps
- Each test-list row: covered, or named as missing.
- Trunk and security commits read in full.
- The logic matches the description and the use case.
- Each extension's error path, and its log line.
- Tests check the contract, not a mock's echo.
:::

::: note
So here is ours. Five items.

Each test-list row: covered by a test, or named as missing. The trunk and security commits read in full. The logic matches the description and the use case. Each extension's error path, and whether it logs. And the tests check the contract, not a mock's echo. If a test only checks the value a mock was told to return, it cannot fail. It is a test of the mock.

Items three and four come from the twenty eighteen version of this course. Yes, I am recycling my own slides. Good ideas age better than slide designs.

The other items from that old list, syntax, duplication, unused code, are real. They belong to the linters starting in week ten. Until then, a nit comment.
:::

## Label every comment

```text
issue (blocking): test-list row "UC-NOT 4a" has no test.
  What does POST /reminders do for an inactive week?
nitpick (non-blocking): `cnt` → `sentCount`.
```

::: note
When you write a comment, label it. This convention is called Conventional Comments. Issue, suggestion, question, nitpick, praise. And each one is blocking or non-blocking.

Read the two examples. Issue, blocking: test-list row four a has no test. What does POST reminders do for an inactive week? And nitpick, non-blocking: rename c n t to sent count.

The label tells the author what you need from them. And notice the first comment asks a question with a specific answer. That is worth far more than "this looks odd." "This looks odd" makes the author guess. A specific question makes them check.
:::

## When to approve

::: key
Approve when the change is better than what was there, not when it is perfect.
:::

::: joke
"nit: missing period in comment." On a pull request that drops the users table.
:::

::: note
So when do you approve? Google's standard is the one I like best.

Read the key line. Approve when the change is better than what was there, not when it is perfect.

Hold out for perfect, and the team stalls. Approve what you did not check, and you are the rubber stamp. Between those two is a simple rule: never approve with a blocking comment open.

Read the joke. "Nit: missing period in comment." On a pull request that drops the users table.

Wait a beat. That reviewer was not lazy. They were busy, on the easy thing. The checklist exists to move your attention from where it is easy to where it matters.
:::

## The author's half

| Section | Carries |
|---|---|
| **Why** | The problem, readable without the issue |
| **What changed** | A summary; decisions the code does not show |
| **How it was verified** | **Verified:** tests mapped to rows. **Not verified:** what nobody checked |
| **Reviewer focus** | The trunk commit, any security rule, where to start |

::: ai
"Agents write convincing looking pull request descriptions. You need to review these too!" (Simon Willison)
:::

::: note
Review is not only the reviewer's job. The author can make it far easier, by bringing proof.

Your pull request template has four sections. Why: the problem, readable without opening the issue. What changed: a summary, plus any decision the code does not show. How it was verified: what you checked, mapped to test-list rows, and also what you did not check. And reviewer focus: which commit is the trunk, where the security rule is, where to start.

Read the quote. Simon Willison: "Agents write convincing looking pull request descriptions. You need to review these too!" His other rule: never file a pull request with code you have not reviewed yourself.

One number. A study of eighty thousand pull requests found only about fourteen percent explained their tests, and the ones that named the feedback they needed were much more likely to merge. That is a correlation, not proof. But the reviewer focus section costs you one minute.
:::

## The most useful line {.center}

```text
Not verified: the email failure path.
```

::: key
It tells the reviewer where to look. It is never penalized.
:::

::: note
If you remember one line from the author's half, make it this one. Not verified: the email failure path.

It tells the reviewer exactly where to look. And in this course it is never penalized. I would much rather read an honest "not verified" than a confident "all tests pass."

Remember the Stanford study from earlier. High confidence is not evidence. An honest "not verified" is evidence. It tells us where the risk is.
:::

## Your turn: the seeded pull request

::: ask
Find what matters. Label each comment. Do not block on nits.
:::

::: note
Your turn. On screen is a pull request for the reminder. I will tell you a secret: it was planted. Someone put defects in it on purpose, so we know the answers.

Read the instructions. Find what matters. Label each comment. Do not block on nits.

Four minutes on your own. Then three minutes with a neighbor. Start with your triage line, then go to the test list.

Time it. When the seven minutes are up, take answers aloud. Ask for a triage line first, then the test list. Then ask what they found. Give the room credit for every planted defect it finds, and give extra credit, out loud, to the pair who saw the nits and chose not to block on them.

If the seeded pull request is not ready, use Project Pulse pull request seventy-six instead: real, merged, eight hundred and eighty-four lines, three commits. Say: you have seven minutes for an eight hundred line pull request, so you cannot read it all. Write the triage line, which commit you read in full and why, and one labeled comment. Then compare triage lines across the room. Different triage lines are fine. Unwritten ones are not.
:::

## The agent as first reviewer

::: steps
- Fresh context: it never saw the conversation that wrote the code.
- `/code-review 42`; `--comment` posts its findings.
- It reviews the **diff**, not the change, unless you give it the contract.
:::

::: joke
The reviewer bot approved its own pull request. It found the code clear, well structured, and written by someone with excellent taste.
:::

::: note
Now let the agent review. Claude Code has a code review command. You give it a pull request number, and with the comment flag it posts its findings on the pull request.

Two things make it useful. First, it runs in a fresh context. It never saw the conversation that wrote the code, so it cannot inherit the author's reasoning, or the author's blind spots.

Second, the catch. By default it reviews the diff, not the change. Its own documentation says it focuses on correctness, not missing test coverage. And a missing extension is missing test coverage. So unless you give it the contract, it has the same Heartbleed blind spot a lazy human has.

Read the joke. The reviewer bot approved its own pull request. It found the code clear, well structured, and written by someone with excellent taste.

That joke is real research. Language models tend to favor their own output. That is why the review runs in a fresh context, and why Anthropic's managed reviewer can never approve or block. The person approves.
:::

## Same pull request, run twice

| Run | Found | Missed |
|---|---|---|
| `/code-review <PR>` | | |
| With the use case and test list | | |

::: note
If the two runs are done: here is the same seeded pull request, reviewed twice by the agent. Once with only the pull request number. Once with the use case and the test list named in the request. Walk the Found column and the Missed column of each, and put them beside what the room found. Then ask: who did better on the missing extension, you or the plain run?

If the two runs are not done, say so plainly: I am running both this weekend, and I will post both lists with screenshots on the module page. Then say what we are testing: whether naming the contract changes what the agent finds. Do not predict the result. That is the point of running it.

One honest note either way. The output varies from run to run, so treat one run as one sample, not a verdict.
:::

## Triage its findings

::: steps
- Each finding: fixed, or rejected with a reason.
- Spot-check one it flagged and one it passed.
- No mention of the test list? It reviewed the diff.
:::

::: note
Whatever the agent finds, treat it like a teammate's review, not a ruling.

Each finding is either fixed, or rejected with a reason. Write which, under how it was verified.

Spot-check one thing it flagged and one thing it passed. The second one matters more. A reviewer you never check becomes a reviewer you simply trust.

And a simple smell test: if its review never mentions the test list, it reviewed the diff.
:::

## Before your slice merges

::: steps
- A teammate who did not write it reviews it.
- The triage line, and every test-list row marked.
- Labeled comments.
- One `/code-review` run with the contract, each finding answered.
:::

::: note
So here is what this means for your team, starting with your proving slice.

A teammate who did not write it reviews it. Not the author, and not the author's agent. The review carries the triage line, and every test-list row marked covered or missing. The comments are labeled. And there is one code review run with the contract, with every finding answered.

Your teaching assistant reads two reviews per team. And assignment three, due Friday, October thirtieth, asks you for the same review on your own pull request before you submit.

One last thing. On Monday, you are the reviewer and the midterm is the pull request. Read the whole question, write down what you skip, and you will be fine. Good luck, and have a good weekend.
:::
