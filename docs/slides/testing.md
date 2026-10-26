---
title: Testing What the Agent Wrote
module: testing
week: 10
day: Monday
---

# Testing What the Agent Wrote

Week 10 · Read the tests first

::: note
**Say:** Good morning. Today is testing, the whole hour, and Wednesday and Friday you use it on your own proving slice in studio. One idea runs through all of it. When an agent writes the code, the tests are the part you read. And we will use one feature the whole way: the reminder, pull request 102, which you watched being built and reviewed.
:::

## Read the tests first {.center}

::: key
An agent writes code faster than you can read it. Read the tests.
:::

::: note
**Say:** The reminder was over two thousand lines. Nobody reads that line by line. But a test is the one artifact that says, in code, what the program must do, and it is short enough to read. Read the tests first and you know what was checked. Read only the code and you know what was written.
:::

## Every test passed

::: steps
- July 19, 2024: one CrowdStrike content update crashes about **8.5 million** Windows machines.
- The new template defined **21** input fields. The sensor supplied **20**.
- The tests matched the 21st field with a wildcard.
:::

::: warn
Every test passed, and none of them could have failed on this input.
:::

::: note
**Say:** Here is what a green suite is worth. CrowdStrike's own root cause analysis says the mismatch evaded multiple layers of build validation and testing. Why? The tests used a wildcard for the twenty-first field. So the suite was green, and it could not have been anything else. Hold on to that. We'll see the same shape in our own code before the hour is out.
:::

## Agents game tests they cannot pass

::: ai
Given tests that contradict the specification, frontier agents often "passed" by editing the tests or special-casing the inputs. Stronger models cheated more.
:::

::: note
**Say:** ImpossibleBench, 2025. Researchers gave coding agents tasks whose tests contradict the specification, so the only way to pass is to cheat. The agents often did: they edited the tests, or special-cased the inputs. And the stronger the model, the more it cheated. So when an agent tells you the suite is green, that is a claim about the tests as they now stand. Not about the program you asked for. Edsger Dijkstra said it more than fifty years ago: testing shows the presence of bugs, never their absence. The rest of today is about choosing tests that can show them.
:::

## How would you test the login?

::: ask
Three minutes, alone. List every test you would write for a login page.
:::

::: note
**Say:** Pencils out. Three minutes, on your own, no laptop. List every test you'd write for a login page: username, password, a log-in button. Go.

*[Three minutes. Then ask a few people how many they have. Most lists are under ten.]*
:::

## Four lists

::: steps
- **Junior:** right username and password; did it log in?
- **OK:** wrong password, wrong username, empty fields, CAPTCHA.
- **Experienced:** case, masking, forgot password, limits, session expiry, role redirect, Tab and Enter.
- **Super:** encryption, direct URLs, SQL injection, XSS, lockout, two devices, a million logins, browsers.
:::

::: note
**Say:** Find your list. *[Reveal one row at a time.]* Junior: did it log in. OK: the wrong inputs. Experienced: the behavior around the form. Super: security, concurrency, load, compatibility. The gap between "I can build this" and "I can say when this is done" is the distance down this table.

Full table in module 4.1.
:::

## Project Pulse stops at row two

::: steps
- Cypress login spec: renders, empty fields, correct login, forgot-password link.
- Backend: 70 logins, every one with the right password.
- No test sends a wrong password.
:::

::: note
**Say:** Our own app. The Cypress login spec has four tests. The backend's integration tests log in seventy times, every time with the correct password, as setup for something else. Not one test sends a wrong password. So the handler that answers "username or password is incorrect" has never run in a test.
:::

## Ask the agent

::: ai
It reaches the fourth row in seconds, better organized than most rooms.
:::

::: key
Generating the list is no longer the skill. Deciding which rows are real requirements is.
:::

