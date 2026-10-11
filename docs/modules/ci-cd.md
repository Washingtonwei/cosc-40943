# CI/CD and Continuous Deployment

> **Purpose (one line):** _to be written when authored._


!!! note "This module is still being written"
    The course is being revamped this term, so modules go up as they are written rather than all at once. What is here is usable; the rest is coming. Lectures and studio do not depend on the missing parts.

## Drafting notes (raw — distribute into template sections, then delete before `stable`)

### Two anchoring failures: Knight Capital (2012) and Cloudflare (2025)

Open with Knight Capital because it is fast and the number is brutal. Spend the time on Cloudflare, because its postmortem is a teaching artifact in its own right.

**Knight Capital, 1 August 2012. Budget two minutes.** A technician deployed new Retail Liquidity Program code by hand to **seven of eight** SMARS servers. The eighth still held **Power Peg**, dead code from 2003 that had never been removed. The new code **reused the feature flag** that had once activated Power Peg. When the flag went live, the eighth server woke the dead code: 212 parent orders became **millions of child orders, 4 million executions across 154 stocks, more than 397 million shares, in about 45 minutes**. Roughly **$440-460 million** lost, the firm did not survive independently, and the SEC imposed a $12 million penalty for market access rule violations.

Three release-engineering decisions, each individually defensible: a manual deploy with no verification that every node matched, dead code left in the tree, and a flag repurposed instead of retired.

**Cloudflare, 18 November 2025. Budget ten minutes.** A database permissions change caused a metadata query to return rows from a second database, because the query never filtered on database name. A generated Bot Management feature file **more than doubled in size** and exceeded a **hardcoded limit of 200 features** against a normal load of about 60. The Rust proxy called `.unwrap()` on the resulting `Err`, and the worker thread panicked. **5 hours 46 minutes** total, with core impact for 3 hours 10 minutes. X, ChatGPT, and Shopify went down, and Downdetector itself went offline.

Their own first remediation is the line to put on a slide:

> Harden ingestion of Cloudflare-generated configuration files in the same way we would for user-generated input.

That is a **trust boundary** decision. Someone decided, implicitly and years earlier, that configuration the company generated itself did not need validating, and nothing in the pipeline ever tested that assumption.

**The AI angle for both:** an agent asked to write that query omits the database filter too, because nothing in the specification says the second database exists. Generation speed does not touch a wrong assumption, it ships it sooner. The gate is what catches it, which is the reason this module exists.

**Sources:** Cloudflare's own outage postmortem (18 November 2025), and the SEC administrative proceeding against Knight Capital Americas LLC (2013).

### Authored: releases, rollback, and reproducible builds (move into Core concepts when the module is written)

These sections are finished prose (`DECISION-configuration-management`). Week 2's [4.10](ai-augmented-team.md#410-knowing-exactly-what-you-built) named configuration items, baselines, and agent provenance and deferred releases to here. Renumber when the module takes shape.

#### The same commit, the same build

A build is **reproducible** when the same commit always produces the same artifact. A lockfile records the exact version of every dependency, but only if the build obeys it. `npm ci` installs exactly what `package-lock.json` says and fails if the lockfile and `package.json` disagree; `npm install` may update the lockfile within the ranges `package.json` allows. Project Pulse's deploy workflow (`.github/workflows/azure-webapps-deploy.yml`) runs `npm install`, and its Maven step passes `--update-snapshots`, so two deploys of one commit can ship different dependencies. The fix is one word: `npm ci`. What the workflow gets right is the image tag: every container is tagged with the commit's SHA, so production can always be traced to one commit.

#### Versions, tags, and release notes

A **tag** marks a baseline: this commit is what we released. **Semantic Versioning** (`MAJOR.MINOR.PATCH`) says what kind of change a release is: a patch fixes, a minor version adds, a major version breaks something a user or another system relied on. For a web application with no API consumers, the version is mostly a sentence to the client.

Project Pulse's [`v1.4.2`](https://github.com/Washingtonwei/project-pulse/releases/tag/v1.4.2) is the model. `v1.4.1` reset every instructor's selected course section at login; the next day `v1.4.2` shipped as a patch, and its release notes name the regression, the issue ([#28](https://github.com/Washingtonwei/project-pulse/issues/28)), and the fix. Its counter-example is the same repository today: the last tag is `v1.5.0`, from December 2025, 47 merged pull requests ago, and `pom.xml` says `2.0.0`, a version no tag names.

GitHub generates a draft of release notes from the pull requests merged since the last tag, and an agent can rewrite that draft for the client. A human checks it against what actually changed for users, because a pull request title describes the code, not what the client will notice.

**Your team:** tag a release for every demo from Checkpoint 2 on (`v0.1.0` at Checkpoint 2, `v0.2.0` at Checkpoint 3, `v1.0.0` for the MVP your client receives), each with release notes, and always be able to say which tag or commit production runs.

#### Rolling back: the code and the data

Rolling back code is fast if it was planned. Project Pulse deploys to an Azure staging slot and swaps it into production, so undoing a bad release is a swap back, in seconds, with no rebuild.

Rolling back data is not. Project Pulse's schema changes are Flyway migrations (`V1` through `V5` in `backend/src/main/resources/db/migration/`), and they run forward only: the previous build, swapped back in, meets the new schema. So a schema change that the previous build cannot live with is a release you cannot roll back.

The way out is to split one change into steps that each keep both builds working (*expand and contract*):

1. **Expand.** Add the new column, nullable, used by nothing.
2. **Write.** Ship code that writes it.
3. **Read.** Ship code that reads it, handling the rows where it is still empty.
4. **Contract.** Only when every running build uses it, tighten it or remove what it replaced.

Project Pulse's `V5__mandatory_association_columns_not_null.sql` is a contract step done right. The code had already refused to write nulls in those columns (`@ManyToOne(optional = false)`), and the migration's header records that every column "was verified to hold zero nulls in both staging and prod before this migration was written." Code first, data checked, schema last.

#### Feature flags, and retiring them

A **feature flag** ships code switched off, so turning a feature on and off is a configuration change rather than a deploy. Project Pulse has one: `app.reminders.enabled`, which stops the weekly reminder scheduler without a release. Flags are also a configuration item, and they rot. Knight Capital's 2012 loss began with a flag reused for new code while one server still ran the old code it used to switch on. Every flag gets an owner and a removal date, and a retired flag is deleted, never repurposed.

#### The AI angle

An agent asked to add a column writes the migration and the code that reads it in one change, which is the one shape that cannot be rolled back. An agent asked to fix a failing install deletes the lockfile and regenerates it. Neither is visible unless the reviewer asks two questions of every pull request that touches the schema or a lockfile: can the previous build run against this, and did the dependency set change on purpose?

#### Sources for these sections

- IEEE 828-2012, *Standard for Configuration Management in Systems and Software Engineering*.
- Preston-Werner, T. *Semantic Versioning 2.0.0*. <https://semver.org/>
- npm documentation, `npm ci`. <https://docs.npmjs.com/cli/commands/npm-ci>
- Meiklejohn, C. S. "Reliably Releasing Software." CMU 17-313 lecture, Spring 2026. Dark launches, flag ramps, and the four-step database change.
- Project Pulse facts checked against `main` at `8768a1d` on 2026-10-10: the deploy workflow's `npm install`, `--update-snapshots`, SHA image tag, and staging slot; tags through `v1.5.0` and 47 merged pull requests after it; `pom.xml` at `2.0.0`; the `v1.4.2` release notes; `V5`'s header; `app.reminders.enabled`.
