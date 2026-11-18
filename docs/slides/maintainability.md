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

::: key
2027 starts on a Friday: ISO weeks and the server's locale disagree all year.
:::

::: note
**Say:** I ran this yesterday. Ask for the second through fourth weeks of 2027 and you get the third through fifth. Every week of next year is off by one, so in the spring every student sees the wrong week's evaluations. Any guesses why? *[Take two or three.]* Project Pulse stores ISO week keys: week 1 is the first week with four days in the new year. The pattern `YYYY-'W'ww` quietly uses the server's locale instead, and in the US week 1 is the week with January 1 in it. This year the two agree. Next year starts on a Friday, so they disagree every week. And the test uses weeks from 2023, another year where they agree, so it could not see it. That's the partition lesson from week 10. You know the joke: there are two hard problems in computer science, cache invalidation, naming things, and off-by-one errors. *[Pause.]* But the off-by-one is not today's lesson. The lesson is how it got there.
:::

## The right rule already existed

```java
/**
 * The one place that turns calendar time into
 * an ISO-8601 week key such as "2026-W40" ...
 */
public final class WeekKeys {
```

> Left open: EvaluationService.parseWeekDate/getWeeksBetween not using WeekKeys.

Pull request #102, description, merged October 2026

::: warn
A merged pull request is where debt goes to be forgotten.
:::

::: note
**Say:** In October the team wrote WeekKeys. Its own comment says it's "the one place" for week keys. The new reminder code uses it. The old report code was never moved over, so the code had two copies of one rule, and one of them is wrong. And somebody knew: it's written right there, in one line of a pull request description. Then the pull request merged. Who goes back and reads merged pull request descriptions? *[Nobody.]* Exactly. That's my pull request, by the way. I'm not proud of it, but it's a good example.
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

## Maintainability

::: key
The cost of the next change.
:::

::: steps
- You, in three months
- A teammate
- Next year's senior design team
- An agent
:::

ISO/IEC 25010: "the degree of effectiveness and efficiency with which a product or system can be modified by the intended maintainers"

::: note
**Say:** Two terms today. The first is maintainability: how cheaply and safely someone can make the next change. The formal one is ISO's, at the bottom. "The intended maintainers": who are they? You in three months counts as a stranger. And the agent is the one people forget. It reads your code to learn how you do things. If there are two week rules, it might copy the wrong one into your next feature. Messy code isn't only slow for humans now. It teaches your agent the wrong habits. ISO splits maintainability into five parts (modularity, analysability, modifiability, testability, reusability), and readability sits under all of them, because a change starts with somebody reading. The module has the table. Today, the habits that get you there.
:::

## 1. One place for each rule

```java
// WeekKeys.of: the rule, in its one place
date.get(WeekFields.ISO.weekBasedYear()), date.get(WeekFields.ISO.weekOfWeekBasedYear())

// EvaluationService: the same rule again, wrong in 2027
current.format(DateTimeFormatter.ofPattern("YYYY-'W'ww"))
```

::: ask
If this rule changed tomorrow, how many places would you edit?
:::

::: note
**Say:** ISO says what to aim for. Now five habits that get you there, one class at a time, each with a classic name from object-oriented design. Learn the names: your reviewers and your agent use them, and "this breaks single responsibility" is faster than the paragraph it stands for. Habit one. Don't Repeat Yourself is not about lines that look alike. These two share no code at all. But they answer the same question: which week is this date in? One rule, written twice, and the copies drifted. That's our week bug. And the reverse is fine: a username check and a password check can look identical, because they're two rules that happen to match today.
:::

## 2. One reason to change

```java
public class UserInfo {
    private long userId;
    private String username;
    private String avatarUrl;
    private String email;
    private String telephone;
    private String street, city, state, zipCode;
}
```

::: ask
One job, or three?
:::

::: note
**Say:** Single responsibility: a class should do one job, so it has one reason to change. Martin's version: ask who would ask for it to change. Here's a social app's user. One job, or three? *[Take answers; both sides will show up.]* The honest answer: it depends. If the app only shows profiles, this is one job, and splitting it would just scatter it. Now the app adds shopping: checkout needs a shipping address and a billing address. Then the company adds single sign-on, and login cares about email, phone, and a password. Same class, three needs: profile, checkout, login. A change for any one of them edits the class the other two depend on. Now you split: credentials for login, a list of addresses for checkout. The lesson: the class was right on day one and wrong a year later. Start simple, and split when the second kind of need shows up. If you can't split yet, that's debt: write the row. And don't overdo it: a serializer split into Serializer and Deserializer means one format change edits two classes. That breaks habit 1.
:::

