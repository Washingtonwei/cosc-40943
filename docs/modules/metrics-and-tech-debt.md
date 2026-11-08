# Software Metrics and Technical Debt

> **Purpose (one line):** _to be written when authored._


!!! note "This module is still being written"
    The course is being revamped this term, so modules go up as they are written rather than all at once. What is here is usable; the rest is coming. Lectures and studio do not depend on the missing parts.

## Drafting notes (raw: distribute into template sections, then delete before `stable`)

### The anchoring failure: Southwest Airlines, December 2022

The economics-of-rigor argument with a price tag attached.

Southwest ran crew scheduling on **SkySolver**, built roughly two decades earlier when the airline served **58 destinations**. It leaned heavily on manual input and degraded past roughly **300 simultaneous schedule reassignments**. A winter storm produced far more than that. The optimizer could not converge, the manual fallback collapsed under the volume, and Southwest cancelled about **16,900 flights**, roughly two-thirds of its schedule, stranding **more than 2 million passengers** over the holidays. Losses ran to about **$1 billion**.

The detail that makes this a technical debt case rather than a weather case: **crews were frequently in the right place to fly, and the system had no way to know it.** The capability existed in the world and not in the software.

**Teach it as:** a quality attribute that was correct when written and was never revisited. Nobody made a bad decision. A good decision aged out of validity while the system kept passing every test it had. Ask the room which artifact should have caught this and steer toward the architecture's quality-attribute record plus a scheduled re-examination, not "better code".

**The AI angle:** agents make it cheaper than ever to *add* to a system like SkySolver, and no cheaper at all to notice that its central assumption expired. Debt accrues in the decisions, not in the typing.

**Source:** the *Environmental Research: Infrastructure and Sustainability* paper on the 2022 Southwest scheduling crisis is the most rigorous account.

### Measurement as a thread through the whole course (Fall 2027 design, 2026-11-08)

**The thesis:** engineers use numbers to make decisions, and every metric was invented by someone trying to make one. AI makes artifacts cheap, so judging them is the scarce skill, and numbers are how engineers judge at scale. Teach each metric with its story: what decision it was invented for, so students can tell when it still answers that question and when it has started to lie.

#### Every phase has a number that drives a decision

| Phase | A number | The decision it drives | How it lies |
|---|---|---|---|
| Requirements | open questions per use case; requirements churn | Is the spec ready to design from? | Questions nobody wrote down don't count |
| Estimation | estimate vs. actual (the calibration ratio, `MODULE-implementation` 4.4) | How much to commit to next sprint | Padding makes the ratio look good |
| Design | coupling, the size of each module's interface | Where to split, what to refactor first | Low coupling on paper, a shared database underneath |
| Code | cyclomatic complexity, duplication | What to review hardest, what to simplify | Splitting one hard method into five meaningless ones |
| Review | pull request size, time to first review | Size the step to the review | Rubber-stamp approvals are fast |
| Testing | coverage, mutation score | Where tests are missing | Coverage tells you what ran, not what was checked |
| Static analysis | findings and the baseline trend | Is quality getting better or worse? | Suppressing a warning lowers the count |
| CI/CD | the DORA metrics | Ship faster, or stabilize first? | Deploying empty changes raises frequency |
| Operations | SLI against the SLO; error budget left | Spend the budget on features, or stop and fix reliability? | A probe that cannot fail measures nothing |

#### Each metric is someone's answer to a decision (origin stories)

From memory; check every name, year, and quote against its source before it goes on a slide.

| Number | Who and when | The decision it was invented for | How it lies |
|---|---|---|---|
| The man-month | Brooks, *The Mythical Man-Month*, 1975 | How many people to put on a late project | Adding people to a late project makes it later |
| Coupling and cohesion | Stevens, Myers, and Constantine, "Structured Design," IBM Systems Journal, 1974 | Where to draw module boundaries | Low coupling on paper, a shared database underneath |
| Cyclomatic complexity | McCabe, "A Complexity Measure," IEEE TSE, 1976 | How many tests a method needs (one per independent path), and when to split it (he suggested 10) | Split one hard method into five meaningless ones |
| Function points | Albrecht, IBM, 1979 | How big a system is, independent of the programming language | Expensive to count, so nobody does |
| Code coverage | Miller and Maloney, CACM, 1963 | Which parts of the program the tests never ran | Tells you what ran, not what was checked |
| Mutation score | DeMillo, Lipton, and Sayward, "Hints on Test Data Selection," 1978 | Whether the tests would catch a real bug | Slow to compute; some mutants change nothing |
| Goal-Question-Metric | Basili, 1980s, NASA Software Engineering Laboratory | Which numbers to collect at all: start from the goal, not from what is easy to count | A method, so it lies only when skipped |
| Technical debt | Cunningham, OOPSLA experience report, 1992 | Whether to ship now and pay back later | A metaphor, so tools put a dollar figure on it nobody can justify |
| Story points | Extreme Programming, late 1990s (Ron Jeffries has said he may have invented them, and is sorry) | How much fits in an iteration | They become a target and inflate |
| SLO and error budget | Google SRE, 2000s (Beyer et al. 2016) | Ship features, or stop and fix reliability? | A probe that cannot fail measures nothing |
| DORA metrics | State of DevOps reports from 2014; *Accelerate*, 2018; five metrics today (dora.dev) | Is our delivery getting better? | Deploying empty changes raises frequency |
| Goodhart's law | Goodhart, economist, 1975 | The warning over all of the above | "When a measure becomes a target, it ceases to be a good measure" (Strathern's later phrasing) |

**The AI twist:** agents break the old numbers. Lines of code and commit counts mean nothing when an agent writes 2,000 lines in a minute, and coverage is cheap to inflate with tests that check nothing. Ask which numbers still mean something when AI writes the code: how often an agent's pull requests merge without rework, revert rate, mutation score over coverage.

#### The design for the next offering

1. **Week 2, one lecture on measuring engineering:** measure vs. metric, Goal-Question-Metric, whether a number measures what it claims to (construct validity), and Goodhart's law. Two or three origin stories as the hook; open with Brooks's man-month. Draw on CMU 17-313's metrics lecture (`notes/cmu-17-313-notes.md`).
2. **Every module gets a "The number" box:** one metric, its origin story in a paragraph, the decision it informs, and how it lies. It lives where the decision happens: complexity in static analysis, coverage and mutation score in testing, DORA in CI/CD (4.11 already introduces them), SLOs in reliability, the calibration ratio in implementation. Fall 2026 has one so far: "What does this number measure?" in observability 4.4.
3. **A team engineering dashboard all term,** pulled from GitHub: pull request size, time to first review, CI pass rate, the coverage trend, deploy frequency. At every checkpoint, each team reports **one decision it made from a number.**
4. **Research:** 13 teams' numbers across a term, half of it AI-written code, is data for the AI4SE paper or Hiep's work. Settle consent and IRB before the term starts.

**This module's role then:** the week 2 lecture's home, or the owner of the shared vocabulary that each module's box links to. Decide which when the week 2 schedule is set.
