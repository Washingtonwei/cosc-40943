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