## 3. Add, don't edit

```java
public void check(String api, long requestCount, long errorCount, long durationOfSeconds) {
    long tps = requestCount / durationOfSeconds;
    if (tps > rule.getMatchedRule(api).getMaxTps()) { notification.notify(...); }
    if (errorCount > rule.getMatchedRule(api).getMaxErrorCount()) { notification.notify(...); }
}
```

::: ask
"Also alert when too many requests time out." What do you edit?
:::

::: note
**Say:** Open/closed: a new kind of thing should mean new code, not edits to code that already works. Here's a small API monitor. Two rules: too many transactions per second, too many errors. It works. Then the product manager asks for a third rule: timeouts. *[Ask.]* You add a parameter, so every caller changes. And you add another if to a method that's already tested. Every new rule edits the same method, and every edit can break the rules already in it.
:::

## One class per rule

```java
public interface AlertHandler {
    void check(ApiStatInfo apiStatInfo);
}

public class AlertMonitor {
    private final List<AlertHandler> handlers = new ArrayList<>();
    public void addAlertHandler(AlertHandler h) { handlers.add(h); }
    public void check(ApiStatInfo info) {
        for (AlertHandler h : handlers) { h.check(info); }
    }
}
```

New rule: add a TimeoutAlertHandler, register it. check() never changes.

::: note
**Say:** Same monitor, refactored. Each rule is its own class behind one interface, and the monitor just runs them all. The timeout rule is a new class, registered with one line. The check method and the two old rules aren't touched, so their tests still hold. Not zero edits: the stats object gets a timeout field, and setup registers the new handler. But the logic that already works stays closed. Many design patterns exist to get exactly this; the Gang of Four book from 1994 has twenty-three, and Strategy, Decorator, and Chain of Responsibility are built for it. The name is the point: "make each rule a Strategy" is a whole design in five words, for a teammate or for your agent.
:::

## 4. Ask for what you need

```java
public EvaluationService(PeerEvaluationRepository evaluationRepository,
                         StudentRepository studentRepository,
                         SectionRepository sectionRepository,
                         Clock clock) {
```

Production: the real clock. Dev: August 20, 2023, 11:30 pm. A test: any moment it needs.

::: note
**Say:** Dependency injection sounds fancy. It's this: don't build what you need, ask for it. This service never calls "now". Spring hands it a clock. In production it's the real one; in dev it's frozen in August 2023 to match the sample data; in a test it's whatever you want. You can test New Year's Eve in the middle of July. That's the testability row from the table, built in.
:::

## 5. Build for the change you can see

::: steps
- One alert rule, nobody asking for a second: the if is fine
- The second or third rule arrives: refactor then
- Ask for "extensible" and an agent may build three layers for two options
:::

::: joke
How many design patterns does it take to change a light bulb? A Strategy for the bulb, a Factory to make it, an Observer to tell everyone, and the bulb is a Singleton.
:::

::: note
**Say:** Every habit can be overdone. Each pattern adds classes, and the next reader pays for them. One alert rule doesn't need an AlertHandler interface. When more rules show up, refactor then, with the tests to keep you honest. Agents lean the other way, because pattern-heavy code is everywhere in what they learned from. Your test from the design week still works: name the requirement that needs the flexibility, or leave it out.
:::

## Technical debt

> Shipping first time code is like going into debt. A little debt speeds development so long as it is paid back promptly with a rewrite.

Ward Cunningham, OOPSLA 1992

::: cols
**Principal**

The work to fix it. Week keys: about ten lines.
|||
**Interest**

What every change pays while it stays. Week keys: two rules to know, and in 2027, a defect.
:::

::: note
**Say:** The second term. Ward Cunningham, who also invented the wiki, came up with it in 1992 to explain to his managers why the team needed time to rework code that already worked. Notice: "a little debt speeds development." He's not against debt. He's against not paying it back. The metaphor has two numbers. Principal is the fix. Interest is what you pay every time you touch the code while the debt is still there. Quick vote: a file is messy, nobody has changed it in two months, and nobody plans to. Is it debt? *[Vote.]* Kruchten and his coauthors say no interest, probably no debt: spend your effort where changes happen. And debt is not a bug. A bug is wrong behavior today; debt makes the next change expensive. They're linked: two copies of a rule is debt, and the day one copy is wrong, it's a bug.
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
**Say:** Debt isn't only in code. Every row here is real, from Project Pulse's own debt table or its history. The last one is the sneakiest: a traceability row that says Verified for a test that's gone. That's worse than no row, because people trust it. And look at the assumption row: the reminder job runs on every server. One server, fine. Add a second for load, and every student gets every reminder twice. Nothing in the code warns you. Only the record does.
:::

