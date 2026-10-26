---
title: Testing What the Agent Wrote
module: testing
week: 10
day: Monday
---

# Testing What the Agent Wrote

Week 10 · From a sorting method to Project Pulse

::: note
**Say:** Good morning. Today is testing, the whole hour, and Wednesday and Friday you use it on your own proving slice in studio. We start small, with one sorting method, and end with the tests that guard Project Pulse every time someone opens a pull request. By the end you can write a unit test with a mock, pick test cases on purpose, and say which kind of test a rule needs.
:::

## How do you know a method is correct? {.center}

::: cols
**Code review: static**

Read the code. Reason about what it would do.
|||
**Testing: dynamic**

Run the code. Watch what it does.
:::

::: note
**Say:** Two weeks ago you did code review: you read a method and convinced yourself it was right. Good, and keep doing it. But reading is static. You never ran the code; you reasoned about it. Testing is dynamic: you run the code on chosen inputs and compare what happens with what should happen. Next week we add a third kind, static analysis, where a tool does the reading.

*[Ask: how would you convince me the method on the next slide is correct?]*
:::

## Selection sort

```java
public static int[] sort(int[] input) {
    int[] a = input.clone();
    for (int i = 0; i < a.length - 1; i++) {
        int min = i;
        for (int j = i + 1; j < a.length; j++) {
            if (a[j] < a[min]) {
                min = j;
            }
        }
        int tmp = a[i];
        a[i] = a[min];
        a[min] = tmp;
    }
    return a;
}
```

::: note
**Say:** Selection sort, which you all wrote in CS 1. Find the smallest element of what is left, swap it to the front, repeat. It copies the input so the caller's array is untouched.

You could review this, and you probably believe it. Now let's prove it a different way: run it.
:::

## Our first unit tests

```java
class SelectionSortTest {

    @Test
    void sortsAnUnsortedArray() {
        int[] result = SelectionSort.sort(new int[] {5, 2, 9, 1});
        assertThat(result).containsExactly(1, 2, 5, 9);
    }

    @Test
    void keepsDuplicates() {
        int[] result = SelectionSort.sort(new int[] {3, 1, 3, 1});
        assertThat(result).containsExactly(1, 1, 3, 3);
    }

    @Test
    void sortsAnEmptyArray() {
        assertThat(SelectionSort.sort(new int[] {})).isEmpty();
    }
}
```

::: note
**Say:** Here are three JUnit 5 tests. Each is a method marked @Test. Each one calls the method with an input we chose and checks the output against the answer we expected, with AssertJ's assertThat, the same style Project Pulse uses. Read it as a sentence: assert that the result contains exactly 1, 2, 5, 9, in that order. Run them in IntelliJ and you get three green checks in a fraction of a second.

*[Ask: what other inputs would you try? Collect: one element, already sorted, reversed, negatives, all equal. Every one is a test.]*
:::

## What is a unit test?

::: steps
- **Unit:** the smallest piece you can test alone, usually one method or one class.
- **Test case:** an input, plus the output you expect.
- **Oracle:** whatever decides that the output is right.
:::

::: key
A test is inputs plus an oracle.
:::

::: note
**Say:** Three words. A unit is the smallest piece you can test on its own; for us, a method or a class. A test case is an input and the expected output. And the oracle is whatever decides the output is right. In the last slide the oracle was the expected array we typed in.

The inputs decide what the code does. The oracle carries what "right" means. Most bad tests have a bad oracle.
:::

## A weak oracle

```java
@Test
void resultIsSorted() {
    int[] result = SelectionSort.sort(new int[] {5, 2, 9, 1});
    assertThat(result).isSorted();
}
```

::: ask
Which broken sort passes this test?
:::

::: steps
- `return new int[0];` is sorted. Green.
- The real oracle: the output is sorted **and** holds exactly the input's elements.
:::

::: note
**Say:** Here's an oracle that sounds fine: the output is sorted. Turn to your neighbor: write a broken sort that passes it. Thirty seconds.

