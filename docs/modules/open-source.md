# Open Source: Dependencies, Supply Chain, and Unfamiliar Code

> **Purpose (one line):** _to be written when authored._


!!! note "This module is still being written"
    The course is being revamped this term, so modules go up as they are written rather than all at once. What is here is usable; the rest is coming. Lectures and studio do not depend on the missing parts.

## Drafting notes (raw — distribute into template sections, then delete before `stable`)

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
