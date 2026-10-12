---
title: Requirements Traceability
module: traceability
week: 8
day: Friday
---

# Requirements Traceability

Week 8 · Forward, backward, and the release plan

## "What will I have in December?" {.center}

::: key
A release plan: every use case placed in the release it ships in.
:::

::: note
The estimate answers "when can I use this one?" The client's next question is about the whole term. Agile teams have always planned releases with stories and velocity; we keep the idea and change the units.
:::

## A column, not a document

| UC | Build | Verify | **Release** |
|---|---|---|---|
| `UC-NOT-remind-non-submitters` | 📐 Designed |  | `v1.6.0` |
| `UC-AI-critique` | ❌ Not started |  | `v1.8.0` |
| `UC-AI-draft-skeleton` | ❌ Not started |  | `Later` |

::: steps
- Yours: `v0.1.0` slice, `v0.2.0` Checkpoint 3, `v1.0.0` December, `Spring`, `Out`.
- Order: risk first, then what the client needs, then dependencies.
- An empty cell is work nobody planned.
:::

::: note
Rows from Project Pulse's traceability matrix. Plan and progress share a row, so they cannot disagree. Project Pulse shipped up to v1.5.0 with no release plan; its plan starts with the work left. Risk alone would put the first AI assistant (v1.8.0) before finishing the editor (v1.7.0); the client chose the editor first, and the pull request that set the column says why. Writing the column also caught a disagreement: the vision listed real-time co-editing as out of the MVP, while traceability showed it as unstarted work. The use case's Status line (Deferred) settles it; Project Pulse keeps scope on the use case and timing in the column.
:::

## Forecast, then talk to the client

::: key
Hours still needed = remaining `v1.0.0` estimate midpoints × your ratio.
:::

```text
Forecast: 6 rows left in v1.0.0, 38 to 60 h at ratio 1.4; about 70 h available.
```

::: warn
Doesn't fit? Move rows out of `v1.0.0` with your client at the next meeting. Change the scope, not the estimate.
:::

::: note
A use case not yet designed has no test list, so size it from its main scenario and extensions, as a wider range: it is earlier in the cone of uncertainty. Compare with the hours the team will have before the demo, judged from what the weekly activity reports show the team actually works. Revise the Release column at every use-case close.
:::