*[Take answers. Someone finds "return an empty array", or "return all zeros".]*

An empty array is sorted. So is an array of zeros. The test is green and the sort is useless. The full oracle for sorting has two halves: the output is in order, and it is a rearrangement of the input, nothing lost, nothing added. containsExactly, like the previous slide, checks both at once: these elements, in this order.

Where did the weak oracle come from? Someone looked at what the code obviously does. An agent asked to "write tests for this method" reads the method too. Write your oracle from the specification.
:::

## Why unit tests matter

::: steps
- **Fast:** hundreds run in seconds, so you run them on every change.
- **Precise:** a red test names the method that broke.
- **Repeatable:** same input, same answer, on any machine, forever.
- **A specification you can run:** the test says what the code must do.
:::

::: note
**Say:** Why bother, when you could just run the app and click around? Because a unit test is fast enough to run every few minutes, it points at the exact method that broke, and it gives the same answer on your laptop, your teammate's, and GitHub's. And with an agent writing code faster than you can read it, the tests are the shortest honest statement of what the code is supposed to do. Read the tests first.
:::

## The JUnit 5 and AssertJ you need

```java
assertThat(result).containsExactly(1, 2, 5, 9);
assertThat(result).hasSize(4);
assertThat(result).isSorted();
assertThat(result).contains(5).doesNotContain(7);
assertThat(evaluation.getWeek()).isEqualTo("2023-W31");
assertThat(catchThrowable(() -> SelectionSort.sort(null)))
        .isInstanceOf(NullPointerException.class);
```

::: steps
- `@Test` marks a test; `@BeforeEach` gives every test fresh setup.
- `@ParameterizedTest` runs one test body over many rows of input.
- JUnit 5 runs the tests; AssertJ's `assertThat` checks the results, as in Project Pulse.
:::

::: note
**Say:** Two libraries, two jobs. JUnit 5 finds and runs the tests. AssertJ checks the results, and Project Pulse uses it everywhere, so we do too. Every check starts with assertThat of the actual value, then reads like a sentence: contains exactly, has size, is sorted, is equal to. When the right answer is an exception, catchThrowable captures it and you assert on that, the way Project Pulse's tests do. Type a dot after assertThat and IntelliJ lists everything you can check.

@BeforeEach builds fresh objects before each test, so no test depends on another. @ParameterizedTest we'll see in a few minutes.

You'll also see JUnit's own assertEquals in tutorials online. It works, but mixing two styles in one codebase makes tests harder to read. Pick one in your charter; Project Pulse picked AssertJ.
:::

## Project Pulse: a method with a database behind it

```java
public PeerEvaluation addPeerEvaluation(PeerEvaluation newPeerEvaluation) {
    // Make sure the submission week is one of the course section's active weeks and is still open
    requireOpenSubmissionWindow(...);

    // ... the evaluator is on a team, and the evaluator and evaluatee are on the same team ...

    // Make sure this is not a duplicate evaluation
    if (this.evaluationRepository.findByWeekAndEvaluatorIdAndEvaluateeId(
            week, evaluatorId, evaluateeId).isPresent()) {
        throw new PeerEvaluationIllegalArgumentException(
            "You have already submitted an evaluation for ... in this week.");
    }
    return this.evaluationRepository.save(newPeerEvaluation);
}
```

Shortened from `EvaluationService` on Project Pulse `main`.
{: .small }

::: note
**Say:** Now real code. When you submit a peer evaluation in Project Pulse, this method runs. It checks four rules: the week is open, you are on a team, the person you're evaluating is on your team, and you haven't already evaluated them this week. Then it saves.

The problem for testing: the duplicate check asks the database. A unit test that needs a running MySQL isn't a unit test anymore; it's slow, and you have to set up the right rows first. So what do we do?
:::

## Mock the repository

