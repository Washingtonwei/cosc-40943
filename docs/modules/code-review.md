# Code Review

> **Purpose (one line):** _to be written when authored._


!!! note "This module is still being written"
    The course is being revamped this term, so modules go up as they are written rather than all at once. What is here is usable; the rest is coming. Lectures and studio do not depend on the missing parts.

## Drafting notes (raw: distribute into template sections, then delete before `stable`)

### Placement (`DECISION-code-review-week-8`)

Design review is already taught: [Design-of-Record](design-of-record.md) 4.13 owns the design gate's review questions and names the rubber stamp. This module owns review of **code**, which starts when the first implementation pull requests open in week 8 (the proving slice). Taught on a week 8 lecture day beside `MODULE-implementation`, best right after the agent builds something live so the room reviews what it just produced. First practiced in assignment 3 (self-review, below), then one review act in every later studio. Point back to 4.13 rather than reteaching it; the two share the rubber stamp and the "review against the contract" stance. Examined on the final, not the midterm.

The schedule's "Threaded through every week" list already says every studio reviews AI output. Through week 7 that is not yet true; this module is what makes it true.

### The spine: two questions every review answers

1. **Does this change do what the contract says?** The contract is the use case (every extension, not just the main flow), its business rules, and the design-of-record's API table and test list. A reviewer reading only the diff cannot answer this, because **a diff shows what was added and never what was left out.** A missing extension is invisible in the diff and visible in the test list.
2. **How deep must I read this part, given where it lands?** Depth is set by blast radius and reversibility, not spread evenly over every line. The reviewer writes that decision down (see "Risk-scaled depth" below), so a skim is a defensible choice rather than a hidden one.

### Research findings to teach (all checked 2026-10-04)

| Finding | Source | What a student does with it |
|---|---|---|
| Formal inspection (planning, preparation, meeting, rework, follow-up) finds defects but is too slow and synchronous for most teams; modern review is its lightweight, tool-based descendant. | Fagan 1976; history as told in Sadowski et al. 2018 | Know where the practice came from and why pull-request review replaced the meeting. |
| Finding defects is the top **expected** benefit, but reviews turn up fewer defects than developers expect; knowledge transfer, team awareness, and alternative solutions are major outcomes. Understanding the change is the reviewer's main difficulty. | Bacchelli and Bird 2013 | Review your teammates' code even where a bot reviews it too, because on a five-person team review is how anyone learns the parts they did not write. |
| About 75% of the defects reviews find are evolvability defects (readability, structure, maintainability), not functional ones. | Mäntylä and Lassenius 2009 | Hand style and structure to linters (week 10), then aim human attention deliberately at behavior and the contract, or human review finds little. |
| Low review coverage and low review participation are linked to up to two and five additional post-release defects per component, respectively. | McIntosh, Kamei, Adams, and Hassan 2014 (Qt, VTK, ITK) | The rubber stamp has a measured cost; a review counts only if the reviewer actually took part. |
| At Google: median change of 24 lines, median of one reviewer, median latency for the whole review under 4 hours; reviewers ask fewer questions as they learn the codebase, which the authors read as review's educational payoff. | Sadowski, Söderberg, Church, Sipko, and Bacchelli 2018 | Keep pull requests small. Review the same day. |
| Review effectiveness drops past roughly 200 to 400 lines per session, above about 500 lines per hour, and after 60 to 90 minutes. | SmartBear's Cisco study (Cohen 2006). **Vendor study, not peer reviewed; label it as industry data.** | An agent's 1,500-line pull request cannot be reviewed in one sitting. Ask for it split before reviewing it. |
| Participants with an AI assistant wrote less secure code than those without and were **more** likely to believe it was secure (47 participants, five security tasks). | Perry, Srivastava, Kumar, and Boneh, CCS 2023 | The author's confidence is not evidence, and an agent's self-rated confidence even less. |
| Automation bias and complacency: people over-rely on automated aids, and experts are affected as well as novices. | Parasuraman and Manzey 2010 | A green check from a review bot is the moment to stay alert, not the moment to approve. |
| LLM evaluators recognize their own outputs and rate them higher. | Panickssery, Bowman, and Feng, NeurIPS 2024. **Studied on summarization, not code; use as supporting evidence only.** | Review agent output with a fresh session that never saw the author's conversation. |

