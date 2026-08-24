# Requirements as the Contract

> **Purpose (one line):** _to be written when authored._


!!! note "This module is still being written"
    The course is being revamped this term, so modules go up as they are written rather than all at once. What is here is usable; the rest is coming. Lectures and studio do not depend on the missing parts.

## Drafting notes (raw — distribute into template sections, then delete before `stable`)

### The 737 MAX belongs here, not in week 1

The failure story this module is built around. It moved out of `MODULE-se-and-ai` because week 1 opens on a senior design collapse students recognize themselves in, which is the better opening but cannot make this module's argument: **a contract that was met can still be the wrong contract.** Land it here, after students have spent a week writing glossaries and use cases and are beginning to suspect it is busywork.

MCAS worked as specified. It read a single angle-of-attack sensor and pushed the nose down. The software did what the requirements said. The requirements were wrong, the hazard analysis understated the failure mode, the single-sensor dependency survived review, and pilots were not told the system existed. 346 people died from a process failure, not a coding failure.

Strip the airplane and every link in that chain is an artifact this module owns:

| The failure | The artifact that should have caught it |
|---|---|
| The requirement was wrong | Vision and scope; the use case's failure paths |
| Hazard analysis understated the failure mode | Quality attributes, risk analysis |
| Single-sensor dependency survived review | Architecturally significant requirement; design review |
| Pilots not told the system existed | Scope: is the operator inside the system boundary? |
| It shipped meeting its spec | Verification against validation |

**The punchline, which is the reason to keep it in an AI-native course:** an agent asked to implement MCAS from that specification would have implemented it faster, with better test coverage, and just as fatally. Cheap generation does not touch a wrong requirement; it ships it sooner.

Also the cleanest available example for the Napkin's "risks as mechanisms, not categories": *single sensor, no cross-check, no disagreement alarm* is a mechanism. *Safety risk* is bingo.

**Restore alongside it when authoring:**

- Learning objective: explain why a failure like the 737 MAX is a requirements failure rather than a coding failure, and identify which parts of that chain an agent cannot own.
- Self-check: MCAS met its specification. Where in the chain from business need to shipped code should it have been caught, and what artifact would have caught it?
- Delegation-boundary callback to [SE and What AI Changes](se-and-ai.md): "delegate everything" produces the MCAS outcome at speed.
- Readings: the Joint Authorities Technical Review and the House Committee on Transportation reports (2019-2020), requirements and hazard-analysis chapters. Nancy Leveson, *Engineering a Safer World* (2011), chapters 1-2, on failures as control-structure failures. CMU 17-313's case study deck is in `reference/courses/CMU-17-313-foundations-of-software-engineering/03-737MAX.pdf`.

Budget about ten minutes. It no longer has to carry the course opening.

### The Yellow Walkman: what users say versus what they take

Carried forward from the 2025 deck (appendix). Elicitation content that was parked behind the introduction lecture and never taught.

Sony runs a focus group on a yellow sport Walkman. The room loves it: sporty, fresh, so much better than another black one. On the way out, participants are offered a free Walkman from two tables, black on one and yellow on the other. Everyone takes a black one.

**Teach it as:** what people say in an interview is data about the interview, not about what they will do. Asking "would you use this?" reliably produces yes. The fix is not better questions, it is arranging a situation where the answer costs something: a pre-order page, a signup, a choice between two real options, a prototype they have to actually work with.

**Why it belongs in this module:** students will elicit requirements from a real client who wants to be helpful and will agree with almost any feature proposed enthusiastically. That is how a team ends up building the yellow Walkman. Pair it with the use-case work: a use case with real preconditions and failure paths is harder to nod along to than a feature name.

**The AI-native turn:** an agent asked to generate requirements from a client interview transcript will faithfully encode everything the client said, including the parts they did not mean. It has no way to tell enthusiasm from commitment. Neither does a transcript. That distinction is elicited by a human, in the room, by watching what the client does rather than what they say.

**Source:** <https://www.alexandercowan.com/yellow-walkman-data-art-of-customer-discovery/>

### Other notes

- **User stories are introduced, then critiqued** (`DECISION-user-stories-demoted`): teach them as the mainstream agile unit students will meet in industry, then show where they run out.