```java
@ExtendWith(MockitoExtension.class)
class EvaluationServiceTest {

    @Mock
    PeerEvaluationRepository evaluationRepository;
    @Mock
    StudentRepository studentRepository;
    @Mock
    Clock clock; // Mock the clock bean

    @InjectMocks
    EvaluationService evaluationService;
```

::: steps
- `@Mock`: a fake whose answers the test controls.
- `@InjectMocks`: the real class under test, handed the fakes.
- `given(mock.call()).willReturn(value)`: "when asked this, answer that".
:::

::: note
**Say:** We replace the repository with a mock: a stand-in object that answers whatever the test tells it to. No database, milliseconds per test. @Mock makes the fakes. @InjectMocks builds the real EvaluationService and hands it the fakes through its constructor. Then given, willReturn scripts an answer.

This only works because the service receives its repository through the constructor. A class that creates its own dependencies can't be handed a mock. That's a design lesson hiding in a testing lesson.
:::

## Given, when, then

```java
@Test
void testAddPeerEvaluationDuplicatedEvaluation() {
    // Given
    PeerEvaluation newPeerEvaluation = new PeerEvaluation("2023-W31", john, eric, ...);
    given(this.evaluationRepository.findByWeekAndEvaluatorIdAndEvaluateeId("2023-W31", 3, 4))
            .willReturn(Optional.of(newPeerEvaluation));

    // When
    Throwable throwable = catchThrowable(
            () -> this.evaluationService.addPeerEvaluation(newPeerEvaluation));

    // Then
    assertThat(throwable)
            .isInstanceOf(PeerEvaluationIllegalArgumentException.class)
            .hasMessage("You have already submitted an evaluation for "
                    + newPeerEvaluation.getEvaluatee().getFirstName() + " in this week.");
}
```

Shortened from `EvaluationServiceTest` (the fixed clock setup is left out).
{: .small }

::: note
**Say:** Every good test has three parts, and Project Pulse writes them as comments. Given: the world before. Here the mock repository says John already evaluated Eric in week 31. When: the one action, John submits again. Then: what must be true. Here, the right exception with the right message.

Write the three comments first, then fill them in. And look at the name: it says the behavior being checked. One behavior per test.

These three parts come straight from your use case. The precondition or the extension's condition is the Given, the step is the When, the outcome is the Then.
:::

## Mock less than you can

::: steps
- Mock the slow and the uncontrollable: database, network, email, the clock.
- Use real objects when they are fast and predictable.
- Assert on results first; check calls only when the call is the outcome.
:::

::: warn
The clock is a dependency too. A test that reads today's date passes this week and fails some other week.
:::

::: note
**Say:** Mocks are powerful, so people overuse them. Google's advice: prefer real objects when they're fast and deterministic. A test full of mocks checks how the code is wired, and it breaks on every refactoring even when behavior didn't change.

Notice the Clock in the mock list two slides ago. Whether the evaluation window is open depends on today's date. Project Pulse injects a Clock, and the tests pin it to August 8, 2023, so they give the same answer next year. Call LocalDate.now directly and your test passes this week and fails in some other one.
:::

## How to pick test cases: partitions

`letterGrade(score)`: 90–100 A · 80–89 B · 70–79 C · 60–69 D · 0–59 F · anything else invalid

::: key
A partition is a group of inputs the code should treat the same way. One test per group.
:::

::: steps
- Seven partitions: A, B, C, D, F, below 0, above 100.
- One input from each: `95` · `85` · `75` · `65` · `30` · `-5` · `120`
:::

::: note
**Say:** You can't test every input, so you choose, on purpose. First idea: partitions. Group the inputs the code should handle the same way, and one input stands for its whole group.

*[Ask: how many groups? Most say five. Wait for someone to find the two invalid ones.]*

Seven: five letters, and two kinds of invalid. The invalid groups are the ones a happy-path list forgets, and the ones an agent forgets unless you ask.
:::

## Boundaries, edges, and corners