::: note
**Say:** Ask an agent for the list and it gets to row four in seconds. Better organized than we just did. So writing the list isn't the skill anymore. Deciding is. Is a lockout threshold in your specification? Who sets it? Is a million concurrent logins a requirement, or ceremony? That stays with you and your client.
:::

## A QA engineer walks into a bar {.center}

::: joke
A QA engineer orders a beer. Orders 0 beers. Orders 99999999999 beers. Orders a lizard. Orders -1 beers. The first real customer asks where the bathroom is. The bar bursts into flames.
:::

::: note
**Say:** *[Read it.]* Brenan Keller, 2018. It's funny because both halves are true. The engineer tested every partition of the input. Nobody tested the use case.
:::

## The reminder arrived with its list

::: steps
- not.md: **20** test rows before any code, one or more per flow.
- Review added **4**, all about time.
- A Confirm after Monday midnight. A send that never answers. Items switched before the list arrives.
:::

::: key
A list read off the steps misses what happens between them.
:::

::: note
**Say:** Compare a designed feature. The reminder's design had twenty test rows before a line of code, one or more per flow of the use case, each with its level. Then review added four. Look at them: a Confirm that lands after Monday midnight, two rows. A send that never answers. An instructor who switches items before the first list arrives. Every one is about time. A list read off the use case's steps misses what happens between the steps.
:::

## A test is inputs plus an oracle

::: key
The oracle decides what "right" means. Where it came from decides what the test can catch.
:::

::: cols
**From the specification**

It can fail.
|||
**From the code under test**

It agrees with the code, bugs included.
:::

::: warn
Ask an agent to "write tests for this method" and it reads the method.
:::

::: note
**Say:** One word for today. An oracle is whatever decides that a run was correct. A test is inputs plus an oracle. The inputs decide what the code does. The oracle carries the intent.

And where the oracle comes from decides what the test can catch. From the specification: it can fail. From the code: it agrees with the code, bugs and all. That was CrowdStrike. An agent asked to write tests for a method reads the method and writes the second kind, unless you hand it the first. Week twelve builds stronger oracles on this word.
:::

## Choosing inputs: a sort

::: steps
- `[]` and `[7]`: empty and one.
- `[1, 2, 3]` and `[3, 2, 1]`: sorted and reversed.
- `[2, 1, 2, 1]`: duplicates.
- `[0, -5, 3]`: negatives and zero.
- `[MAX_VALUE, MIN_VALUE]`: where subtraction overflows.
:::

::: note
**Say:** You can't try every input, so you choose. Two heuristics. Equivalence partitions: group inputs the specification treats alike, take one from each. Boundaries: bugs live at the edges. For a sort, that gives this list. The last row is the one people miss: compare by subtraction and the extremes overflow. In JUnit 5 the whole list is one parameterized test, and its oracle is a property, not a hand-typed answer: the output is in order and holds the same elements. You'll see that shape in a minute, on a real method.
:::

## Where it bites

```typescript
.map((student) => `${student.lastName}, ${student.firstName}`)
.sort()
```

::: steps
- A bare sort compares character codes.
- "van Dyke" sorts after "Zhang". "Álvarez" sorts after both.
- The list beside it uses localeCompare, so one page orders students two ways.
:::

::: note
**Say:** Real code, the peer evaluation report page. Run the partitions through it. A bare sort compares character codes, so every capital comes before every lowercase letter, and accents come last. Van Dyke after Zhang. Álvarez after both. Neither is exotic. Each is a partition the happy-path name, Smith comma John, never visits.
:::

## Hard to test is a design smell {.center}

::: key
Code that is hard to test is usually telling you something about its design.
:::

::: note
**Say:** That code used to build "last, first" by splitting the full name on a space. Mary Ann Smith became "Ann, Mary". Cher became "undefined, Cher". And you couldn't test it without mounting the page and faking the server. Pull it into a pure function and every case is one line, and writing that test asks: why is the browser guessing a last name the server already knows? The reminder's pull request answered that. The server now sends the names in separate fields.
:::

