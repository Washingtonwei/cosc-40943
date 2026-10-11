---
title: Reviewing What the Agent Built
module: code-review
week: 8
day: Wednesday
---

# Reviewing What the Agent Built

Week 8 · Review the change, not the diff

## Approved, merged, shipped {.center}

::: key
A diff shows what was added, never what was left out.
:::

::: note
Heartbleed. On New Year's Eve 2011 a developer committed OpenSSL's heartbeat feature, and a core maintainer reviewed and merged it. The code copied back as many bytes as the message claimed to contain, without checking the claim. The missing check was not in the diff because it was never written. Shipped in OpenSSL 1.0.1, March 2012; disclosed April 2014; any server running it could be asked for 64 KB of its memory at a time, private keys included.
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
Bacchelli and Bird 2013 (Microsoft): defects are the top expectation, but knowledge transfer and team awareness are major outcomes, and understanding the change is the hardest part. Mäntylä and Lassenius 2009: three quarters of review findings are evolvability defects. So: hand style to linters in week 10, and aim people at behavior and the contract. On a team of six, review is how anyone learns the parts they did not write.
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
McIntosh et al. 2014 (Qt, VTK, ITK): low coverage up to two, low participation up to five additional defects. Cohen 2006 is SmartBear's Cisco study, industry data and not peer reviewed: about 400 lines a session, 500 lines an hour, 60 to 90 minutes. Perry et al. 2023, 47 participants. The reminder pull request is 884 lines: not one sitting. The joke is the 400-line finding in one sentence.
:::

## Every layer has holes {.center}

::: steps
- The agent, its tests, the linters, CI: the code checked against **itself**.
- You: the code checked against **the use case**.
:::

::: key
Your slice is the only one holding the use case.
:::

::: note
Reason's Swiss cheese model (2000), which CMU 17-313 uses for review: every defense has holes, and accidents happen when they line up. The agent, its tests, the linters, and CI all check the code against itself. Only the reviewer checks it against what the client asked for.
:::

## Two questions every review answers

::: steps
- Does this change do what the **contract** says?
- How deep must I read **this part**, given where it lands?
:::

::: note
The contract: the use case, every extension included, its business rules, and the design's API table and test list. The diff alone cannot answer the first question.
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
Four of the 18 rows in not.md's test list. Fill the Test column in the room, from the seeded pull request. For each row, find the test that covers it or write that none does. A row with no test is the Heartbleed shape: nothing in the diff to look at.
:::

## How deep

| Commit | Read |
|---|---|
| **Trunk** | Every line |
| **Security rule or migration** | Every line, and where it sits |
| **Leaf** | Its tests against the test list; skim the rest |

::: note
The commits from Monday set the depth. Trunk: code many paths depend on, behavior users rely on, hard to undo. Leaf: reached only through the new feature.
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
Abridged. SecurityConfiguration ends its API rules with denyAll(), so a new route fails closed until someone writes its rule, and Spring applies the first rule that matches. The agent's integration test gets a 403; loosening the rule is the fastest green. The proof is the test-list row "UC-NOT authorization". This is why the rule goes in a commit of its own.
:::

## Write the triage down

```text
Trunk: SubmissionStatusService, read in full.
Security: the two route rules, read in full.
Leaves: controller and dialog; tests checked against rows 1 to 9; skimmed the rest.
```

::: key
A skim you wrote down is a decision. A skim you did not is a rubber stamp.
:::

## Checklists save lives {.center}

::: key
Five steps for central lines. Infections: 11% to zero.
:::

::: note
Peter Pronovost at Johns Hopkins, told by Atul Gawande in "The Checklist", The New Yorker, 2007. The steps were ones every doctor knew. The checklist caught the ones skipped under pressure, which is what a review checklist is for too.
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
Items 3 and 4 come from the 2018 version of this course's "What to review?" list. Its other items (syntax, duplication, unused code) are real and belong to the linters from week 10; until then, a "Nit:" comment.
:::

## Label every comment

```text
issue (blocking): test-list row "UC-NOT 4a" has no test.
  What does POST /reminders do for an inactive week?
nitpick (non-blocking): `cnt` → `sentCount`.
```

::: note
Conventional Comments: issue, suggestion, question, nitpick, praise, each blocking or non-blocking. The label tells the author what you need. A question with a specific answer beats "looks odd".
:::

## When to approve

::: key
Approve when the change is better than what was there, not when it is perfect.
:::

::: joke
"nit: missing period in comment." On a pull request that drops the users table.
:::

::: note
Google's standard of code review. Holding out for perfect stalls the team; approving what you did not check is the rubber stamp. Never approve with a blocking comment open. The joke is the failure the checklist prevents: attention spent where it is easy.
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
The template is .github/PULL_REQUEST_TEMPLATE.md in the course templates. Willison's rule: never file a pull request with code you have not reviewed yourself. Across 80,000 pull requests, only 13.7% explained their tests, and naming the feedback you need went with 64 to 72% higher merge likelihood (Pirouzkhah et al. 2026, correlation). Reviewer focus is that element.
:::

## The most useful line {.center}

```text
Not verified: the email failure path.
```

::: key
It tells the reviewer where to look. It is never penalized.
:::

::: note
"High confidence" is not evidence (Perry et al.). An honest "not verified" is evidence about where the risk is.
:::

## Your turn: the seeded pull request

::: ask
Find what matters. Label each comment. Do not block on nits.
:::

::: note
Four minutes alone, three with a neighbour, then answers aloud. Planted: four kinds of defect (see the lecture plan). Push for the triage line first, then the test list. Credit the pair who declines to block on the nits.
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
Its documentation says it "focuses on correctness... not formatting preferences or missing test coverage". A missing extension is missing test coverage. Anthropic's managed reviewer always ends its check neutral: it cannot approve or block. LLM evaluators favor their own output (Panickssery et al. 2024, on summaries), which is the joke and the reason for the fresh context.
:::

## Same pull request, run twice

| Run | Found | Missed |
|---|---|---|
| `/code-review <PR>` | | |
| With the use case and test list | | |

::: note
Fill in from the rehearsal before class, and keep screenshots: the output varies between runs. Put both lists beside the room's.
:::

## Triage its findings

::: steps
- Each finding: fixed, or rejected with a reason.
- Spot-check one it flagged and one it passed.
- No mention of the test list? It reviewed the diff.
:::

## Before your slice merges

::: steps
- A teammate who did not write it reviews it.
- The triage line, and every test-list row marked.
- Labeled comments.
- One `/code-review` run with the contract, each finding answered.
:::

::: note
The TA reads two reviews per team. Assignment 3 (due Fri Oct 30) asks for the same review on your own pull request before you submit.
:::
