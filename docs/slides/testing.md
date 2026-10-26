---
title: Testing What the Agent Wrote
module: testing
week: 10
day: Monday
---

# Testing What the Agent Wrote

Week 10 · Unit, integration, end to end, on Project Pulse

::: note
**Say:** Good morning. Today is testing, the whole hour, and Wednesday and Friday you use it on your own proving slice in studio. The goal is practical: by the end of the hour you can write a unit test with a mock, say which layer a test belongs on, and read a test an agent wrote. One feature carries us the whole way: the reminder, pull request 102, which you watched being built and reviewed.
:::

## Read the tests first {.center}

::: key
An agent writes code faster than you can read it. Read the tests.
:::

::: note
**Say:** The reminder was over two thousand lines. Nobody reads that line by line. But a test is the one artifact that says, in code, what the program must do, and it is short enough to read. Read the tests first and you know what was checked. Read only the code and you know what was written.

Dijkstra said it more than fifty years ago: testing shows the presence of bugs, never their absence. So the hour is about tests that can show them.
:::

## Write the list before the code

::: steps
- The design lists the tests first: one or more per flow of the use case, each with its layer.
- The reminder's design had **20** rows before any code. Review added **4**, all about time.
- Every extension is a test. Your use case already wrote most of the list.
:::

::: note
**Say:** When do you write tests? The list comes before the code, in the design. The reminder's design had twenty test rows before a line of code, one or more per flow of the use case, each with its layer: unit, integration, or end to end.

Then review added four, and every one is about time: a Confirm that lands after Monday midnight, a send that never answers, an instructor who switches items before the list arrives. A list read off the use case's steps misses what happens between them.

The good news: your extensions are most of your list already. The tests themselves come with the code, in the same pull request.
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

*[Ask: where could an oracle come from? Wait for an answer before revealing the columns.]*

From the specification: it can fail. From the code: it agrees with the code, bugs and all. An agent asked to write tests for a method reads the method and writes the second kind, unless you hand it the use case. So tell it: write the tests from the specification, not from the code.
:::

## Choosing inputs: partitions and boundaries

`letterGrade(score)`: 90–100 A · 80–89 B · 70–79 C · 60–69 D · 0–59 F · anything else invalid

::: cols
**Partitions: one input from each group**

`-5` · `30` · `65` · `75` · `85` · `95` · `120`
|||
**Boundaries: both sides of every edge**

`-1, 0` · `59, 60` · `69, 70` · `79, 80` · `89, 90` · `100, 101`
:::

::: joke
A QA engineer orders a beer. Orders 0 beers. Orders 99999999999 beers. Orders a lizard. Orders -1 beers. The first real customer asks where the bathroom is. The bar bursts into flames.
:::

::: note
**Say:** You can't try every input, so you choose, and two heuristics do most of the work.

Partitions: a partition is a group of inputs the rule treats the same way, so one input stands for the whole group. The grading scale has seven: five letters and two kinds of invalid, below zero and above a hundred. One test each.

Boundaries: bugs live at the edges. Somebody writes greater-than where they meant greater-or-equal, and 90 becomes a B. So test both sides of every edge: 89 and 90, 59 and 60, and the outer walls, minus one and zero, a hundred and a hundred and one.

Ask an agent for these tests and it will write them in seconds. Check one thing: did it find the invalid groups? Those are the ones a happy-path list forgets.

*[Read the joke.]* Brenan Keller, 2018. The engineer tested every partition of the input. Nobody tested the use case. You need both.
:::

## The JUnit 5 you need

```java
@ParameterizedTest
@CsvSource({ "0, F", "59, F", "60, D", "69, D", "70, C", "79, C",
             "80, B", "89, B", "90, A", "100, A" })
void letterGradeFollowsTheScale(int score, String grade) {
    assertThat(Grades.letterGrade(score)).isEqualTo(grade);
}

@Test
void letterGradeRejectsScoresOutsideZeroToHundred() {
    assertThat(catchThrowable(() -> Grades.letterGrade(101)))
            .isInstanceOf(IllegalArgumentException.class);
}
```

