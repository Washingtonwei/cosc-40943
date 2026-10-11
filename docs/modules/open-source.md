# Open Source: Dependencies, Supply Chain, and Unfamiliar Code

> **Purpose (one line):** _to be written when authored._


!!! note "This module is still being written"
    The course is being revamped this term, so modules go up as they are written rather than all at once. What is here is usable; the rest is coming. Lectures and studio do not depend on the missing parts.

## Drafting notes (raw — distribute into template sections, then delete before `stable`)

### Recovering a spec from code you did not write

**Why here.** Most first jobs, and some client projects, start from a system with code and few documents. The method's answer is [Starting from an existing codebase](../method.md#starting-from-an-existing-codebase); this section carries it into the module. Do not restate the method's steps; teach the one judgment.

**The judgment: the code is evidence, never authority.** Ask an agent to document an existing system and it writes down what the code does, defects included. It has no way to tell an intended rule from an accident, so a missing check, a wrong default, or a race it reads back arrives in the draft as a requirement. Each recovered statement needs someone who owns the intent (the client, or the project's maintainer) to call it intended, corrected, or a defect.

**Worked example still to find.** Project Pulse's requirements were written before its code, so it has no recovery story. Candidates: a client team's existing codebase this term (with permission), or an open-source project the module already uses. Pick one where the draft would have promoted a real defect into a requirement.

**Exercise idea.** Have the agent draft use cases for one area of an unfamiliar repository, then mark each step intended, unclear, or suspect before anyone asks the maintainer. Count the suspects.

### The anchoring failure: xz-utils, CVE-2024-3094, March 2024

The case that proves this module cannot be taught as a code-reading skill alone. This is the one module taught as self-study, so the write-up has to carry the whole argument on its own.

`xz-utils` ships on effectively every Linux and macOS machine. A contributor operating as "Jia Tan" spent roughly **two to three years** building genuine credibility on the project while sockpuppet accounts pressured the original, burnt-out maintainer into handing over more responsibility. Having obtained it, they landed a backdoor targeting the RSA path in `sshd`. **CVSS 10.0.**

It was caught because a Microsoft engineer noticed SSH logins were **roughly half a second slower than expected** and went looking.

Why it belongs here and not only in a security lecture:

- **The attack surface was the human process**, not the code. Review, tests, CI, and signing were all in place, and none of them was the control that failed.
- It is a direct argument that **maintainer burnout is a supply chain risk**, and these students will be contributing to, or depending on, projects like this within a year of graduating.
- Nobody in this course would have caught it either. Say that out loud. The lesson is about dependency posture, not personal vigilance.

**The AI angle:** an agent will happily add a dependency and will not ask who maintains it, how many people can merge to it, or whether the last three releases came from an account created eighteen months ago. Those questions are the human's.

**Source:** the Open Source Security Foundation write-up on CVE-2024-3094 is the best short primer.
