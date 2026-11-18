# Maintainability and Technical Debt

> **Purpose (one line):** keep the next change cheap: spot technical debt in code you did not write, record it where your team will see it, decide whether to pay it now or carry it, and pay it down safely with an agent.

## 1. Learning objectives

By the end of this module, a student can:

1. Explain maintainability as the cost of the next change, and name what makes code cheap or expensive to change.
2. Describe a piece of technical debt as principal and interest: what fixing it costs, and what every change pays while it stays.
3. Sort debt with Fowler's quadrant, and say which kinds are a normal engineering choice and which are not.
4. Record debt where the next reader will find it: a row in section 11 of your architecture-of-record, not a sentence in a merged pull request.
5. Decide whether to pay a debt now, pay it later, or carry it, from how often the code changes, when the debt comes due, and what it costs to fix.
6. Pay down one debt item with an agent: a test that fails first, a refactor on its own, and the old copy deleted.

## 2. Where it fits

- **Prerequisites:** [Software Architecture, Just Enough](architecture.md), where maintainability is a quality attribute and section 11 of the template holds risks and debt; [Testing](testing.md), because a refactor without a test is a guess; [Static Analysis](static-analysis.md), whose baseline is debt you can count.
- **Leads into:** your MVP demo and the spring semester, when your team (or the next one) changes code written in a hurry this fall.
- **How it's taught:** the Wednesday lecture of week 13, the last lecture of the term. The refactor and the traceability honesty check happen in your team's own meeting time that week.
- **About the examples:** the Project Pulse code is pinned to commit [`cff8d29`](https://github.com/Washingtonwei/project-pulse/tree/cff8d29ea49e403a5ea868de0a2cb953c5c7ba8e) (November 17, 2026).
- **Course outcome it delivers:** [apply static and dynamic analysis and read software metrics to reason about quality, maintainability, and technical debt](../syllabus.md#learning-outcomes) (outcome 5).

## 3. Motivation

Project Pulse lets a student read their own peer evaluations over a range of weeks, and an instructor read any student's. Behind both pages is one method in `EvaluationService` that lists the weeks in the range ([at `cff8d29`](https://github.com/Washingtonwei/project-pulse/blob/cff8d29ea49e403a5ea868de0a2cb953c5c7ba8e/backend/src/main/java/team/projectpulse/evaluation/EvaluationService.java#L271-L301)):

```java
private List<String> getWeeksBetween(String startWeek, String endWeek) {
    List<String> weeks = new ArrayList<>();
    LocalDate startDate = parseWeekDate(startWeek);
    LocalDate endDate = parseWeekDate(endWeek);
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("YYYY-'W'ww");
    LocalDate current = startDate;
    while (!current.isAfter(endDate)) {
        weeks.add(current.format(formatter));
        current = current.plusWeeks(1);
    }
    return weeks;
}
```

It works. Its test passes. Every report in fall 2026 is right.

Now ask it for the weeks `2027-W02` to `2027-W04`. It returns `2027-W03`, `2027-W04`, `2027-W05`. Every week of 2027 comes back one week late, so in the spring semester each student would see the wrong week's evaluations.

Why? Project Pulse stores weeks as ISO week keys, where a week starts on Monday and week 1 is the first week with four days in the new year. The pattern `YYYY-'W'ww` does not use ISO weeks. It uses the server's locale, and in a US locale week 1 is the week that contains January 1. In 2026 the two rules happen to agree. 2027 starts on a Friday, so they disagree by one week all year. The existing test uses weeks from 2023, a year where both rules agree, so it could not see the difference.

Here is the part that makes this a lesson about debt, not about dates. Project Pulse already had the right rule. In October 2026 the team wrote [`WeekKeys`](https://github.com/Washingtonwei/project-pulse/blob/cff8d29ea49e403a5ea868de0a2cb953c5c7ba8e/backend/src/main/java/team/projectpulse/system/WeekKeys.java), whose comment calls it "the one place that turns calendar time into an ISO-8601 week key". The new reminder code used it. The old report code was not moved over, and the gap was written down, in one line of [pull request #102](https://github.com/Washingtonwei/project-pulse/pull/102)'s description: "Left open: `EvaluationService.parseWeekDate`/`getWeeksBetween` not using `WeekKeys`." Once the pull request merged, nobody would ever read that sentence again. The code had two copies of one rule, one of them wrong, and the debt was recorded in the one place guaranteed to be forgotten.

**The same shape, at the scale of a country.** On Friday, November 13, 2026, the FAA stopped every departure in the United States for more than four hours, and thousands of flights were cancelled over the weekend. Seventeen of the 22 centers that guide planes between airports lost stable radio and radar. The FAA has linked it to a router just installed in El Dorado, Arkansas, where a contractor was replacing old copper lines with fiber. With a second new router in Amarillo, it flooded the network with about 1,000 connection attempts every 4 to 5 seconds. Why the routers did that is still under investigation.

The debt was not a secret. The copper lines date from the 1960s. In 2024, the FAA's own assessment rated 51 of its 138 air traffic control systems unsustainable and 54 more potentially unsustainable (GAO-24-107001). The same network went down for five hours in 2009 over a misconfigured router, and in 2010 the Department of Transportation's Inspector General warned that upgrades "could also introduce risks to network operations if not properly planned and managed." Two months before the ground stop, GAO wrote that "the FAA is buying delivery speed at the risk of cost uncertainty and potential disruptions" (GAO-26-107992). North Texas had a preview: on September 19, 2025, DFW and Love Field stopped for about five hours over failing telecommunications, which the FAA called a "clear example of the FAA's outdated infrastructure." The day after the ground stop, the FAA Administrator said agencies had "for better than two decades" flagged this network "as a critical weakness."

There are two lessons here. Carry debt long enough and it comes due, on a bad day. And paying it is a change too: the copper was being replaced, as everyone had asked for years, and the replacement is what failed. That second lesson is why [4.7](#47-paying-it-down-with-an-agent) pays debt in small, tested steps.

Airlines show the first lesson inside one company. In December 2022, Southwest cancelled or delayed more than 16,900 flights and stranded more than 2 million passengers when its in-house crew scheduling software could not keep up with the reassignments after a winter storm (U.S. Department of Transportation). A month earlier, the pilots' union had said the airline was "one IT router failure away from a complete meltdown." The DOT fined Southwest $140 million, on top of about $600 million in refunds. In July 2024, Delta had its own version: after the CrowdStrike outage, a crew-tracking tool "unable to effectively process the unprecedented number of changes" kept Delta cancelling flights for days after other airlines had recovered, at a cost its CEO put at half a billion dollars.

Debt does not hurt on the day you take it on. It hurts on the day it comes due, and that day is usually a bad one.

## 4. Core concepts

### 4.1 Maintainability: the cost of the next change

You will spend more of your first job reading and changing code than writing new code. Someone wrote it before you, and someone will change yours after you. Maintainability is how cheaply and safely that next change can be made. The formal definition is ISO/IEC 25010's: "the degree of effectiveness and efficiency with which a product or system can be modified by the intended maintainers."

Who are the intended maintainers? You in three months, a teammate, next year's senior design team, and an agent. The agent matters more than it seems. It reads your code to learn how you do things, so if a rule is written two ways, it may copy either one.

ISO/IEC 25010 splits maintainability into parts. Each has a plain question and a Project Pulse instance:

| Part | The plain question | In Project Pulse |
|---|---|---|
| Modularity | Can I change one feature without touching the others? | `MNT-feature-locality`: one feature, one package, and no package reads a sibling's repository |
| Analysability | Can I find where a behavior lives and why it fails? | Log lines that name what failed ([Implementation 4.9](implementation.md#49-log-what-the-person-at-2-am-will-need)) |
| Modifiability | Can I change it without breaking something else? | `QS-add-bounded-context`: a new feature in at most two person-days, with zero edits to other features |
| Testability | Can I check the change quickly? | `WeekKeys` reads the date from an injected `Clock`, so a test can pick the day |
| Reusability | Is there one place for each rule? | `WeekKeys`, the one place for week keys, and the copy that ignored it |

**Readability is where all of these start.** Code is read far more often than it is written, and a change begins with someone understanding what is there. Clear names, one way of doing each thing, and short methods are not style points. They are what the next change costs.

### 4.2 Technical debt: principal and interest

Ward Cunningham coined the term in 1992 to explain to his managers why the team needed time to rework code that already worked: "Shipping first time code is like going into debt. A little debt speeds development so long as it is paid back promptly with a rewrite."

The metaphor has two numbers, and both matter:

- **Principal** is the work to fix it. For the week keys, about ten lines.
- **Interest** is the extra cost every change pays while the debt stays. For the week keys, every future developer, and every agent, has to know there are two week rules and pick the right one. In 2027 the interest becomes a defect.

The definition a team can use comes from a 2016 Dagstuhl seminar: technical debt is "design or implementation constructs that are expedient in the short term, but set up a technical context that can make future changes more costly or impossible."

Three consequences, from Kruchten, Nord, and Ozkaya's principles of technical debt:

- **If you pay no interest, it is probably not debt.** Ugly code that nobody will ever change costs nothing. Spend your effort where changes happen.
- **Debt is not the same as bad quality.** A bug is wrong behavior now. Debt is what makes the next change expensive. The week keys show the link: the debt (two copies of one rule) is what let the bug in.
- **Architecture debt costs the most.** A wrong week rule is ten lines. A wrong boundary between modules touches every change near it.

### 4.3 Where debt lives

Debt is not only in code. Here is where Project Pulse carries it, from its own [Risks and Technical Debt](https://github.com/Washingtonwei/project-pulse/blob/main/docs/design/architectural-design.md#risks-and-technical-debt) table and its history:

| Kind | Project Pulse example | The interest |
|---|---|---|
| Code | Two week rules, one ignoring `WeekKeys` | Every reader has to know which to use; wrong weeks in 2027 |
| Architecture | `TD-feature-locality`: the code breaks `MNT-feature-locality` 12 times (sibling repository reads, three dependency cycles in the requirements module) | A schema change in one feature can break its siblings |
| A deployment assumption | `TD-duplicate-scheduler`: the reminder job runs on every server | Fine on one server; the day someone adds a second, every student gets every reminder twice |
| Tooling | `TD-analyzer-baselines`: 237 SpotBugs and 130 PMD findings accepted untriaged; 18 frontend type errors that do not block a merge | A new type error merges unnoticed |
| Dependencies | After the Spring Boot 4 upgrade, tracing was silently off until [#112](https://github.com/Washingtonwei/project-pulse/pull/112) | Nobody could trace a request, and nothing said so |
| Documentation | A traceability row that says `✅ Verified` for a test that no longer exists | Worse than no row: people trust it |

Look at `TD-duplicate-scheduler` next to Southwest. Both are an assumption that was true when the code was written (one server, a manageable number of reassignments) and stays true until the day it is not. Nothing in the code warns you. Only the record does.

### 4.4 Not all debt is bad: Fowler's quadrant

Martin Fowler sorts debt along two questions: did you take it on purpose, and did you take it carefully?

| | **Reckless** | **Prudent** |
|---|---|---|
| **Deliberate** | "We don't have time for tests." | "We must ship now and deal with the consequences." Project Pulse runs one server, knows the scheduler would double-send on two, and wrote that down with the fix (`TD-duplicate-scheduler`). |
| **Inadvertent** | "What's layering?" With an agent: accepting code nobody on the team understands ([cognitive debt](implementation.md#46-size-the-step-to-the-review)). | "Now we know how we should have done it." Writing `WeekKeys` during #102's review is how the team learned the ISO rule. The old copy is what they learned from. |

Deliberate, prudent debt is a normal engineering choice, the same way a mortgage is a normal financial one. Your MVP will carry some, and it should. The other three boxes are where trouble comes from. Inadvertent, prudent debt is unavoidable, because you learn by building; what matters is that you write it down the day you learn it.

### 4.5 Make it visible

Debt nobody can see does not get paid. Project Pulse's architecture-of-record keeps one table of risks and debt, and your template has the same slot: section 11, "Risks and Technical Debt." One row per item:

| Column | What to write | Week keys example |
|---|---|---|
| ID | `TD-<slug>` | `TD-week-range-rule` |
| Priority | P0 (fix now) to P3 (low) | P1: it comes due on a known date |
| Item and impact | What it is, and the interest in one sentence | `getWeeksBetween` uses the locale's weeks, not `WeekKeys`; every week of 2027 comes back one late |
| Fix | The principal | Use `WeekKeys.monday` and `WeekKeys.of`; delete `parseWeekDate` |
| Due | The trigger, if there is one | Before the first week of 2027 |

**Where debt goes to be forgotten:** a merged pull request's description, a `// TODO` comment, a Slack thread, a teammate's memory. Test any record with one question: could someone who never saw the conversation find it next semester? A row in section 11 passes. A GitHub issue linked from the row passes. "Left open:" in a merged pull request does not.

![A rubber duck labelled "Temporary Fix (DO NOT TOUCH - Oct 2019)" holds up a server rack labelled "Production Environment (Enterprise Grade)"](../slides/img/temporary-fix-duck.jpg)

Someone did write this debt down, with a date. It has no owner, no fix, and no due date, and "do not touch" is the interest: years later, nobody dares change anything near that rack. A record without an owner and a due date is a label, not a register. (Source unknown; the creator's watermark is in the image.)

### 4.6 Pay now, pay later, or carry it

You will never pay off all of it, and you should not try. Four questions decide each item:

1. **How often does this code change?** That is the interest rate. Code nobody touches charges almost nothing.
2. **Is there a due date?** A known trigger (a new year, a second server, a client's launch) sets the deadline.
3. **How big is the principal?** Ten lines today can be a week of work after three more features are built on top.
4. **Does it compound?** Architecture debt grows with every feature that depends on the wrong boundary.

Applied to three Project Pulse items:

| Item | Changes often? | Due date | Principal | Decision |
|---|---|---|---|---|
| Week range rule | Rarely | First week of 2027 | Ten lines | **Pay now**, before the date |
| `TD-duplicate-scheduler` | Rarely | Only when a second server is added | A lock library or leader election | **Carry it**, with the trigger written down |
| `TD-feature-locality` | Every change in the requirements module | None, but it compounds | Large | **Pay in pieces**, one open issue per violation, and freeze the rest with a test so no new violation merges |

That last move is worth stealing. An architecture test such as ArchUnit's `FreezingArchRule` records today's violations as a baseline and fails the build on any new one, so the debt can only shrink. It is the same idea as a static analysis baseline ([Static Analysis](static-analysis.md)), applied to your module boundaries.

### 4.7 Paying it down with an agent

Paying debt is a refactor: change the structure, keep the behavior. It is also a change, and changes break things; the FAA's ground stop in the [motivation](#3-motivation) happened while the debt was being paid. With an agent, the risk is that "keep the behavior" quietly stops being true, because the agent edits fast and confidently. Four steps keep it honest, shown on the week keys:

**1. Write a test that fails first.** Pin the behavior you want before touching the code:

```java
@Test
void testGenerateEvaluationSummariesForStudentUsesIsoWeeksIn2027() {
    // 2027 begins on a Friday, so its ISO weeks and the JVM locale's weeks are numbered one apart
    ...
    List<PeerEvaluationAverage> averages = this.evaluationService.generateEvaluationSummariesForStudent(4, "2027-W02", "2027-W04");
    assertThat(averages).extracting(PeerEvaluationAverage::getWeek).containsExactly("2027-W02", "2027-W03", "2027-W04");
}
```

On the old code it fails with `["2027-W03", "2027-W04", "2027-W05"]`. A test that passes before the fix proves nothing about the fix.

**2. Refactor on its own.** Use the one place for the rule and delete the copy:

```java
private List<String> getWeeksBetween(String startWeek, String endWeek) {
    List<String> weeks = new ArrayList<>();
    LocalDate lastMonday = WeekKeys.monday(endWeek);
    for (LocalDate monday = WeekKeys.monday(startWeek); !monday.isAfter(lastMonday); monday = monday.plusWeeks(1)) {
        weeks.add(WeekKeys.of(monday));
    }
    return weeks;
}
```

Three lines added, twenty-nine removed, and no feature in the same pull request. A reviewer can then read it as "same behavior, one rule" instead of untangling a refactor from a feature ([Implementation 4.6](implementation.md#46-size-the-step-to-the-review): propose a refactor first, then make it alone).

**3. Run every gate.** The new test passes, and so do the other 566 tests and the SpotBugs and PMD gate (checked on Project Pulse, November 17, 2026). A green test only counts if it was red first.

**4. Close the record.** Mark the debt row closed, or delete it and link the pull request from the issue. Otherwise the register drifts from the code, and a stale register is the documentation debt from [4.3](#43-where-debt-lives).

A prompt that does all four:

> Read `docs/design/architectural-design.md`, Risks and Technical Debt, and `system/WeekKeys.java`. `EvaluationService.getWeeksBetween` has its own week rule instead of using `WeekKeys`. First write a test in `EvaluationServiceTest` that asks for 2027-W02 to 2027-W04 and show me it failing. Then, and only then, make `getWeeksBetween` use `WeekKeys` and delete `parseWeekDate`. Change nothing else. Run `./mvnw verify` and show me the result.

## 5. The AI-native lens

- **Delegate to AI:** finding candidates ("list every place that turns a date into a week key"), explaining unfamiliar code before you change it, drafting a debt row, and the mechanical refactor once a failing test pins the behavior.
- **Keep human:** what counts as debt and how much interest it charges, which is a judgment about the future of your client's product; the pay, carry, or pay-in-pieces decision; and whether a convention is the right one before the agent spreads it.
- **Context to supply:** the debt register itself, the "one place" for each rule (`WeekKeys` says so in its own comment, which is context the agent can read), and the instruction to change nothing else.
- **How to verify:** the test was red before and is green after; the diff touches only what the debt row names; the analyzer counts did not go up.

Why this matters more now: agents make adding code nearly free, and they do not make noticing an expired assumption any cheaper. A 2026 study of open-source repositories that adopted coding agents found static analysis warnings up about 18% and code complexity up about 39%, and those increases did not fade even after the speed gains did (Agarwal, He, and Vasilescu, MSR 2026). Fast code with no record of its shortcuts is how a team ends up with Southwest's problem on a smaller scale.

## 6. Risks & mitigations

| Risk (classic + AI-introduced) | Human judgment that catches it | Mitigation |
|---|---|---|
| Debt recorded only where it will be forgotten (a pull request description, a `TODO`, a chat) | "Could someone who never saw this conversation find it?" | A row in section 11 of the architecture-of-record, with an issue for anything you plan to pay |
| The agent "tidies up" inside a feature pull request, so a behavior change hides in a refactor | The reviewer asks which lines are the feature | Refactors go in their own pull request, proposed first |
| "Let the agent rewrite the module": a big rewrite with no test pinning the old behavior | Asking what proves the behavior is the same | Tests first, small steps, and a freeze rule so new debt cannot merge while old debt is paid |

## 7. Hands-on (studio + optional individual assignment)

**Studio (team, own project)**

- **Goal:** know your debt, write it down, and pay one item before the MVP demo.
- **In your team's meeting this week:**
    1. **Find it (20 minutes).** Ask your agent to list debt candidates in your repository: duplicated rules, `TODO` comments, checks on `continue-on-error`, baselined findings, assumptions that hold only for your demo (one server, one client, test data). The team decides which are real.
    2. **Record it.** One row per real item in section 11 of your architecture-of-record, with its interest in one sentence and its due date if it has one.
    3. **Pay one.** Pick the item with the nearest due date, and run [4.7](#47-paying-it-down-with-an-agent)'s four steps as its own pull request.
    4. **Check the traceability matrix honestly.** Every link resolves, and every `✅ Verified` names a test that exists and passes. A stale row is debt too.
- **Adapt to your stack:** the steps are the same in any language; only the test runner and the gate change. Run the [adapt step](../studio.md#adapt) if your project is not Java.
- **Deliverable & assessment:** the debt rows and the refactor pull request, in your repository. Anything you baselined or left out of your pipeline is already a section 11 row at [Checkpoint 3](../project.md#checkpoint-3-checklist).

**Individual assignment (Project Pulse)**: none.

## 8. Summary / key takeaways

- Maintainability is the cost of the next change, and the next person to make it may be an agent that copies whatever it finds.
- Technical debt has principal (the fix) and interest (what every change pays). No interest, no debt.
- Deliberate, prudent debt is a normal choice. Debt nobody wrote down is the dangerous kind.
- Record debt in section 11 with its interest and its due date, never only in a merged pull request.
- Pay it with a test that fails first, a refactor on its own, and the record closed.

## 9. Key papers & further reading

- Ward Cunningham, "The WyCash Portfolio Management System," OOPSLA 1992 experience report. The origin of the metaphor, in two pages.
- Martin Fowler, ["Technical Debt Quadrant"](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html) (2009) and ["Technical Debt"](https://martinfowler.com/bliki/TechnicalDebt.html).
- Philippe Kruchten, Robert Nord, and Ipek Ozkaya, *Managing Technical Debt: Reducing Friction in Software Development*, Addison-Wesley, 2019. The principles in [4.2](#42-technical-debt-principal-and-interest).
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall, 2004. How to put tests around code you are afraid to change.
- Shyam Agarwal, Hao He, and Bogdan Vasilescu, ["AI IDEs or Autonomous Agents? Measuring the Impact of Coding Agents on Software Development"](https://doi.org/10.1145/3793302.3793589), MSR 2026.
- U.S. Government Accountability Office, ["Air Traffic Control Systems: Ambitious New Modernization Effort Needs to Improve Cost and Schedule Planning"](https://www.gao.gov/products/gao-26-107992), GAO-26-107992, September 2026. The copper lines, the 51 of 138, and the warning two months before the ground stop.
- U.S. Department of Transportation, the December 18, 2023 consent order with Southwest Airlines over the 2022 holiday disruption.
- [Project Pulse's Risks and Technical Debt table](https://github.com/Washingtonwei/project-pulse/blob/main/docs/design/architectural-design.md#risks-and-technical-debt), a real register to copy the shape from.

## 10. Self-check

1. A file in your project is messy but nobody has changed it in two months, and nobody plans to. Is it technical debt? What would make it debt?
2. Name the principal and the interest of `TD-duplicate-scheduler`. Why is "carry it" a reasonable decision, and what must be written down for it to stay reasonable?
3. The old week code had a test, and the test passed. What was wrong with the test, and which partition from [Testing](testing.md) would have caught it?
4. Place each in Fowler's quadrant: (a) "We'll add input validation after the demo," written in your debt table; (b) your agent added a second date-parsing helper because it did not find the first; (c) skipping code review all week to hit Checkpoint 3.
5. Your agent opens a pull request that fixes a bug and also "cleans up" three unrelated files. What do you ask for, and why?

## Related

- [Software Architecture, Just Enough](architecture.md): maintainability as a quality attribute, and section 11 of the template.
- [Static Analysis](static-analysis.md): a baseline that only shrinks is debt you can count.
- [Requirements Traceability](traceability.md): why a stale matrix is worse than none.
- [AI-Assisted Implementation](implementation.md): cognitive debt, and proposing a refactor before making it.
- [Senior Design Project](../project.md): the Checkpoint 3 checklist.
- [Schedule](../schedule.md): when this is taught.