::: steps
- `@ParameterizedTest`: one test body, every boundary a row.
- `@Test`, and `catchThrowable` when the right answer is an exception.
- `@BeforeEach` for fresh setup, so no test depends on another.
:::

::: note
**Say:** Here is the last slide's list as code. The edges become rows of one parameterized test. The invalid side gets its own test, because the right answer there is an exception, and catchThrowable captures it so you can assert on it. A complete version would take minus one too, a second row of the same kind.

Project Pulse's backend uses exactly this: JUnit 5 with AssertJ's assertThat. @BeforeEach gives every test fresh setup. That is the whole toolkit for most of your tests; the full table is in module 4.4.
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
**Say:** Now the shape of one test. Each extension is a test, and the parts map one to one. The condition is the Given. The step is the When. The outcome is the Then. Write the three comments first, then fill them in.
:::

## Extension 6a, as a test

```java
@Test
void testRemindContinuesAfterOneSendFailsAndReportsWhoWasNotReached() {
    // Given (6a): three students owe a report; the send to s2 fails
    willDoNothing().given(emailService).sendReminderEmail(anyString(), anyString(), anyString());
    willThrow(new RuntimeException("Failed to send reminder email"))
            .given(emailService).sendReminderEmail(eq("s2@abc.edu"), anyString(), anyString());

    // When: step 6
    ReminderResult result = reminderService.remind(section, owed, WEEK);

    // Then: 6a1, all three were tried; 6a2, s2 is named
    verify(emailService, times(3)).sendReminderEmail(anyString(), anyString(), anyString());
    assertThat(result.failed()).containsExactly(s2);
}
```

Shortened from Project Pulse's `ReminderServiceTest`; full version in module 4.4.
{: .small }

::: note
**Say:** The reminder's extension 6a: a reminder to one or more students can't be sent. 6a1, the system continues with the rest. 6a2, it names who it couldn't reach. The test is that extension line for line. Given: the send to s2 fails. When: step six. Then: all three were tried, and s2 is named.

Look at the name. It says the behavior, not the method. One behavior per test.
:::

## Mock what you cannot control

```java
@ExtendWith(MockitoExtension.class)
class SubmissionStatusServiceTest {
    @Mock StudentRepository studentRepository;
    @Mock ActivityService activityService;
    @Mock EvaluationService evaluationService;
    @InjectMocks SubmissionStatusService submissionStatusService;
```

::: steps
- `given(mock.call()).willReturn(value)`: an answer.
- `willThrow(e).given(mock).call()`: a failure, like s2's.
- `then(mock).should().call()`: the call happened.
:::

::: note
**Say:** How could that test make s2's send fail? EmailService talks to Gmail, so the test replaces it with a mock: an object whose answers the test controls. Milliseconds, nobody emailed, and a failure on demand, which no real mail server gives you when you ask nicely.

Here is the setup you copy. @Mock for each dependency, @InjectMocks for the class under test, which receives them. Then three calls do most of the work.

This only works because the service receives its dependencies through its constructor. A class that news up its own mail client can't be given a mock.

One charter tip: Project Pulse's charter names only the given half, so its agent never writes then-should. Put both halves in yours.
:::

## Mock less than you can

::: steps
- Mock the slow and the uncontrollable: database, network, email, the clock.
- Use real objects otherwise, when they are fast and deterministic.
- Assert on results first, on calls only when the call is the outcome.
:::

::: warn
The clock is a dependency too. A test that reads the real time passes today and fails in some other week.
:::

::: note
**Say:** Google's guidance: prefer real objects when they are fast and deterministic. A test that checks which calls were made breaks on every refactoring, even when the behavior didn't change. The 6a test checks a call because "every student was tried" is the outcome, and a call is the only place it shows.

And the dependency everyone forgets is the clock. Project Pulse injects a Clock, and the tests pass a fixed one, so their dates never move. Call LocalDate.now directly and your test passes this week and fails some other week.
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
**Say:** Now you read one the agent wrote. The weekly reminder only reminds about active weeks, and the last active week's evaluation gets its reminder in the week after. Read the test. Turn to your neighbor: what change to the code would make this test fail? One minute.