## Not all debt is bad

| | Reckless | Prudent |
|---|---|---|
| **Deliberate** | "We don't have time for tests." | "Ship now, deal with it later." Written down, with the fix. |
| **Inadvertent** | "What's layering?" Or: merging agent code nobody understands. | "Now we know how we should have done it." |

Martin Fowler, Technical Debt Quadrant

::: key
Your MVP will have debt. That's fine. Debt nobody wrote down is the dangerous kind.
:::

::: note
**Say:** Fowler's quadrant. Two questions: on purpose or by accident, careful or careless. Top right is a normal engineering choice, like a mortgage. Project Pulse's scheduler is there. Bottom right is unavoidable: WeekKeys is how the team learned the right rule, and the old copy is what they learned from. The two left boxes are where trouble comes from. Agents add a new one bottom left: merging code nobody on the team understands. Remember cognitive debt from week 8. And I want to be clear, because some of you are worried right now: your MVP will carry debt in two weeks. It should; you're shipping on a deadline. Taking on debt on purpose is not a failure. Forgetting you took it is.
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

::: joke
A TODO comment is a promise written to someone who doesn't work here yet.
:::

::: ask
Could someone who never saw the conversation find it next semester?
:::

::: note
**Say:** Here's the test for any record of debt. Could someone who wasn't in the conversation find it next semester? A row in section 11: yes. A GitHub issue linked from that row: yes. My "Left open" line: no. Neither is a TODO in a file nobody opens. Try this tonight: search your repository for TODO and look at the oldest one.
:::

## Temporary fix {.center}

![A rubber duck labelled "Temporary Fix (DO NOT TOUCH - Oct 2019)" holds up a server rack labelled "Production Environment (Enterprise Grade)"](img/temporary-fix-duck.jpg){ height="520" }

::: note
**Say:** *[Let them laugh.]* Somebody did write this debt down. It has a date. Look what's missing: no owner, no fix, no due date. And "do not touch" is the interest: seven years later, nobody dares change anything near that rack. A record with no owner and no due date is a label, not a register. Source unknown; the creator's watermark is in the image.
:::

## Pay now, carry it, or pay in pieces

| Item | Due | Principal | Decision |
|---|---|---|---|
| Week range rule | First week of 2027 | Ten lines | Pay now |
| TD-duplicate-scheduler | A second server | A lock library | Carry it, trigger written down |
| TD-feature-locality | None, but compounds | Large | Pay in pieces, and freeze the rest |

::: note
**Say:** You'll never pay off all of it, and you shouldn't try. Four questions. How often does this code change? That's the interest rate. Is there a due date? How big is the principal? Does it compound? Applied: the week rule is due soon and costs ten lines, so pay it now. The scheduler only comes due if we add a server, so carry it, but write down the trigger. Feature locality is big and keeps growing, so pay a piece at a time, one issue per violation. And a trick worth stealing for your job: snapshot today's violations and fail the build on any new one, so the debt can only shrink. You did exactly this with the SpotBugs baseline in week 11; ArchUnit's FreezingArchRule does it for module boundaries.
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
**Say:** Then every gate: 567 tests and both analyzers, all green. Last step, the one everybody skips: close the record. Otherwise the debt table drifts from the code, and a stale table is documentation debt. Full disclosure: this fix lives on my laptop. I'm in the middle of other changes to Project Pulse, so it waits its turn. Until it merges, the row stays open. That's not a failure; that's the register telling the truth. The prompt that does all four steps is in the module, section 4.7: it points the agent at the record, says "show me it failing" before anything changes, and says "change nothing else."
:::

## Agents and debt

::: steps
- Static analysis warnings: up about 18%
- Code complexity: up about 39%
- Still up after the speed gains faded
:::

Open-source repositories after adopting coding agents. Agarwal, He, and Vasilescu, MSR 2026

::: joke
Coding agents didn't invent technical debt. They just raised your credit limit.
:::

::: note
**Say:** One piece of evidence from this year. Researchers at CMU followed open-source projects after they started using coding agents. The speed boost came early and faded. The warnings and complexity went up and stayed up. Agents make adding code nearly free. They don't make noticing an expired assumption any cheaper. *[Joke, beat.]* Which is fine, if you keep the statements. That's what section 11 is.
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
