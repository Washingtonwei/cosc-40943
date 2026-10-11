---
title: Security
module: security
week: 8
day: Monday
---

# Security

Week 8 · The agent and the attacker

## The attacker brought no tools {.center}

::: steps
- August 2025: malicious versions of `nx` published to npm.
- On install, it looked for Claude Code, Gemini CLI, Amazon Q.
- Ran them with permission checks off, and asked them to find your keys.
:::

::: key
The developer had a secret scanner installed. It was their agent.
:::

::: note
Wiz Research's write-up of the s1ngularity attack, August 26, 2025. The flags were --dangerously-skip-permissions, --yolo, and --trust-all-tools. What the agents found was committed, base64-encoded, to a new public repository in the victim's own GitHub account.
:::

## The lethal trifecta

| Leg | On your laptop, by default |
|---|---|
| Private data | The repo, `.env`, your GitHub token |
| Untrusted content | Web pages, outsiders' issues, dependency code |
| A way out | Fetching a URL, `git push`, `gh` |

::: key
All three: exploitable. Take a leg away wherever you can.
:::

::: note
Simon Willison, June 2025. An agent that cannot read your secrets has nothing to leak.
:::

## It cannot tell your instructions from text it reads

::: ask
An outsider's issue on your public repo has an HTML comment you can't see. A teammate replies "@claude fix this." What does the agent read?
:::

::: note
Everything, including the comment. Project Pulse's claude.yml fires on any @claude mention; what stops strangers is the action's own default, write access only. The leftover risk is exactly this one, a maintainer tagging the agent on an outsider's text. The action strips hidden content, which its docs say "reduces but does not eliminate prompt injection risk." Indirect prompt injection is OWASP's number one LLM risk.
:::

## Read it raw first

::: key
Before an agent reads content your team did not write, you read it. Raw.
:::

## A request, a lock, a wall

::: steps
- **Charter:** "never read .env". A request to the model.
- **Deny rule:** `Read(**/.env)`. Enforced by the tool.
- **Sandbox, branch protection:** enforced by the OS and by GitHub.
:::

::: note
Claude Code's docs: permission rules are enforced by Claude Code, not by the model; CLAUDE.md instructions don't change what it allows. A deny rule still misses grep -r across the folder, or a script that opens the file itself. The sandbox blocks those.
:::

## The team's settings file

```json
{
  "permissions": {
    "deny": [
      "Bash(git push --force *)",
      "Bash(gh pr merge *)",
      "Bash(gh repo delete *)",
      "Read(**/.env)",
      "Read(**/.env.*)",
      "Read(**/secrets/**)",
      "Read(**/*.pem)",
      "Read(**/*.key)"
    ]
  }
}
```

::: note
.claude/settings.json, committed once so every teammate's Claude Code picks it up. The full file, with the PowerShell twins and the short force-push spelling, is on the Agent Setup page, section 10. Open it as a pull request so the team reviews what the agent may not do. The Read rules are the new part this week: anything the agent reads goes to the model provider. Test it yourself: ask the agent to read your .env and see it refused. Your TA opens this file at Checkpoint 2.
:::

## Never switch the checks off

::: warn
`--dangerously-skip-permissions` in a folder with your secrets is the state the nx attack went looking for.
:::

::: joke
The S in "AI agent" stands for security.
:::

## What it reads, it may write

::: steps
- A commit message.
- A pull request description.
- A comment on a public issue.
:::

::: note
Whatever the agent reads is sent to the provider and can reappear in anything it writes. Secrets live in environment variables or behind a deny rule. Anything prefixed VITE_ is compiled into the browser bundle, so it is public by construction. Project Pulse's committed .env.production holds only the app title and the server URL.
:::

## The package that does not exist

::: cols
**2025, 16 models**
5.2% (commercial) to 21.7% (open source) of suggested packages invented.
|||
**2026, frontier models**
4.6% to 6.1%. 53 names all five invent, still registrable.
:::

::: note
Spracklen et al., USENIX Security 2025: 576,000 samples, 205,474 distinct invented names. Churilov, arXiv 2026. Register the name an agent keeps inventing, fill it with malware, wait. It is called slopsquatting.
:::

## Before a dependency merges

::: steps
- It **exists** on the registry.
- It is **the one you meant**: publisher, repository, age, use.
- The change added **only it**.
:::

## A model inside your product

::: steps
- Keys stay on the server.
- Uploaded documents can carry instructions.
- Output is data to validate, never authority.
- Do not give it a way out.
:::

::: note
Project Pulse's specified AI assistants: CO-server-side-llm-proxy, FR-AI-source-material-context, SI-llm-json. An assistant that reads one team's documents and uploaded material already has two legs; no tool that emails, fetches, or writes elsewhere.
:::

## Before Friday

::: steps
- `Read` deny rules for your secrets in the team's `.claude/settings.json`, by pull request.
- Ask the agent to read `.env`. Watch it refused.
- Charter line: no dependency without a person's check.
- Checked at Checkpoint 2.
:::
