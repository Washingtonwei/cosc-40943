# Static Analysis

> **Purpose (one line):** use analyzers to catch, before anyone reviews or runs the code, the bugs a machine can find: triage what they report, make them a gate on every pull request (from the first commit on a new project, behind a shrinking baseline on an old one), and hold the agent's code to the same bar.

## 1. Learning objectives

By the end of this module, a student can:

1. Explain, from Rice's theorem, why every analyzer has false positives or false negatives, and where static analysis sits beside testing and code review.
2. Name what each rung of the analysis ladder catches (compiler, formatter, linter, null types, dataflow, dependencies, containers, secrets), how it reads the code, and the tool for each on a Spring Boot and Vue project.
3. Run SpotBugs, PMD, and ESLint on an unfamiliar codebase without changing its build, and read the results by rule before reading them by file.
4. Triage a finding as real, false positive, or not worth fixing, and record the verdict where the next reader will see it: a fix, a suppression with a written reason, or a rule turned off for the whole project.
5. Make analyzers a gate on the pull request: before the first feature on a new project, and with a baseline that only shrinks on an existing one.
6. Turn a team convention into a custom rule, and test it with one example it must flag and one it must pass.
7. Use analyzers as the deterministic gate on agent-written code, and say what an agent may and may not decide about a finding.

## 2. Where it fits