::: cols
**Boundaries: both sides of every edge**

`-1, 0` · `59, 60` · `69, 70` · `79, 80` · `89, 90` · `100, 101`
|||
**Corners: the odd shapes**

Empty · one element · all equal · null · huge
:::

::: joke
A QA engineer walks into a bar. Orders a beer. Orders 0 beers. Orders 99999999999 beers. Orders a lizard. Orders -1 beers. The first real customer asks where the bathroom is. The bar bursts into flames.
:::

::: note
**Say:** Second idea: bugs live at the edges. Someone writes greater-than where they meant greater-or-equal, and 90 becomes a B. So test both sides of every edge, including the outer walls.

And corners: the odd shapes. Remember the sort: empty array, one element, all equal. Those are corner cases, and they are where real code crashes.

*[Read the joke.]* Brenan Keller, 2018. The engineer tested every partition and every boundary. Nobody tested the use case. You need both, which is where we go next.
:::

## One test, every boundary

```java
@ParameterizedTest
@CsvSource({ "0, F", "59, F", "60, D", "69, D", "70, C", "79, C",
             "80, B", "89, B", "90, A", "100, A" })
void letterGradeFollowsTheScale(int score, String grade) {
    assertThat(Grades.letterGrade(score)).isEqualTo(grade);
}

@ParameterizedTest
@ValueSource(ints = { -1, 101 })
void letterGradeRejectsScoresOutsideZeroToHundred(int score) {
    assertThat(catchThrowable(() -> Grades.letterGrade(score)))
            .isInstanceOf(IllegalArgumentException.class);
}
```

::: note
**Say:** Here is the whole list as code. A parameterized test runs one body once per row, so every boundary is a row. The invalid side gets its own test, because the right answer there is an exception.

This is exactly what to ask an agent for, and it'll write it in seconds. Your job is to check the list: are the invalid partitions there? Are both sides of every edge there?
:::

## Integration tests: the real thing, wired together

::: steps
- Real Spring, real MySQL in a Docker container, real HTTP requests.
- Each test logs in as a seeded user and calls an API route.
- Each test rolls back, so the next one starts from the same data.
:::

```java
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("dev")
@Tag("integration")
@Transactional
public abstract class AbstractIntegrationTest {
    @ServiceConnection
    static final MySQLContainer<?> mysql = SharedContainers.MYSQL;
```

Shortened from Project Pulse's `AbstractIntegrationTest`.
{: .small }

::: note
**Say:** A unit test checks one class with its dependencies faked. But some rules don't live in one class. Who may call which route is decided by Spring Security. Which rows come back is decided by a SQL query. A mock can't check either, because the mock is exactly the part that got faked.

So Project Pulse has integration tests. Every one extends this class: the whole Spring application starts, a real MySQL runs in a container through Testcontainers, and requests go in through MockMvc as real HTTP. Each test runs in a transaction that rolls back, so the seeded data is the same for the next test. Slower than a unit test, seconds instead of milliseconds, but it tests the system the way it runs.
:::

## Where do the test cases come from?

::: steps
- The use case: every main step and every extension is at least one test.
- The design: it lists the tests, each with its layer, before any code.
- The reminder's design had **20** test rows. Review added **4**, all about time.
:::

::: key
Trace every test back to a use case. A flow with no test was never checked.
:::

::: note
**Say:** Partitions and boundaries tell you how to choose inputs. The use case tells you which behaviors to check at all. This is traceability again, from last week, pointing the other way: every step and every extension of the use case should trace forward to a test.

The reminder you watched being built had twenty test rows in its design before a line of code was written. Then review added four, and all four were about time: a Confirm that lands after Monday midnight, a send that never answers, an instructor who switches items before the list arrives. A list read off the use case's steps misses what happens between them. So read the use case and the design side by side and ask what's not covered.
:::

## Access control: John asks for Eric's peer evaluations