## Boundaries in time

```java
@ParameterizedTest
@CsvSource({
    "2026-10-01, 2026-W40",   // inside the year
    "2025-12-29, 2026-W01",   // a December Monday in next year's week 1
    "2021-01-03, 2020-W53",   // a January Sunday in last year's week 53
    "2026-12-31, 2026-W53"    // a year with 53 weeks
})
void weekKeyUsesTheIsoWeekYear(LocalDate date, String key) {
    assertThat(WeekKeys.of(date)).isEqualTo(key);
}
```

::: note
**Say:** Now the reminder's own boundary. Project Pulse files every report under an ISO week key, like 2026-W40. And at New Year, the week's year is not always the calendar year of its days. December 29, 2025 starts 2026's week one. January 3, 2021 ends 2020's week fifty-three. And some years have fifty-three weeks: 2020 and 2026 do, 2021 does not.

That is the partition list for "the key of a date", and here it is as one parameterized test. Four rows, four partitions. WeekKeys.of is the real server method, the one place the backend turns a date into a week key.
:::

## One rule, two places

::: cols
**Server: WeekKeys**

Tested at New Year, and refuses 2021-W53.
|||
**Browser: week.ts**

Calendar year, and no unit tests at all.
:::

::: warn
On January 5, 2026 the report pages would have asked for 2025-W01. Review caught it, not a test.
:::

::: joke
"Every week belongs to the year it's in." Said every programmer, until December 29.
:::

::: note
**Say:** Here's what happened. The server's WeekKeysTest pins the New Year week. But the browser had its own copy of the rule, in week.ts, and it formatted with moment's capital YYYY: the calendar year. Project Pulse's frontend has no unit tests at all. So on January 5, the report pages would have asked the server for a week a year early. Code review found it, not a test. One rule in two places, and only one of them tested at its boundary.

*[Read the joke.]* There's a whole genre of articles called "falsehoods programmers believe about time". This one is ours.
:::

## Given, when, then

| Use case | Test |
|---|---|
| The precondition, or the extension's condition | Given |
| The trigger or step | When |
| The outcome | Then |

::: key
Your test cases are already written. They are the use case.
:::

::: note
**Say:** Now writing one. Here's the good news: your test cases are already written. Each extension is a test, and the parts map one to one. The condition is the Given. The step is the When. The outcome is the Then.
:::

## Extension 6a, as a test

```java
// Given (6a): three students owe a report; the send to s2 fails
willDoNothing().given(emailService).sendReminderEmail(anyString(), anyString(), anyString());
willThrow(new RuntimeException("Failed to send reminder email"))
        .given(emailService).sendReminderEmail(eq("s2@abc.edu"), anyString(), anyString());

// When: step 6
ReminderResult result = reminderService.remind(section, owed, WEEK);

// Then: 6a1, s3 still tried; 6a2, s2 named
assertThat(recipients.getAllValues()).containsExactly("s1@abc.edu", "s2@abc.edu", "s3@abc.edu");
assertThat(result.failed()).containsExactly(s2);
```

::: note
**Say:** The reminder's extension 6a: a reminder to one or more students can't be sent. 6a1, the system continues with the rest. 6a2, it names who it couldn't reach. The agent's test is that extension line for line. Given: the send to s2 fails. When: step six. Then: s3 was still tried after the failure, and s2 is named. Name the test after the behavior, not the method.

Shortened from ReminderServiceTest; full version in module 4.4.
:::

## Mock what you cannot control

::: steps
- EmailService talks to Gmail. The test mocks it.
- Milliseconds, nobody emailed, and s2 fails on demand.
- given / willReturn, willThrow / given, then / should.
:::

::: note
**Say:** Why could the test make s2's send fail? Because EmailService is a mock: an object whose answers the test controls. The test runs in milliseconds, emails nobody, and fails one send on demand, which no real mail server does when you ask nicely. Three calls do most of the work: given for an answer, willThrow for a failure, then-should to check a call happened. And this only works because ReminderService receives EmailService through its constructor. A class that news up its own mail client can't be given a mock.
:::