### Practices to teach (established practice, not research)

- **The approval standard.** Google's engineering practices: approve once the change definitely improves the overall health of the code, even if it is not perfect. Prefix optional polish with "Nit:" so the author knows it does not block.
- **Label every comment.** Conventional Comments (`issue`, `suggestion`, `question`, `nitpick`, `praise`, each blocking or non-blocking). This connects to 4.13's line that a useful comment is a specific question with a specific answer.
- **The author's half.** Small pull request; self-review before requesting review; a description that says what changed, which use case and design it implements, and how it was verified, shorter than the diff; the design-of-record updated in the same pull request if the code departed from it (4.13's stale-design row).
- **A checklist.** CMU 17-313's code-review lecture pairs review with risk and argues for checklists (Gawande's surgical checklist). Our checklist is short: the two spine questions, the triage line, the test-list check. Instructor source: `notes/cmu-17-313-notes.md`, "09-code-review-risk".

### Risk-scaled depth: trunk and leaf

Taken from a practitioner video (see the source note below) and kept because it answers the problem students face from week 8: the agent writes more code than they can read line by line. A rule that says "read everything" will be quietly ignored. A triage rule they can defend is better.

- **Trunk:** code many paths depend on, that changes behavior existing users rely on, or that is hard to roll back. Read every line.
- **Leaf:** new code reached only through the new feature, covered by its own tests. Read the tests' assertions and skim the rest.
- **The reviewer writes the triage into the review:** "Trunk: X, read in full. Leaf: Y, checked tests against test-list rows 3 to 7, skimmed the rest." This makes the depth decision visible and gradeable, and it is what stops "risk-based" from becoming a license to skim. A novice cannot triage a codebase they do not know, so the triage is a skill to be practiced, not assumed.

**Worked example on Project Pulse** (checked at `main` `a3e3abc`, 2026-10-04; re-check before `stable`). The week 8 `/implement` run on `docs/design/not.md` will add two routes, `GET /sections/{sectionId}/submission-status` and `POST /sections/{sectionId}/reminders`. Most of that pull request is leaf: a new controller method, a new service method, the dialog. The trunk part is **two lines in `security/SecurityConfiguration.java`**:

- That file holds one authorization rule per route, about 380 lines, and its API rules end with `.requestMatchers(this.baseUrl + "/**").denyAll()`. The code comment says why: a new endpoint "fails closed, loudly" until someone writes its rule. Spring Security applies the first matching rule, so where the new line sits relative to that catch-all, and to broader matchers above it, decides who can reach the route.
- The design's API table fixes the rule: `AuthorizationManagers.anyOf(sectionInstructorAuthorizationManager, sectionOwnershipAuthorizationManager)`, added before the `denyAll()` catch-all.
- **The failure to look for:** the agent's new integration test gets a 403, and the quickest way to make it pass is a looser rule. `.authenticated()` in place of `.access(...)` is a one-word change that lets any logged-in student trigger an email to an entire course section. The proof the reviewer checks is the design's test row "UC-NOT authorization": an instructor not assigned to the section and a student both get 403 on both routes, and the owning course admin gets 200.
- For scale: `system/Result.java` is imported by 19 files and `system/UserUtils.java` is referenced in 28. A change to either is trunk however small the diff.

The same file shows trunk reasoning written down: the comment on the actuator rules explains why they sit outside the API catch-all and would otherwise fall through to `.anyRequest().permitAll()` (tracked as `TD-actuator-exposure`).

### The author's half: proof in the pull request

The reviewer can read less code when the author brings proof, so the author's job is to bring it. Four kinds, strongest first:

1. **Tests**, mapped to rows of the design-of-record's test list, with assertions that check the contract (the oracle, from `MODULE-testing`). A row with no test is a gap the author names, not one the reviewer has to find.
2. **Existing behavior**: tests showing what users already rely on still works. Required for every trunk change.
3. **Runtime**: the feature used end to end, and what the author saw.
4. **Visual**: a screenshot or short video of what the user will see, for UI changes.