*[Take two or three answers. Someone usually says "break the active-weeks check".]*
:::

## It mocks what it claims to test

::: steps
- The scheduler never reads activeWeeks. Delete that line: green.
- The rule lives in one query, and the test stubs that query.
- Drop the query's condition: this test, and the whole suite, stay green.
:::

::: joke
I mocked the database, the mail server, and the clock. The test passed. So did the bug.
:::

::: note
**Say:** Here's the answer. The scheduler never reads activeWeeks, so that Given line is decoration. Delete it, still green. Which sections get reminded is decided by one query, findReminderEligibleSectionsForWeek, and the test stubs that query. Drop the query's condition: still green. The whole suite stays green, because no test runs that query.

The missing test is an integration test: two sections on a real database, one whose active weeks include the week and one whose don't, and only the first comes back. Hold that thought; it's the next idea.
:::

## Break the code once

::: key
Delete a line. If no test goes red, no test was checking it.
:::

::: steps
- Where did the oracle come from: the specification, or the code?
- Would the test fail if the behavior broke?
- Does it mock the thing it claims to test?
:::

::: note
**Say:** Three questions before you trust a test, yours or the agent's. And the fastest check there is: delete a line, run the tests, watch for red. That's manual mutation testing; tools like PIT do it to every line. We just did it twice on the scheduler.
:::

## Three layers

| Layer | Checks | Project Pulse |
|---|---|---|
| Unit | One class, dependencies mocked; milliseconds | about 125 |
| Integration | Real Spring, real MySQL, HTTP | about 320 |
| End to end | The browser, the whole stack | 19 Cypress, not in CI |

::: note
**Say:** Unit tests are cheap, fast, and point at the exact failure. End-to-end tests are slow and brittle but closest to the user. Integration sits between: the real Spring context, a real MySQL in a container, requests through HTTP.

Google aims for about eighty percent unit. Project Pulse is closer to the reverse, mostly integration, partly because its rules about who may see which team's work cross layers, and only an integration test exercises them. Know which shape you have, and why.
:::

## Which layer, when

::: steps
- **Unit:** a rule you can check on data made up in the test. The reminder: **22**, for who owes what.
- **Integration:** a rule in a query, or who may call a route. The reminder: **21**, on seed data.
- **End to end:** what only the browser shows. The reminder: **9** Cypress, for the dialog's timing.
:::

::: key
Find where the rule lives. Test it at that layer.
:::

::: note
**Say:** One pull request, all three layers, each checking what only it can. Unit tests for the rule of who owes what, on students the test makes up. Integration tests for the real queries and for authorization. Cypress for timing in the browser: a double click on Confirm, lists arriving out of order, a send that never answers.

And now you can place the scheduler's missing test. The rule lives in a query, so it belongs in the middle row. The design's test list put it at unit, and that is how the bug got through.
:::

## Coverage shows what ran {.center}

::: key
Coverage shows what ran, not what was checked.
:::

::: note
**Say:** Last tool. The scheduler's tests run every line of sendWeeklyReminders. One hundred percent. And the rule that picks which sections get reminded is checked nowhere. Use coverage to find code no test touches. Never read it as a score.
:::

## What stays human

::: cols
**Delegate**

The candidate list, boilerplate, parameterized cases, running the suite.
|||
**Keep**

The oracle, which tests are in scope, and every change to a failing test.
:::

::: note
**Say:** Delegate the list, the boilerplate, running the suite. Keep the oracle, the scope, and every change to a test that was failing. An agent never edits a failing test to pass without saying so in the pull request.
:::

## For your team

::: steps
- Every extension of your proving slice's use case has a test named after it, in given/when/then.
- Your charter: both BDDMockito halves, and no failing test edited without a reason in the pull request.
- Assignment 3: name each kept test's oracle, and break the code once.
:::

::: key
When an agent writes the code, the tests are the part you read.
:::

::: note
**Say:** Three things. One test per extension of your proving slice's use case, named after the extension. Two lines in your charter. And in assignment three, due Friday November 6, one line per AI-generated test you keep naming where its oracle came from, and proof you broke the code once and saw red. Wednesday and Friday are studio: bring this to your slice.
:::