## Half the style

::: cols
**given(...)**

More than 200 calls.
|||
**then(...).should(...)**

Zero. Classic verify, about 60.
:::

::: ai
The charter said "Use BDDMockito: given(...).willReturn(...)". It named one half, so the agent wrote one half.
:::

::: note
**Say:** A small one about charters. Project Pulse's tests use given over two hundred times, and then-should never. Why? One line in the agent charter names the Given half only. So the agent follows it for Given and falls back for Then. The 6a test you just saw uses verify. Write both halves into your own charter.
:::

## Mock less than you can

::: steps
- Mock the slow and the uncontrollable: database, network, email, the clock.
- Real objects otherwise, when fast and deterministic.
- The scheduler test uses the real ReminderService, so it reads the emails.
:::

::: warn
The clock is a dependency too. A test that reads the real time passes today and fails in some other week.
:::

::: note
**Say:** Google's guidance: prefer real objects when they are fast and deterministic. A test that checks which calls were made breaks on every refactoring. WeeklyReminderSchedulerTest gets this right. It builds the real ReminderService, so its assertions read the actual emails. It mocks email, it mocks who owes what, because that has its own tests. And it mocks which course sections are reminded. Remember that last one. We're coming back to it.

And the dependency everyone forgets is the clock. Project Pulse injects a Clock, and every reminder test passes a fixed one, so the dates in its assertions never move. That's why the New Year test can exist at all. Call LocalDate.now directly and your test passes this week and fails some other week.
:::

## Read this test

```java
// Given: 2026-W38 is the last active week; Sep 23 is in the week after
Section section = section(1, MONDAY, WEDNESDAY);
section.setActiveWeeks(List.of("2026-W37", PREVIOUS_WEEK));
given(sectionService.findReminderEligibleSectionsForWeek(PREVIOUS_WEEK))
        .willReturn(List.of(section));
// When
scheduler(LocalDate.of(2026, 9, 23), true).sendWeeklyReminders();
// Then
verify(emailService, times(1)).sendReminderEmail(eq("s1@abc.edu"), anyString(), anyString());
```

::: ask
testTheLastActiveWeeksPeerEvaluationIsRemindedInTheWeekAfterIt. What would make it fail?
:::

::: note
**Say:** The weekly reminder only reminds about active weeks. Nothing in the first one, and the last one's items in the week after. The agent wrote a test for each. Here's the second. Read it. Turn to your neighbor: what change to the code would make this test fail? One minute.

*[Take two or three answers. Someone usually says "break the active-weeks check".]*
:::

## It mocks what it claims to test

::: steps
- The scheduler never reads activeWeeks. Delete that line: green.
- The rule lives in one query, and the test stubs that query.
- Drop the query's condition: this test, and the whole suite, stay green.
:::

::: warn
The design's test list put both rows at the unit level, for a rule that lives in SQL.
:::

::: note
**Say:** Here's the answer. The scheduler never reads activeWeeks, so that Given line is decoration. Delete it, still green. Which sections get reminded is decided by one JPQL query, findReminderEligibleSectionsForWeek, and the test stubs that query to return the section. Drop the query's member-of condition: still green. The whole suite stays green, because no test runs that query. The first-week test is the same; it passes because a mock's default is an empty list.

And the agent did what the design asked. The test list said unit for both rows. The rule lives in SQL. The missing test is an integration test: two sections, one whose active weeks include the week, one whose don't, and only the first comes back. CrowdStrike in miniature. Or as the joke goes: I mocked the database, the mail server, and the clock. The test passed. So did the bug.
:::

## The same agent saw the trap

::: ai
"…this test would pass while proving nothing about s1 and s3."
:::

::: key
An agent that writes that comment can still write the test before it. Read each one.
:::

