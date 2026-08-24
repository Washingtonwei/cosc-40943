# Software Metrics and Technical Debt

> **Purpose (one line):** _to be written when authored._


!!! note "This module is still being written"
    The course is being revamped this term, so modules go up as they are written rather than all at once. What is here is usable; the rest is coming. Lectures and studio do not depend on the missing parts.

## Drafting notes (raw — distribute into template sections, then delete before `stable`)

### The anchoring failure: Southwest Airlines, December 2022

The economics-of-rigor argument with a price tag attached.

Southwest ran crew scheduling on **SkySolver**, built roughly two decades earlier when the airline served **58 destinations**. It leaned heavily on manual input and degraded past roughly **300 simultaneous schedule reassignments**. A winter storm produced far more than that. The optimizer could not converge, the manual fallback collapsed under the volume, and Southwest cancelled about **16,900 flights**, roughly two-thirds of its schedule, stranding **more than 2 million passengers** over the holidays. Losses ran to about **$1 billion**.

The detail that makes this a technical debt case rather than a weather case: **crews were frequently in the right place to fly, and the system had no way to know it.** The capability existed in the world and not in the software.

**Teach it as:** a quality attribute that was correct when written and was never revisited. Nobody made a bad decision. A good decision aged out of validity while the system kept passing every test it had. Ask the room which artifact should have caught this and steer toward the architecture's quality-attribute record plus a scheduled re-examination, not "better code".

**The AI angle:** agents make it cheaper than ever to *add* to a system like SkySolver, and no cheaper at all to notice that its central assumption expired. Debt accrues in the decisions, not in the typing.

**Source:** the *Environmental Research: Infrastructure and Sustainability* paper on the 2022 Southwest scheduling crisis is the most rigorous account.