- **Prerequisites:** [AI-Assisted Implementation](implementation.md), whose agent writes the code these tools check; [Code Review](code-review.md), which reviews what the tools cannot; [Testing](testing.md), the dynamic half of verification.
- **Leads into:** CI/CD (Wednesday of the same week), which runs these checks on every pull request; dynamic analysis (week 12), which watches the program run; metrics and technical debt, where a baseline is debt you can count.
- **How it's taught:** Monday of week 11, with live runs on Project Pulse. Friday's studio puts the checks in your team's pipeline. Practised alone in *Triage the analyzers* (assignment 4).
- **About the examples:** every Project Pulse example is the project as it stood in fall 2026, at commit [`90668c5`](https://github.com/Washingtonwei/project-pulse/tree/90668c51b83f5352acf8d0f304a46590625cc87c), and every code link is pinned to that commit. Project Pulse has fixed some of what you see here since; the findings still teach.
- **Course outcome it delivers:** [build, test, and ship a working MVP](../syllabus.md#learning-outcomes) (outcome 4), and verifying AI output without lowering the bar (outcome 6).

## 3. Motivation

Here is a method from Project Pulse, the running example of this course, as it stood in fall 2026 ([`ActivityController`](https://github.com/Washingtonwei/project-pulse/blob/90668c51b83f5352acf8d0f304a46590625cc87c/backend/src/main/java/team/projectpulse/activity/ActivityController.java#L66-L72)):

```java
public Result addActivityComment(@PathVariable Integer activityId, @RequestBody Map<String, String> commentMap) {
    String comment = commentMap.get("comment");
    Activity updatedActivity = this.activityService.addActivityComment(activityId, comment);
    ActivityDto updatedActivityDto = this.activityToActivityDtoConverter.convert(updatedActivity);
    return new Result(true, StatusCode.SUCCESS, "Add comment successfully", null);
}
```

It compiled, and it sat on `main` from Project Pulse's first commit in October 2024 into fall 2026. Look at the fourth line: the method converts the activity to a DTO, then never uses it, and returns `null` instead. Was the DTO supposed to be returned? Two tools noticed in seconds, without running a single test: SpotBugs reported a "dead store," and PMD an "unused local variable."

That is **static analysis**: a program that reads your code without running it and points at likely mistakes. You have probably seen one already without knowing the name:

| Where you saw it | The analyzer |
|---|---|
| A gray "variable is never used" in IntelliJ or VS Code | The IDE's inspections |
| A red squiggle in a JavaScript file | ESLint |
| "Object is possibly 'undefined'" | The TypeScript compiler |
| An email from GitHub about a vulnerable library, or a "Code scanning" alert | Dependabot, CodeQL |
| A pull request blocked by a "quality gate" at your internship | SonarQube |

An unused variable is the small end. The same idea finds a user's input flowing into a SQL query, a password committed to GitHub, or a library with a known security hole.

**So why doesn't everyone run them all the time?** They add no feature. Setting one up takes an afternoon, and the first run on an existing project usually prints hundreds of warnings, most about code that works. Developers often give up on the tools because of that noise (Johnson et al., 2013).

**Because some mistakes are too boring for people to catch.** In 2014, Apple's code for checking secure connections had one line accidentally copied twice: `goto fail;`. The copy made the program skip the security check, so an attacker could pretend to be any secure website, your bank included. The mistake sat in plain sight, and it shipped on millions of iPhones and Macs. People miss this kind of thing because their eyes slide over it. A tool does not get bored. The compiler even had a warning for exactly this mistake; it just was not among the warnings people usually turn on.

It is not only Apple. In fall 2026, every Project Pulse deploy shipped 18 type errors. Its type checker had been there since the first commit, but the [deploy workflow](https://github.com/Washingtonwei/project-pulse/blob/90668c51b83f5352acf8d0f304a46590625cc87c/.github/workflows/azure-webapps-deploy.yml#L35) skipped it, and since nothing ever failed, nobody noticed.

**AI makes this matter more.** An agent writes code faster than you can read it, and it makes these mistakes too: when Veracode tested more than 100 AI models in 2025, 45% of the code they wrote failed its security tests. The good news is that an agent is also good at the tedious part. When the tool flags a mistake, the agent can fix it and run the check again, without you. The need for static analysis went up just as its cost went down.

So let the tool catch the boring mistakes before any person looks at the code. Static analysis runs first because it is cheap and fast, and it does not need the program running. If a cheap check can reject a change, there is no reason to spend ten minutes on tests or an hour of a reviewer's time. That is "fail fast." It is an order of cost, not of importance: the question only people can judge, does this code do what the client needs?, matters most, which is why it gets your attention once the machines are done.

## 4. Core concepts

### 4.1 What a static analyzer can and cannot tell you

**Static analysis, testing, and code review look for different problems.** You have done the other two; here is where the third fits:

| | Asks | Catches | Cannot see | The story you know |
|---|---|---|---|---|
| **Static analysis** | Does any path break a known rule? | Mechanical defects on every path, run or not | What the code is for | goto fail ([section 3](#3-motivation)) |
| **Testing** | Does it do what we checked, on the inputs we ran? | Wrong behavior on the paths you exercise | Cases nobody wrote | CrowdStrike: every test passed ([Testing](testing.md#3-motivation)) |
| **Code review** | Is this what the use case asks for, built the way we agreed? | Missing behavior, design, the contract | Line 600 of a tired afternoon | Heartbleed: reviewed and merged ([Code Review](code-review.md#3-motivation)) |

The machines run first, because they are cheapest ([section 3](#3-motivation)), and that is what makes the gate a productivity tool: it lets you read an agent's 800-line pull request for intent, not for null checks.

**Every path, but only approximately.** A test checks the paths it executes; a static analyzer reasons about every path, including the ones no test reaches. It cannot do that exactly, and you already know why. Whether a program can ever reach a given line is undecidable, because the halting problem reduces to it, and **Rice's theorem** generalizes the result: every nontrivial question about what a program does ("can this dereference null?", "can this input reach that query?") is undecidable. An analyzer that always finishes must therefore approximate, and every approximation errs in one direction or the other:

| Error | What it is | What it costs | In theory terms |
|---|---|---|---|
| **False positive** | A warning about code that is fine | Time, and trust: a team that sees enough of them stops reading warnings | The tool is not *complete* |
| **False negative** | A real bug the tool says nothing about | A clean report is not a proof of safety | The tool is not *sound* |

No useful analyzer is both sound and complete; most are neither, and tune the balance for the people reading the report. A tool that claimed to be both would be claiming to solve the halting problem.

**Heartbleed beat the analyzers too.** Coverity, one of the best commercial analyzers, did not flag it ([Code Review](code-review.md#3-motivation)). The reviewer's hole and the analyzer's hole lined up, which is the Swiss cheese model in one bug.

**Trust is the scarce resource.** Google's static analysis team found that developers act on a tool only if most of what it says is worth acting on, and set a target of under 10% *effective* false positives: warnings the developer does not act on, whatever the tool thinks (Sadowski et al., 2018). Interviews at other companies give the same reason for unused tools (Johnson et al., 2013). Every rule you turn on spends some of that trust. Turn on the ones that pay.

### 4.2 The ladder, on Project Pulse

Each tool approximates a different kind of problem, by reading the code in a different way. Lower rungs are cheaper and run earlier.

| Rung | What it catches | How it reads the code | Tools (Java; Vue) | Project Pulse before #104 (fall 2026) |
|---|---|---|---|---|
| **Compiler and IDE** | Syntax, types, unreachable code | Parses and type-checks, as in your compilers course | `javac`, IntelliJ inspections; `vue-tsc` | `vue-tsc` installed, 18 errors, never run in CI |
| **Formatter** | Inconsistent layout | Reprints the syntax tree in one style | Spotless; Prettier | Prettier installed, 75 files differ |
| **Linter (bug patterns)** | Known mistakes: empty catch, `==` on strings, dead stores | Matches patterns in the syntax tree (PMD, ESLint) or in the compiled bytecode (SpotBugs) | SpotBugs, PMD, Error Prone; ESLint, eslint-plugin-vue | None on the backend; ESLint 8 installed, broken script |
| **Null types** | Null dereferences, at compile time | A type system that tracks which values may be null | JSpecify annotations plus NullAway; TypeScript `strictNullChecks` | Spring Boot 4 is annotated; Project Pulse was not |
| **Dataflow and taint** | Untrusted input reaching a dangerous call (SQL, HTML, shell) | Follows values across methods and files: dataflow analysis, queried like a database | CodeQL | None |
| **Dependencies** | Libraries with known vulnerabilities | Matches your lockfile against a vulnerability database | Dependabot | None |
| **Containers and configuration** | A Dockerfile that runs as root, an unpinned base image | Reads the Dockerfile's instructions, or the built image | Hadolint, Trivy | None |
| **Secrets** | A key or password committed to the repository | Matches known key formats in every push | GitHub secret scanning and push protection | Off |

**SonarQube bundles several rungs in one product** (SonarQube for IDE, formerly SonarLint, in the editor; SonarQube Cloud, free for public repositories, or the self-hosted Community Build on the server). It is common in industry and a reasonable choice for a team. This course uses the separate tools because each one is free, runs in your own build, and needs no account.

This module works the linter rung first (4.3 to 4.8), because that is where the findings are and where every habit is learned. Then it climbs: null types and dataflow in [4.9](#49-the-higher-rungs-null-types-and-dataflow), and the rungs outside your own code in [4.10](#410-beyond-your-code-dependencies-containers-secrets-and-your-own-tools).

### 4.3 The first run, without touching the build

**On a codebase you just joined, look before you change anything.** Maven runs any plugin by its coordinates, so you can see what SpotBugs and PMD think of Project Pulse without editing `pom.xml`:

```bash
cd backend
./mvnw compile
./mvnw com.github.spotbugs:spotbugs-maven-plugin:4.10.5.0:spotbugs
./mvnw org.apache.maven.plugins:maven-pmd-plugin:3.28.0:pmd -Dformat=xml
```

The reports land in `target/spotbugsXml.xml` and `target/pmd.xml` (add `spotbugs:gui` for a browsable view). On the frontend, run the checks without `--fix`, so nothing changes under you:

```bash
cd frontend
npx eslint . --ext .vue,.js,.ts --ignore-path ../.gitignore
npm run type-check
npx prettier --check src/
```

**Read the result by rule before you read it by file.** A wall of 237 findings is unreadable; grouped by rule, Project Pulse's SpotBugs report is four lines:

| Rule | Findings | First read |
|---|---|---|
| `EI_EXPOSE_REP`, `EI_EXPOSE_REP2` (a getter returns, or a setter stores, a mutable object) | 219 | JPA entities and Spring beans share objects by design. Probably one decision for the whole rule, not 219 |
| `NP_NULL_ON_SOME_PATH_FROM_RETURN_VALUE` | 14 | Every one is a call to a method Spring marks `@Nullable`. Read them |
| `CT_CONSTRUCTOR_THROW` (a constructor can throw, leaving a half-built object) | 3 | Matters for classes a hostile subclass could extend. Read one |
| `DLS_DEAD_LOCAL_STORE` | 1 | Read it now |

Ninety-two percent of the report is one rule family, and the finding most worth reading is the single line at the bottom. That shape is typical of a first run.

**Why run both SpotBugs and PMD? They barely overlap.** Of Project Pulse's 367 findings, one was reported by both: the dead variable in `ActivityController.addActivityComment` (SpotBugs' `DLS_DEAD_LOCAL_STORE`, PMD's `UnusedLocalVariable`). Every other finding came from one tool, because they read different things:

| | SpotBugs (237 findings) | PMD (130 findings) |
|---|---|---|
| **Reads** | Compiled bytecode | Java source |
| **Strongest at** | How values flow through a method: nulls, casts, comparisons, mutable objects escaping | How the code is written: structure, unused code, risky idioms, style |
| **Its Project Pulse findings** | `EI_EXPOSE_REP` (219), null dereferences on Spring's `@Nullable` methods (14), constructors that can throw (3) | `toLowerCase()` without a `Locale` (18), `LiteralsFirstInComparisons` (6), `SimplifyBooleanReturns` (5), an unused private method, braces and constructor style |

Bytecode lets SpotBugs follow a value and read the `@Nullable` annotations compiled into Spring's jars; source lets PMD see what compilation erases: braces, the order of `"literal".equals(x)`, a private method nobody calls. The two bugs planted in [4.6](#46-an-existing-codebase-baseline-then-ratchet) split the same way: SpotBugs caught the `String` compared with `==`, PMD the empty `catch`. The second tool costs a configuration file, a baseline, and part of the minute `verify -DskipTests` takes. When two tools this different agree, as on the dead store, take it seriously. If you had to keep one, keep SpotBugs, which finds more bugs and less style. But PMD's unique findings include real ones (`toLowerCase()` without a `Locale` breaks a search on a server whose default locale is Turkish), so keep PMD too and decide which of its rules fit.

### 4.4 Triage: real, false positive, or not worth it

**Every finding gets one of three verdicts, and every verdict is recorded where the next reader will see it.** A verdict that lives only in your head is made again by the next person, or by the agent, which will happily "fix" a false positive.

| Verdict | Meaning | Record it as |
|---|---|---|
| **Real** | The code is wrong, or will be | A fix, with a test if the bug can be shown |
| **False positive** | The code is right; the tool cannot see why | A suppression at the site, with the reason |
| **Not worth it** | Technically true, not worth the change here | A suppression with the reason, or the rule turned off project-wide with the reason in the configuration |

Five findings from Project Pulse, one per kind of judgment:

**A real finding whose fix needs a decision.** Back to `addActivityComment` from [section 3](#3-motivation), which builds a DTO and returns `null`. The conversion is wasted work, but which fix is right? The frontend's type for this response declares `data: null`, and the use case would say whether the caller needs the updated activity. Delete the line, or return the DTO: the tool found the inconsistency, and the specification settles it.

**True by the contract, false in context.** Twelve of the fourteen `NP` findings, such as in [`UserUtils.getUserCourseId`](https://github.com/Washingtonwei/project-pulse/blob/90668c51b83f5352acf8d0f304a46590625cc87c/backend/src/main/java/team/projectpulse/system/UserUtils.java), dereference `SecurityContextHolder.getContext().getAuthentication()` or the `getAuthority()` of what it returns. Spring Security 7 annotates both methods `@Nullable`, and SpotBugs reads the annotation. Inside a request that passed the security filter chain, the authentication is never null. So is it a false positive? Only if every caller is behind that chain. A scheduled job or a test calling the same method has no authentication. The honest suppression names the assumption ("only called on authenticated routes"), which is also the sentence a reviewer can check.

**Deliberate, and the rule cannot know it.** PMD's `CompareObjectsWithEquals` flags `team.getSection() != from` in [`TeamService.transferTeam`](https://github.com/Washingtonwei/project-pulse/blob/90668c51b83f5352acf8d0f304a46590625cc87c/backend/src/main/java/team/projectpulse/team/TeamService.java). In general `==` on objects is a bug. Here both are JPA entities from the same persistence context, which guarantees one Java object per database row, so identity is the intended comparison. Suppress it and say so, or the next agent will "fix" it to `.equals()` and change the meaning.

**Same rule, different verdict.** ESLint's `no-empty` flags nine empty `catch {}` blocks in the requirements pages, such as `loadGlossary` in [`RamGlossary.vue`](https://github.com/Washingtonwei/project-pulse/blob/90668c51b83f5352acf8d0f304a46590625cc87c/frontend/src/pages/ram/RamGlossary.vue). In Java an empty catch usually hides a failure. Here the shared Axios interceptor in [`request.ts`](https://github.com/Washingtonwei/project-pulse/blob/90668c51b83f5352acf8d0f304a46590625cc87c/frontend/src/utils/request.ts) has already shown the error to the user, so the page has nothing left to do. A one-line comment in the block (`// error already shown by the request interceptor`) satisfies the rule and tells the reader why.

**Fix the configuration, not the code.** 117 of ESLint's 130 problems are `no-undef` on `cy`, `it`, and `describe` in the Cypress tests. The code is fine; the linter was never told those files run under Cypress. One override in the ESLint configuration removes all 117. When one rule floods a report, ask first whether the tool is configured for this codebase.

**How to suppress, with the reason attached:**

| Tool | At one site | For the whole project |
|---|---|---|
| SpotBugs | `@SuppressFBWarnings(value = "EI_EXPOSE_REP", justification = "...")` (from `spotbugs-annotations`) | An exclude filter file, one `<Match>` per decision, with an XML comment (Project Pulse: `backend/config/spotbugs-exclude.xml`) |
| PMD | `// NOPMD - reason` on the line, or `@SuppressWarnings("PMD.RuleName")` | An `<exclude>` in your own ruleset file, with a comment (Project Pulse: `backend/config/pmd-ruleset.xml`) |
| ESLint | `// eslint-disable-next-line rule-name -- reason` | `rules: { 'rule-name': 'off' }`, with a comment |

**A suppression without a reason is a bug report you deleted.** The reason should be a claim someone can check ("both entities come from one persistence context"), not a feeling ("false positive").

### 4.5 Make it a gate

**A verdict means nothing unless the build enforces it.** A tool that does not fail the build is decoration ([section 3](#3-motivation)). The **gate** is the set of checks a change must pass before it merges, and on a team it lives on the pull request.

**Shift left: the earlier a check runs, the cheaper the fix.** A warning in the editor costs seconds; the same bug found in review costs a conversation, and in production an incident.

| Where | What runs there | Why |
|---|---|---|
| **Editor** | IntelliJ inspections, SonarQube for IDE, ESLint and `vue-tsc` in VS Code | Fastest feedback, while the code is still in your head |
| **Before commit** (optional) | Formatter, fast linters, as a Git hook | Keeps noise out of review; skippable, so never the only gate |
| **Pull request** | Everything that must pass: `mvn verify`, ESLint, type check, Hadolint, CodeQL | **The gate.** Nothing merges red |
| **On a schedule** | Dependabot, CodeQL on `main` | New vulnerabilities are published about code that did not change |

**In the gate, check; on your machine, fix.** Run the fixing variants (`eslint --fix`, `prettier --write`) locally. In CI run the checking variants (`eslint`, `prettier --check`, `npm run type-check`), because a CI job that fixes code changes what it was asked to check. And make the deploy run the same checks: Project Pulse deployed with `npm run build-only`, which skips `vue-tsc`, and that is how its 18 type errors reached production ([section 3](#3-motivation)).

**Keep the gate fast and the rule set small.** A check that adds ten minutes to every pull request gets skipped, and a rule that fires on code the team considers fine gets turned off in anger. Start with the defaults of a few good tools, add a rule when a real bug gets past, and remove one when its findings are never acted on.

**Watch the gate fail before you trust it.** Plant one bug the tools should catch and confirm the build goes red. A gate you have never seen fail is a gate you are only hoping works. Wednesday's [CI/CD](../schedule.md) lecture wires these checks into the pipeline.

How you turn the gate on depends on one question: does the codebase already have code the tools complain about?

### 4.6 An existing codebase: baseline, then ratchet

**You cannot fix 367 findings before you turn the checks on, and you should not wait,** because every day without the gate adds to the pile. The standard way in:

1. **Record what exists today as a baseline**, untriaged.
2. **Fail the build only on findings outside the baseline.** New code meets the bar from the first day; old code is not blocked.
3. **Shrink the baseline**: fix or suppress an old finding, delete its entry. Never add an entry to make a build pass. The file only gets smaller. That is the ratchet.

**Project Pulse's pull request [#104](https://github.com/Washingtonwei/project-pulse/pull/104) does this,** and you can copy the pattern to your team's repository:

- `pom.xml` binds SpotBugs' and PMD's `check` goals to `mvn verify`.
- SpotBugs reads an exclude filter, `backend/config/spotbugs-baseline.xml`, with one `<Match>` (class, method, rule) per existing finding: 237 entries.
- PMD reads `backend/config/pmd-baseline.properties`, one line per class listing the rules it may break: 130 findings in 68 classes. Both files open with a comment saying they only shrink.
- Decisions live elsewhere: `spotbugs-exclude.xml` and `pmd-ruleset.xml` (PMD's quickstart, unchanged) start empty and hold each rule the team decides not to enforce, with the reason. Keeping them apart from the baseline means "we decided" never hides inside "we have not looked yet".

With the baselines in place, `./mvnw verify` passed. Adding one method that compared a `String` parameter with `==` failed the build at once with SpotBugs' `ES_COMPARING_PARAMETER_STRING_WITH_EQ` (priority High), and an empty `catch` failed PMD's check: the gate, seen failing.

**Know your baseline's grain.** SpotBugs' entries name the method, so a new finding in an old method's neighbor still fails. PMD's name only the class and rule, so a *new* empty catch in a class that already had one passes. Coarser baselines are easier to keep and leak more; say which you have.

**Warn first, then block.** The frontend checks failed on so much existing code that #104 ran them as report only (`continue-on-error: true`): every pull request showed the count, and nothing was blocked yet. Each check becomes blocking once its findings are fixed or baselined. Do not stay there; a warning nobody must act on is soon a warning nobody reads.

**Upgrading a tool can break its baseline.** The PMD plugin (3.28.0) bundles PMD 7.17.0, and #104 pinned 7.29.0, the newest release in fall 2026. The findings were the same 130, but one rule had been renamed (`UseUtilityClass` became `InstantiableUtilityClass`), so 12 baselined findings came back as new and failed the build until the baseline was regenerated. Treat an analyzer upgrade as its own pull request, and compare the counts by rule before and after. Do not skip upgrades either: ESLint 8 reached end of life on 5 October 2024, and in fall 2026 Project Pulse still ran it with the old `.eslintrc.cjs` format, while ESLint 9 made the flat `eslint.config.js` the default. An outdated analyzer is a finding too.

**Format in one commit.** Formatting is a decision, made once: Prettier (or Spotless in Java) ends arguments about layout. Pick the configuration (Project Pulse's is `.prettierrc.json`), reformat the whole codebase in one commit, alone and early, and list that commit in a `.git-blame-ignore-revs` file so `git blame` skips it. Then `prettier --check` joins the gate.

### 4.7 A new project: the gate comes first

**On new code, turn the gate on before the first feature, and no baseline is ever needed.** A walking skeleton has a handful of findings: triage them in an afternoon, and from then on every finding is new and every one fails the build. In the method this is part of the proving slice ([Phase B](../method.md#phase-b-prove-the-architecture-with-one-vertical-slice)), the first code your agent writes. A team that adds the gate at its tenth feature is back in [4.6](#46-an-existing-codebase-baseline-then-ratchet), carrying a baseline.

**Setting up the tools is a set of decisions, and each already has a home.** No new document:

| What you decided | Where it is recorded |
|---|---|
| Which analyzers and formatter run, the gate command, and how a finding is settled | A "Static analysis" subsection in section 8.2 of your architecture-of-record, because every component follows it; cite the `SEC-*` or `MNT-*` attribute that asked for it, if one did |
| The rule the agent obeys | One line in your charter, citing that subsection |
| A rule turned off, and why | The tool's configuration file, as a comment beside the exclusion, where the tool enforces it |
| Where each check runs | Section 7 of the architecture-of-record, "how a change gets there" |
| A baseline, if you have one | Section 11, as a debt row with the counts |

Two places it does not go. The specification says what the product must do for your client, and SpotBugs is not a client requirement. Nor is it a `KD-*`: an analyzer can be swapped in an afternoon, and key decisions are for what is hard to reverse. Project Pulse shows the shape: a "Static analysis" bullet in its [Architectural conventions](https://github.com/Washingtonwei/project-pulse/blob/90668c51b83f5352acf8d0f304a46590625cc87c/docs/design/architectural-design.md#architectural-conventions), `TD-analyzer-baselines` among its debts, and a short reminder in `CLAUDE.md` that links to both ([#107](https://github.com/Washingtonwei/project-pulse/pull/107)).

### 4.8 Your own rules: turn a repeated review comment into a check

**Every rule so far was written by strangers.** The SpotBugs and PMD authors know common Java mistakes; they do not know your team's conventions. Those live in section 8.2 of your architecture-of-record and in review comments. When a reviewer writes the same comment for the third time, the comment is a rule waiting to be written.

**A convention no tool ships.** Project Pulse's logging rule says a failure must leave a trace ([AI-Assisted Implementation 4.9](implementation.md#49-log-what-the-person-at-2-am-will-need)), and Code Review's checklist asks for it on every error path. Its last-resort exception handler breaks the rule ([`ExceptionHandlerAdvice`](https://github.com/Washingtonwei/project-pulse/blob/90668c51b83f5352acf8d0f304a46590625cc87c/backend/src/main/java/team/projectpulse/system/exception/ExceptionHandlerAdvice.java#L212-L215)):

```java
@ExceptionHandler(Exception.class)
@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
Result handleOtherException(Exception ex) {
    return new Result(false, StatusCode.INTERNAL_SERVER_ERROR, "A server internal error occurs.", ex.getMessage());
}
```

An unexpected exception becomes a 500, and nothing is logged. No shipped rule flags it, because nothing in the code is wrong as Java. It is wrong as *Project Pulse*.

**The rule, in PMD.** PMD parses each file into an abstract syntax tree, the same tree your compilers course built, and a custom rule is an XPath query over it: every node the query returns is a finding. This one says "a method that handles an exception and answers 500, but never calls `error` or `warn` on a logger":

```xml
<rule name="ServerErrorHandlerMustLog" language="java"
      message="An exception handler that answers 500 must log the exception"
      class="net.sourceforge.pmd.lang.rule.xpath.XPathRule">
  <priority>2</priority>
  <properties>
    <property name="xpath">
      <value><![CDATA[
//MethodDeclaration
  [ModifierList/Annotation[@SimpleName = 'ExceptionHandler']]
  [ModifierList/Annotation[@SimpleName = 'ResponseStatus']
     //FieldAccess[@Name = 'INTERNAL_SERVER_ERROR']]
  [not(.//MethodCall[@MethodName = ('error', 'warn')]
                    [*[1][matches(@Name, '^(log|logger|LOG|LOGGER)$')]])]
      ]]></value>
    </property>
  </properties>
</rule>
```

It goes in the team's own ruleset (Project Pulse's `backend/config/pmd-ruleset.xml`), so `mvn verify` runs it with everything else. Run on Project Pulse at `90668c5`, it reported exactly one finding: `handleOtherException`.

**A rule is code, so test it both ways.** With the rule in Project Pulse's ruleset, `./mvnw verify` failed on `handleOtherException`. Declaring a logger in the class and adding `LOGGER.error("Unhandled exception", ex);` to the handler, the fix [AI-Assisted Implementation 4.9](implementation.md#49-log-what-the-person-at-2-am-will-need) proposes, made it pass. Keep one example the rule must flag and one it must pass, as PMD's rule tests or Semgrep's `ruleid:` and `ok:` annotations do. Without the second example you cannot tell a rule that works from one that matches everything; without the first, from one that matches nothing.

**Your own rules need triage too.** A broader first draft, "every `catch` that does not rethrow must log", flagged 1 of Project Pulse's 11 catch blocks: `PathVariables.readId`, which returns `null` on a malformed ID on purpose, because the authorization managers treat anything unresolvable as a denial. That is a false positive by design. Narrow the rule, or suppress that site with its reason, exactly as in [4.4](#44-triage-real-false-positive-or-not-worth-it).

**The same idea in other tools:**

| Tool | Writes the rule as | Good for |
|---|---|---|
| PMD (XPath) | A query over the Java syntax tree | Code conventions, in the build you already have |
| Semgrep | A pattern that looks like the code, with `$X` placeholders | Many languages, readable rules, quick to try |
| ArchUnit | A JUnit test over classes and packages | Architecture rules, such as "no controller calls a repository" |
| ESLint `no-restricted-syntax` | An AST selector in the configuration | Frontend conventions, no plugin needed |

**This is where an agent changes the economics.** Writing a rule used to cost more than repeating the review comment, so teams repeated the comment. An agent drafts an XPath or Semgrep rule in a minute. You write, or at least read, the two examples, because they are the rule's specification, and you decide which convention is worth a rule. Each rule then holds the agent's next thousand lines to the convention without anyone repeating the comment.

Pattern rules, the shipped ones and your own, look at one method's syntax at a time. Some bugs travel: a `null` returned in one method and dereferenced in another, a request parameter that reaches a query three calls later.

### 4.9 The higher rungs: null types and dataflow

**Make null part of the type.** Tony Hoare called the null reference his "billion-dollar mistake". A type system can track it, the way it already tracks `int` against `String`: TypeScript does with `strictNullChecks`, and Java can with **JSpecify** annotations (`@Nullable` where null is legal, `@NullMarked` to make a package non-null by default) checked at compile time by **NullAway**, a plugin for Google's Error Prone compiler. Spring Boot 4's own APIs are annotated this way, which is why SpotBugs could flag `getAuthentication()` in [4.4](#44-triage-real-false-positive-or-not-worth-it). Marking a single Project Pulse package `@NullMarked` produced 14 compile errors. One was [`UserUtils.getUserId()`](https://github.com/Washingtonwei/project-pulse/blob/90668c51b83f5352acf8d0f304a46590625cc87c/backend/src/main/java/team/projectpulse/system/UserUtils.java), which returns `null` on four paths while its signature promises an `Integer`; `ActivitySecurityService.canAccessActivity` passes the result straight to `findById`, which throws on `null`. No test had taken those paths; the type checker found all four without running any. Adopt it one package at a time; unmarked packages are not checked.

**CodeQL follows untrusted data through the program.** It turns the code into a relational database and runs queries over it, written in QL, a Datalog-style logic language: the databases course, applied to programs. A security query asks whether data from a **source** (a request parameter, a header) reaches a **sink** (a SQL string, an HTML response, a shell command) without passing a **sanitizer** (a parameterized query, an encoder). That is the dataflow analysis of your compilers course, and the shape of SQL injection, cross-site scripting, and command injection. On a public GitHub repository, turning on code scanning's *default setup* (Settings, Code security) scans Java and TypeScript on every pull request; Java needs no build step. Project Pulse's search code, such as `StudentSpecs`, builds queries through the JPA Criteria API, so Hibernate binds the user's text as a parameter and no SQL string is built from input: the sanitizer CodeQL looks for.

**Its first alert went through triage.** CodeQL's first run on Project Pulse, in fall 2026, on `main` after #104, opened a single alert, rated high: `java/spring-disabled-csrf-protection`, at `.csrf(csrf -> csrf.disable())` in [`SecurityConfiguration`](https://github.com/Washingtonwei/project-pulse/blob/90668c51b83f5352acf8d0f304a46590625cc87c/backend/src/main/java/team/projectpulse/security/SecurityConfiguration.java). Cross-site request forgery gets a victim's browser to send a request carrying credentials the browser attaches by itself, usually a session cookie. Project Pulse has none to borrow: the frontend sends its token in an `Authorization: Bearer` header ([`request.ts`](https://github.com/Washingtonwei/project-pulse/blob/90668c51b83f5352acf8d0f304a46590625cc87c/frontend/src/utils/request.ts)), and the server keeps no session (`SessionCreationPolicy.STATELESS`). The verdict from [4.4](#44-triage-real-false-positive-or-not-worth-it) is false positive in context, and the alert is dismissed with that reason, which is also the condition to recheck: the day the token moves into a cookie, the alert becomes true.

Everything so far reads code your team wrote. Most of what you ship, you did not write.

### 4.10 Beyond your code: dependencies, containers, secrets, and your own tools

**Most of your code is other people's.** Project Pulse's backend declares 26 dependencies, and Maven resolves 263 once their own dependencies are counted. When Log4Shell (CVE-2021-44228) was published in December 2021, the vulnerable code was in nobody's own repository; it was in a logging library under almost every Java application. Dependabot reads `pom.xml` and `package-lock.json`, alerts on known vulnerabilities, and opens pull requests that update them. Turn it on once CI can catch a broken update. In fall 2026 Project Pulse held it back until its frontend job built the app and blocked, because until then an update that broke the frontend would still have shown a green check.

**A clean report can still miss the point.** Hadolint passes Project Pulse's [`Dockerfile`](https://github.com/Washingtonwei/project-pulse/blob/90668c51b83f5352acf8d0f304a46590625cc87c/Dockerfile) with no findings, yet in fall 2026 its runtime image had no `USER` line, so the application ran as root inside its container. Hadolint checks the instructions that are written; a missing one is invisible to it. Image scanners such as Trivy check the built image's packages and configuration, including the user.

**Secrets never belong in the repository.** GitHub's secret scanning finds committed keys, and push protection rejects a push that contains one. Turn both on (free for public repositories). A secret that reached a public repository is compromised even if you delete the commit: rotate it.

**Your security tools are part of your supply chain.** A line such as `uses: aquasecurity/trivy-action@0.28.0` downloads someone else's code and runs it inside your CI job, with the job's secrets. The part after `@` decides which code:

| | Example | What it means |
|---|---|---|
| **Tag** | `@v4` | Whatever commit the action's owner points `v4` at today. The owner, or anyone holding the owner's credentials, can move it, and your workflow file does not change. |
| **Commit SHA** | `@11d5960a326750d5838078e36cf38b85af677262` | A fingerprint of the exact code. Change one byte and the SHA changes, so nobody can make it mean different code. |

**On 19 March 2026, the scan was the attack.** Attackers holding credentials stolen from Trivy's project in an earlier breach moved 75 of the 76 version tags of `aquasecurity/trivy-action`, the official GitHub Action for the Trivy scanner, to code of their own. They edited nobody's workflow. Every pipeline that named the action by a tag ran their code on its next run, and that code collected the secrets the job could reach: deploy keys, cloud credentials, registry tokens. The window was about twelve hours (Microsoft and Wiz both published analyses). Pipelines pinned to a commit SHA ran the same code as the day before. The step teams added to be more secure was the way in.

**Pin the fact, and let a bot propose new ones.** Name every Action by its full commit SHA, with the version in a comment, as #104's workflow does:

```yaml
uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4.4.0
```

A pinned SHA never updates itself, so you would also miss the action's fixes. Dependabot's `github-actions` ecosystem opens a pull request that changes the SHA and the comment together, so updates still come, as a change someone reviews. On Project Pulse the stakes are the deploy workflow: it holds the Azure publish profile, so a moved tag there could deploy code of the attacker's choosing.

**Pinning has two limits.** A SHA pinned while a tag pointed at malicious code pins the malicious code, which is why an action update is read, not auto-merged. And an action can fetch other code by tag inside itself; `hadolint-action` at #104's pinned commit pulls its image by digest (`@sha256:…`), the image equivalent of a SHA, so that path is pinned all the way down.

## 5. The AI-native lens

- **Delegate to AI:** explaining an unfamiliar rule and why it fired; fixing findings with an obvious fix (an unused import, braces, a `Locale` argument); grouping a report by rule; drafting the baseline and the configuration; writing the test that shows a real finding is a bug; drafting a custom rule from a written convention.
- **Keep human:** every verdict that is not "fix it". A suppression, a rule turned off, and an entry kept in the baseline are claims about the codebase that someone must be able to defend. An agent may not add to a baseline or suppress a finding to make a build pass without saying so in the pull request. Which conventions deserve a custom rule, and the two examples that test it, are yours too.
- **Context to supply:** the command that is the gate (`./mvnw verify` in Project Pulse's `CLAUDE.md`), the rule that baselines only shrink, and the facts the tool cannot see: which methods run only behind authentication, which comparisons are entity identity, which errors the interceptor already shows.
- **How to verify:** run the gate yourself; read every suppression in the diff as you would read code; and for each "fixed" finding, check the fix is the right one and not the quietest one. An agent that silences `CompareObjectsWithEquals` by switching `==` to `.equals()` on an entity has changed behavior to quiet a warning.

## 6. Risks & mitigations

| Risk (classic + AI-introduced) | Human judgment that catches it | Mitigation |
|---|---|---|
| **Classic:** alert fatigue: hundreds of warnings, so nobody reads any | Reading the report by rule and asking which rules fit this codebase | Few good rules, a baseline for the rest, remove rules nobody acts on |
| **Classic:** tools installed but never run | Asking "what fails the build?" rather than "what is installed?" | Put every check in the pull request gate |
| **AI-introduced:** the agent quiets findings instead of fixing them (a suppression, a baseline entry, a changed comparison) | Reading suppressions and baseline diffs in review | Charter rule: baselines only shrink; every suppression carries a checkable reason |
| **AI-introduced:** the agent "fixes" a false positive and changes behavior | Asking what the code meant before the fix | Suppress deliberate code with its reason, so the next agent sees it |
| **Classic:** a clean report read as "secure" | Knowing each tool's blind spot (Hadolint and the missing `USER`) | Cover each rung with a tool; test what matters |
| **AI-introduced:** an agent-written custom rule that matches nothing, or everything | Asking to see it flag one bad example and pass one good one | Keep both examples as the rule's test |
| **Classic:** a compromised or upgraded tool changes what runs | Comparing finding counts across a tool upgrade; pinning versions | Pin Actions to commit SHAs; review tool updates like code |

## 7. Hands-on (studio + optional individual assignment)

**In class (Monday):** SpotBugs and PMD on Project Pulse from the command line, the report read by rule, three findings triaged live, a planted bug failing the gate, the custom logging rule run both ways, and NullAway on one package.

**Team, own project (Friday's studio):**

- **First run:** run the analyzers for your stack, record the counts by rule, and decide which rules your team turns off, with the reason in the configuration.
- **Gate:** make the checks fail your pull request build. Your repository is young, so triage everything and skip the baseline if you can; baseline only what you cannot finish today. Plant one bug and watch it fail.
- **Write it down** ([4.7](#47-a-new-project-the-gate-comes-first)): a "Static analysis" subsection in section 8.2 of your architecture-of-record, and a charter line citing it: the gate command, suppressions carry reasons, and a baseline only shrinks.
- **Your own rule** (optional, [4.8](#48-your-own-rules-turn-a-repeated-review-comment-into-a-check)): pick one convention from your section 8.2, have your agent draft a rule for it, and commit it with one example it flags and one it passes.

**Individual assignment:** [*Triage the analyzers*](../assignments/triage-the-analyzers.md) (assignment 4). Start from a copy of Project Pulse with the analyzers and baselines of #104, make four project-wide rule decisions, triage your slice of the baseline, fix the real findings (one shown by a test), suppress the rest with reasons, and shrink the baseline, with the pipeline green. The triage is the assignment.

## 8. Summary / key takeaways

- A tool that does not fail the build is decoration. Put every check in the pull request gate.
- Analyzers catch the boring, mechanical defects on every path; tests catch wrong behavior on the paths you run; review catches what the code is for. Run the machines before the reviewer.
- Every analyzer approximates (Rice's theorem), so every report has false positives or false negatives. A clean report is not a proof, and trust is spent one useless warning at a time.
- Read a report by rule first. Most of it is a few rules that do not fit; the bugs are few.
- Every finding ends as a fix, a suppression with a checkable reason, or a rule turned off with its reason.
- On an existing codebase, baseline what exists and fail only on what is new. The baseline only shrinks.
- On a new project, turn the gate on before the first feature, and there is nothing to baseline. Record the setup in section 8.2 of the architecture-of-record, the rule in the charter, and each rule turned off in the tool's configuration.
- When the same review comment comes back, write it as a rule, and test the rule both ways. An agent drafts it; you choose the convention and the examples.
- Pattern rules see one method; null types and dataflow follow values across the program, and the rungs outside your code (dependencies, images, secrets, your CI actions) need their own tools.
- The analyzer is the reviewer that reads all of the agent's code. The verdicts stay with you.

## 9. Key papers & further reading

- Sadowski, C., Aftandilian, E., Eagle, A., Miller-Cushon, L., and Jaspan, C. "Lessons from Building Static Analysis Tools at Google." *Communications of the ACM* 61(4), 2018.
- Bessey, A., et al. "A Few Billion Lines of Code Later: Using Static Analysis to Find Bugs in the Real World." *Communications of the ACM* 53(2), 2010.
- Johnson, B., Song, Y., Murphy-Hill, E., and Bowdidge, R. "Why Don't Software Developers Use Static Analysis Tools to Find Bugs?" ICSE 2013.
- Pearce, H., Ahmad, B., Tan, B., Dolan-Gavitt, B., and Karri, R. "Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions." IEEE S&P 2022.
- Veracode. [*2025 GenAI Code Security Report*](https://www.veracode.com/resources/genai-code-security-report/). 2025.
- Langley, A. "[Apple's SSL/TLS bug](https://www.imperialviolet.org/2014/02/22/applebug.html)." ImperialViolet, 22 February 2014.
- Rice, H. G. "Classes of Recursively Enumerable Sets and Their Decision Problems." *Transactions of the American Mathematical Society* 74(2), 1953.
- Banerjee, S., Clapp, L., and Sridharan, M. "NullAway: Practical Type-Based Null Safety for Java." ESEC/FSE 2019.
- Winters, T., Manshreck, T., and Wright, H. *Software Engineering at Google*. O'Reilly, 2020. Chapter 20, Static Analysis.
- Tool documentation: [SpotBugs](https://spotbugs.readthedocs.io/), [PMD](https://docs.pmd-code.org/latest/) and [its XPath rules](https://docs.pmd-code.org/latest/pmd_userdocs_extending_writing_xpath_rules.html), [Semgrep](https://semgrep.dev/docs/), [ArchUnit](https://www.archunit.org/), [NullAway](https://github.com/uber/NullAway/wiki), [JSpecify](https://jspecify.dev/), [Spring null safety](https://docs.spring.io/spring-framework/reference/core/null-safety.html), [CodeQL](https://codeql.github.com/docs/), [ESLint](https://eslint.org/docs/latest/), [Dependabot](https://docs.github.com/en/code-security/dependabot).

## 10. Self-check

1. A teammate says a good enough analyzer would report every bug and nothing else. Use Rice's theorem to answer, and say which kind of error you would rather tolerate in a pull request gate.
2. A first SpotBugs run on your team's repository reports 400 findings. What do you do in the first ten minutes, and what do you not do?
3. Give one Project Pulse finding of each verdict (real, false positive, not worth it) and say how each is recorded.
4. `@SuppressFBWarnings(value = "NP_NULL_ON_SOME_PATH_FROM_RETURN_VALUE", justification = "false positive")`. What is wrong with it, and what would a good justification say for `UserUtils.getUserCourseId`?
5. Your PMD baseline lists `TeamService=CompareObjectsWithEquals`. A teammate adds a new `==` comparison to `TeamService`. Does the build fail? What does that tell you about the baseline?
6. An agent's pull request turns the build green by adding twelve entries to the SpotBugs baseline. What do you ask for in review?
7. Your team starts a new repository. Where do you record which analyzers run, the gate command, and a PMD rule you turned off? Why not in the specification?
8. Your reviewers keep writing "this catch swallows the exception." What do you build instead of writing it again, and what two examples do you commit with it? Where is the one place it should not fire in Project Pulse?
9. Why can NullAway catch the `null` that `UserUtils.getUserId()` returns when no test does?
10. Hadolint reports no findings on a Dockerfile whose image runs as root. Which rung of the ladder covers that, and with what tool?
11. Your workflow uses `actions/checkout@v4`. What changes if you write the commit SHA instead, and what keeps it up to date?

## Related

- [Testing](testing.md): the dynamic half; a real finding gets a test that shows the bug.
- [Code Review](code-review.md): what a human reviewer checks that no analyzer can.
- [AI-Assisted Implementation](implementation.md): the agent charter, where the gate command and the baseline rule go.
- [Schedule](../schedule.md): week 11, static analysis on Monday and CI/CD on Wednesday.
- [Triage the analyzers](../assignments/triage-the-analyzers.md): assignment 4, this module on Project Pulse.