```java
@Test
void testStudentJohnGenerateOwnWeeklyPeerEvaluationSummary() throws Exception {
    this.mockMvc.perform(get(this.baseUrl + "/evaluations/students/4/week/2023-W31")
                    .header(HttpHeaders.AUTHORIZATION, this.studentJohnToken))
            .andExpect(jsonPath("$.code").value(StatusCode.SUCCESS))
            .andExpect(jsonPath("$.data.privateComments").isEmpty()); // privateComments MUST be empty
}

@Test
void testStudentJohnGenerateAnotherStudentsWeeklyPeerEvaluationSummary() throws Exception {
    this.mockMvc.perform(get(this.baseUrl + "/evaluations/students/5/week/2023-W31")
                    .header(HttpHeaders.AUTHORIZATION, this.studentJohnToken))
            .andExpect(jsonPath("$.code").value(StatusCode.FORBIDDEN))
            .andExpect(jsonPath("$.message").value("No permission."));
}
```

Shortened from `EvaluationIntegrationTest`.
{: .small }

::: note
**Say:** My favorite pair in Project Pulse. John is student 4. In the first test he asks for his own weekly summary: success, and the private comments his teammates wrote to the instructor must be empty. In the second he changes one number in the URL, 4 to 5, and asks for Eric's. The answer must be forbidden.

Nobody clicks a button to do that. A curious student edits a URL. The happy-path tests never try it, and the user interface never shows it, which is exactly why it needs a test. And only an integration test can check it, because the rule lives in Spring Security's configuration, not in one class.
:::

## What else may John not do?

::: ask
The use case says students see only their own evaluations. List every request that should be forbidden.
:::

::: steps
- Update another evaluator's evaluation: `testEvaluatorJohnUpdatesAnotherEvaluatorsEvaluation`
- Read another student's detailed evaluations: `testStudentJohnGetDetailedWeeklyPeerEvaluationsOfSingleStudent`
- Generate the whole section's evaluations: `testStudentJohnGenerateWeeklyPeerEvaluationForSection`
- Smuggle another evaluator's rating ids into his own: `testStudentJohnCannotAdoptAnotherEvaluatorsRatingsThroughCreate`
:::

::: note
**Say:** Your turn. Students see only their own peer evaluations. With your neighbor, list every request John could make that should be refused. One minute.

*[Take answers, then reveal one at a time.]*

Every one of these is a real test in Project Pulse, and each reads like a sentence in the use case. The last one is sneaky: a create request that carries rating ids belonging to someone else's evaluation. Nobody would think of it by reading the use case alone. For your own slice, every "only" in your use case, only the instructor, only their own team, is a family of forbidden tests.
:::

## Test coverage

::: key
Coverage shows what ran, not what was checked.
:::

::: cols
**What it is**

The share of lines (or branches) your tests executed.
|||
**What it is for**

Finding code no test touches. Never a score to chase.
:::

::: note
**Say:** Coverage measures how much of your code the tests executed: lines, or better, branches. IntelliJ shows it with Run with Coverage, green and red bars beside each line. Project Pulse doesn't run a coverage tool in its build yet, so IntelliJ is how we look.

Red lines are useful: no test ran them, so no test could catch a bug there. Green lines prove much less than they look. A line that ran is not a line that was checked. Here's the proof.
:::

## 100% coverage, and the rule is checked nowhere

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

::: steps
- The test claims to check "only active weeks get reminders".
- The rule lives in one query, and the test mocks that query.
- Delete the query's condition: this test, and the whole suite, stay green.
:::

::: joke
I mocked the database, the mail server, and the clock. The test passed. So did the bug.
:::

::: note
**Say:** From the reminder, written by the agent. The weekly reminder should only go out for active weeks. This test runs every line of sendWeeklyReminders: one hundred percent coverage.

But which sections get reminded is decided by one database query, findReminderEligibleSectionsForWeek, and the test mocks it. The mock answers whatever we told it. So the activeWeeks line in the Given is decoration, and if you delete the condition from the real query, everything stays green.

