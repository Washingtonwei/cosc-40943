# Agent Setup

This page takes you from nothing installed to an AI agent that can read your code, file an issue, and open a pull request on GitHub. It assumes you have never used Git, GitHub, a terminal, or Claude Code. If you have, skim for the two checks marked **Check** and the guardrails at the end.

Budget an hour the first time. Do it early in the week, not the night before something is due. If a step fails, post the exact command and the exact error text in the Slack help channel.

Which agent to use, and how to pay for it, is on [Working with AI](ai.md#getting-access). This page is about making it work. It is written for **Claude Code**, the course baseline; [Copilot CLI](#if-you-use-copilot-cli) differences are at the end.

## Six words you need first

| Word | What it means |
|---|---|
| **Repository** (repo) | A project folder whose full history Git tracks. It lives on GitHub, and you keep a copy on your laptop. |
| **Fork** | Your own copy of someone else's repository, on GitHub, under your account. You can change it freely. |
| **Clone** | Downloading a repository from GitHub to your laptop so you can work on it. |
| **Commit** | A saved snapshot of your changes, with a message saying what changed. |
| **Branch** | A separate line of commits, so your work does not touch `main` until it is reviewed. |
| **Pull request** (PR) | A request to merge your branch into `main`. It is where your work is reviewed, and in this course it is what you submit. An **issue** is the task the pull request resolves. |

## 1. Open a terminal

The terminal is a window where you type commands. Every command on this page goes there, one line at a time: paste it, press Enter, and wait for the prompt to come back before the next one.

- **Windows:** press the Windows key, type `PowerShell`, and open **Windows PowerShell**. The prompt looks like `PS C:\Users\you>`.
- **Mac:** press Cmd+Space, type `Terminal`, and press Enter. The prompt ends in `%`.

**After you install anything, close the terminal and open a new one.** A terminal opened before an install does not know the new command exists, and "not recognized" or "command not found" right after an install almost always means this.

## 2. Install Git, the GitHub CLI, and Claude Code

Git tracks your changes. The **GitHub CLI**, a command called `gh`, lets you and your agent talk to GitHub from the terminal: create issues, open pull requests, check where they went. Claude Code is the agent.

**Windows**, one line at a time:

```powershell
winget install --id Git.Git -e
winget install --id GitHub.cli -e
irm https://claude.ai/install.ps1 | iex
```

Accept any prompts. Git for Windows also gives Claude Code a Bash shell to run commands in, which is why it comes first.

**Mac:** first run `git --version`. If a window offers to install the command line developer tools, click **Install** and wait for it to finish. Then:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

For `gh`, download the macOS installer from [cli.github.com](https://cli.github.com/) and run it. (If you already use Homebrew, `brew install gh` does the same.)

Close the terminal, open a new one, and **check**:

```bash
git --version
gh --version
claude --version
```

Each prints a version number. If one prints "not recognized" or "command not found", reinstall that one and open a fresh terminal again.

## 3. Tell Git who you are

Every commit is stamped with a name and an email. Your repositories are public, so use GitHub's private address rather than your own. Find it at [github.com/settings/emails](https://github.com/settings/emails): turn on **Keep my email addresses private**, and copy the address that ends in `@users.noreply.github.com`.

```bash
git config --global user.name "Your Full Name"
git config --global user.email "12345678+yourusername@users.noreply.github.com"
```

Use your real name. Your team's contribution history is part of how the project is assessed, and a commit nobody can attribute counts for nobody.

## 4. Log the GitHub CLI in to your account

You need a GitHub account first. Use one you will keep all year, with your real name on it ([sign up](https://github.com/signup) if you have none).

```bash
gh auth login
```

It asks four questions. Answer with the arrow keys and Enter:

| Question | Answer |
|---|---|
| Where do you use GitHub? | **GitHub.com** |
| Preferred protocol for Git operations? | **HTTPS** |
| Authenticate Git with your GitHub credentials? | **Yes** |
| How would you like to authenticate? | **Login with a web browser** |

It shows a one-time code. Press Enter, paste the code into the browser page that opens, and approve. This single login also lets `git push` work, so you will not be asked for a password again.

**Check:**

```bash
gh auth status
```

It should say `Logged in to github.com account yourusername`.

## 5. Log in to Claude Code

```bash
claude
```

The first time, it opens a browser to log in with your Claude account. The free Claude plan does not include Claude Code; see [Working with AI](ai.md#getting-access) for what does, and for the free Copilot route. When you see the prompt, type `/exit` to leave for now.

## 6. Get an assignment repository onto your laptop

Every individual assignment has its own class repository on its page. The example here is [assignment 2](assignments/spec-a-feature.md); swap the name for the assignment you are on.

First decide where your course work lives, and go there. `cd` means "change directory":

```bash
cd ~
mkdir cosc-40943
cd cosc-40943
```

Then fork, clone, and set things up. Replace `yourusername` with your GitHub username:

```bash
gh repo fork tcu-cosc-40943/spec-a-feature --clone
cd spec-a-feature
gh repo edit yourusername/spec-a-feature --enable-issues
gh repo set-default yourusername/spec-a-feature
```

Line by line: make your fork and download it; step into the folder; switch Issues on (a new fork has them off); and tell `gh` that **your fork** is the repository to act on. That last line is the one that matters. Without it, `gh` treats the class repository as the default, and a pull request you or your agent opens lands in front of the whole class instead of in your fork.

**Check:**

```bash
gh repo view --json nameWithOwner
```

It should print your username, not `tcu-cosc-40943`.

## 7. Start the agent in the repository

Always start Claude Code from inside the repository folder, because the folder you start it in is what it can see:

```bash
claude
```

Three things to try in your first session.

**Confirm it read the project's instructions.** Project Pulse carries `CLAUDE.md` files that tell an agent how the project works. Type `/memory` to see which ones loaded, then ask: *"In three sentences, what is this project and how do I run its backend tests?"* An answer that names Spring Boot and `mvnw` means it read them.

**Plan before it writes.** Press **Shift+Tab** until the bottom of the screen says **plan mode**. In plan mode the agent reads and proposes but does not change files. Part 3 of assignment 2 runs here.

**Find the course commands.** Type `/` to see the commands this repository provides, including `/design`, `/implement`, and `/spec-build`.

**When it asks permission to run a command, read the command.** "Yes" runs it once. "Yes, and don't ask again" allows it for good in this repository, so save that for commands you have seen and understood.

## 8. The daily loop

What doing a piece of work looks like, from issue to pull request. You can type these yourself or ask the agent to run them; either way, know what each does.

```bash
gh issue create --title "Specify the non-submitter reminder"
git switch -c spec-non-submitter-reminder
```

That files the issue in your fork (it asks for a body, and prints the issue number) and creates a branch to work on. Now do the work. Then save and send it:

```bash
git add docs/requirements/use-cases.md
git commit -m "Add UC for reminding students who have not submitted"
git push -u origin spec-non-submitter-reminder
gh pr create --base main
```

`git add` picks the files for the next commit, `git commit` saves the snapshot, `git push` uploads your branch to your fork, and `gh pr create` opens the pull request. Put `Closes #N` in its description, with your issue's number, to link the two.

**Check before you submit:**

```bash
gh pr view --web
```

It opens the pull request in your browser. The top of the page must name **your fork**. Submit that page's URL.

## 9. Guardrails: what the agent must never do

An agent with `gh` can do anything you can: merge, force-push over history, delete a repository. On your own fork that is a bad afternoon. On your team's repository it is your teammates' work. Block the worst of it.

In Claude Code, type `/permissions`, open the **Deny** tab, and add each of these rules. On Windows add both columns, because Claude Code may run a command in either shell.

| Rule (Mac, and Windows Bash) | Rule (Windows PowerShell) | Blocks |
|---|---|---|
| `Bash(git push --force *)` | `PowerShell(git push --force *)` | Overwriting history on GitHub |
| `Bash(git push -f *)` | `PowerShell(git push -f *)` | The same, spelled short |
| `Bash(gh pr merge *)` | `PowerShell(gh pr merge *)` | Merging a pull request. Merging is a human decision after review. |
| `Bash(gh repo delete *)` | `PowerShell(gh repo delete *)` | Deleting a repository |

Save them to **User settings** so they apply in every repository on your laptop.

**These rules are a seatbelt, not a lock.** A command spelled differently slips past a pattern, and the Claude Code docs say so plainly. The lock is on GitHub: branch protection on your team's `main`, below.

## 10. Your team repository

Your team repository is not a fork, so step 6's fork and `set-default` lines do not apply. After the owner has created it and invited you ([Where your repository lives](studio.md#where-your-repository-lives)):

```bash
cd ~/cosc-40943
gh repo clone ownerusername/cosc-40943-team-NN-slug
cd cosc-40943-team-NN-slug
claude
```

Three things are different, and all three are team decisions, not individual ones.

**Branch protection is the real guardrail.** The owner turns it on once, from [Git Workflow: Repository settings](git-workflow.md#repository-settings): pull requests required, one approving review, no direct pushes to `main`. With that on, no agent on any teammate's laptop can push straight to `main`, however it spells the command.

**Share the deny rules.** Instead of each member adding them alone, commit them once as `.claude/settings.json` in the team repository, so every teammate's Claude Code picks them up:

```json
{
  "permissions": {
    "deny": [
      "Bash(git push --force *)",
      "Bash(git push -f *)",
      "Bash(gh pr merge *)",
      "Bash(gh repo delete *)",
      "PowerShell(git push --force *)",
      "PowerShell(git push -f *)",
      "PowerShell(gh pr merge *)",
      "PowerShell(gh repo delete *)"
    ]
  }
}
```

Open that as a pull request like any other change, so the team reviews what the agent may not do.

**Your repository needs its own agent instructions.** Project Pulse's agent knows the project because of its `CLAUDE.md` files. Yours starts knowing nothing. What goes in that file is taught in [Context Engineering](modules/context-engineering.md).

## If you use Copilot CLI

Steps 1 to 4, 6, 8, and 10's branch protection are identical; `gh` and Git do not care which agent you run. The differences:

- **Install:** `winget install GitHub.Copilot` on Windows, `brew install --cask copilot-cli` on a Mac, or see [GitHub's install page](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli). Start it with `copilot` and log in with `/login`.
- **Plan mode:** also Shift+Tab.
- **Instructions:** it reads the same `CLAUDE.md` files.
- **Course commands:** `/design`, `/implement`, and `/spec-build` are Claude Code's; run those steps by hand.
- **Guardrails** are start-up flags instead of a settings file. Copilot asks before every shell command unless you start it with `--allow-all-tools`, so don't. To stop it pushing at all, start it with `copilot --deny-tool='shell(git push)'` and push yourself. See GitHub's [allowing and denying tools](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools).

## When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `not recognized` or `command not found` right after installing | The terminal predates the install | Close it and open a new one |
| `claude` starts, but in the wrong project | You started it from the wrong folder | `/exit`, `cd` into the repository, start again |
| `git push` asks for a password, or says `Permission denied` | Git is not using your `gh` login | Run `gh auth setup-git`, then push again |
| `gh issue create` fails with "issues are disabled" | Issues are off in your fork | Run the `--enable-issues` line from step 6 |
| Your pull request is in `tcu-cosc-40943`, not your fork | `set-default` was skipped | Close that pull request, run the `set-default` line from step 6, and open it again |
| The agent keeps asking permission for the same safe command | Normal | Choose "Yes, and don't ask again" once you know what it does |

Checked against the Claude Code, GitHub CLI, and Copilot CLI documentation on September 25, 2026. These tools change often. If a step here disagrees with what your screen shows, trust the screen and tell the instructor.

## Related

- [Working with AI](ai.md): which agent, how to get access, and what "individual work" means with one.
- [Git Workflow](git-workflow.md): branches, conflicts, and the team's daily loop.
- [Resources](resources.md#setting-up-project-pulse): the toolchain for running Project Pulse itself (JDK, Node.js, Docker).
