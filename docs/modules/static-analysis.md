# Static Analysis

> **Purpose (one line):** add analyzers to a codebase you did not write, triage what they report into real bugs, false positives, and noise, and make them a gate that holds new code (yours and the agent's) to a bar the old code has not met yet.

## 1. Learning objectives

By the end of this module, a student can:

1. Name what each rung of the analysis ladder catches (compiler, formatter, linter, null types, dataflow, dependencies, containers, secrets) and pick the tool for each on a Spring Boot and Vue project.
2. Run SpotBugs, PMD, and ESLint on an unfamiliar codebase without changing its build, and read the results by rule before reading them by file.
3. Triage a finding as real, false positive, or not worth fixing, and record the verdict where the next reader will see it: a fix, a suppression with a written reason, or a rule turned off for the whole project.
4. Adopt analyzers on a brownfield project with a baseline, so the build fails only on new findings, and shrink that baseline over time.
5. Use analyzers as the deterministic gate on agent-written code, and say what an agent may and may not decide about a finding.

## 2. Where it fits

- **Prerequisites:** [AI-Assisted Implementation](implementation.md), whose agent writes the code these tools check; [Code Review](code-review.md), which reviews what the tools cannot; [Testing](testing.md), the dynamic half of verification.
- **Leads into:** CI/CD (Wednesday of the same week), which runs these checks on every pull request; dynamic analysis (week 12), which watches the program run; metrics and technical debt, where a baseline is debt you can count.
- **How it's taught:** Monday of week 11, with live runs on Project Pulse. Friday's studio puts the checks in your team's pipeline. Practised alone in *Triage the analyzers* (assignment 4, due Fri Nov 13).
- **Course outcome it delivers:** [build, test, and ship a working MVP](../syllabus.md#learning-outcomes) (outcome 4), and verifying AI output without lowering the bar (outcome 6).

## 3. Motivation

**Project Pulse ran no analyzer for its first two years.** Its backend build compiled and ran the tests, nothing more. The first SpotBugs run reported 237 findings, and PMD's starter rules 130 more. The frontend has had ESLint, Prettier, and the `vue-tsc` type checker since its first commit in October 2024, and none of them passes: 130 ESLint problems, 18 type errors, 75 unformatted files. `npm run lint` did not even start, because it pointed at a `.gitignore` that does not exist. Nobody noticed, because nothing ran them. A tool that is installed but not run is decoration.

**One duplicated line turned off a signature check in iOS and macOS.** In February 2014 Apple shipped a fix for CVE-2014-1266, "goto fail". In `SSLVerifySignedServerKeyExchange` the line `goto fail;` appeared twice in a row, so the second one always jumped past the signature verification, and an attacker on the network could impersonate any secure website. The code after the second `goto` could never run, which is exactly what an unreachable-code warning reports. The compiler had the check; the build did not turn it on.

**Agents write the same bugs, faster.** Pearce and colleagues asked GitHub Copilot to complete 89 security-relevant scenarios and got 1,689 programs; about 40% were vulnerable (IEEE S&P 2022). They found the vulnerabilities with CodeQL, the same analyzer this module puts in your pipeline. An agent that writes a feature in ten minutes also writes its null dereference and its unescaped query in ten minutes, and it reports the work done. The analyzer is the reviewer that reads every line, every time, the same way.

## 4. Core concepts

### 4.1 What a static analyzer can and cannot tell you

**A static analyzer reads the code without running it.** Testing (dynamic analysis) checks the paths you executed; a static analyzer reasons about every path, including the ones no test reaches. To finish in seconds on a large program it approximates, so every analyzer has two kinds of error:

| Error | What it is | What it costs |
|---|---|---|
| **False positive** | A warning about code that is fine | Time, and trust: a team that sees enough of them stops reading warnings |
| **False negative** | A real bug the tool says nothing about | A clean report is not a proof of safety |

**Trust is the scarce resource.** Google's static analysis team found that developers act on a tool only if most of what it says is worth acting on, and set a target of under 10% *effective* false positives: warnings the developer does not act on, whatever the tool thinks (Sadowski et al., 2018). Interviews at other companies give the same reason for unused tools (Johnson et al., 2013). Every rule you turn on spends some of that trust. Turn on the ones that pay.

### 4.2 The ladder, on Project Pulse

Each rung catches a different class of problem, and each needs its own tool. Lower rungs are cheaper and run earlier.

| Rung | What it catches | Spring Boot (Java) | Vue (TypeScript) | Project Pulse, before #104 |
|---|---|---|---|---|
| **Compiler and IDE** | Syntax, types, unreachable code | `javac`, IntelliJ inspections | `vue-tsc` | `vue-tsc` installed, 18 errors, never run in CI |
| **Formatter** | Inconsistent layout | Spotless, spring-javaformat | Prettier | Prettier installed, 75 files differ |
| **Linter (bug patterns)** | Known mistakes: empty catch, `==` on strings, dead stores | SpotBugs (bytecode), PMD (source), Error Prone (in the compiler) | ESLint, eslint-plugin-vue | None on the backend; ESLint 8 installed, broken script |
| **Null types** | Null dereferences, at compile time | JSpecify annotations plus NullAway | TypeScript `strictNullChecks` | Spring Boot 4 is annotated; Project Pulse is not |
| **Dataflow and taint** | Untrusted input reaching a dangerous call (SQL, HTML, shell) | CodeQL | CodeQL | None |
| **Dependencies** | Libraries with known vulnerabilities | Dependabot | Dependabot | None |
| **Containers and configuration** | A Dockerfile that runs as root, an unpinned base image | Hadolint, Trivy | | None |
| **Secrets** | A key or password committed to the repository | GitHub secret scanning and push protection | | Off |

**SonarQube bundles several rungs in one product** (SonarQube for IDE, formerly SonarLint, in the editor; SonarQube Cloud, free for public repositories, or the self-hosted Community Build on the server). It is common in industry and a reasonable choice for a team. This course uses the separate tools because each one is free, runs in your own build, and needs no account.

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

Bytecode lets SpotBugs follow a value and read the `@Nullable` annotations compiled into Spring's jars; source lets PMD see what compilation erases: braces, the order of `"literal".equals(x)`, a private method nobody calls. The two bugs planted in [4.5](#45-adding-analyzers-to-a-brownfield-project-baseline-then-ratchet) split the same way: SpotBugs caught the `String` compared with `==`, PMD the empty `catch`. The second tool costs a configuration file, a baseline, and part of the minute `verify -DskipTests` takes. When two tools this different agree, as on the dead store, take it seriously. If you had to keep one, keep SpotBugs, which finds more bugs and less style. But PMD's unique findings include real ones (`toLowerCase()` without a `Locale` breaks a search on a server whose default locale is Turkish), so keep PMD too and decide which of its rules fit.

### 4.4 Triage: real, false positive, or not worth it

**Every finding gets one of three verdicts, and every verdict is recorded where the next reader will see it.** A verdict that lives only in your head is made again by the next person, or by the agent, which will happily "fix" a false positive.

| Verdict | Meaning | Record it as |
|---|---|---|
| **Real** | The code is wrong, or will be | A fix, with a test if the bug can be shown |
| **False positive** | The code is right; the tool cannot see why | A suppression at the site, with the reason |
| **Not worth it** | Technically true, not worth the change here | A suppression with the reason, or the rule turned off project-wide with the reason in the configuration |

Five findings from Project Pulse, one per kind of judgment:

**A real finding whose fix needs a decision.** SpotBugs and PMD both flag [`ActivityController.addActivityComment`](https://github.com/Washingtonwei/project-pulse/blob/main/backend/src/main/java/team/projectpulse/activity/ActivityController.java): it converts the updated activity to a DTO, then returns `null` as the data. The conversion is wasted work, but which fix is right? The frontend's type for this response declares `data: null`, and the use case would say whether the caller needs the updated activity. Delete the line, or return the DTO: the tool found the inconsistency, and the specification settles it.

**True by the contract, false in context.** Twelve of the fourteen `NP` findings, such as in [`UserUtils.getUserCourseId`](https://github.com/Washingtonwei/project-pulse/blob/main/backend/src/main/java/team/projectpulse/system/UserUtils.java), dereference `SecurityContextHolder.getContext().getAuthentication()` or the `getAuthority()` of what it returns. Spring Security 7 annotates both methods `@Nullable`, and SpotBugs reads the annotation. Inside a request that passed the security filter chain, the authentication is never null. So is it a false positive? Only if every caller is behind that chain. A scheduled job or a test calling the same method has no authentication. The honest suppression names the assumption ("only called on authenticated routes"), which is also the sentence a reviewer can check.

**Deliberate, and the rule cannot know it.** PMD's `CompareObjectsWithEquals` flags `team.getSection() != from` in [`TeamService.transferTeam`](https://github.com/Washingtonwei/project-pulse/blob/main/backend/src/main/java/team/projectpulse/team/TeamService.java). In general `==` on objects is a bug. Here both are JPA entities from the same persistence context, which guarantees one Java object per database row, so identity is the intended comparison. Suppress it and say so, or the next agent will "fix" it to `.equals()` and change the meaning.

**Same rule, different verdict.** ESLint's `no-empty` flags nine empty `catch {}` blocks in the requirements pages, such as `loadGlossary` in [`RamGlossary.vue`](https://github.com/Washingtonwei/project-pulse/blob/main/frontend/src/pages/ram/RamGlossary.vue). In Java an empty catch usually hides a failure. Here the shared Axios interceptor in [`request.ts`](https://github.com/Washingtonwei/project-pulse/blob/main/frontend/src/utils/request.ts) has already shown the error to the user, so the page has nothing left to do. A one-line comment in the block (`// error already shown by the request interceptor`) satisfies the rule and tells the reader why.

**Fix the configuration, not the code.** 117 of ESLint's 130 problems are `no-undef` on `cy`, `it`, and `describe` in the Cypress tests. The code is fine; the linter was never told those files run under Cypress. One override in the ESLint configuration removes all 117. When one rule floods a report, ask first whether the tool is configured for this codebase.

**How to suppress, with the reason attached:**

| Tool | At one site | For the whole project |
|---|---|---|
| SpotBugs | `@SuppressFBWarnings(value = "EI_EXPOSE_REP", justification = "...")` (from `spotbugs-annotations`) | An exclude filter file, one `<Match>` per decision, with an XML comment (Project Pulse: `backend/config/spotbugs-exclude.xml`) |
| PMD | `// NOPMD - reason` on the line, or `@SuppressWarnings("PMD.RuleName")` | An `<exclude>` in your own ruleset file, with a comment (Project Pulse: `backend/config/pmd-ruleset.xml`) |
| ESLint | `// eslint-disable-next-line rule-name -- reason` | `rules: { 'rule-name': 'off' }`, with a comment |
| NullAway | `@SuppressWarnings("NullAway")`, or `@Nullable` where null is legal | Leave the package out of `@NullMarked` |

**A suppression without a reason is a bug report you deleted.** The reason should be a claim someone can check ("both entities come from one persistence context"), not a feeling ("false positive").

### 4.5 Adding analyzers to a brownfield project: baseline, then ratchet

**You cannot fix 367 findings before you turn the checks on, and you should not wait,** because every day without the gate adds to the pile. The standard way in:

1. **Record what exists today as a baseline**, untriaged.
2. **Fail the build only on findings outside the baseline.** New code meets the bar from the first day; old code is not blocked.
3. **Shrink the baseline**: fix or suppress an old finding, delete its entry. Never add an entry to make a build pass. The file only gets smaller. That is the ratchet.

**Project Pulse's pull request [#104](https://github.com/Washingtonwei/project-pulse/pull/104) does this,** and you can copy the pattern to your team's repository:

- `pom.xml` binds SpotBugs' and PMD's `check` goals to `mvn verify`.
- SpotBugs reads an exclude filter, `backend/config/spotbugs-baseline.xml`, with one `<Match>` (class, method, rule) per existing finding: 237 entries.
- PMD reads `backend/config/pmd-baseline.properties`, one line per class listing the rules it may break: 130 findings in 68 classes. Both files open with a comment saying they only shrink.
- Decisions live elsewhere: `spotbugs-exclude.xml` and `pmd-ruleset.xml` (PMD's quickstart, unchanged) start empty and hold each rule the team decides not to enforce, with the reason. Keeping them apart from the baseline means "we decided" never hides inside "we have not looked yet".

**Check that the gate works before you trust it.** With the baselines in place, `./mvnw verify` passed. Adding one method that compared a `String` parameter with `==` failed the build at once with SpotBugs' `ES_COMPARING_PARAMETER_STRING_WITH_EQ` (priority High), and an empty `catch` failed PMD's check. A gate you have never seen fail is a gate you are only hoping works.

**Know your baseline's grain.** SpotBugs' entries name the method, so a new finding in an old method's neighbor still fails. PMD's name only the class and rule, so a *new* empty catch in a class that already had one passes. Coarser baselines are easier to keep and leak more; say which you have.

**Warn first, then block.** The frontend checks fail on so much existing code that #104 runs them as report only (`continue-on-error: true`): every pull request shows the count, nothing is blocked yet. Each check becomes blocking once its findings are fixed or baselined. Do not stay there; a warning nobody must act on is soon a warning nobody reads.

**Upgrading a tool can break its baseline.** The PMD plugin bundles PMD 7.17.0, and #104 pins the current 7.29.0. The findings were the same 130, but one rule had been renamed (`UseUtilityClass` became `InstantiableUtilityClass`), so 12 baselined findings came back as new and failed the build until the baseline was regenerated. Treat an analyzer upgrade as its own pull request, and compare the counts by rule before and after.

**Format in one commit.** Formatting a whole codebase is one commit that touches every file. Do it alone, early, and list it in a `.git-blame-ignore-revs` file so `git blame` skips it.

### 4.6 On a new project: the gate comes first

**On new code, turn the gate on before the first feature, and no baseline is ever needed.** A walking skeleton has a handful of findings: triage them in an afternoon, and from then on every finding is new and every one fails the build. In the method this is part of the proving slice ([Phase B](../method.md#phase-b-prove-the-architecture-with-one-vertical-slice)), the first code your agent writes. A team that adds the gate at its tenth feature is back in [4.5](#45-adding-analyzers-to-a-brownfield-project-baseline-then-ratchet), carrying a baseline.

**Setting up the tools is a set of decisions, and each already has a home.** No new document:

| What you decided | Where it is recorded |
|---|---|
| Which analyzers and formatter run, the gate command, and how a finding is settled | A "Static analysis" subsection in section 8.2 of your architecture-of-record, because every component follows it; cite the `SEC-*` or `MNT-*` attribute that asked for it, if one did |
| The rule the agent obeys | One line in your charter, citing that subsection |
| A rule turned off, and why | The tool's configuration file, as a comment beside the exclusion, where the tool enforces it |
| Where each check runs | Section 7 of the architecture-of-record, "how a change gets there" |
| A baseline, if you have one | Section 11, as a debt row with the counts |

Two places it does not go. The specification says what the product must do for your client, and SpotBugs is not a client requirement. Nor is it a `KD-*`: an analyzer can be swapped in an afternoon, and key decisions are for what is hard to reverse. Project Pulse shows the shape: a "Static analysis" bullet in its [Architectural conventions](https://github.com/Washingtonwei/project-pulse/blob/main/docs/design/architectural-design.md#architectural-conventions), `TD-analyzer-baselines` among its debts, and a short reminder in `CLAUDE.md` that links to both ([#107](https://github.com/Washingtonwei/project-pulse/pull/107)).

### 4.7 Where the checks run

**Shift left: the earlier a check runs, the cheaper the fix.** A warning in the editor costs seconds; the same bug found in review costs a conversation, and in production an incident.

| Where | What runs there | Why |
|---|---|---|
| **Editor** | IntelliJ inspections, SonarQube for IDE, ESLint and `vue-tsc` in VS Code | Fastest feedback, while the code is still in your head |
| **Before commit** (optional) | Formatter, fast linters, as a Git hook | Keeps noise out of review; skippable, so never the only gate |
| **Pull request** | Everything that must pass: `mvn verify`, ESLint, type check, Hadolint, CodeQL | **The gate.** Nothing merges red |
| **On a schedule** | Dependabot, CodeQL on `main` | New vulnerabilities are published about code that did not change |

**Keep the gate fast and the rule set small.** A check that adds ten minutes to every pull request gets skipped, and a rule that fires on code the team considers fine gets turned off in anger. Start with the defaults of a few good tools, add a rule when a real bug gets past, and remove one when its findings are never acted on. Wednesday's [CI/CD](../schedule.md) lecture wires these checks into the pipeline.

### 4.8 Null safety: JSpecify and NullAway

**The null pointer exception is among the most common crashes in Java, and a type checker can prevent most of them.** The approach the Spring team chose for Spring Framework 7 and Spring Boot 4 has two parts:

- **JSpecify annotations** say where null is legal. `@NullMarked` on a package (in its `package-info.java`) makes every type in it non-null by default; `@Nullable` marks the exceptions. Spring Boot 4's own APIs are annotated this way, which is why SpotBugs could flag `getAuthentication()` in [4.4](#44-triage-real-false-positive-or-not-worth-it).
- **NullAway** (from Uber), a plugin for Google's Error Prone compiler, checks the annotations at compile time and fails the build on a possible null dereference.

**What it found in one Project Pulse package.** Marking only `team.projectpulse.system` as `@NullMarked` and compiling with NullAway produced 14 errors. The most instructive is [`UserUtils.getUserId()`](https://github.com/Washingtonwei/project-pulse/blob/main/backend/src/main/java/team/projectpulse/system/UserUtils.java), declared to return `Integer`: it returns `null` on four paths (no authentication, a principal that is not a JWT, no `userId` claim, an unexpected claim type), and nothing in its signature says so. Its callers trust it. `ActivitySecurityService.canAccessActivity` passes it straight to `studentRepository.findById(...)`, which throws on `null`, although the authorization managers' package documentation promises that "anything unresolvable is a denial, never an exception". Whether any real request reaches that path is a question for a test; NullAway's contribution is that the question can no longer hide. Writing `@Nullable Integer getUserId()` makes the compiler send you to every caller.

**Adopt it a package at a time.** Add `@NullMarked` to one package, fix or annotate what NullAway reports, and move on; unmarked packages are not checked. Two setup facts: Error Prone needs extra `javac` flags in `.mvn/jvm.config`, and its current releases need a recent JDK (JDK 22, or a JDK 21 update with type-annotation support; an early JDK 21.0.2 fails). Check the NullAway wiki for the pair of versions that matches your JDK.

### 4.9 Security: dataflow, dependencies, containers, secrets

**CodeQL follows untrusted data through the program.** It treats the code as a database and asks whether data from a **source** (a request parameter, a header) reaches a **sink** (a SQL string, an HTML response, a shell command) without passing a **sanitizer** (a parameterized query, an encoder). That is the shape of SQL injection, cross-site scripting, and command injection. On a public GitHub repository, turning on code scanning's *default setup* (Settings, Code security) scans Java and TypeScript on every pull request; Java needs no build step. Project Pulse's search code, such as `StudentSpecs`, builds queries through the JPA Criteria API, so Hibernate binds the user's text as a parameter and no SQL string is built from input: the sanitizer CodeQL looks for.

**CodeQL's first run on Project Pulse found one thing, and it is a false positive in context.** On `main` after #104, the scan of Actions, TypeScript, and Java opened a single alert, rated high: `java/spring-disabled-csrf-protection`, at `.csrf(csrf -> csrf.disable())` in [`SecurityConfiguration`](https://github.com/Washingtonwei/project-pulse/blob/main/backend/src/main/java/team/projectpulse/security/SecurityConfiguration.java). Cross-site request forgery gets a victim's browser to send a request carrying credentials the browser attaches by itself, usually a session cookie. Project Pulse has none to borrow: the frontend sends its token in an `Authorization: Bearer` header ([`request.ts`](https://github.com/Washingtonwei/project-pulse/blob/main/frontend/src/utils/request.ts)), and the server keeps no session (`SessionCreationPolicy.STATELESS`). That is the standard setup for a stateless token API, so the alert is dismissed with that reason, which is also the condition to recheck: the day the token moves into a cookie, the alert becomes true.

**Most of your code is other people's.** Project Pulse's backend declares 26 dependencies, and Maven resolves 263 once their own dependencies are counted. When Log4Shell (CVE-2021-44228) was published in December 2021, the vulnerable code was in nobody's own repository; it was in a logging library under almost every Java application. Dependabot reads `pom.xml` and `package-lock.json`, alerts on known vulnerabilities, and opens pull requests that update them. Turn it on once CI can catch a broken update. Project Pulse waits until its frontend job builds the app and blocks, because today an update that broke the frontend would still show a green check.

**A clean report can still miss the point.** Hadolint passes Project Pulse's [`Dockerfile`](https://github.com/Washingtonwei/project-pulse/blob/main/Dockerfile) with no findings, yet the runtime image has no `USER` line, so the application runs as root inside its container. Hadolint checks the instructions that are written; a missing one is invisible to it. Image scanners such as Trivy check the built image's packages and configuration, including the user.

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

**Secrets never belong in the repository.** GitHub's secret scanning finds committed keys, and push protection rejects a push that contains one. Turn both on (free for public repositories). A secret that reached a public repository is compromised even if you delete the commit: rotate it.

### 4.10 The frontend: ESLint, types, and formatting

**ESLint 8 reached end of life on 5 October 2024,** and Project Pulse still runs it with the old `.eslintrc.cjs` format. ESLint 9 made the flat configuration file (`eslint.config.js`) the default, and `eslint-plugin-vue` ships flat presets. Upgrading is a pull request of its own: config migration, then the rule changes it brings. An outdated analyzer is a finding too.

**`vue-tsc` is the frontend's compiler, and Project Pulse ships around it.** Its 18 type errors include passing a `string | undefined` where a `string` is required, in `UserRegistration.vue`. `npm run build` runs `vue-tsc`, but the deploy workflow calls `npm run build-only`, which skips it, so type errors reach production.

**Formatting is a decision, made once.** Prettier ends arguments about layout. Pick the configuration (Project Pulse's is in `.prettierrc.json`), reformat in one commit ([4.5](#45-adding-analyzers-to-a-brownfield-project-baseline-then-ratchet)), then make `prettier --check` part of the gate. Run the fixing variants (`eslint --fix`, `prettier --write`) on your machine; in CI run the checking variants, because a CI job that fixes code changes what it was asked to check.

## 5. The AI-native lens

- **Delegate to AI:** explaining an unfamiliar rule and why it fired; fixing findings with an obvious fix (an unused import, braces, a `Locale` argument); grouping a report by rule; drafting the baseline and the configuration; writing the test that shows a real finding is a bug.
- **Keep human:** every verdict that is not "fix it". A suppression, a rule turned off, and an entry kept in the baseline are claims about the codebase that someone must be able to defend. An agent may not add to a baseline or suppress a finding to make a build pass without saying so in the pull request.
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
| **Classic:** a compromised or upgraded tool changes what runs | Comparing finding counts across a tool upgrade; pinning versions | Pin Actions to commit SHAs; review tool updates like code |

## 7. Hands-on (studio + optional individual assignment)

**In class (Monday):** SpotBugs and PMD on Project Pulse from the command line, the report read by rule, three findings triaged live, a planted bug failing the gate, and NullAway on one package.

**Team, own project (Friday's studio):**

- **First run:** run the analyzers for your stack, record the counts by rule, and decide which rules your team turns off, with the reason in the configuration.
- **Gate:** make the checks fail your pull request build. Your repository is young, so triage everything and skip the baseline if you can; baseline only what you cannot finish today. Plant one bug and watch it fail.
- **Write it down** ([4.6](#46-on-a-new-project-the-gate-comes-first)): a "Static analysis" subsection in section 8.2 of your architecture-of-record, and a charter line citing it: the gate command, suppressions carry reasons, and a baseline only shrinks.

**Individual assignment:** [*Triage the analyzers*](../assignments/triage-the-analyzers.md) (assignment 4, due Fri Nov 13). Start from a copy of Project Pulse with the analyzers and baselines of #104, make four project-wide rule decisions, triage your slice of the baseline, fix the real findings (one shown by a test), suppress the rest with reasons, and shrink the baseline, with the pipeline green. The triage is the assignment.

## 8. Summary / key takeaways

- A tool that does not fail the build is decoration. Put every check in the pull request gate.
- Read a report by rule first. Most of it is a few rules that do not fit; the bugs are few.
- Every finding ends as a fix, a suppression with a checkable reason, or a rule turned off with its reason.
- On an existing codebase, baseline what exists and fail only on what is new. The baseline only shrinks.
- On a new project, turn the gate on before the first feature, and there is nothing to baseline. Record the setup in section 8.2 of the architecture-of-record, the rule in the charter, and each rule turned off in the tool's configuration.
- A null-aware type checker turns null dereferences into compile errors (NullAway in Java, `strictNullChecks` in TypeScript); adopt it a package at a time.
- The analyzer is the reviewer that reads all of the agent's code. The verdicts stay with you.

## 9. Key papers & further reading

- Sadowski, C., Aftandilian, E., Eagle, A., Miller-Cushon, L., and Jaspan, C. "Lessons from Building Static Analysis Tools at Google." *Communications of the ACM* 61(4), 2018.
- Bessey, A., et al. "A Few Billion Lines of Code Later: Using Static Analysis to Find Bugs in the Real World." *Communications of the ACM* 53(2), 2010.
- Johnson, B., Song, Y., Murphy-Hill, E., and Bowdidge, R. "Why Don't Software Developers Use Static Analysis Tools to Find Bugs?" ICSE 2013.
- Pearce, H., Ahmad, B., Tan, B., Dolan-Gavitt, B., and Karri, R. "Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions." IEEE S&P 2022.
- Banerjee, S., Clapp, L., and Sridharan, M. "NullAway: Practical Type-Based Null Safety for Java." ESEC/FSE 2019.
- Winters, T., Manshreck, T., and Wright, H. *Software Engineering at Google*. O'Reilly, 2020. Chapter 20, Static Analysis.
- Tool documentation: [SpotBugs](https://spotbugs.readthedocs.io/), [PMD](https://docs.pmd-code.org/latest/), [NullAway](https://github.com/uber/NullAway/wiki), [JSpecify](https://jspecify.dev/), [Spring null safety](https://docs.spring.io/spring-framework/reference/core/null-safety.html), [CodeQL](https://codeql.github.com/docs/), [ESLint](https://eslint.org/docs/latest/), [Dependabot](https://docs.github.com/en/code-security/dependabot).

## 10. Self-check

1. A first SpotBugs run on your team's repository reports 400 findings. What do you do in the first ten minutes, and what do you not do?
2. Give one Project Pulse finding of each verdict (real, false positive, not worth it) and say how each is recorded.
3. `@SuppressFBWarnings(value = "NP_NULL_ON_SOME_PATH_FROM_RETURN_VALUE", justification = "false positive")`. What is wrong with it, and what would a good justification say for `UserUtils.getUserCourseId`?
4. Your PMD baseline lists `TeamService=CompareObjectsWithEquals`. A teammate adds a new `==` comparison to `TeamService`. Does the build fail? What does that tell you about the baseline?
5. An agent's pull request turns the build green by adding twelve entries to the SpotBugs baseline. What do you ask for in review?
6. Your team starts a new repository. Where do you record which analyzers run, the gate command, and a PMD rule you turned off? Why not in the specification?
7. Why can NullAway catch the `null` that `UserUtils.getUserId()` returns when no test does?
8. Hadolint reports no findings on a Dockerfile whose image runs as root. Which rung of the ladder covers that, and with what tool?
9. Your workflow uses `actions/checkout@v4`. What changes if you write the commit SHA instead, and what keeps it up to date?

## Related

- [Testing](testing.md): the dynamic half; a real finding gets a test that shows the bug.
- [Code Review](code-review.md): what a human reviewer checks that no analyzer can.
- [AI-Assisted Implementation](implementation.md): the agent charter, where the gate command and the baseline rule go.
- [Schedule](../schedule.md): week 11, static analysis on Monday and CI/CD on Wednesday.
- [Triage the analyzers](../assignments/triage-the-analyzers.md): assignment 4, this module on Project Pulse.
