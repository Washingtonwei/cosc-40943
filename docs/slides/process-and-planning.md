---
title: Estimating When the Agent Writes the Code
module: process-and-planning
week: 8
day: Monday
---

# Estimating When the Agent Writes the Code

Week 8 · Before the fan-out

## When can I use it? {.center}

::: ask
The reminder's design is approved. The instructor asks: when can I use it? What do you answer?
:::

::: note
Take two or three numbers from the room and write them on the board. Do not comment on them yet; they come back at the end. The design is Project Pulse's docs/design/not.md from week 7.
:::

## The old answer: count the code

::: steps
- A controller, a `SubmissionStatusService`, a scheduler change, a dialog, their tests.
- Lines of code, times hours per line.
- That is COCOMO (Boehm, 1981).
:::

::: ai
The agent writes all of it in one session. By that arithmetic, the answer is "this afternoon."
:::

## It is not this afternoon

::: cols
**18**
rows in the test list. Each one is a behavior a person has to see pass.
|||
**5**
open risks. One (80 emails during one request) can only be settled by measuring on staging.
:::

::: key
The agent made the typing free and left everything else.
:::

## Your feeling of speed is not data

::: steps
- Before: developers expected AI to make them **24% faster**.
- Measured: they took **19% longer**.
- After: they still believed they had been **20% faster**.
:::

::: note
METR's randomized controlled trial, July 2025: 16 experienced open-source developers, 246 issues in their own repositories. METR's 2026 follow-up suggests newer tools probably do speed people up, but its confidence intervals include no change, and METR calls its own data very weak evidence. The point for estimation survives either way: felt speed was off by about 40 points, in the flattering direction.
:::

## The hours moved

::: cols
**Pull requests**
154% larger, 98% more of them.
|||
**Review time**
up 91%.
:::

::: note
Faros AI telemetry, more than 10,000 developers on 1,255 teams, June 2025. A vendor's correlational data, not an experiment. It points the same way as METR: generation got cheap, and the cost moved to the person reading the result.
:::

## Three things that sound alike

| | Who owns it | Sounds like |
|---|---|---|
| Estimate | You | "8 to 16 hours" |
| Target | The client | "Before the midterm" |
| Commitment | The team | "On staging by Friday" |

::: warn
When the target and the estimate do not fit, change the scope, not the estimate.
:::

::: note
McConnell, Software Estimation, 2006. An estimate is a range because it is uncertain; a commitment is one date because someone plans around it. The range narrows as decisions get made (the cone of uncertainty, Boehm 1981), which is why you estimate after the design is approved.
:::

## Every classic model: size times a rate

| Model | Size | Rate |
|---|---|---|
| Function points | What it does for users | Hours per function point |
| COCOMO | Lines of code | Effort per line |
| Velocity | Story points | Points per iteration |

::: key
The rates were measured when people wrote the code. Keep the size. Measure your own rate.
:::

::: note
Function points: Albrecht, 1979. Velocity breaks for a second reason: it assumes a stable pace, and the agent changes every few months. Expert judgment is still the most used technique and no worse than the models on average (Jørgensen, 2004), but only if the expert's experience includes working with an agent. Planning poker survives untouched: independent estimates still beat one anchored voice.
:::

## Where the hours go now

::: steps
- **Specify:** closing the gaps the agent would guess at.
- **Build and review:** driving the agent, reading every line of the diff.
- **Verify:** seeing each test row pass, end to end.
:::

::: joke
The first 90 percent of the code takes the first 90 percent of the time. The remaining 10 percent takes the other 90 percent. (Tom Cargill, Bell Labs)
:::

::: note
The joke is now literally true: the agent does the first 90 percent of the code in minutes, and the other 90 percent of the time is review and verification. Each part maps onto weekly activity report categories: specify is DESIGN or DOCUMENTATION, build and review is DEVELOPMENT, verify is TESTING or BUGFIX.
:::

## Size it by the test list

::: steps
- Each row is one behavior a person has to see working.
- It counts what the software must do, like a function point.
- The open risks set the width of the range.
:::

## The reminder, estimated

| Part | Basis | Hours |
|---|---|---|
| Specify | Questions test already run | 1 to 2 |
| Build and review | Two flows, a scheduler change | 3 to 6 |
| Verify | 18 rows, latency on staging | 4 to 8 |
| **Total** | | **8 to 16** |

::: note
Do this live before running /implement on not.md. Commitment: on staging by Friday with the latency measured, or a message to the instructor by Wednesday saying why not. Compare with the numbers the room gave on the first slide.
:::

## Write it down before you build

On the issue:

```text
Estimate: specify 1–2 h, build and review 3–6 h, verify 4–8 h
```

In every weekly activity report line about it:

```text
UC-NOT-remind-non-submitters: reviewed the agent's diff against the sequence diagram
```

::: note
Project Pulse already stores planned and actual hours on every activity line (the Activity entity). The use case ID at the start is what lets you add them up later.
:::

## Calibrate

::: key
Calibration ratio = actual hours ÷ midpoint of the estimate.
:::

::: steps
- Estimated 8 to 16, logged 18: ratio 1.5.
- Next use case you would call 4 to 8: say 6 to 12.
- A slip you see coming goes to the client at the next meeting, not on the date.
:::

::: joke
Hofstadter's Law: it always takes longer than you expect, even when you take into account Hofstadter's Law.
:::

::: note
The ratio is how you take Hofstadter's Law into account for real. Track it per person and per team: six ratios is how a team finds out that review, not building, is where its hours go.
:::

## Graded on honesty, not accuracy {.center}

::: key
A ratio of 2.3 with a reason earns the same as a ratio of 1.0.
:::

::: warn
Logging fewer hours to look accurate is inflating a weekly activity report, and it is academic dishonesty.
:::

## Friday

::: steps
- Your build-context issue gets an estimate before the agent builds.
- Your weekly activity report lines carry the use case ID.
- Checkpoints 2 and 3: estimate, actual, ratio, and one sentence on the biggest miss.
:::