Then a statement of **what was verified and what was not**: what the author checked personally, what they took on trust from the agent or a tool, and what nobody checked. This is not a confidence score. "High confidence" is not evidence (Perry et al.), but "I did not test the email failure path" tells the reviewer where to look, and a reviewer can check it. It only works if grading rewards an honest "not verified" and never penalizes it; say so to the TAs.

A test that only echoes a mock's return value is not proof. `MODULE-testing`'s `ActivityServiceTest.testSaveActivity` example is the one to cite; do not reteach it here.

### Writing the description: what the standards agree on (checked 2026-10-04)

| Source | What a description must carry |
|---|---|
| Google, "Writing good CL descriptions" | An imperative first line that stands alone in history; a body with **what** and **why**, why this approach, shortcomings, and links; enough context to survive dead links. Review the description before sending. |
| Linux kernel, "Submitting patches" | The **problem**, its user-visible **impact**, then the solution; imperative mood; stands alone. One logical change per patch: "If your description starts to get long, that's a sign that you probably need to split up your patch." Quantify trade-offs. |
| GitHub Docs, "Helping others review your changes" | Small, focused pull requests; purpose, overview, and links; **the type of feedback you need** and which files to read first; review, build, and test your own pull request first. |
| Microsoft, Code-With Engineering Playbook | One goal per pull request; does not break the build; includes tests; Conventional Commits for titles; no fixed template. |
| AWS CDK's template | Issue, reason, description of changes (with alternatives rejected and design decisions), new permissions, **how you validated**. |
| Alibaba | No public company-wide standard found. Its open-source projects (Nacos) use *purpose of the change*, *brief changelog*, *verifying this change*, with an issue required first. |

**Research.** Pirouzkhah, Wurzel Gonçalves, and Bacchelli (2026) derived eight recommended elements from industry guidelines and tested them on 80,000 pull requests across 156 projects. Only 13.7% explained their tests. An explanation of the code changes was associated with a 12 to 20% higher merge likelihood, and stating the type of feedback needed with 64 to 72% higher likelihood plus more reviewer comments (correlation, not cause). Surveyed developers rated purpose, reason, and issue link as the elements that matter on nearly every pull request. For agent-authored pull requests, Siddiq et al. (2026) found rejection more strongly associated with complexity and **verbosity** than with security topics: the practitioner video's complaint, measured.

**The convergence:** why, what changed (summarized, not narrated), how it was verified, and where the reviewer should focus. The length rule comes from the sources too: one logical change, and a description that will not fit on one screen means the pull request should be split.

**The template** is [`.github/PULL_REQUEST_TEMPLATE.md`](https://github.com/tcu-cosc-40943/course-templates/blob/main/.github/PULL_REQUEST_TEMPLATE.md) in the course templates repository, copied into each team repository in week 8. One template for code, specification, and design pull requests: an imperative title, `Closes #`, `Traces to:` (use case, business rule, or design), then **Why**, **What changed**, **How it was verified** (with visible **Verified:** and **Not verified:** lines), and **Reviewer focus**. Design choices worth teaching:

- **The examples live in HTML comments**, which do not appear in the posted description. That is how one template covers code (tests mapped to the test list, existing behavior, runtime, screenshot), specification (the source and what else was updated to stay consistent), and design (the questions test, [Design-of-Record](design-of-record.md) 4.13, in a collapsed `<details>` block the length limit does not count) while the posted description stays four short sections.
- **Why stays, even with `Closes #`.** Google and the kernel both require the description to stand alone, because it outlives links and is read for years. One or two sentences.
- **Short answers, not checkboxes.** "☑ A fresh reviewer reviewed the diff" costs one click and proves nothing. The agent review goes under How it was verified as what it found and what the author did about each.
- **Reviewer focus** is the author's half of the trunk-and-leaf triage and the "type of feedback needed" element the research found most predictive. For a design, it names the decisions most likely to be wrong and any change to the architecture-of-record. The reviewer still makes their own call.
- **AI verbosity is fixed with context, not willpower.** Each team's `CLAUDE.md` gets: "Pull request descriptions follow `.github/PULL_REQUEST_TEMPLATE.md`: at most three lines per section (a design's questions-test list goes in a collapsed `<details>` block, outside the cap), and never restate the diff." Project Pulse's `CLAUDE.md` carries the same line, and its `/design` and `/implement` commands draft to the template. The agent reads the template from the repository, so the rule applies where the long descriptions are written.

