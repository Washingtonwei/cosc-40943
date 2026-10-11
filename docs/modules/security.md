# Security: The Agent and the Attacker

**Slides:** [Security: The Agent and the Attacker](../slides/security.html) (the fast version).

> **Purpose (one line):** work with a coding agent without lending it to an attacker: limit what it can read and run, treat everything it reads from outside your team as possibly hostile, and check every dependency it names before it enters your build.

!!! note "This module is still being written"
    This page covers the risks an agent adds. Authentication, authorization, and secure coding on your own stack are coming; the trust boundary they start from is in [Software Architecture, Just Enough](architecture.md#49-security-as-a-quality-attribute-the-trust-boundary).

## 1. Learning objectives

By the end of this module, a student can:

1. State the lethal trifecta and say which of its three legs a given agent setup has.
2. Explain prompt injection, direct and indirect, and list where content your team did not write enters an agent's context on your project.
3. Configure an agent so that secrets are unreadable and destructive actions need a person, and say what those rules cannot stop.
4. Check a dependency an agent proposes before it enters the lockfile.
5. Treat a language model inside your own product as untrusted on both sides: what goes in can carry instructions, and what comes out is data to validate.

## 2. Where it fits

- **Prerequisites:** [Software Architecture, Just Enough](architecture.md#49-security-as-a-quality-attribute-the-trust-boundary), whose trust boundary this module extends to the agent; the [Agent Setup](../agent-setup.md) page, whose guardrails it explains.
- **Leads into:** every build session from week 8 on, and [Checkpoint 2](../project.md#checkpoints), where your TA checks your team's agent settings.
- **How it's taught:** a short segment in week 8, just before the agent starts building; the rest is reading. It is practiced through your team's `.claude/settings.json` and its charter.
- **Course outcome it delivers:** [collaborating with AI across the lifecycle, delegating appropriately and verifying its output](../syllabus.md#learning-outcomes) (outcome 6).

## 3. Motivation

**The attacker brought no tools.** On August 26, 2025, malicious versions of `nx`, a widely used JavaScript build tool, were published to npm. Installing one ran a script that looked for AI coding assistants on the developer's machine (Claude Code, Gemini CLI, Amazon Q) and, if it found one, ran it with its permission checks switched off (`--dangerously-skip-permissions`, `--yolo`, `--trust-all-tools`) and asked it to search the disk for wallets, tokens, and keys. What it found went into a new public repository in the victim's own GitHub account. The attacker did not need to write a secret scanner. The developer had one installed, with access to everything, waiting for instructions.

**Your agent reads things you did not write.** Project Pulse runs the Claude GitHub Action ([`claude.yml`](https://github.com/Washingtonwei/project-pulse/blob/main/.github/workflows/claude.yml)): mention `@claude` in an issue or a comment and an agent starts working on the repository. Project Pulse is public, so anyone can open an issue, and the workflow's own condition checks only whether the text contains `@claude`, never who wrote it. What stops a stranger is a default in the action itself: it runs only for users with write access to the repository. That leaves one path open, which the action's own security guide names. A maintainer who tags `@claude` on an issue a stranger wrote hands the agent the stranger's text, and hidden instructions in it can steer the agent. The action strips HTML comments and invisible characters, which, in its documentation's words, "reduces but does not eliminate prompt injection risk."

## 4. Core concepts

### 4.1 The lethal trifecta

Willison (2025) named the combination that turns an agent into a leak. An agent is exploitable when it has all three:

| Leg | What it means | In your Claude Code session, by default |
|---|---|---|
| **Private data** | It can read something worth stealing | Your repository, any `.env` file, the GitHub CLI's token, your SSH keys |
| **Untrusted content** | It reads text an attacker could have written | Web pages it fetches, issues and comments by outsiders, a dependency's README and code, a document a client sent |
| **A way out** | It can send data somewhere | Fetching a URL, `git push`, `gh`, `curl` |

A coding agent on a developer's laptop has all three out of the box. The defense is structural: take a leg away wherever the task allows. An agent that cannot read your secrets has nothing to leak; an agent that never reads untrusted content has no one to take orders from.

### 4.2 Prompt injection

A language model receives one stream of text, and it cannot reliably tell the instructions you gave it from the data it was asked to process. Anything in its context can steer it. **Direct** injection is a user typing instructions into a system that has a model behind it. **Indirect** injection is instructions planted in content the model reads later: a web page, an issue, a code comment, an uploaded file. OWASP ranks prompt injection first among the risks of applications built on language models (OWASP 2025).

Indirect injection is the one that reaches a coding agent. Text a person cannot see in the rendered page, such as an HTML comment in an issue, is plain text to the agent. No filter is complete, which is why the Claude GitHub Action's documentation tells maintainers to read the raw content of anything from an outside contributor before tagging the agent on it. The rule for your team is the same: **before you point an agent at content your team did not write, read it yourself, raw.**

### 4.3 Permissions: what they stop, and what they do not

Claude Code's documentation is explicit: "Permission rules are enforced by Claude Code, not by the model. Instructions in your prompt or `CLAUDE.md` shape what Claude tries to do, but they don't change what Claude Code allows." A line in your charter saying "never read `.env`" is a request. A deny rule is a lock.

Three layers, from weakest to strongest:

| Layer | What it is | What it cannot stop |
|---|---|---|
| **Charter instructions** | Text the agent reads every session | Anything; it is advice to the model |
| **Permission rules** | `Read(./.env)` and similar deny rules in `.claude/settings.json`, enforced by the tool | A command that reads files without naming them (`grep -r` across the folder) or a script that opens the file itself. The docs say so in a warning |
| **Sandbox, and branch protection** | The operating system blocks the process; GitHub refuses the push | What the agent may legitimately do inside its allowance |

Two consequences. **Never start an agent with its permission checks switched off** (`--dangerously-skip-permissions` in Claude Code, `--allow-all-tools` in Copilot CLI) in a folder that holds anything you would mind losing; it is exactly the state the `nx` attack looked for. And keep the real locks where the agent cannot argue with them: branch protection on `main`, set once by your repository's owner ([Git Workflow](../git-workflow.md#repository-settings)).

### 4.4 Secrets in the agent's context

Whatever the agent reads is sent to the model provider and can come back out in what it writes: a commit, a log line, a pull request description, an issue comment on a public repository. Treat "the agent read it" as "it may now be anywhere the agent writes."

So secrets live outside the folder the agent works in, or behind a deny rule: environment variables on the server, a `.env` file that is in `.gitignore` and denied to the agent. Project Pulse keeps production credentials in its host's environment, and its committed `frontend/.env.production` holds only values meant to be public (the app title and the server URL). That is not an accident of taste: Vite compiles every `VITE_`-prefixed variable into the JavaScript bundle that every browser downloads, so a secret placed there is published. The [actuator incident](architecture.md#49-security-as-a-quality-attribute-the-trust-boundary) showed what a leaked credential costs: rotation first, then the fix.

### 4.5 Dependencies the agent names

An agent asked for a library sometimes names one that does not exist. Spracklen et al. (2025) generated 576,000 code samples with 16 models and found that at least 5.2% of the packages commercial models suggested, and 21.7% of those open-source models suggested, did not exist: 205,474 distinct invented names. A 2026 re-test of five current frontier models found rates between 4.6% and 6.1%, and 127 names that all five invented identically, 53 of which an attacker could still register (Churilov 2026). An invented name that recurs is an invitation: register it, put malware in it, and wait for an agent to suggest it. The practice has a name, *slopsquatting*.

A real package can be malicious too: the `nx` versions in [the motivation](#3-motivation) were real releases of a real project, and the attack ran from an install script.

Before a dependency an agent proposed enters your lockfile, a person confirms three things: **it exists** on the registry, **it is the one you meant** (the publisher, the repository it links to, how long it has existed, how widely it is used), and **the agent's change added only it**. Then it goes through a pull request like any configuration item ([Knowing exactly what you built](ai-augmented-team.md#410-knowing-exactly-what-you-built)).

### 4.6 When your product contains a model

Some of your clients' systems will call a language model. Then the trifecta applies to your product, not just your laptop.

Project Pulse's specification shows the shape, for AI assistants that are specified but not yet built:

- **Keys stay on the server.** Every model call goes through the REST API's proxy (`CO-server-side-llm-proxy`), so the browser never holds the credential.
- **Input can carry instructions.** The assistants read team-uploaded source material as context (`FR-AI-source-material-context`). A document with "ignore your instructions and…" in it is indirect injection against your own product.
- **Output is data, not authority.** Responses must follow a structured schema (`SI-llm-json`), so the server can validate them before use. Never let model output decide what a user may see or do; authorization stays in code.
- **Count the legs.** An assistant that reads one team's private documents and also reads uploaded material has two legs. Do not give it the third: no tool that sends email, calls a URL, or writes outside that team's data.

## 5. The AI-native lens

- **Delegate to AI:** drafting the deny rules for your stack, listing every dependency a change added, and summarizing a dependency's publisher and history for you to judge. An agent in plan mode can also list every place untrusted text enters its own context on your project.
- **Keep human:** what the agent may read and run, the decision to add a dependency, and the decision to point an agent at content from outside the team. These are trust decisions, and the agent is the thing being trusted.
- **Context to supply:** which files hold secrets, which content in your project comes from outside the team, and the rule that new dependencies need a person's confirmation.
- **How to verify:** test the lock, not the request. Ask the agent to read a denied file and confirm the tool refuses. Read the lockfile diff of every pull request that touches dependencies. Read raw any outside content before an agent processes it.

## 6. Risks & mitigations

| Risk (classic + AI-introduced) | Human judgment that catches it | Mitigation |
|---|---|---|
| **Classic:** a secret committed to the repository | Reading the diff for anything that looks like a key | Secrets in environment variables; `.env` in `.gitignore`; rotate first if one leaks |
| **AI-introduced:** instructions hidden in an issue, a page, or a file steer the agent | Asking "who wrote the text this agent is about to read?" | Read outside content raw first; deny secrets so a hijacked agent has nothing to take |
| **AI-introduced:** an invented or malicious package enters the lockfile | Noticing a dependency nobody on the team chose | Confirm existence and identity before merge; review lockfile diffs |
| **AI-amplified:** an agent run with permission checks off, for convenience | Asking why the prompts were annoying, not how to silence them | Allow specific safe commands instead; never bypass mode in a folder with secrets |

## 7. Hands-on (studio + optional individual assignment)

**Studio (team, own project)**

- **Goal:** your team's agents cannot read your secrets, and no dependency enters without a person's check.
- **On your own project, before the build starts:** add `Read` deny rules for your secrets to the team's committed `.claude/settings.json` (the [Agent Setup](../agent-setup.md#10-your-team-repository) page has the file), by pull request. Then ask the agent to read one of the denied files and confirm it is refused. Add one line to your charter's list of things the agent must not do: no dependency is added until a person confirms it exists and is the intended one.
- **Deliverable & assessment:** at [Checkpoint 2](../project.md#checkpoints), your TA opens `.claude/settings.json` and the charter and checks both.

**Individual assignment (Project Pulse):** none.

## 8. Summary / key takeaways

- An agent with private data, untrusted content, and a way out can be turned against you. Remove a leg wherever the task allows.
- A model cannot reliably tell your instructions from text it reads. Read outside content yourself before an agent does.
- A charter instruction is a request; a deny rule is a lock; the sandbox and branch protection are stronger locks. Never switch the checks off in a folder with secrets.
- Whatever the agent reads may reappear in whatever it writes.
- Confirm that every dependency an agent names exists and is the one you meant.
- A model inside your product is untrusted on both sides.

## 9. Key papers & further reading

- Willison, S. "The Lethal Trifecta for AI Agents: Private Data, Untrusted Content, and External Communication." June 16, 2025. <https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/>
- OWASP. *Top 10 for LLM Applications 2025*, LLM01: Prompt Injection. <https://genai.owasp.org/llmrisk/llm01-prompt-injection/>
- Spracklen, J., et al. "We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs." *USENIX Security* 2025. <https://arxiv.org/abs/2406.10279>
- Churilov, A. "The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort." arXiv:2605.17062, 2026.
- Wiz Research. "s1ngularity: Supply Chain Attack Leaks Secrets on GitHub." August 2025. <https://www.wiz.io/blog/s1ngularity-supply-chain-attack>
- Anthropic. "Configure permissions," Claude Code documentation. <https://code.claude.com/docs/en/permissions>
- Anthropic. Claude Code GitHub Action, security guide. <https://github.com/anthropics/claude-code-action/blob/main/docs/security.md>

## 10. Self-check

1. Your agent can fetch web pages, read your repository, and push to GitHub. Name the three legs of the trifecta in that setup, and the one you would remove first for a session that only refactors code.
2. Your `CLAUDE.md` says "never read `.env`." Your teammate says that is enough. What is the difference between that line and `Read(./.env)` in `.claude/settings.json`, and what can the deny rule still not stop?
3. A user opens an issue on your public repository, and a teammate replies "@claude please fix this." What should the teammate have done first, and why is the action's sanitizing not enough?
4. Your agent adds `react-query-helpers-pro` to `package.json`. List what you check before merging.
5. Your client's app summarizes uploaded PDFs with a model and can email the summary to any address. Which legs of the trifecta does it have, and what one change would you propose?

## Related

- [Software Architecture, Just Enough](architecture.md#49-security-as-a-quality-attribute-the-trust-boundary): the trust boundary and the actuator incident.
- [Agent Setup](../agent-setup.md): the guardrails and the team settings file.
- [The AI-Augmented Team](ai-augmented-team.md#410-knowing-exactly-what-you-built): dependencies and lockfiles as configuration items.
- [Schedule](../schedule.md): when this is taught.

<!--
## Drafting notes (raw: distribute into template sections, then delete before `stable`)

### Still to author in this module (DECISION-security-into-architecture)

- Authentication and authorization on the team's own stack (Spring Security, reusing the instructor's Web Tech notes), secure coding in implementation, taint in static analysis (week 10), secrets and known-vulnerable dependencies in CI (week 11).

### Sources to check before `stable`

- nx attack: date, the three flags, the self-exfiltration repository, from Wiz; confirm the CLI list against Wiz's post.
- Claude Code permissions quotes checked 2026-10-10 against https://code.claude.com/docs/en/permissions (the enforcement sentence and the Read/Edit deny warning).
- Claude GitHub Action: write-access default, sanitizing list, and "reduces but does not eliminate" quoted from docs/security.md, read 2026-10-10.
- Project Pulse facts checked against `main` at `8768a1d` on 2026-10-10: claude.yml's `if` condition; no committed .claude/settings.json (only settings.local.json in .gitignore); frontend/.env.production keys (NODE_ENV commented, VITE_APP_TITLE, VITE_SERVER_URL); CO-server-side-llm-proxy, FR-AI-source-material-context, SI-llm-json in the SRS.
- Copilot CLI flag name `--allow-all-tools`: matches the Agent Setup page; confirm against current Copilot CLI docs.
-->
