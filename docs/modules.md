# Modules

A module is the full written version of a lecture topic. The deck is the fast version you see in class; the module is the one you read when you want more than the deck, or when you missed the hour.

**Reading a module is optional unless the [schedule](schedule.md) says otherwise.** The schedule is also where you find out when each topic is taught, and it links that week's slides and reading directly.

Modules go up as they are written, in the order the course teaches them, so this list grows through the term.

## Published so far

[**SE and What AI Changes**](modules/se-and-ai.md) · [slides](slides/se-and-ai.html)
: What is left for a software engineer when the agent can write the code. Places a task on the delegation boundary, and sizes an unfamiliar problem in twenty minutes well enough to defend it against the agent's version.

[**The AI-Augmented Team**](modules/ai-augmented-team.md) · [slides](slides/ai-augmented-team.html)
: Set your team up so the work is legible to every member, including the one that forgets everything between sessions. Put what governs the project in the repository, and make every unit of work traceable from requirement to merged code.

[**Professionalism**](modules/professionalism.md) · [slides](slides/professionalism.html)
: Run a team problem the way you run a defect: observe the behavior, analyze its impact, investigate before you assume, and agree on a fix with an owner and a date. The standards themselves are on the [Professionalism handbook](professionalism.md).

[**Requirements as the Contract**](modules/spec-driven-requirements.md) · [week 3 slides](slides/spec-driven-requirements.html) · [week 4 slides](slides/writing-the-specification.html)
: Find out what your client actually needs, and write it down so your team and your agent build the same thing. Running a first client meeting, business objectives and success metrics, the project glossary, and the scope line you will need in October, and use cases an agent can build from. The nine kinds of requirement are in [Requirement Types](requirement-types.md). Business rules, quality attributes, and the specification are still being written.

[**Context Engineering**](modules/context-engineering.md) · [slides](slides/context-engineering.html)
: Assemble, for one unit of work, the context an agent cannot infer out of the specification you already wrote, and tell whether you supplied enough by measuring what got built rather than how good the prompt felt. How big the context window really is, how an agent finds code, managing a session that fills up, and why you cite the specification instead of copying it.

[**Software Architecture, Just Enough**](modules/architecture.md) · [slides](slides/architecture.html)
: Decide, before the code exists, the few things that will be expensive to change, and let the quality attributes your client cares about choose them rather than the feature list. Architecturally significant requirements, C4 context and container diagrams, dividing a system by domain, one deployable or several, writing a decision down, and the trust boundary.

[**Requirements Traceability**](modules/traceability.md)
: Keep a use case honest end to end, forward (is it built and tested?) and backward (why does this code exist?), and see why that matters more, not less, when an AI writes the code. Still being written.