Adapted, not copied, from the practitioner video's template and proof list (source note below): kept the proof kinds and "what stayed unchanged"; added the trace line and the test-list mapping; turned his checkboxes into answers; dropped the self-rated confidence.

### AI-native lens seeds

- **Delegate:** the first pass to a review agent running in a fresh context (for example Claude Code's `/code-review`, or a new session given only the diff, the use case, and the design); style and formatting to linters.
- **Keep human:** the triage, the check against the use case and test list, every trunk line, and the decision to approve.
- **Context to supply the review agent:** the use case, its business rules, and the design-of-record. Never the author's conversation.
- **How to verify the review agent:** spot-check one of its findings and one thing it passed. If its review never mentions the test list, it reviewed the diff, not the change.

### Agent review: what Claude Code offers (checked 2026-10-05 against code.claude.com)

Three products share the "Claude reviews my pull request" idea. Teach the first, show the second on one slide, skip the third.

| | Local `/code-review` | Code Review (managed) | GitHub Actions `@claude` |
|---|---|---|---|
| Trigger | The student types `/code-review`, optionally with a target (`/code-review 42`, a branch, a path) | Automatic on a pull request, or a top-level comment `@claude review` (`always` subscribes the pull request to a review on every push) | A comment mentioning `@claude`, or a workflow on `pull_request` |
| What runs | A background subagent with its own context. Effort `low` and `medium` report only high-confidence findings; `high` to `max` widen coverage and admit less certain ones; `ultra` sends it to a deeper multi-agent cloud review | Several agents in parallel, each hunting one class of defect, then a verification step that checks each candidate against the code before it is posted | Claude Code on a GitHub runner, usually the same code-review plugin |
| Output | Findings in the terminal; `--comment` posts them inline on the pull request; `--fix` applies them | Inline comments marked 🔴 Important, 🟡 Nit, 🟣 Pre-existing, and a check run that always ends neutral, so it never approves or blocks | Comments on the pull request |
| Reads | `CLAUDE.md`, not `REVIEW.md` | `CLAUDE.md` (violations become nits) and `REVIEW.md` (review-only rules: what counts as Important, nit caps, skip paths, checks for every pull request) | `CLAUDE.md` |
| Cost and access | Any Claude Code plan, so every student has it | Team and Enterprise only, research preview, about $15 to 25 per review billed on top of the plan | Any plan, but a repository secret (one person's subscription token or an API key) and GitHub Actions minutes |

**Why the local command for students:** it is the only one all 77 already have. The managed product at 13 teams and several pull requests each is hundreds of dollars on a plan the students are not on; the Actions route ties a team's reviews to one student's subscription token.

**Fresh context, confirmed.** `/code-review` runs as a skill with `context: fork`, which the skills documentation says "doesn't see your conversation history" and is not a fork of the conversation. So it can be run from the session that wrote the code without inheriting the author's reasoning. It still reads what the author left in the repository, including an agent-written pull request description; the reviewer agent sees the author's claims there, just as a human reviewer does.

**What to teach about it: the default reviews the diff, not the change.** The managed reviewer's documentation says it "focuses on correctness... not formatting preferences or missing test coverage." That is spine question 1 turned around: a missing extension is invisible in the diff, so an agent given only the diff will not find it. The fix is context, the week 5 lesson applied to review: give the review the use case and the test list (point it at them in the target text, or put the rule in `CLAUDE.md`; on the managed product, in `REVIEW.md`). Project Pulse's version of a `REVIEW.md` rule: "every new route under the API base URL has an authorization rule above the `denyAll()` catch-all, and the design's authorization test row has a test."

**The neutral check run is a design worth naming.** Anthropic's own reviewer is built so it cannot approve a pull request. The human approves. This is the automation-bias finding (Parasuraman and Manzey) turned into product design.

**Pace of change.** The documentation records behavior changes by version (`/review` merged into `/code-review` at v2.1.223; `@claude review` stopped subscribing to every push in July 2026). Teach the pattern (a fresh-context reviewer, given the contract, whose findings a human triages) with Claude Code as the instance; keep exact commands on the [Agent Setup](../agent-setup.md) page, not in the module text, and re-check them before each offering.

### Risks seeds

| Risk | Human judgment that catches it | Mitigation |
|---|---|---|
| The rubber stamp: approval without reading. AI amplifies it with long, plausible pull requests. | A reviewer who writes the triage line and checks the test list | Triage line required in every review; TAs sample review comments |
| Reviewing the diff instead of the change: the missing extension is not in the diff. | Reading the test list beside the diff | Pull request description links the use case and design; review comments cite test-list rows |
| The author agent reviews itself and agrees with itself. | Noticing the review shares the author's context | Fresh-context review session; a teammate who did not write it approves |
| An oversized agent pull request. | Refusing to review past about 400 lines in one sitting | Split by use case step or layer before review |

### Hands-on seeds

- **Studio:** pairs review each other's implementation pull requests from the proving slice. Every review carries the triage line, one comment per test-list row it checked, and labeled comments. The TA reads two reviews per team.
- **Individual assignment: a part of assignment 3, "Add a use case" (due Fri Oct 16), not a new assignment.** Before submitting, the student reviews the agent's pull request and writes the review into it: the trunk-and-leaf triage line, each row of the use case's test list marked covered or not, and at least one labeled comment on something they changed or rejected. Graded on whether the triage is right and the test-list check is honest, not on how many comments there are.
- **In-class exercise (week 8 lecture): a seeded pull request** with one trunk defect (a loosened security rule), one missing extension, one tautological test, and several nits. The room finds what matters and declines to block on the nits. Build and check the seeded pull request before the lecture.
- **Live demo after the room's review: the agent on the same seeded pull request, twice.** First `/code-review <PR#>` with nothing else; then again with the use case and test list named in the target text. Put both finding lists beside the room's. Expected (not yet observed): the first run catches the loosened rule and misses the extension; the second finds the extension. Rehearse both runs before class and keep screenshots, because the output varies between runs and a live miss of the wrong kind would teach the wrong thing.
- **Assignment 3 self-review gains one step:** run `/code-review` on the pull request and record, under How it was verified, each finding and what was done about it (fixed, rejected with a reason). The student's own triage line and test-list check stay theirs; the agent's findings are input to them.

### Self-check seeds

1. A diff adds a controller, a service method, a Vue dialog, and one line to `SecurityConfiguration`. Which part do you read in full, and why?
2. Your teammate approved a 1,200-line agent pull request in six minutes. Name two research findings that say what that review is worth.
3. Why is a missing use case extension easier to find from the test list than from the diff?
4. The review bot passed the change. What do you still check yourself?

### Source note: a practitioner video, filtered

"How I Review AI Code" (a senior staff engineer at Meta), YouTube, <https://www.youtube.com/watch?v=b2QkhmQ0sT0>. One practitioner's opinion, not evidence. If assigned, it is an optional watch with the prompt: what is missing from his idea of proof?

- **Kept:** review depth scaled by blast radius (trunk and leaf); a fresh-context adversarial review agent (the same principle as the design gate's questions test); style nits handed to linters (consistent with Mäntylä and Lassenius); the author attaching proof (tests, runtime, visual) and a pull request template, adapted as described above; pull request descriptions shorter than the diff; merge-ready is not launch-ready (weeks 12 and 13); his closing point that knowing the codebase is what makes triage possible.
- **Dropped:** the agent's self-reported confidence as proof; "AI already reviews better than most humans" (asserted, not shown); canary releases and A/B tests (student projects lack the traffic; a boolean feature flag is worth one sentence); proof that the code runs, with checking against the spec left to the end.
- **Missing from it, supplied above:** checking against the spec; review's knowledge-transfer role.

### Source note: Willison's agentic engineering patterns, filtered

Simon Willison, *Agentic Engineering Patterns*, a living guide begun 2026-02-23 with no per-chapter dates (read 2026-10-04). One practitioner, writing mostly as a solo open-source developer. Assign two chapters as reading for week 8; neither replaces anything above.

- **"Anti-patterns: things to avoid."** The rule is "Don't file pull requests with code you haven't reviewed yourself": an unreviewed agent pull request hands the author's work to the reviewer. His list for a good pull request (it works and you are confident it does, small, context and links, show your work with test notes or screenshots) is the author's half above, from a different source. Quote one line on a slide: "Agents write convincing looking pull request descriptions. You need to review these too!" It argues for the **Verified** and **Not verified** lines.
- **"Writing code is cheap now."** Writing code got cheap; good code did not. His nine properties of good code (works, verified, solves the actual problem, handles errors, simple, regression-tested, documented, changeable, meets its quality attributes) are a candidate reviewer checklist; map them to the two spine questions rather than adding a third list.
- **Dropped:** "fire off a prompt anyway" when a feature seems not worth building. It assumes free tokens; students work on their own subscriptions under `ai.md`'s credit budgeting. Say so when assigning the chapter.
- **Missing from it:** the spec. His review checks that code works, not that it is the right code against the use case and test list.

### Further reading (to verify links before `stable`)

- Michael E. Fagan, "Design and Code Inspections to Reduce Errors in Program Development," *IBM Systems Journal* 15(3), 1976.
- Alberto Bacchelli and Christian Bird, "Expectations, Outcomes, and Challenges of Modern Code Review," ICSE 2013.
- Mika V. Mäntylä and Casper Lassenius, "What Types of Defects Are Really Discovered in Code Reviews?" *IEEE TSE* 35(3), 2009.
- Shane McIntosh, Yasutaka Kamei, Bram Adams, and Ahmed E. Hassan, "The Impact of Code Review Coverage and Code Review Participation on Software Quality," MSR 2014.
- Caitlin Sadowski, Emma Söderberg, Luke Church, Michal Sipko, and Alberto Bacchelli, "Modern Code Review: A Case Study at Google," ICSE-SEIP 2018.
- Neil Perry, Megha Srivastava, Deepak Kumar, and Dan Boneh, "Do Users Write More Insecure Code with AI Assistants?" CCS 2023.
- Raja Parasuraman and Dietrich H. Manzey, "Complacency and Bias in Human Use of Automation," *Human Factors* 52(3), 2010.
- Arjun Panickssery, Samuel R. Bowman, and Shi Feng, "LLM Evaluators Recognize and Favor Their Own Generations," NeurIPS 2024.
- Google, "The Standard of Code Review," in *Google Engineering Practices*, <https://google.github.io/eng-practices/review/reviewer/standard.html>.
- Conventional Comments, <https://conventionalcomments.org>.
- Google, "Writing good CL descriptions," in *Google Engineering Practices*, <https://google.github.io/eng-practices/review/developer/cl-descriptions.html>.
- The Linux kernel, "Submitting patches: the essential guide to getting your code into the kernel," <https://docs.kernel.org/process/submitting-patches.html>.
- GitHub Docs, "Helping others review your changes," <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/helping-others-review-your-changes>.
- Microsoft, "Pull Requests," in the *Code-With Engineering Playbook*, <https://microsoft.github.io/code-with-engineering-playbook/code-reviews/pull-requests/>.
- AWS CDK pull request template, <https://github.com/aws/aws-cdk/blob/main/.github/PULL_REQUEST_TEMPLATE.md>; Alibaba Nacos pull request template, <https://github.com/alibaba/nacos/blob/develop/.github/PULL_REQUEST_TEMPLATE.md>.
- Simon Willison, "Anti-patterns: things to avoid" and "Writing code is cheap now," in *Agentic Engineering Patterns*, <https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/> and <https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/>, read 2026-10-04.
- Anthropic, "Code Review" (including "Review a diff locally"), "Claude Code GitHub Actions," and "Skills" (running skills in a subagent), in the Claude Code documentation, <https://code.claude.com/docs/en/code-review>, <https://code.claude.com/docs/en/github-actions>, <https://code.claude.com/docs/en/skills>, read 2026-10-05.
- Shirin Pirouzkhah, Pavlína Wurzel Gonçalves, and Alberto Bacchelli, "The Value of Effective Pull Request Description," 2026, <https://arxiv.org/abs/2602.14611>.
- Mohammed Latif Siddiq, Xinye Zhao, Vinicius Carvalho Lopes, Beatrice Casey, and Joanna C. S. Santos, "Security in the Age of AI Teammates: An Empirical Study of Agentic Pull Requests on GitHub," 2026, <https://arxiv.org/abs/2601.00477>.
