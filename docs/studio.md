# Friday Studio

Friday is not a lecture and not a lab on a toy problem. It is the hour your team works on **your own client project**, in the room, with a TA who knows your project.

## How it runs

- Same room, same time, whole class. Thirteen teams work in parallel, seated in three zones by TA. You sit in the same zone every Friday.
- **Each TA owns four or five teams for the entire semester.** You get the same TA every week, at every checkpoint. They know your project's history, which is the point.
- Every studio has **one scoped objective**, summarized on the [Schedule](schedule.md) and set out in full [below](#each-studio). It is the move you saw demonstrated on Project Pulse in Wednesday's lecture, now applied to your code.
- TAs circulate. They are there to unblock and to review, not to lecture.
- **On three Fridays, studio is your checkpoint presentation** to your TA. That week's objective moves to out-of-class team time, and [the checkpoints](project.md#checkpoints) say what you present. Checkpoint 2 is the exception: you book it with your TA outside class in week 11.

Attendance in studio counts the same as lecture attendance: each absence is a 1% grade reduction.

## Teaching assistants

Led by **Hiep Nguyen**. Each TA takes four or five of the thirteen teams and keeps them all semester.

| TA | Email | Teams |
|---|---|---|
| Hiep Nguyen (lead) | HIEP.N.NGUYEN@tcu.edu | 1, 2, 5, 9, 13 |
| Ali Gasimli | A.GASIMLI@tcu.edu | 3, 6, 10, 12 |
| Yuv Raj Pant | YUV.RAJ.PANT@tcu.edu | 4, 7, 8, 11 |

Team numbers are on the [Teams page](teams.md).

## Where your repository lives

**One member owns it, under their own GitHub account.** Name that person before you create anything, and write their name and the repository URL into your contract's header.

- The repository is **public**, named `cosc-40943-team-NN-<slug>` to match your brief on TCU Online. Create it with a README so it has a `main` branch from the start. Public means your client's material does not go in it: see [what belongs in the repository and what belongs in Drive](project.md#what-you-deliver-this-fall).
- The owner invites **every other member, all three TAs, and the instructor** as collaborators: nine people for a team of six, eight for a team of five. A personal repository gives every collaborator write access, which is what you want.
- **A Project's access list is separate from the repository's.** Everyone can be on the repository and still be unable to move a card. After you create the Project and link it, the owner adds the team and your TA under the Project's own settings. This is the step teams forget, and your TA checks it from an account that is not the owner's.
- **The owner has to be someone continuing into COSC 40993 in the spring.** If they leave the course, transfer the repository before they go. Everyone clones on day one, so no single account is ever holding your history hostage.

Once it exists, the owner turns on branch protection and the merge settings in the [Git Workflow](git-workflow.md#repository-settings) page. Everyone else reads that page before their first branch.

Environment setup is not studio work. Getting Project Pulse running on your own machine is [assignment 1](assignments/hello-project-pulse.md), and the [setup steps](resources.md) are the place to start if yours still does not run. With 77 students and three TAs, studio cannot absorb cold installations.

## Where your requirements documents live

**In your team repository, under `docs/requirements/`, next to your code.** Not in Google Drive, not in a shared document. Your AI teammate reads your repository and nothing else, so a specification it cannot open is a specification it cannot build from.

Blank templates are in [course-templates](https://github.com/tcu-cosc-40943/course-templates). Copy them in once and they are yours from then on. `traceability.md` lands one level up, at `docs/traceability.md`, because from week 8 it maps design, code, and tests as well as requirements:

```bash
git clone https://github.com/tcu-cosc-40943/course-templates.git
cd your-team-repo
mkdir -p docs
cp -r ../course-templates/requirements docs/
cp ../course-templates/traceability.md docs/
```

If you copied `requirements/` in week 3, run only the last line.

Copy them, do not fork. Each file opens with instructions telling you what the section is for, how to produce it, and how to check it; leave those in place until the document is finished, because they are context for your agent on every later pass. The [Requirements as the Contract](modules/spec-driven-requirements.md) module is the reading behind them.

One of them is used before a client meeting, not in studio. `client-interview-guide.md` is your script for each client meeting and the record of what was said in it. Work it with your agent beforehand, take it into the meeting on the scribe's laptop, and commit it the same day as `client-interview-YYYY-MM-DD.md`, one file per meeting. Your repository is public, so the record names people by role, never by name, and carries no contact details or anything the client asks you to keep private; those go in your Drive ([why](project.md#what-you-deliver-this-fall)). Everything it leaves unanswered becomes an entry in `OPEN-ISSUES.md`.

## The Napkin drill

Rounds 0 and 1 ran in weeks 3 and 5; the drill is paused for the rest of the term ([schedule](schedule.md#the-napkin-drill)). **[The frame and its rubric stay in the module](modules/se-and-ai.md#the-napkin-six-prompts)**, and its one rule still applies before any agent session: **write yours first, then ask the agent, then diff.** Prompting first anchors you on the agent's answer.

## What studio is not

- It is not a substitute for your team's working meetings. Fifty minutes a week does not build a product.
- It is not office hours for the exams.
- It is not a place to start the week's work from zero. Arrive having read the objective.

## Each studio

One section per studio, in date order. If you missed one, the section says what your team did and what it produced; your repository is the record of it. What each checkpoint reviews is on the [Project](project.md#checkpoints) page; a checkpoint Friday gets a section here when the hour also has work in it, as Sep 4 and Oct 2 do. Fridays with no studio are marked on the [Schedule](schedule.md).

### Week 2, Sep 4: your team's first hour

**Objective:** a meeting slot, a signed contract in a repository, and a client meeting requested, all by minute 50. This is [Checkpoint 0](project.md#checkpoints), verified in the room rather than presented.

**Before you arrived:** read your client brief on TCU Online, and finish [assignment 1](assignments/hello-project-pulse.md), due that morning.

| When | What your team did |
|---|---|
| 0-6 | Found your team in your TA's zone. |
| 6-15 | Names, contact details, the Slack channel. Then fixed the recurring weekly meeting time. |
| 15-25 | Stood up the repository and the Projects board, in the order under [Where your repository lives](#where-your-repository-lives). |
| 25-33 | Read the brief together, wrote the three questions to ask the client first, and sent the meeting request. |
| 33-45 | Filled in the [team contract](team-contract.md) as `docs/team-contract.md`. Each member signed it in the browser, in their own commit. This was the one time anyone committed straight to `main`. |
| 40-50 | Your TA cleared Checkpoint 0, while the last signatures landed. Teams already clear opened their first two issues from the brief. |

**What you produced:** `docs/team-contract.md`, signed; the repository, Projects board, and Slack channel, with your TA and the instructor on each; a sent client meeting request with a date proposed.

**How your TA checked it:** one signature commit per member, from that member's own account; clause 1 names a day and a time ("Tuesdays" fails); clause 7 says what actually happens when someone does not deliver; the TA and instructor are collaborators and the Project opens for someone who is not the owner; the meeting request was sent, not drafted.

The repository you stood up is where everything after this lives, starting the next Friday.

### Week 3, Sep 11: Napkin round 0, then the first requirements

**Objective:** your team's first hour on your client's requirements: Napkin round 0 on your own project, then the first draft of `docs/requirements/`, written on branches through pull requests. The hour was also the deadline to register in Project Pulse.

**Before you arrived:**

- The repository owner turned on branch protection for `main` with "Require status checks to pass" left off, following [Git Workflow](git-workflow.md#repository-settings).
- A team that had met its client committed its notes as `docs/requirements/client-interview-YYYY-MM-DD.md`.
- Everyone brought a laptop and the client brief.

| When | What your team did |
|---|---|
| 10 min | [Napkin](#the-napkin-drill) round 0 on your own project, committed as `docs/napkin-round-0.md` and sealed. |
| 25 min | Copied the [templates](#where-your-requirements-documents-live) in and drafted, one person per section, each on its own branch and pull request: Background, Business Opportunity, Business Objectives (each with a number), Vision Statement, Glossary, and `OPEN-ISSUES.md`. |
| By 10:50 | Pull requests merged, with commits from every member. |

Three rules for the drafting: expect merge conflicts in `vision-and-scope.md` and resolve them locally; do not finish the document; do not invent content, and put anything you do not know in `OPEN-ISSUES.md`. A vision and scope generated by AI that nobody read fails.

**Project Pulse registration closed at 10:50.** The invitation came from peer.evaluation.tool.senior.design@gmail.com, which also sends the weekly activity report and peer evaluation reminders every Monday and Tuesday. Late submissions are not accepted, so keep that address out of junk: mark it "Not junk" and add it to Safe senders (Outlook on the web: Settings, Mail, Junk email, Safe senders and domains). If you never received the invitation, tell your TA.

**What you produced:** `docs/napkin-round-0.md`, sealed; the six sections in `docs/requirements/`; commits from every member; a Project Pulse account.

**How your TA checked it:** branch protection is on, business objectives carry numbers, commits come from more than one member, and every member is registered in Project Pulse.

**Then week 4, with no studio.** The rest of vision and scope, the feature list, the use cases, the business rules, and the start of the specification were team work in your own meeting slot, to be checked at the next studio.

### Week 5, Sep 25: finish the specification for Checkpoint 1

**Objective:** bring your specification to what [Checkpoint 1](project.md#checkpoints) reviews on Oct 2, and have your TA review one use case with you. This is the supervised hour week 4's work did not get. Checkpoint 1's other half, the architecture-of-record, comes from week 6's lectures and is drafted in the [Oct 2 studio](#week-6-oct-2-checkpoint-1-and-your-architecture-of-record).

**Before you arrive:** your TA checks week 4's work on GitHub before class. Check it yourself first:

- [ ] `docs/requirements/` exists and has your content, not only the blank templates.
- [ ] Your use cases came in through pull requests, not straight commits to `main`.
- [ ] `business-rules.md` has at least one rule, with a source.
- [ ] Each use case lists the `BR-*` identifiers that govern it in its **Business Rules** field, and the quality attributes that apply in **Associated Information**.
- [ ] `docs/traceability.md` exists. See [the copy command](#where-your-requirements-documents-live) if it does not.

**Pick your riskiest use case before class**, the one most likely to break your architecture or surprise your client. It is the one your TA reviews, and the one you build first.

| When | What your team does |
|---|---|
| 0-3 | Your TA tells you what the pre-class check found. |
| 3-8 | The frame, from the front: what Checkpoint 1 reviews, and how to split the hour. |
| 8-50 | **Work the specification**, one owner per piece, one branch and one pull request each. Your TA sits with each of its teams for about eight minutes to review your riskiest use case. |

What to work on, as the [week 4 team work](modules/spec-driven-requirements.md#7-hands-on-studio-optional-individual-assignment) split it:

- **Glossary and vision and scope:** finish the sections week 3 left open, and bring both up to date with what your client meetings changed.
- **Use cases:** every one written in full, extensions included.
- **Business rules:** a source for every rule, and each rule's identifier in the Business Rules field of every use case it governs.
- **Constraints and quality attributes** in the specification, each quality attribute with a number and a way to measure it.
- **Both tables in `docs/traceability.md`**, with their checks.
- **`OPEN-ISSUES.md`:** everything only your client can answer, as the agenda for your next client meeting.

**The use case review.** Your TA reads your riskiest use case with you against the checklist at the bottom of the use case template, most common failure first:

1. Is there at least one extension per step that can fail?
2. Can the system test every precondition?
3. Does every business rule appear as an identifier only?
4. Does every step alternate actor and system?
5. Does the name start with a verb?
6. Could a tester write test cases from this without asking you anything?

**What you produce:** merged pull requests that move each piece forward, and the reviewed use case revised by pull request before Checkpoint 1.

**How your TA checks it:** the pre-class check, the six questions on your riskiest use case, and commits from every member.

The use case your TA reviews is also your first build-context, in [week 8](#week-8-your-first-build-context-in-your-team-meeting).

### Week 6, Oct 2: Checkpoint 1, and your architecture-of-record

**Objective:** your TA reviews your specification with you, which is the first half of [Checkpoint 1](project.md#checkpoints), and your team drafts its architecture-of-record, the second half. The reading is [Software Architecture, Just Enough](modules/architecture.md), and [assignment 2](assignments/spec-a-feature.md) is due before class the same morning.

**Before you arrive:**

- Copy the architecture template into your repository. From the root of your team repository, with the [course templates](https://github.com/tcu-cosc-40943/course-templates) cloned beside it:

    ```bash
    git -C ../course-templates pull
    mkdir -p docs/design
    cp ../course-templates/design/architectural-design.md docs/design/
    ```

    The first line updates the copy you cloned in week 3. If you never cloned it, run `git clone https://github.com/tcu-cosc-40943/course-templates.git` beside your team repository first.

- Section 9 of your specification has a number in every quality attribute. The architecture's requirements table is built from them.
- Your use case areas are settled: listed at the top of the Use Case List in `use-cases.md`, with every use case in one. Every area gets a row in the architecture.

    Your TA checks these two on GitHub before class. A team that fails either fixes it first, in the room, before starting the architecture.
- Read Project Pulse's [architecture-of-record](https://github.com/Washingtonwei/project-pulse/blob/main/docs/design/architectural-design.md): its Quality Goals, its architecturally significant requirements, and `KD-modular-monolith`, `KD-relational-graph`, and `KD-vertical-slices`.

| When | What your team does |
|---|---|
| 0-3 | Your TA tells you what the pre-class check found. |
| 3-8 | The frame, from the front: what the weekend check reads, and the order to fill the template in. |
| 8-50 | **Draft the architecture-of-record**, one owner per section, one branch and one pull request each. Your TA sits with each of its teams for about eight minutes to review the specification. |

**The specification review.** Your TA reads your specification with you against what Checkpoint 1 names: glossary, vision and scope, use cases, business rules, and the draft specification. It starts from the riskiest use case reviewed on Sep 25 and whether its revision landed.

**The order to draft in.** The template marks what is due now: sections 1 through 5, section 8 (both 8.1 and 8.2), and section 9. Start with the ranked table of architecturally significant requirements (section 9.1), because every other section cites it. Then the context diagram, the container diagram, and the component table, running the two checks at its end, then section 8.1, which names the trust boundary in writing. Then section 8.2: one short subsection for every concept in its table, each a rule in one sentence and the reason for it. The file that shows each rule done right comes later, once there is code; do not invent one. 8.2 is the part most teams finish after the hour, before the deadline. Write `KD-deployment-shape` last, with the requirement that would have forced the other answer. Your agent draws the diagrams; the ranking and the decision stay with the team.

**What you produce:** `docs/design/architectural-design.md`, merged to `main` by **11:59 pm Friday**. Whatever is on `main` then is what your TA reads.

**How your TA checks it,** over the weekend, with feedback as one issue in your repository by **8 pm Sunday**:

1. Every use case area in `use-cases.md` has a row in the component table (section 5.2).
2. Every external system on the context diagram appears in some "Depends on" cell.
3. The requirements table (section 9.1) reuses your specification's identifiers and includes at least one `SEC-*`.
4. `KD-deployment-shape` cites the requirement that drives it and names a rejected alternative.
5. Section 8.1 names the trust boundary and answers all three questions: how users authenticate, what each role may see beyond its role, and where sensitive data lives.
6. Nothing is designed below responsibility: no endpoints, no classes, no columns. (A convention in 8.2 that every endpoint follows, such as a URL prefix or an error format, is a rule, not a design, and passes.)
7. Section 8.2 has a subsection for every concept in its table, each with a one-sentence rule and the reason for it.

Fix what the issue raises by pull request, and close the issue from it. Week 7's design-of-record builds on this map from Monday.

### Week 8: your first build-context, in your team meeting

**Friday Oct 16 is a lecture this term, not a studio.** Run this hour in your team's own meeting after Wednesday's lecture, and finish it **by Sunday Oct 18, 11:59 pm**, before your agent builds the proving slice. There is no frame from the front: this page is the frame. Your TA checks it on GitHub and replies on each issue by Tuesday Oct 20.

**Objective:** each pair on your team writes one use case up as a build-context, an issue that cites the use case instead of copying it, runs the questions test on it, and sorts the gaps it exposes before building. The reading is [Context Engineering](modules/context-engineering.md), sections 4.5 and 4.7, and your individual practice run was [assignment 2](assignments/spec-a-feature.md).

**Before your meeting:** at least one member of each pair has a working agent session on a laptop they are bringing. Your riskiest use case is your proving slice, designed in week 7 and due running at [Checkpoint 2](project.md#checkpoints). Your charter carries a one-line rule, citing section 8.2 of your architecture-of-record, for at least **error handling** and **time** ([why](modules/architecture.md#410-crosscutting-concepts-what-every-component-does-the-same-way)). Your build-context cites them; it does not restate them.

| When | What your team does |
|---|---|
| 0-5 | Read this section together. |
| 5-22 | **Write the issues, in pairs.** The pair with your riskiest use case takes it; the other pairs take the next two. A team of five runs a pair and a trio. One person writes, the other checks that the use case exists at the path you gave and that its Business Rules field is filled in. |
| 22-38 | **Run the questions test, in pairs,** then sort what comes back. |
| 38-50 | **Pool as a team.** Each pair reads out its specification pile. Questions only your client can answer go into `OPEN-ISSUES.md`. Each pair posts its sorted list as a comment on its issue. |

**The issue cites the use case, and the use case cites the rest.** Its Business Rules field carries the `BR-*` identifiers and its Associated Information carries the quality attributes, so the issue does not list them again; a second list goes stale the same way a pasted use case does. Project-wide constraints (the stack, the hosting, the client's systems) belong in your charter, which the agent reads every session. Open the issue on your board and fill in this skeleton. Anything longer than a line or two under "Not yet in the specification" belongs in the specification: write it there, then cite it.

```markdown
## Build-context: UC-<AREA>-<slug>

**Realizes:** UC-<AREA>-<slug> (docs/requirements/use-cases.md)
**Touches:** <paths you expect it to change, or "new:" and the path>

### Not yet in the specification
<Decided, but not written down anywhere yet.>

### Estimate
clarify and design <low>–<high> h, build and review <low>–<high> h, verify <low>–<high> h
```

Do not paste the use case in. A pasted use case is a second use case, and one of them goes stale.

**The questions test.** Open your agent at the root of your team repository, switch to plan mode (Shift+Tab in Claude Code), paste in the issue body, and then this:

```text
Read the use case this issue cites and everything it references.
Before writing any code, list every assumption you would have to
make to implement it: rules, thresholds, terms, data, who may do
what, and which files you would change. For each one, say whether
you found it in the repository (and where) or had to invent it.
```

Agreeing with the list is not the output. A decision on each invented assumption is. Sort every one into a pile:

- **Specification.** A rule, a threshold, or a term that should be written down where your client can see it. Usually the biggest pile. A new rule goes in `business-rules.md` and its identifier goes in the use case's Business Rules field; a rule that exists but the use case never cited needs only the second edit.
- **Charter.** A convention or project-wide constraint about how the project runs, for your `AGENTS.md`, because the agent reads it every session.
- **Issue.** True of this task only.

If everything landed in the issue pile, go around again.

**What you produce:** one issue per pair on your board, with its sorted list as a comment, and new entries in `OPEN-ISSUES.md`. Close the specification and charter piles by pull request before the agent builds from the issue. Then the use case's owner fills in the Estimate, the refined one, sized from the design's test list ([how](modules/implementation.md#42-where-the-hours-go-now)), still before the agent builds. From then on, every weekly activity report line about that use case starts with its ID.

**How your TA checks it,** on GitHub by Tuesday Oct 20, replying on each issue: the issue cites the use case rather than copying it or listing its rules; the use case it cites exists; the sorted list is posted; not everything is in the issue pile; the Estimate is a range in all three parts, and it was written before the first commit the agent made for this use case.

### Week 10, Oct 28 and 30: catch up on your proving slice

**Wednesday and Friday are both studio this week, and Checkpoint 2 moves to week 11.** Your team demonstrates its slice to your TA in a slot you book outside class, any time from Mon Nov 2 to Fri Nov 6 ([what it checks](project.md#checkpoint-2-checklist)). These two hours are for getting there.

**Objective:** by the end of Friday your proving slice (your riskiest use case) has a merged design-of-record, is built by the agent from that design, is reviewed by a teammate against the design's test list, and is merged. Tag `v0.1.0` by your Checkpoint 2 slot.

#### How `/design` and `/implement` work

[`course-templates`](https://github.com/tcu-cosc-40943/course-templates) now carries two commands, in `.claude/commands/`, that run the method's two build stages ([Phase C](method.md)). Each is a plain Markdown file of instructions the agent follows when you type its name. You give it a use case ID, for example `/design UC-ORD-place-order`.

| | `/design <UC-ID>` | `/implement <UC-ID>` |
|---|---|---|
| **What it reads** | The use case (every extension), the business rules and `FR-*` it cites, the glossary, `OPEN-ISSUES.md`, your architecture-of-record with section 8 in full, the design-of-record template, the area's existing design if there is one, the existing code, and your charter | The merged design-of-record for the area, the same use case and rules, the glossary, section 8 of your architecture-of-record in full, your charter, the use case's row in `docs/traceability.md`, and the code the design points at |
| **What it does** | Drafts every section of the template: the sequence diagram, components, the API contract, key decisions, the data change, and one test row per flow. Lists every point it had to assume, and challenges anything in the specification that looks wrong | Builds on a branch in readable commits: any needed refactor first, then the trunk (shared code), then one commit per leaf. Writes a test for every row of the design's test list, checks the diff against section 8, runs the suites, and updates the traceability row |
| **Where it stops for you** | After the draft: you answer its assumptions and accept the shape before it writes `docs/design/<area>.md` | Before a refactor the design did not name, and after the trunk commit, so the owner reads it and says what it changed |
| **What it leaves you** | The design file, the traceability row set to `📐 Designed`, any specification fix, and a pull request description with the questions test | Code and tests on a branch, the traceability row's Build and Verify set honestly, and a pull request description mapping each test-list row to its test |
| **What it never does** | Write code, or approve its own design. A teammate who did not write it reviews and merges the pull request | Build from an unmerged design, add a dependency nobody checked, or approve its own work. A teammate reviews the pull request |

Run each one in a fresh session (`/clear` first), so the agent reads your documents rather than an earlier conversation. Read both files before you run them; they are short. On Copilot CLI, follow their phases by hand, as a checklist.

**Make them yours.** They are your team's files once they are in your repository, so change them by pull request like any other file the agent reads: point them at the paths your project actually uses, add your stack's test commands and conventions, add a check your reviews keep catching, or drop a step that does not fit your project. Keep the stops for a person (the accepted shape, the trunk read, a teammate's merge), because those are where your judgment goes in. Say in the pull request what you changed and why.

**Before Wednesday:** at least two members bring a laptop with a working agent session in your team repository. Pull `course-templates` (`git pull` in your clone of it, or clone it as in [where your requirements documents live](#where-your-requirements-documents-live)). Know which use case is your slice, and whether its area's design-of-record is merged on `main`.

#### Wednesday Oct 28: install the commands, then the design

| When | What your team does |
|---|---|
| 0-10 | **Install the commands by pull request.** One member copies them in, opens the pull request, and a teammate merges it. |
| 10-45 | **No design merged yet:** the slice's owner and a partner run `/design UC-<AREA>-<slug>`. Read the draft, answer every assumption it lists (a question only your client can answer goes into `OPEN-ISSUES.md`), accept the shape, then run the questions test in a fresh session. **Design already merged:** run the questions test on it in a fresh session and fix what it finds by pull request. Everyone else finishes the build-context issues from [week 8](#week-8-your-first-build-context-in-your-team-meeting) or the Checkpoint 2 items that are not code (the calibration table, the coarse estimates, the release plan). |
| 45-50 | **Open the design's pull request** and name the teammate who reviews it. It must merge before anyone runs `/implement`, so aim for Thursday. |

```bash
cd your-team-repo
git switch -c add-workflow-commands
mkdir -p .claude/commands
cp ../course-templates/.claude/commands/design.md ../course-templates/.claude/commands/implement.md .claude/commands/
git add .claude/commands
git commit -m "Add the /design and /implement commands"
git push -u origin add-workflow-commands
```

#### Friday Oct 30: build, review, merge

| When | What your team does |
|---|---|
| 0-5 | Confirm the slice's design is merged on `main`. If not, merge it first; nobody builds from an unmerged design. |
| 5-35 | **The owner runs `/clear`, then `/implement UC-<AREA>-<slug>`.** It will stop to propose a refactor if one is needed, and it stops after the trunk commit: read that commit and say what it changed and why before letting it go on. The rest of the team runs the fresh-context review on whatever the agent has pushed and starts the calibration table rows from your activity reports. |
| 35-50 | **A teammate who did not build it reviews the pull request** against the use case and the design's test list, marking each row covered or not ([how](modules/code-review.md)). Apply Monday's testing lecture to each test the agent wrote: what is its oracle, and would it fail if the code were wrong ([how](modules/testing.md)). |

**What you produce:** the commands on `main`, the slice's design merged, and the slice's implementation pull request open or merged by the end of Friday. Your TA is in the room both days to unblock you; this is not a checkpoint, and nothing is graded in the room.

**Before your Checkpoint 2 slot:** the slice merged, `v0.1.0` tagged with release notes, and every item on the [checklist](project.md#checkpoint-2-checklist) ready to show. Book the slot with your TA in your team's Slack channel by the end of Friday's studio.
