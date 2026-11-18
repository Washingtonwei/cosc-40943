---
title: Maintainability and Technical Debt
module: maintainability
week: 13
day: Wednesday
---

# Maintainability and Technical Debt

Week 13 · The last lecture: the cost of the next change

::: note
**Say:** Good morning. This is our last lecture. After Thanksgiving the room is yours: you present, I listen. So today is about the thing you will do most in your internship and your first job, and it is not writing new code. It is changing code somebody else wrote. Or code you wrote in a hurry in October, which is the same thing.
:::

## This code works

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

Project Pulse, EvaluationService, at cff8d29

::: note
**Say:** Real code from Project Pulse, on main as of yesterday. When you open your own peer evaluations for a range of weeks, this method lists the weeks. It works. Its test passes. Every report this semester is right. Keep that in mind.
:::

## Now ask it about spring

::: steps
- Ask for 2027-W02 to 2027-W04
- It returns 2027-W03, 2027-W04, 2027-W05
- Every week of 2027 comes back one week late
:::

::: ask
Same code, same test. What changed?
:::

::: note
**Say:** I ran this yesterday. Ask for the second through fourth weeks of 2027 and you get the third through fifth. Every week of next year is off by one, so in the spring every student sees the wrong week's evaluations. Any guesses why? *[Take two or three. Someone may say "locale" or "year boundary".]*
:::

## Two rules for "week 1"

::: cols
**ISO, what Project Pulse stores**

Week 1 is the first week with four days in the new year.
|||
**YYYY-'W'ww, what this code uses**

The server's locale. In the US, week 1 is the week with January 1 in it.
:::

::: key
2026: the rules agree. 2027 starts on a Friday: they disagree all year.
:::

::: note
**Say:** Project Pulse stores ISO week keys. The pattern in this method quietly uses the server's locale. This year the two happen to agree. Next year starts on a Friday, so they disagree by one week, every week. And the test? It uses weeks from 2023, another year where they agree. The test could not see it. That's a partition problem from week 10.
:::

## A classic

::: joke
There are two hard problems in computer science: cache invalidation, naming things, and off-by-one errors.
:::

::: note
**Say:** *[Pause for the laugh.]* This one is literally an off-by-one error. But the off-by-one is not today's lesson. The lesson is how it got there.
:::

## The right rule already existed

```java
/**
 * The one place that turns calendar time into
 * an ISO-8601 week key such as "2026-W40" ...
 */
public final class WeekKeys {
```

Written in October 2026, for the reminders

::: note
**Say:** In October the team wrote WeekKeys. Its own comment says it's "the one place" for week keys. The new reminder code uses it. The old report code was never moved over. So the code had two copies of one rule, and one of them is wrong.
:::

## Where the gap was written down

> Left open: EvaluationService.parseWeekDate/getWeeksBetween not using WeekKeys.

Pull request #102, description, merged October 2026

::: warn
A merged pull request is where debt goes to be forgotten.
:::

::: ask
Who reads a merged pull request's description again?
:::

::: note
**Say:** Somebody knew. It's written right there, in one line of a pull request description. Then the pull request merged. Who goes back and reads merged pull request descriptions? *[Nobody.]* Exactly. That's my pull request, by the way. I'm not proud of it, but it's a good example.
:::

## Last Friday

::: ask
Who got stuck somewhere on Friday?
:::

::: steps
- November 13: every US departure stopped for more than four hours
- 17 of 22 en route centers lose stable radio and radar
- Thousands of flights cancelled over the weekend
- The FAA: a router just installed in El Dorado, Arkansas, flooding the network
:::

