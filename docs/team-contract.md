# Team Contract

Your team's operating agreement. You draft and sign it in the [first studio](studio.md), and it is the first thing your TA checks at [Checkpoint 0](project.md#checkpoints).

## Where it lives, and why

**In your team's repository, at `docs/team-contract.md`.** Not in a shared document somewhere else. That repository is public and owned by one named member; [the studio page](studio.md#where-your-repository-lives) says how to stand it up.

The contract is a set of decisions about how your team works, and decisions your team makes belong where the rest of your team's memory lives. Two of its clauses (the git workflow and the AI usage guidelines) are instructions your coding agent should be able to read, which it can only do if the file is in the repository. See [The AI-Augmented Team](modules/ai-augmented-team.md) for why that matters more than it sounds.

## How you sign it

**Each member adds their own signature line, in their own commit.** Not one person typing everybody's name. That makes `git log docs/team-contract.md` the evidence, and it is what your TA looks at. One commit per member, from that member's own account, or the contract is not signed.

**In the studio, sign in the browser.** The owner commits the filled-in template to `main`. Everyone else opens `docs/team-contract.md` on GitHub, clicks the edit pencil, adds their own line, and commits directly to `main`. Six people editing one file in the same minute is safe, because GitHub serializes the commits for you, and it needs nothing installed. This is the one time you commit to `main`; clause 5 of the contract you are signing forbids it from Monday on.

**Afterwards, amendments go through a branch**, like every other change:

```
git switch -c contract-amend
# edit the clause
git commit -am "Amend clause 5: two approving reviews"
```

## Filling it in

Ten minutes, together, out loud. Two rules:

**Fix the meeting time first.** Everyone's calendar open, find the slot, write it down. It is the clause the others depend on, and the single most reliable predictor of a struggling senior design team is a team that never found a time to meet.

**Write what you will actually do.** "We will communicate effectively" is not a clause. "Slack, replies within 24 hours on weekdays" is a clause. If you would not be comfortable being held to it in November, do not write it in September.

## The template

Copy this into `docs/team-contract.md` and replace everything in angle brackets.

```markdown
# Team Contract: <team name>

**Project:** <client project name>
**Members:** <every member's name>
**Repository:** <url>, owned by <name>
**Signed:** <date>

## 1. Meeting time

We meet every **<day>** at **<time>** in **<place or link>**, for <duration>.
A member who cannot attend tells the team **<how far ahead>** and reads the minutes.

## 2. Communication

Primary channel: **<Slack channel>**. Client contact goes through **<name>**.
We reply within **<n>** hours on weekdays. Anything urgent: **<how>**.

## 3. How we decide

Routine calls: **<e.g. whoever owns the use case decides>**.
Anything affecting the whole team: **<e.g. discussed at the weekly meeting, majority, ties go to the project lead>**.
A decision that survives the meeting is written down in **<where>**.

## 4. How work is claimed

Work is divided **by use case, not by layer**. One member owns a use case end to
end: front end, back end, tests, and the pipeline.
Claiming: **<e.g. assign yourself the sub-issue and move the card>**.
Nobody is the "front-end person" or the "tester".

## 5. Git workflow and review

Coding conventions (naming, formatting, layout) live in `AGENTS.md`, not here.
This clause is about how work moves.

Branch per sub-issue, named **<convention, e.g. feat/42-short-slug>**.
Never push to `main`. Every change arrives as a pull request.
A pull request needs **<n>** approving review(s) from someone who does not own the use case.
A reviewer reads the issue before the diff. Blocking a merge: **<what blocks it>**.

## 6. Working with AI

We use **<tools>**. Our charter lives in `AGENTS.md`.
Every member can explain any line submitted under their name.
We do not merge agent output that nobody has read.
Additional limits we agree on: **<anything else>**.

## 7. When someone does not deliver

First: **<who raises it, and how soon>**. We attack the problem, not the person.
If it happens again: **<what the team does>**.
Still unresolved: we escalate to our TA, then to the instructor. We escalate early.

## Signatures

Each member adds their own line, in their own commit.

- <name>, <date>
```

## What Checkpoint 0 checks

Your TA reads for four things, at your row, in about two minutes:

1. A **named day and time** in clause 1. Not "weekly, TBD".
2. **One signature line per member, each in its own commit.** `git log` is the proof.
3. Clause 7 says something specific about what actually happens, rather than restating that problems should be avoided.
4. The file is committed to your repository at `docs/team-contract.md`, and the header names the repository owner.

## Changing it later

Amend it by pull request, like anything else in the repository. A contract nobody amends is usually one nobody reads. If a clause turns out to be wrong in week 6, change it deliberately rather than quietly ignoring it.

## Related

- [Friday Studio](studio.md): the hour you draft and sign this.
- [Senior Design Project](project.md#conflict): what happens when the contract is not enough.
- [The AI-Augmented Team](modules/ai-augmented-team.md): why this lives in the repository.
