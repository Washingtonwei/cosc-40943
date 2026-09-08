# Git Workflow

How six people share one repository without stepping on each other, and what to do the first time git refuses to merge.

This page is reference. Read sections 1 through 3 before you cut your first branch, then come back for the conflict recipe when you need it. **Why a branch is sized the way it is, and why the pull request is now the first human read of the code, is in [The AI-Augmented Team](modules/ai-augmented-team.md#46-what-a-branch-should-be)**, and this page does not repeat it.

Every member of your team is a collaborator on your one team repository, so you branch inside it and merge back. There are no forks there. (Forks are for the individual assignments, where you fork a class repository into your own copy. Different mechanism, different purpose.) `main` is the single source of truth and is always expected to build and pass tests.

## The one idea to take away

Merge conflicts are mostly an organizational problem, not a git problem. Git only conflicts when two people change **the same lines of the same file** during **the same window of time**. So the two things that actually control your conflict rate are how you divide the work and how often you integrate. Nobody ever solved a conflict problem by learning more git commands.

## 1. The single biggest lever: short-lived branches

A branch that lives one day almost never conflicts. A branch that lives two weeks always does, because `main` has moved underneath it the whole time and you are now merging two months of divergent thinking.

**Expectation for this course: a branch opens and merges within one or two days.** If a feature cannot be finished in that window, it is too big and needs to be split into pieces that each make sense on their own. "Add the API endpoint" and "wire up the UI" are two branches, not one.

## 2. Team agreements to make before you write any code

**Divide the work by use case, not by layer.** This is clause 4 of the contract you signed, and it is also your conflict-avoidance strategy. One member owns a use case end to end, which means the two people most likely to fight over a file, the "front-end person" and the "back-end person" on one feature, do not exist on your team. What remains is two owners whose separate use cases meet in the same service class. That is normal and expected, and the next three habits are how you handle it.

**Name your hot files and treat them carefully.** Every project has a few files that everyone eventually has to touch. In Project Pulse they are `SecurityConfiguration.java`, `DataInitializer.java`, `routes.ts`, `package.json`, and `docs/requirements/OPEN-ISSUES.md`: the security configuration, the seed data, the router, the dependency manifest, and the shared list. Yours will be the equivalents. Name them in week 3 and pin the list in your Slack channel. Three habits for these files: change them in their own small pull request, add new entries at the end rather than editing the middle, and tell the team in chat before you start.

**Announce renames and refactors in advance.** Renaming or moving a file that someone else is currently editing produces the worst conflicts git can generate, because git sees a deletion plus an addition rather than an edit.

**Agree on formatting once and never argue about it again.** Put it in `AGENTS.md`, where clause 5 says your conventions live, so the agent follows it too. If one person reformats a file, git sees every line as changed and the next person gets a whole-file conflict that contains no real disagreement.

## 3. Your daily loop

Starting a new piece of work:

```
git switch main
git pull
git switch -c feat/42-assign-student-backend
```

The number is the sub-issue you are working. Carry it in the branch name, in your commit messages, and in the pull request description. That is what lets `git log` on a strange line six months from now lead back to the branch, the branch to the sub-issue, and the sub-issue to the use case that asked for it.

While working:

```
git add -p
git commit          # commit often, in small pieces
git push            # push freely, this is your backup
```

Push early and push often. A pushed branch is backed up, gives you CI feedback, and lets teammates see what is coming if you open the pull request as a draft. Messy work in progress is fine on your own branch.

**Before you request review, and once every morning:**

```
git switch main && git pull
git switch feat/42-assign-student-backend
git merge main
./mvnw test          # this step is the whole point
git push
```

`./mvnw test` is how Project Pulse runs its backend suite, from the `backend/` directory (`mvnw.cmd test` on Windows). Substitute whatever your own project's test command is. What matters is not which command it is, but that something actually runs.

After your pull request is merged:

```
git switch main && git pull
git branch -d feat/42-assign-student-backend
```

## 4. Why you resolve conflicts on your own machine

You may be tempted to let GitHub handle it. GitHub does have a conflict editor in the browser. Do not use it, for three reasons.

**A conflict resolution is code you wrote, and untested code is not finished.** When you resolve locally you can compile it and run the tests. The browser editor gives you a text box and a "mark as resolved" button, and nothing runs. It is very easy to produce a file with no conflict markers that is nonetheless wrong.

**Clean merges can still be broken merges.** Suppose one teammate adds a route rule that references an authorization manager, while another renames that manager. Different lines, different files, so git merges happily and reports no conflict at all. The code does not compile. This is called a semantic conflict, and the only thing that catches it is building and testing the merged result. That is why running your tests after the merge is not optional.

**A pull request that cannot merge wastes your reviewer's time.** They are reviewing a hypothetical version of the code.

## 5. When a conflict does happen

This is routine, not failure. Every working developer does this weekly.

```
git switch main && git pull
git switch feat/42-assign-student-backend
git merge main
```

Git names the files it could not merge. Open each one and you will see:

```
<<<<<<< HEAD
your version
=======
the version from main
>>>>>>> main
```

Decide what the file should actually contain. Often it is both changes, not one or the other. Delete all three marker lines. Then:

```
git add <file>
git commit
./mvnw test
git push
```

The important habit: **you always resolve in your own branch.** `main` is never left broken while you figure it out. If you get lost partway through, `git merge --abort` puts everything back exactly as it was.

## 6. Things that will bite you

**Merging `main` into your branch repeatedly creates merge commits, and that is fine.** Set your repository to squash merge pull requests and all of that integration history collapses into one clean commit on `main`. Do not avoid syncing because you are worried about messy history. The mess is free.

**`git merge` needs a clean working tree.** This is why "commit often" is not just tidiness advice. If you have uncommitted changes, commit them first, or use `git stash` and `git stash pop` around the merge.

**Use `merge`, not `rebase`, for now.** Rebase rewrites history and requires a force push, which can destroy a teammate's work on a shared branch. It is a genuinely useful tool and a good thing to learn later, on your own branches only.

**Never commit directly to `main`.** That is clause 5 of your contract, and you have already used up the one exception: signing the contract in the browser during week 2 studio. Branch protection should refuse it, but the habit matters more than the setting.

## Quick reference

| Situation | Command |
|---|---|
| Start new work | `git switch main && git pull && git switch -c feat/42-thing` |
| Save work locally | `git add -p && git commit` |
| Back up to GitHub | `git push` |
| Sync with the team | `git switch main && git pull && git switch feat/42-thing && git merge main` |
| Undo a merge midway | `git merge --abort` |
| See what changed | `git status`, `git diff`, `git log --oneline` |
| Clean up after merge | `git switch main && git pull && git branch -d feat/42-thing` |

Shorter sync, once you understand remote-tracking branches, which works even with a dirty tree:

```
git fetch origin
git merge origin/main
```

## Repository settings

For the member who [owns the repository](studio.md#where-your-repository-lives). Do this once, in week 3, and tell the team in Slack when it is on.

On `main`, under branch protection: require a pull request before merging, require at least one approving review, require the build check to pass, and disallow direct pushes.

In general settings: allow squash merging only, so history stays uniform, and enable "automatically delete head branches" so merged branches clean themselves up.

Skip `CODEOWNERS`. It routes review requests by directory, which helps only when people own directories. Yours own use cases that cut across them.

## Related

- [The AI-Augmented Team](modules/ai-augmented-team.md): the module. Why a branch is sized the way it is, and what to actually read in a pull request.
- [Team Contract](team-contract.md): clause 4 (how work is claimed) and clause 5 (git workflow and review), in your team's own words.
- [Friday Studio](studio.md#where-your-repository-lives): who owns the repository and who gets access.
- [Senior Design Project](project.md): what your team owes and when.
