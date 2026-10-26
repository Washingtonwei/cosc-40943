# Testing

> **Purpose (one line):** choose the tests a feature needs, write them as JUnit 5 unit tests with Mockito, and read any test (yours or the agent's) for what it actually checks, because when an agent writes the code, the tests are the part you read.

## 1. Learning objectives

By the end of this module, a student can:

1. List the tests a feature needs beyond the happy path, and decide which of an agent's longer list are in scope.
2. Name a test's oracle and say where it came from: the specification, or the code under test.
3. Choose inputs by equivalence partition and boundary, and write them as a JUnit 5 parameterized test.
4. Write a unit test from a use case extension in given/when/then form, isolating the unit's dependencies with Mockito, and say when a real object beats a mock.
5. Read a test and judge whether it would fail if the behavior broke, and prove it by breaking the code once.
6. Place a test on the pyramid, and say what coverage does and does not tell you.

## 2. Where it fits

- **Prerequisites:** [Spec-Driven Requirements](spec-driven-requirements.md), whose extensions are most of your test cases; [Design-of-Record](design-of-record.md#48-the-test-list-before-the-code), whose test list is written before the code; [AI-Assisted Implementation](implementation.md); and [Code Review](code-review.md), which reviews the change against that test list.
- **Leads into:** static analysis (week 10, checks that never run the program), CI/CD (week 11, the suite as a gate on every pull request), and dynamic analysis (week 12, which builds on the oracle named here).
- **How it's taught:** Monday of week 10, then two studio days on your proving slice. Practised in *Add a use case* (assignment 3) and in every pull request after it.
- **Course outcome it delivers:** [build, test, and ship a working MVP](../syllabus.md#learning-outcomes) (outcome 4), and verifying AI output without lowering the bar (outcome 6).

## 3. Motivation

**An agent writes code faster than you can read it, so read the tests.** A test is the one artifact that says, in code, what the program must do, and it is short enough to read. Read the tests first and you know what was checked; read only the code and you know what was written.

**A green suite proves only what it checks.** On 19 July 2024 a CrowdStrike content update crashed about 8.5 million Windows machines. A new template type defined 21 input fields; the sensor code supplied 20. CrowdStrike's root cause analysis says the mismatch evaded "multiple layers of build validation and testing", in part because the tests used wildcard matching for the 21st field. Every test passed, and none of them could have failed on this input.

**Agents game tests they cannot pass.** ImpossibleBench (Zhong, Raghunathan, and Carlini, 2025) gave coding agents tasks whose tests contradict the specification, so passing means cheating. Frontier models often "passed" by editing the tests or special-casing their inputs, and stronger models cheated more. An agent's report that the suite is green is a claim about the tests as they now stand, not about the program you asked for.

Testing shows the presence of bugs, never their absence (Dijkstra). The rest of this module is about choosing tests that can show them.

## 4. Core concepts

### 4.1 How would you test the login?

List the tests before reading on. Most lists stop early:

| Level | What the list contains |
|---|---|
| Junior | Correct username and password; did it log in? |
| OK | Wrong password, wrong username, both wrong; both fields empty, one empty; CAPTCHA right and wrong |
| Experienced | Case sensitivity; password masked; default-password reminder; forgot username and password; length and complexity limits; CAPTCHA refresh; session expiry; role-based redirect; focus on load; Tab and Enter |
| Super | Encrypted in transit and at rest; password expiry; protected pages by direct URL; password not in the clipboard or page source; SQL injection; XSS; lockout after repeated failures; the same user on two browsers and two devices; response time; a million concurrent logins; browser and version matrix; error messages that say what to do next |

The gap between "I can build this" and "I can say when this is done" is the distance down that table.

**Project Pulse's own tests stop at the second row.** Its Cypress login spec (`frontend/cypress/e2e/login.spec.cy.js`) has four tests: the page renders, empty fields are rejected, correct credentials log in, and the forgot-password link works. The backend's integration tests call `/users/login` 70 times, every time with the right password, as setup for something else. No test sends a wrong password, so `ExceptionHandlerAdvice.handleAuthenticationException`, which answers a failed login with "username or password is incorrect.", is never reached.

**Ask an agent for the list and it reaches the fourth row in seconds**, better organized than most rooms manage. Generating the list is no longer the skill. Deciding which rows are real requirements for *this* system is: is a lockout threshold in your specification, who sets it, and is a million concurrent logins a requirement or ceremony? That decision stays with you and your client.

**A designed feature arrives with its list.** The reminder's design, [`not.md`](https://github.com/Washingtonwei/project-pulse/blob/main/docs/design/not.md), had 20 test rows before any code was written ([Design-of-Record](design-of-record.md#48-the-test-list-before-the-code)), one or more per flow of `UC-NOT-remind-non-submitters`, each with its level. Review of [pull request #102](https://github.com/Washingtonwei/project-pulse/pull/102) added four more, and all four are about time: a Confirm that lands after Monday midnight (two rows), a send that gets no answer, and an instructor who switches items before the first list arrives. A list read off the use case's steps misses what happens between them.

### 4.2 A test is inputs plus an oracle

An **oracle** is whatever decides that an execution was correct. A test is inputs plus an oracle, and the oracle is the half that carries intent: inputs decide what the code does, and the oracle decides what "right" means.

Where the oracle comes from decides what the test can catch. A test whose oracle comes from the specification can fail. A test whose oracle comes from the implementation agrees with the implementation, which is what CrowdStrike's suite did. An agent asked to "write tests for this method" reads the method and writes the second kind unless you give it the first. Week 12 (dynamic analysis) builds a ladder of stronger oracles on this word.

### 4.3 Choosing inputs: a sort

You cannot try every input (CMU 17-313 estimates 72 billion cases for a four-parameter fare calculator), so you choose. Two heuristics do most of the work:

- **Equivalence partitioning:** group inputs the specification treats alike and take one from each group.
- **Boundary values:** bugs live at the edges, so test the minimum, maximum, and just past each.

For a method that sorts an array of integers, the partitions and boundaries give this list:

| Input | Why |
|---|---|
| `[]` | Empty: the boundary below one |
| `[7]` | One element |
| `[1, 2, 3]` | Already sorted |
| `[3, 2, 1]` | Reversed |
| `[2, 1, 2, 1]` | Duplicates |
| `[0, -5, 3]` | Negatives and zero |
| `[Integer.MAX_VALUE, Integer.MIN_VALUE]` | Extremes, where a comparison by subtraction overflows |

In JUnit 5 the list becomes one parameterized test. The oracle is a property, not a hand-typed answer: the output is in order, and it holds the same elements as the input.

```java
@ParameterizedTest
@MethodSource("arrays")
void sortReturnsTheSameElementsInOrder(int[] input) {
    int[] expected = input.clone();
    Arrays.sort(expected);                 // the reference oracle

    int[] actual = Sorter.sort(input.clone());

    assertThat(actual).containsExactly(expected);
}

static Stream<int[]> arrays() {
    return Stream.of(new int[]{}, new int[]{7}, new int[]{1, 2, 3}, new int[]{3, 2, 1},
            new int[]{2, 1, 2, 1}, new int[]{0, -5, 3},
            new int[]{Integer.MAX_VALUE, Integer.MIN_VALUE});
}
```

**Where it bites in real code.** Project Pulse's peer evaluation report lists the students who missed their evaluations ([`SectionsEvaluations.vue`](https://github.com/Washingtonwei/project-pulse/blob/main/frontend/src/pages/evaluations/admin/SectionsEvaluations.vue), `loadStudentsMissingPeerEvaluations`, on `main`):

```typescript
studentsMissingPeerEvaluations.value = result.data.teams
  .flatMap((team) => team.students)
  .map((student) => `${student.lastName}, ${student.firstName}`)
  .sort()
```

Run the partitions through it. A bare `.sort()` compares character codes, so every capital letter sorts before every lowercase one and accented letters come last: "van Dyke" sorts after "Zhang", and "Álvarez" after both. The averages list beside it sorts with `localeCompare` and gets both right, so one page orders the same students two ways. Neither case is exotic; each is a partition the happy-path name ("Smith, John") never visits.

**The test asks the design question.** Until October 2026 this code built "Last, First" by splitting the full name on a space, so "Mary Ann Smith" became "Ann, Mary" and "Cher" became "undefined, Cher". Logic inside a component's data-loading function cannot be tested without mounting the page and faking the server. Pulled into a pure function, every case is a one-line test, and writing that test asks why the client is guessing a last name the server already knows. The reminder's pull request answered it: the list now comes from the server with the names in separate fields. The sort is still inline. Extract one comparator into `utils/`, test it on the partitions, and both lists use it. Code that is hard to test is usually telling you something about its design.

**Boundaries in time.** Project Pulse files every report under an ISO week key such as `2026-W40`, and at New Year a week's year is not always the calendar year of its days: Monday, December 29, 2025 starts `2026-W01`. The partitions for "the key of a date" are a date inside the year, a December date in next year's week 1, a January date in last year's week 52 or 53, and a year with 53 weeks (2020 and 2026 have one). As one parameterized test on [`WeekKeys.of`](https://github.com/Washingtonwei/project-pulse/blob/main/backend/src/main/java/team/projectpulse/system/WeekKeys.java):

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

The server's `WeekKeysTest` already pins the third row, and refuses `2021-W53`, a week that does not exist. The browser had its own copy of the rule in `frontend/src/utils/week.ts`, which formatted keys with moment's `YYYY`, the calendar year, and Project Pulse's frontend has no unit tests at all. So on January 5, 2026 the report pages would have asked the server for `2025-W01`, a year early. Code review found it in #102, not a test (fix `975c122`, now `GGGG`, the ISO week year). One rule in two places, and only one of them tested at its boundary.

### 4.4 JUnit 5, and given/when/then from a use case

Project Pulse's backend tests use JUnit 5 with AssertJ assertions. The parts you will use every day:

| Annotation or call | Use |
|---|---|
| `@Test` | One test method |
| `@DisplayName("...")` | A readable name in the report |
| `@ParameterizedTest` with `@MethodSource` or `@CsvSource` | One test body over many inputs |
| `@BeforeEach` | Fresh setup before every test, so no test depends on another |
| `assertThat(x).isEqualTo(y)` | AssertJ's readable assertions |
| `catchThrowable(() -> ...)` | Capture an exception, then assert on it |

**Your test cases are already written: they are the use case.** Each extension is a test, and its parts map one to one:

| Use case | Test |
|---|---|
| The precondition, or the extension's condition | Given |
| The trigger or step | When |
| The postcondition, or the extension's outcome | Then |

`UC-NOT-remind-non-submitters` has extension `6a`: a reminder to one or more students cannot be sent. Its outcome has two parts: `6a1`, the system continues with the remaining students, and `6a2`, it names the students it could not reach. The agent tested it in [`ReminderServiceTest`](https://github.com/Washingtonwei/project-pulse/blob/main/backend/src/test/java/team/projectpulse/notification/ReminderServiceTest.java), and the test is the extension, line for line:

```java
@Test
void testRemindContinuesAfterOneSendFailsAndReportsWhoWasNotReached() {
    // Given (UC-NOT-remind-non-submitters 6a): three students owe a report; the send to s2 fails
    Map<Student, List<SubmittableItem>> owed = new LinkedHashMap<>();
    owed.put(s1, List.of(SubmittableItem.WEEKLY_ACTIVITY_REPORT));
    owed.put(s2, List.of(SubmittableItem.WEEKLY_ACTIVITY_REPORT));
    owed.put(s3, List.of(SubmittableItem.WEEKLY_ACTIVITY_REPORT));
    willDoNothing().given(this.emailService).sendReminderEmail(anyString(), anyString(), anyString());
    willThrow(new RuntimeException("Failed to send reminder email"))
            .given(this.emailService).sendReminderEmail(eq("s2@abc.edu"), anyString(), anyString());

    // When: step 6
    ReminderService.ReminderResult result = this.reminderService.remind(this.section, owed, WEEK);

    // Then: 6a1, s3 was still tried after the failure; 6a2, s2 is named
    ArgumentCaptor<String> recipients = ArgumentCaptor.forClass(String.class);
    verify(this.emailService, times(3)).sendReminderEmail(recipients.capture(), eq(ReminderService.SUBJECT), anyString());
    assertThat(recipients.getAllValues()).containsExactly("s1@abc.edu", "s2@abc.edu", "s3@abc.edu");
    assertThat(result.sent()).isEqualTo(2);
    assertThat(result.failed()).containsExactly(s2);
}
```

(Shortened: the real test also builds the three students, and its comments are extended here to name each part.)

The test name says the behavior, not the method: Google's guidance is to test behaviors, not methods, one behavior per test.

### 4.5 Mockito, and when not to mock

`ReminderService` sends through `EmailService`, which talks to Gmail. The test in 4.4 replaces it with a **mock**, an object whose answers the test controls, so the test runs in milliseconds, emails nobody, and makes the send to s2 fail on demand, which no real mail server does when asked. A service with several dependencies gets a mock for each; [`SubmissionStatusServiceTest`](https://github.com/Washingtonwei/project-pulse/blob/main/backend/src/test/java/team/projectpulse/notification/SubmissionStatusServiceTest.java), for who owes what, starts:

```java
@ExtendWith(MockitoExtension.class)
class SubmissionStatusServiceTest {
    @Mock StudentRepository studentRepository;
    @Mock ActivityService activityService;
    @Mock EvaluationService evaluationService;
    @InjectMocks SubmissionStatusService submissionStatusService;   // receives all three mocks
```

A few calls do most of the work, all from `org.mockito.BDDMockito`: `given(mock.call()).willReturn(value)` sets up an answer, `willThrow(exception).given(mock).call()` makes a call fail (the 6a test's s2), and `then(mock).should().call()` checks that a call happened (`should(never())` that it did not). Mockito only works because `ReminderService` receives `EmailService` through its constructor. A class that calls `new` on its own mail client cannot be given a mock, which is one more way a hard test points at a design problem.

**Project Pulse writes half the style.** Its tests call `given(...)` more than 200 times and `then(...).should(...)` never, using classic `verify(...)` about 60 times instead, as the 6a test does. The cause is one comment in the testing section of its agent charter (`backend/CLAUDE.md`), "Use BDDMockito: given(...).willReturn(...)", which names the Given half only, so the agent follows it for Given and falls back for Then. Write both halves into your own charter.

**Mock less than you can.** Google's testing chapters prefer real objects to mocks "as long as the real objects are fast and deterministic", because a test that checks which calls were made breaks on every refactoring, even when the behavior is unchanged. Mock what is slow or out of your control: the database, the network, email, the clock. Assert on results (state) before calls (interactions). [`WeeklyReminderSchedulerTest`](https://github.com/Washingtonwei/project-pulse/blob/main/backend/src/test/java/team/projectpulse/notification/WeeklyReminderSchedulerTest.java) gets the balance right: it builds the real `ReminderService`, so its assertions read the emails themselves. It mocks `EmailService`, who owes what ("because `SubmissionStatusService` has its own tests"), and which course sections are reminded, a choice 4.6 comes back to. The `verify(..., times(3))` in 4.4 earns its place because "every student was tried" is the extension's outcome, and a call is the only place that outcome shows.

**The clock is the dependency everyone forgets.** `EvaluationService` reads today's date through a `Clock` injected in its constructor (`WeekKeys.previousWeek(this.clock)`), so a test can fix the date and run the same way next year. Project Pulse's suite fixes it two ways. `EvaluationServiceTest` mocks the clock, builds a `Clock.fixed(...)`, and stubs `instant()` and `getZone()` with values copied out of it. `WeekKeysTest` passes the `Clock.fixed(...)` straight in: a real, fast, deterministic clock and two stubs fewer, and one of its tests pins the week that spans New Year. A test that reads the real time, or a random number it did not seed, passes today and fails in some other week.

### 4.6 Reading a test the agent wrote

`FR-NOT-weekly-reminder` reminds a course section only about its active weeks: nothing in the first active week, when there is nothing yet to submit, and the last active week's items in the week after it. The agent wrote a test for each, named for exactly that behavior. The second:

```java
@Test
void testTheLastActiveWeeksPeerEvaluationIsRemindedInTheWeekAfterIt() {
    // Given: 2026-W38 is the course section's last active week; Wednesday 2026-09-23 is in the inactive week after
    Section section = section(1, DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY);
    section.setActiveWeeks(List.of("2026-W37", PREVIOUS_WEEK));
    given(this.sectionService.findReminderEligibleSectionsForWeek(PREVIOUS_WEEK)).willReturn(List.of(section));
    given(this.submissionStatusService.findOwedItems(1, List.of(SubmittableItem.PEER_EVALUATION), PREVIOUS_WEEK))
            .willReturn(Map.of(student("s1@abc.edu"), List.of(SubmittableItem.PEER_EVALUATION)));

    // When
    scheduler(LocalDate.of(2026, 9, 23), true).sendWeeklyReminders();

    // Then
    verify(this.emailService, times(1)).sendReminderEmail(eq("s1@abc.edu"), anyString(), anyString());
}
```

The scheduler never reads `activeWeeks`. Which course sections are reminded is decided by one JPQL query, `SectionRepository.findReminderEligibleSectionsForWeek` (`:weekKey member of s.activeWeeks`), and the test stubs that query to return the section. Delete the `setActiveWeeks` line and the test stays green. Drop the query's `member of` condition and it stays green too, as does the whole suite, because no test runs that query. The first-active-week test is the same: it passes because a mock's default answer is an empty list. Both tests mock the very thing their names claim to check, and the design's test list asked for exactly that: it put both rows at the unit level, for a rule that lives in SQL. The missing test is an integration test that runs the query on real data: one course section whose active weeks include the week and one whose do not, and only the first comes back.

The same file shows the agent can see the trap. In the test for a failed send, a comment explains why the broad `willDoNothing()` stub must come first: under Mockito's strict stubs an unmatched call throws, `ReminderService` catches every `RuntimeException`, and the test "would pass while proving nothing". An agent that writes that comment can still write the test above. Read each one.

**Break the code once.** Deleting a line to see whether any test goes red is manual **mutation testing**; tools such as PIT do it to every line. It is the fastest way to find out whether a test checks anything.

**Five questions for any test, before you trust it:**

1. What is the oracle?
2. Did it come from the specification or from the code under test?
3. Would the test fail if the behavior broke? (Break it and see.)
4. Does it test a behavior or just call a method?
5. Does it mock the thing it claims to test?

**Test code is code people read.** Name tests for the behavior, keep each one readable on its own (Google's "DAMP, not DRY": a little repetition beats a chain of helpers), and keep logic out of tests, because a loop or a computed expected value in a test is a second program nobody tests.

### 4.7 The pyramid, on Project Pulse

| Layer | What it checks | Project Pulse on `main` |
|---|---|---|
| Unit | One class, dependencies mocked; milliseconds | About 125 tests in 17 files (`*ServiceTest`, a few security classes, `WeekKeysTest`), Mockito |
| Integration | Real Spring context, real MySQL in a Testcontainer, HTTP through MockMvc | About 320 tests in 25 Spring Boot test files, nearly all extending `AbstractIntegrationTest` |
| End to end | The browser, the whole stack | 19 Cypress tests in 4 specs, not run in CI |

Units are cheap, fast, and pinpoint a failure; end-to-end tests are slow, brittle, and closest to the user. Google aims for about 80% unit and 20% broader tests. Project Pulse is closer to the reverse, mostly integration tests, partly because its business and security rules (who may see which team's work) are enforced across layers and only an integration test exercises them. Know which shape you have and why.

**The reminder's pull request spans all three layers,** each checking what only it can. Its 22 unit tests (`SubmissionStatusServiceTest`, `ReminderServiceTest`, `WeeklyReminderSchedulerTest`, `WeekKeysTest`) check the rules on students made up in the test. Its 21 integration tests (`ReminderIntegrationTest`, `SubmissionStatusServiceIntegrationTest`) run the real queries on seed data and check who may call each route. Its 9 Cypress tests (`reminders.spec.cy.js`, with the server stubbed) check the dialog's timing: a double click on Confirm, two lists arriving out of order, a send that never answers.

**Coverage tells you what ran, not what was checked.** `WeeklyReminderSchedulerTest` runs every line of `sendWeeklyReminders`, and the rule that picks which course sections are reminded is checked nowhere. Use coverage to find code no test touches; never read it as a measure of quality.

**A flaky test is worse than none.** A test that fails at random teaches the team to ignore red. Most flakiness comes from time, ordering, and shared state; fix the cause, never just rerun.

## 5. The AI-native lens

- **Delegate to AI:** drafting the test list from a use case's extensions; the long candidate list (the login table's fourth row); boilerplate setup and parameterized cases; running the suite and reporting.
- **Keep human:** the oracle, meaning what "correct" is; which candidate tests are in scope; and every change to a test that was failing. An agent may not edit or delete a failing test to make the suite pass without saying so in the pull request.
- **Context to supply:** the use case with its extensions, the business rules, and the design's test list. Say "write the tests from the specification, not from the code".
- **How to verify:** read the tests before the code; ask the five questions in 4.6; break the code once and watch the test go red.

## 6. Risks & mitigations

| Risk (classic + AI-introduced) | Human judgment that catches it | Mitigation |
|---|---|---|
| **Classic:** only the happy path is tested | Walking the use case's extensions | One test per extension, named after it |
| **AI-introduced:** tests written from the code, so their oracle agrees with any bug | Asking where each assertion's expected value came from | Supply the specification as context; break the code once per new test |
| **AI-introduced:** the agent edits or weakens a failing test to turn the suite green | Reading the test diff in every pull request | Charter rule: failing tests change only with a reason in the pull request description |
| **Classic:** over-mocking makes tests break on every refactoring | Asking whether a real object would be fast and deterministic | Mock the database, network, and clock; assert on results first |
| **AI-introduced:** a test mocks the very thing its name claims to check | Asking, for each mock, whether the rule under test lives behind it | Find where the rule lives; a rule in a query gets an integration test on real data |
| **Classic:** coverage read as quality | Finding a covered line no assertion checks | Use coverage to find untested code, never as a target |

## 7. Hands-on (studio + optional individual assignment)

**In class (Friday):** list the login tests alone for three minutes, then compare with the table in 4.1, then with an agent's list. Mark which of the agent's tests Project Pulse actually needs.

**Team, own project:**

- **One test per extension:** for your proving slice's use case, every extension has a test named after it, in given/when/then form.
- **Your charter:** add both BDDMockito halves (`given(...).willReturn(...)` and `then(...).should(...)`) and the rule that a failing test is never edited to pass without saying so.

**Individual assignment:** in *Add a use case* (assignment 3, due Fri Nov 6), for each AI-generated test you keep, write one line in the pull request description naming its oracle's source, and break the code once to show it goes red.

## 8. Summary / key takeaways

- When an agent writes the code, the tests are the part you read.
- A test is inputs plus an oracle. An oracle taken from the code under test cannot catch its bugs.
- Choose inputs by partition and boundary; the use case's extensions are your test list.
- Mock what is slow or out of your control, the clock included; prefer real objects otherwise.
- Break the code once: a test that stays green is not testing that line.
- Coverage shows what ran, not what was checked.

## 9. Key papers & further reading

- Winters, T., Manshreck, T., and Wright, H. *Software Engineering at Google*. O'Reilly, 2020. Chapters 11 (Testing Overview), 12 (Unit Testing), and 13 (Test Doubles).
- Aniche, M. *Effective Software Testing: A Developer's Guide*. Manning, 2022. Partitions, boundaries, and testability, with Java examples.
- Sommerville, I. *Software Engineering*, 10th ed. Pearson, 2016. Chapter 8, Software Testing.
- CrowdStrike. "Channel File 291 Incident: Root Cause Analysis." August 2024.
- Zhong, Z., Raghunathan, A., and Carlini, N. "ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases." arXiv:2510.20270, 2025.
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/) and [Mockito documentation](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html).

## 10. Self-check

1. The agent's tests for a login endpoint all pass, and every one logs in with the correct password. Name three tests from the second row of 4.1 that would have to exist before you believed the endpoint works.
2. A test asserts `assertThat(result.getHours()).isEqualTo(10.5)` after stubbing the repository to return the object the test built with 10.5 hours. What is its oracle, and what would it catch?
3. Give the partitions for a method that takes a list of student names and returns them sorted by last name.
4. Write the given/when/then outline for extension 1b of a use case you wrote: which part comes from the precondition, which from the step, which from the outcome?
5. Your service calls `LocalDate.now()`. Why will its test eventually fail, and what one change fixes it?
6. Every line of `WeeklyReminderScheduler.sendWeeklyReminders` runs under its tests. Name the rule that number hides, and the test that would check it.
7. Your frontend computes the same week key as the server, and only the server's code has a test. Which inputs would you add first, and in which code?

## Related

- [Design-of-Record](design-of-record.md#48-the-test-list-before-the-code): the test list written before the code.
- [Code Review](code-review.md): reviewing a change against its test list.
- [Requirements Traceability](traceability.md#43-a-requirement-with-no-test-is-not-traced): a requirement with no test is not traced.
- Dynamic analysis (week 12): stronger oracles, and assertions in the code itself.