The missing test is an integration test: two sections in a real database, one active that week and one not, and only the first comes back. Find where the rule lives, and test it there. The fastest check for any test: break the code once and watch for red.
:::

## End to end: Cypress drives the browser

```javascript
it('sends no reminder when the instructor cancels (5a)', () => {
  openAndChoosePeerEvaluation(owingStatus)

  cy.get('[data-cy=remind-cancel]').click()

  cy.get('[data-cy=remind-dialog]').should('not.be.visible')
  cy.get('@reminders.all').should('have.length', 0)
})
```

From `frontend/cypress/e2e/reminders.spec.cy.js`.
{: .small }

::: steps
- A real browser clicks, types, and reads the page, the way a user does.
- The slowest and most fragile tests, so keep them for what only the browser shows.
- Project Pulse has 19 Cypress tests, and its build does not run them yet.
:::

::: note
**Say:** The top layer. Cypress opens a real browser, logs in, clicks, and checks what's on the screen. This one is the reminder dialog's extension 5a: the instructor clicks Cancel, the dialog closes, and no request was sent. Notice the test name carries the extension number, so it traces straight back to the use case.

These tests are closest to the user and the most expensive: slow, and they break when a button moves. Use them for what only a browser can show: a double click on Confirm, a dialog closing, a list arriving out of order.

Honest note: Project Pulse's CI doesn't run its Cypress tests yet, so they're only as good as someone remembering to run them.
:::

## Three layers, on Project Pulse

| Layer | Checks | Project Pulse |
|---|---|---|
| Unit | One class, dependencies mocked; milliseconds | about 125 |
| Integration | Real Spring, real MySQL, HTTP; seconds | about 320 |
| End to end | The browser and the whole stack; slowest | 19 Cypress, not in CI |

::: key
Find where the rule lives. Test it at that layer.
:::

::: note
**Say:** Put it together. Google aims for about eighty percent unit tests, the classic pyramid. Project Pulse is mostly integration, partly because so many of its rules are about who may see what, and only an integration test exercises those. Neither shape is wrong; know which you have and why.

The rule from today: a rule in one class's logic, unit. A rule in a query or in security, integration. Something only the screen shows, end to end.
:::

## Regression tests: a fixed bug stays fixed

::: steps
- The bug: the report built "Last, First" by splitting the name on a space.
- "Mary Ann Smith" became "Ann, Mary". "Cher" became "undefined, Cher".
- The fix: the server now sends first and last names separately. No test pins the bug.
:::

::: key
Every bug fix comes with a test that fails before the fix and passes after.
:::

::: note
**Say:** A regression is a bug that comes back, usually because someone changed something nearby. Here's a real one from Project Pulse. The peer evaluation report listed missing students as "Last, First", built in the browser by splitting the full name on a space. Mary Ann Smith became "Ann, Mary". A student with one name, Cher, became "undefined, Cher".

The reminder's pull request fixed it: the server now sends first and last names in separate fields. But no test checks a two-word first name, so nothing stops the next change from bringing it back.

The rule: when you fix a bug, first write the test that reproduces it and watch it fail. Then fix, and watch it pass. That test is a regression test, and it stays in the suite forever.
:::

## The suite runs on every pull request

```yaml
on:
  pull_request:
    branches:
      - main
...
      - name: Build and test with Maven
        working-directory: ./backend
        run: mvn --batch-mode package
```

From Project Pulse's `.github/workflows/maven-build.yml`.
{: .small }

::: note
**Say:** Here's why regression tests pay off. Every pull request to main in Project Pulse runs this GitHub Actions workflow, and mvn package runs every unit and integration test, all four hundred and some. Every bug anyone ever wrote a test for is rechecked, for free, on every change. That matters more with an agent: it changes code fast and across many files, and the suite is what tells you it didn't break something it never looked at. We'll go deeper on CI next week.
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
