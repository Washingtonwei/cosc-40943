# AI-Assisted Implementation

> **Purpose (one line):** _to be written when authored._


!!! note "This module is still being written"
    The course is being revamped this term, so modules go up as they are written rather than all at once. What is here is usable; the rest is coming. Lectures and studio do not depend on the missing parts.

## Drafting notes (raw: distribute into template sections, then delete before `stable`)

### Logging: students do not log, and the running example taught them not to

**Code facts.** Project Pulse, `main` at `3a8c4688`, verified 2026-09-10. Re-check before `stable`, and quote the code in the module rather than linking the file, because the fix below changes `main`.

- A logger appears in **2 of 266** backend classes, under two names. `AuthController` declares `LOGGER` and logs once, at debug. `DocumentTemplateRegistry` declares `log` and uses info, debug, warn, and error. There is no `System.out.println` or `printStackTrace` anywhere: the codebase does not log badly, it mostly does not log.
- `system/exception/ExceptionHandlerAdvice.handleOtherException(Exception ex)` is the catch-all. It returns a 500 with `ex.getMessage()` in the body and logs nothing. Spring does not log an exception that an `@ExceptionHandler` has resolved (`spring.mvc.log-resolved-exception` defaults to false), so an unexpected `NullPointerException` in production leaves no stack trace anywhere. The client sees "A server internal error occurs." The operator, and the agent asked to debug it, see nothing. Returning the raw exception message to the client is also a disclosure issue for `MODULE-security`.

**The lesson is not "import `Logger`".** `System.out.println` in a container already reaches the Azure log stream. The lesson is deciding, while writing the code, what the person debugging it at 2 AM will need.

**The AI angle runs in two directions.**

- The agent imitates the code it can see, the same mechanism as the week 2 "reviewee" example in `MODULE-ai-augmented-team`. In a codebase that barely logs, it writes code that does not log.
- Asked to "add logging", it can log everything, request bodies included. In Project Pulse those carry peer evaluations and student records (`CO-ferpa`). Review what was logged, not only whether something was.

**Week 8 half (this module): the rule.** One short section. SLF4J as the API. The four levels and what each is for. Parameterized messages (`log.info("Loaded {} templates", count)`), not string concatenation. Log with the exception object in every catch block that does not rethrow. Never log secrets, tokens, passwords, or student data. Teams write the rule into their agent charter, so the agent logs on every use case from the first week of fan-out. Worked example: the catch-all handler above, before and after.

**Why week 8 and not only week 12.** Fan-out begins in week 8. Taught only in week 12, logging arrives after five weeks of code written without it, and Checkpoint 3 asks for "observability in place" on the Friday of the same week observability is taught.

**Hand-offs.** Move each into its module when that module is authored.

- `MODULE-static-analysis` (week 10): PMD's `SystemPrintln` and `AvoidPrintStackTrace` flag bad logging in student code. No analyzer flags missing logging, so that stays a review item for `MODULE-code-review`.
- `MODULE-observability` (week 12): reading logs, changing a level at runtime through Actuator `/loggers`, correlation IDs with MDC, structured output (Spring Boot's `logging.structured.format.console`), and handing the log to the agent when debugging.

**Assignments.**

- *Hunt the bug* (assignment 5, Fri Nov 20) already says "using logs, traces". Plant the bug so it surfaces as a 500 through the silent catch-all. The student localizes it, fixes it, adds the regression test, and adds the log line that would have localized it. The test stops the bug coming back; the log line localizes the next one nobody knows about yet. No sixth assignment.
- Optional: *Add a use case* (assignment 3, Fri Oct 16) is also graded against the logging rule, as a light week 8 touch.
- **Blocking for assignment 5:** fix logging in Project Pulse `main` before the `hunt-the-bug` upstream is stamped, or there are no logs to hunt with. Quote the current handler into this module first. Course status open item 17 (the planted bug is discoverable by `git diff`) still applies.

### The first test: given, when, then, read off the use case

**Why week 8.** Tests are used before they are taught. The week 8 studio ends at "trace it design to code to first test", and *Add a use case* (assignment 3, Fri Oct 16) asks for vetted AI-generated tests, both before `MODULE-testing` on Wed Oct 21. This module teaches enough to write the first test; week 9 owns the judgment.

**Frame: the use case is the scenario.** BDDMockito's `given`/`willReturn` is the vocabulary of behavior-driven development, not the practice. BDD proper writes Given/When/Then scenarios with the stakeholder and runs them with a tool such as Cucumber. The course already has that half: the use case template's trigger, `PRE-n`, `POST-n`, and extensions. Teach given/when/then as the executable form of a use case, and do not add Cucumber.

| Use case | Test |
|---|---|
| `PRE-n`, or the precondition an extension breaks | Given |
| Trigger or step | When |
| `POST-n`, or the extension's outcome | Then |

**Worked example: extension 1a of `UC-WAR-manage-activities`** (Project Pulse `docs/requirements/use-cases.md`). `PRE-2`: the student is assigned to a team (`BR-team-assignment-required`). Extension `1a1`: the system does not accept the activity and tells the student she must be assigned to a team. `ActivityServiceTest.testSaveActivityRejectsASubmitterWithNoTeam` tests exactly that against `ActivityService.saveActivity`. Rewritten in BDD form throughout:

```java
@Test
void testSaveActivityRejectsASubmitterWithNoTeam() {
    // Given: PRE-2 does not hold (extension 1a)
    Student tracy = new Student("t.nicholson@abc.edu", "Tracy", "Nicholson", "t.nicholson@abc.edu", "123456", true, "student");
    given(this.userUtils.hasRole("ROLE_student")).willReturn(true);
    given(this.userUtils.getStudent()).willReturn(tracy);

    // When
    Throwable thrown = catchThrowable(() -> this.activityService.saveActivity(new Activity()));

    // Then: 1a1, the activity is refused and nothing is saved
    assertThat(thrown)
            .isInstanceOf(ActivityIllegalArgumentException.class)
            .hasMessage("You must be assigned to a team before submitting a weekly activity report.");
    then(this.activityRepository).should(never()).save(any(Activity.class));
}
```

Two changes from the repository version, both worth a slide: `catchThrowable` separates When from Then, where the original wraps both in one "When and then" block around `assertThatThrownBy`; and `then(...).should(never())` replaces `verify(...)`. Imports: `org.mockito.BDDMockito.*`, which carries `never` and `any`, plus AssertJ's `assertThat` and `catchThrowable`. Studio: pick one extension from a use case your team wrote and write its test in this shape.

**Project Pulse writes half of it.** Across the 14 test files that import BDDMockito: `given(...)` 194 times and `when(...).thenReturn` never; `verify(...)` 22 times in 10 files and `then(...).should(...)` never; `doNothing().when(...)` 11 times and `willDoNothing()` never. The cause is one line. The testing section of `backend/CLAUDE.md` says only "Use BDDMockito: given(...).willReturn(...)", so the agent follows the convention for Given and falls back to classic Mockito for Then. Same mechanism as the logging gap above. Teams write both halves into their own agent charter.

**Two slide notes.** `doNothing()` on a void method of a mock is redundant, because doing nothing is already the default. AssertJ's `BDDAssertions.then` and BDDMockito's `then` collide when both are statically imported; use AssertJ's `assertThat` with BDDMockito's `then`.

**Hand-off.** `MODULE-testing` (week 9) takes the happy-path twin of this test, `testSaveActivity`, as its oracle example, and assumes students already write given/when/then from a use case.