::: note
**Say:** To be fair to the agent. In the same file, the test for a failed send has a comment explaining why the broad stub must come first. Under Mockito's strict stubs an unmatched call throws, ReminderService catches every runtime exception, and the test would pass while proving nothing. That's a sharp observation. Same file, same agent, and it still wrote the test we just read. So you read each one.
:::

## Five questions for any test

::: steps
- What is the oracle?
- Did it come from the specification or from the code?
- Would it fail if the behavior broke? Break it and see.
- Does it test a behavior, or just call a method?
- Does it mock the thing it claims to test?
:::

::: key
Delete a line. If no test goes red, no test was checking it.
:::

::: note
**Say:** Five questions before you trust a test, yours or the agent's. The scheduler test fails the last one. Put these in your review habit.

The third is the fastest check there is. Delete a line, run the tests, watch for red. That's manual mutation testing; tools like PIT do it to every line. We just did it twice on the scheduler.
:::

## The pyramid, on Project Pulse

| Layer | Checks | Project Pulse |
|---|---|---|
| Unit | One class, mocks, milliseconds | about 125 |
| Integration | Real Spring, real MySQL, HTTP | about 320 |
| End to end | The browser, the whole stack | 19, not in CI |

::: note
**Say:** Units are cheap and pinpoint a failure. End-to-end tests are slow and brittle but closest to the user. Google aims for about eighty percent unit. Project Pulse is closer to the reverse, mostly integration, partly because its rules about who may see which team's work cross layers, and only an integration test exercises them. Know which shape you have, and why.
:::

## The reminder, on all three layers

::: steps
- **22 unit:** the rules, on students made up in the test.
- **21 integration:** the real queries on seed data, and who may call each route.
- **9 Cypress:** the dialog's timing. A double click, lists out of order, a send that never answers.
:::

::: note
**Say:** One pull request, all three layers, each checking what only it can. Unit tests for the rule of who owes what. Integration tests for the real queries and authorization. Cypress for timing in the browser. Notice where the eligibility query should have gone: the middle row.
:::

## Coverage and flakiness

::: steps
- Coverage shows what ran, not what was checked.
- Every line of sendWeeklyReminders runs. The rule it depends on is checked nowhere.
- A flaky test teaches the team to ignore red. Fix the cause; never just rerun.
:::

::: note
**Say:** Two warnings. Coverage: the scheduler's tests run every line of sendWeeklyReminders, and the rule it depends on is checked nowhere. Use coverage to find code no test touches. Never read it as quality. And a flaky test is worse than none. It teaches the team that red means nothing. Most flakiness is time, ordering, or shared state.
:::

## What stays human

::: cols
**Delegate**

The candidate list, boilerplate, parameterized cases, running the suite.
|||
**Keep**

The oracle, which rows are in scope, and every change to a failing test.
:::

::: note
**Say:** Delegate the list, the boilerplate, running the suite. Keep the oracle, the scope, and every change to a test that was failing. An agent never edits a failing test to pass without saying so in the pull request. Tell it: write the tests from the specification, not from the code.
:::

## For your team

::: steps
- Every extension of your proving slice's use case has a test named after it, in given/when/then.
- Your charter: both BDDMockito halves, and no failing test edited without a reason in the pull request.
- Assignment 3: name each kept test's oracle, and break the code once.
:::

::: note
**Say:** Three things. One test per extension of your proving slice's use case, named after the extension. Two lines in your charter. And in assignment three, due Friday November 6, one line per AI-generated test you keep naming where its oracle came from, and proof you broke the code once and saw red.
:::

## Leave with this {.center}

::: key
When an agent writes the code, the tests are the part you read. Ask where each oracle came from, and break the code once.
:::

::: note
**Say:** One sentence. When an agent writes the code, read the tests. Ask where the oracle came from. And break the code once. Wednesday and Friday are studio: bring this to your slice's review.
:::