::: note
**Say:** Hands up if you were stuck somewhere on Friday. *[Wait. Some of you missed Monday because of this, and that's fine.]* Now scale my week bug up to a country. A router goes in at a remote site in Arkansas, during an upgrade. It starts flooding the network with about a thousand connection attempts every few seconds, and a second new router in Amarillo does the same. Seventeen of the twenty-two centers that guide planes between airports lose stable radio and radar, so the FAA stops everything. Why the routers did that is still under investigation, so we won't guess. We'll talk about what everyone already knew.
:::

## Everyone knew

::: steps
- The copper lines: from the 1960s
- 2009: the same network down five hours, over a misconfigured router
- 2024: 51 of 138 air traffic control systems rated unsustainable, 54 more potentially
- September 2025: DFW and Love Field stopped for five hours
- GAO, September 2026: "buying delivery speed at the risk of ... potential disruptions"
:::

::: key
Debt does not hurt on the day you take it on. It hurts on the day it comes due.
:::

::: note
**Say:** None of this was a surprise. The copper is from the 1960s. The same network went down in 2009 over one misconfigured router. In 2024 the FAA's own review rated more than a third of its systems unsustainable. DFW had its own five-hour stop fourteen months ago, twenty miles from here. And two months before Friday, GAO warned that rushing the upgrade risked disruptions. The day after, the FAA Administrator said agencies had flagged this network as a critical weakness for more than two decades. Everyone knew. And it came due on a Friday afternoon, the worst possible time. That's how debt works.
:::

## It broke while being fixed

::: steps
- The work: copper to fiber, about 70% done
- The change: a new router at a remote site
- The result: a nationwide ground stop
:::

::: key
Paying debt is a change. Changes need tests.
:::

::: note
**Say:** Here's the part I want you to keep. The FAA wasn't ignoring its debt on Friday. It was paying it: the copper replacement everyone had asked for, about 70% done. And the payment is what broke. So carrying debt is dangerous, and paying it is dangerous too, unless you pay in small, tested steps. Hold that thought. We come back to it in twenty minutes with my week bug.
:::

## Not only the FAA

::: steps
- Southwest, December 2022: crew scheduling can't keep up after a storm; more than 16,900 flights
- Its pilots' union, a month before: "one IT router failure away from a complete meltdown"
- Delta, July 2024: a crew-tracking tool can't keep up after CrowdStrike; about $500 million
:::

U.S. Department of Transportation; Delta Air Lines

::: note
**Say:** Airlines show the first lesson inside one company. Christmas 2022, a storm hits everyone; Southwest's crew scheduling can't keep up, and it cancels or delays nearly seventeen thousand flights. A $140 million DOT fine. Then Delta, 2024: the CrowdStrike outage hits every airline, and Delta's crew tracker is the one that can't catch up. Same shape, two companies, two years apart.
:::

## Maintainability

::: key
The cost of the next change.
:::

ISO/IEC 25010: "the degree of effectiveness and efficiency with which a product or system can be modified by the intended maintainers"

::: note
**Say:** So, two terms today. The first is maintainability: how cheaply and safely someone can make the next change. That's the plain version. The formal one is ISO's, on the slide. "The intended maintainers": who are they?
:::

## Who changes your code next?

::: steps
- You, in three months
- A teammate
- Next year's senior design team
- An agent
:::

::: ai
An agent learns your conventions from the code it reads. Two ways of doing one thing: it may copy either.
:::

::: note
**Say:** You in three months counts as a stranger. And the agent is the one people forget. It reads your code to learn how you do things. If there are two week rules, it might copy the wrong one into your next feature. Messy code isn't only slow for humans now. It teaches your agent the wrong habits.
:::

## What makes code cheap to change

| Part | The question | In Project Pulse |
|---|---|---|
| Modularity | Change one feature, touch no other? | MNT-feature-locality |
| Analysability | Find where it lives, and why it fails? | Log lines that name what failed |
| Modifiability | Change it without breaking something? | QS-add-bounded-context: 2 person-days |
| Testability | Check the change quickly? | WeekKeys reads an injected Clock |
| Reusability | One place for each rule? | WeekKeys, and the copy that ignored it |

::: note
**Say:** ISO splits it into five parts. Don't memorize the names. Remember the questions. Project Pulse has a real requirement for the first one, and a measurable scenario for the third: a new feature in two person-days with zero edits elsewhere. Readability sits under all five: a change starts with somebody reading.
:::

## Technical debt

> Shipping first time code is like going into debt. A little debt speeds development so long as it is paid back promptly with a rewrite.

Ward Cunningham, OOPSLA 1992

::: note
**Say:** The second term. Ward Cunningham, who also invented the wiki, came up with it in 1992 to explain to his managers why the team needed time to rework code that already worked. Notice: "a little debt speeds development." He's not against debt. He's against not paying it back.
:::

## Principal and interest

::: cols
**Principal**

The work to fix it.

Week keys: about ten lines.
|||
**Interest**

What every change pays while it stays.

Week keys: everyone must know there are two rules. In 2027, a defect.
:::

::: note
**Say:** The metaphor has two numbers. Principal is the fix. Interest is what you pay every time you touch the code while the debt is still there. For the week keys the principal is tiny. The interest was small too, until it became a bug.
:::

## No interest, no debt

::: ask
A file is messy, nobody has changed it in two months, and nobody plans to. Is it debt?
:::

::: key
Spend your effort where changes happen.
:::

::: note
**Say:** *[Take a vote.]* Kruchten and his coauthors say: if you pay no interest, it's probably not debt. Ugly code that nobody ever touches costs nothing. So don't polish the corners nobody visits. Clean up where the changes happen.
:::

## Debt is not the same as a bug

::: cols
**A bug**

Wrong behavior now.
|||
**Debt**

The next change gets expensive.
:::

The week keys: the debt (two copies of one rule) is what let the bug in.

::: note
**Say:** People mix these up. A bug is wrong behavior today. Debt is about the future cost of change. They're linked: debt is often how bugs get in. Two copies of a rule is debt. The day one copy is wrong, it's a bug.
:::

## Where debt lives

| Kind | Project Pulse |
|---|---|
| Code | Two week rules |
| Architecture | TD-feature-locality: the module rule broken 12 times |
| An assumption | TD-duplicate-scheduler: fine on one server |
| Tooling | 237 SpotBugs, 130 PMD findings baselined; 18 type errors that don't block |
| Dependencies | Tracing silently off after the Spring Boot 4 upgrade |
| Documentation | A "Verified" row whose test no longer exists |

::: note
**Say:** Debt isn't only in code. Every row here is real, from Project Pulse's own debt table or its history. The last one is the sneakiest: a traceability row that says Verified for a test that's gone. That's worse than no row, because people trust it.
:::

## Southwest, in Project Pulse

::: cols
**TD-duplicate-scheduler**

The reminder job runs on every server. One server: fine. Two servers: every student gets every reminder twice.
|||
**Southwest**

Software that kept up with normal days. A storm: it didn't.
:::

::: key
An assumption that is true until the day it isn't. Nothing in the code warns you. Only the record does.
:::

::: note
**Say:** Here's Southwest in miniature, in my own code. The reminder job assumes one server. True today. The day somebody adds a second server to handle load, every student gets two emails every Monday. The code won't warn anyone. The only thing that will is the row in the debt table.
:::

## Not all debt is bad

| | Reckless | Prudent |
|---|---|---|
| **Deliberate** | "We don't have time for tests." | "Ship now, deal with it later." Written down, with the fix. |
| **Inadvertent** | "What's layering?" Or: merging agent code nobody understands. | "Now we know how we should have done it." |

Martin Fowler, Technical Debt Quadrant

::: note
**Say:** Fowler's quadrant. Two questions: on purpose or by accident, careful or careless. Top right is a normal engineering choice, like a mortgage. Project Pulse's scheduler is there. Bottom right is unavoidable: WeekKeys is how the team learned the right rule, and the old copy is what they learned from. The two left boxes are where trouble comes from. Agents add a new one bottom left: merging code nobody on the team understands. Remember cognitive debt from week 8.
:::

## Your MVP will have debt

::: key
That's fine. Debt nobody wrote down is the dangerous kind.
:::

::: note
**Say:** I want to be clear, because some of you are worried right now. Your MVP will carry debt in two weeks. It should; you're shipping on a deadline. Taking on debt on purpose is not a failure. Forgetting you took it is.
:::

## Make it visible: one row

| Column | Week keys |
|---|---|
| ID | TD-week-range-rule |
| Priority | P1: due on a known date |
| Item and impact | Uses the locale's weeks, not WeekKeys; 2027 comes back one week late |
| Fix | Use WeekKeys, delete parseWeekDate |
| Due | Before the first week of 2027 |

Section 11 of your architecture-of-record

::: note
**Say:** Here's where it belongs. Your architecture template has a section 11, Risks and Technical Debt, and Project Pulse keeps the same table. One row per item. The two columns people skip are the ones that matter most: the interest, in one sentence, and the due date.
:::

## Where debt goes to be forgotten

::: steps
- A merged pull request's description
- A TODO comment
- A Slack thread
- A teammate's memory
:::

::: ask
Could someone who never saw the conversation find it next semester?
:::

::: note
**Say:** Here's the test for any record of debt. Could someone who wasn't in the conversation find it next semester? A row in section 11: yes. A GitHub issue linked from that row: yes. My "Left open" line: no. Neither is a TODO in a file nobody opens.
:::

## TODO

::: joke
A TODO comment is a promise written to someone who doesn't work here yet.
:::

::: note
**Say:** *[Beat.]* Try this tonight: search your repository for TODO and look at the oldest one. Some of you will find one the agent wrote, and nobody on the team remembers why.
:::

## Temporary fix {.center}

![A rubber duck labelled "Temporary Fix (DO NOT TOUCH - Oct 2019)" holds up a server rack labelled "Production Environment (Enterprise Grade)"](img/temporary-fix-duck.jpg){ height="520" }

::: note
**Say:** *[Let them laugh.]* Somebody did write this debt down. It has a date. Look what's missing: no owner, no fix, no due date. And "do not touch" is the interest: seven years later, nobody dares change anything near that rack. A record with no owner and no due date is a label, not a register. Source unknown; the creator's watermark is in the image.
:::

## Pay now, carry it, or pay in pieces

::: steps
- How often does this code change? That's the interest rate.
- Is there a due date? A new year, a second server, a launch.
- How big is the principal?
- Does it compound?
:::

::: note
**Say:** You'll never pay off all of it, and you shouldn't try. Four questions. Code that never changes charges almost no interest. A due date sets a deadline. A small fix today can become a week of work once three features sit on top of it. And architecture debt compounds: every feature built on a wrong boundary makes the fix bigger.
:::

## Three decisions

| Item | Due | Principal | Decision |
|---|---|---|---|
| Week range rule | First week of 2027 | Ten lines | Pay now |
| TD-duplicate-scheduler | A second server | A lock library | Carry it, trigger written down |
| TD-feature-locality | None, but compounds | Large | Pay in pieces |

::: note
**Say:** The four questions, applied. The week rule is due soon and costs ten lines: pay it now. The scheduler only comes due if we add a server, and we're not planning to: carry it, but write down the trigger. Feature locality is big and keeps growing: pay a piece at a time, one issue per violation.
:::

## Freeze it so it only shrinks

::: steps
- Record today's violations as a baseline
- Fail the build on any new one
- Pay the old ones down one at a time
:::

ArchUnit's FreezingArchRule; the same idea as your static analysis baseline

::: note
**Say:** One trick worth stealing for your job. Take a snapshot of the violations you have today, and fail the build on any new one. Now the debt can only shrink. You did exactly this with the SpotBugs baseline in week 11. ArchUnit does it for module boundaries.
:::

## Paying it down with an agent

::: steps
- 1. A test that fails first
- 2. Refactor on its own
- 3. Run every gate
- 4. Close the record
:::

::: warn
The risk: "keep the behavior" quietly stops being true.
:::

::: note
**Say:** Paying debt is a refactor: new structure, same behavior. With an agent, the danger is that "same behavior" stops being true and nobody notices, because the agent is fast and sounds sure of itself. Four steps keep it honest. Remember Friday: the FAA was paying its debt when it broke. Let me show you on the week keys. I did this yesterday.
:::

## Step 1: red first

```java
List<PeerEvaluationAverage> averages = this.evaluationService
    .generateEvaluationSummariesForStudent(4, "2027-W02", "2027-W04");
assertThat(averages).extracting(PeerEvaluationAverage::getWeek)
    .containsExactly("2027-W02", "2027-W03", "2027-W04");
```

```text
Expecting actual:   ["2027-W03", "2027-W04", "2027-W05"]
to contain exactly: ["2027-W02", "2027-W03", "2027-W04"]
```

::: note
**Say:** Before I touch the code, I pin the behavior I want. On the old code this fails, and the failure message shows the bug. If your test passes before the fix, it proves nothing about the fix.
:::

## Step 2: one rule, one place

```java
private List<String> getWeeksBetween(String startWeek, String endWeek) {
    List<String> weeks = new ArrayList<>();
    LocalDate lastMonday = WeekKeys.monday(endWeek);
    for (LocalDate monday = WeekKeys.monday(startWeek);
         !monday.isAfter(lastMonday); monday = monday.plusWeeks(1)) {
        weeks.add(WeekKeys.of(monday));
    }
    return weeks;
}
```

3 lines added, 29 removed. No feature in the same pull request.

::: note
**Say:** The fix uses the one place for the rule and deletes the copy. Three lines in, twenty-nine out. That's my favorite kind of diff. And there's no feature in this pull request, so a reviewer can read it as "same behavior, one rule" in two minutes.
:::

## Steps 3 and 4

::: steps
- The new test: green
- The other 566 tests, SpotBugs, PMD: green
- The debt row: closed when the fix merges, linked to the pull request
:::

::: key
A green test only counts if it was red first.
:::

This fix is on my laptop, tested, and not merged into Project Pulse yet.

::: note
**Say:** Then every gate: 567 tests and both analyzers, all green. Last step, the one everybody skips: close the record. Otherwise the debt table drifts from the code, and a stale table is documentation debt. Full disclosure: this fix lives on my laptop. I'm in the middle of other changes to Project Pulse, so it waits its turn. Until it merges, the row stays open. That's not a failure; that's the register telling the truth.
:::

## The prompt

> Read the Risks and Technical Debt table and WeekKeys.java. EvaluationService.getWeeksBetween has its own week rule. First write a test for 2027-W02 to 2027-W04 and show me it failing. Then, and only then, make it use WeekKeys and delete parseWeekDate. Change nothing else. Run ./mvnw verify and show me the result.

::: note
**Say:** Here's the prompt that does all four. Notice three things. It points the agent at the record. It says "show me it failing" before anything changes. And it says "change nothing else," because the agent likes to tidy as it goes, and you saw in week 8 what that does to a review. *[If time allows, run it live on the demo clone; otherwise show the saved run.]*
:::

## Agents and debt

::: steps
- Static analysis warnings: up about 18%
- Code complexity: up about 39%
- Still up after the speed gains faded
:::

Open-source repositories after adopting coding agents. Agarwal, He, and Vasilescu, MSR 2026

::: note
**Say:** One piece of evidence from this year. Researchers at CMU followed open-source projects after they started using coding agents. The speed boost came early and faded. The warnings and complexity went up and stayed up. Agents make adding code nearly free. They don't make noticing an expired assumption any cheaper.
:::

## A new credit limit

::: joke
Coding agents didn't invent technical debt. They just raised your credit limit.
:::

::: note
**Say:** *[Beat.]* Which is fine, if you keep the statements. That's what section 11 is.
:::

## What to give the agent, what to keep

::: cols
**Delegate**

Finding candidates. Explaining unfamiliar code. Drafting a debt row. The refactor, once a red test pins it.
|||
**Keep**

What counts as debt, and its interest. Pay, carry, or pay in pieces. Whether a convention is the right one before the agent spreads it.
:::

::: note
**Say:** The agent is great at finding debt and at the mechanical fix. The judgment stays with you, because "how much does this cost us" is a guess about your client's future, and only you have talked to the client.
:::

## This week, in your team meeting

::: steps
- Find it: ask your agent for candidates; the team decides what's real
- Record it: one row per item in section 11, with interest and due date
- Pay one: the nearest due date, four steps, its own pull request
- Check traceability: every link resolves, every Verified names a passing test
:::

::: note
**Say:** Your homework for the team meeting this week, and it's the schedule's "refactor with the agent" item. Twenty minutes to find debt, then write it down, pay one item, and do an honest pass over traceability.md. Anything you baselined in your pipeline is already supposed to be a section 11 row for Checkpoint 3 on Friday.
:::

## What to take to your first job

::: steps
- Read before you write. Most of the job is changing code you didn't write.
- Write down the shortcuts you take, where the next person will find them.
- Make the next change cheap. That's the job.
:::

::: note
**Say:** *[Instructor's own close goes here: a story from your career, what you hope they carry into internships, and a thank-you for the semester.]* Then: after Thanksgiving, the room is yours. I can't wait to see your demos.
:::
