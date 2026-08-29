# Testing

> **Purpose (one line):** _to be written when authored._


!!! note "This module is still being written"
    The course is being revamped this term, so modules go up as they are written rather than all at once. What is here is usable; the rest is coming. Lectures and studio do not depend on the missing parts.

## Drafting notes (raw — distribute into template sections, then delete before `stable`)

### The anchoring failure: CrowdStrike, 19 July 2024

The case this module is built around, and it is the week-1 deck's green-tests slide made real. Roughly 8.5 million Windows machines blue-screened worldwide.

An IPC template type defined **21 input fields**. The sensor code supplied **20**. Channel File 291 was the first template instance to use a real value in the 21st field rather than a wildcard, the Content Interpreter had **no runtime array bounds check**, and the result was an out-of-bounds read and an invalid page fault in a kernel driver.

The part that belongs in this module rather than in a security lecture:

- **The tests passed because the test data used wildcard matching for the 21st field.** The mismatch could not manifest under those inputs. The suite agreed with the code and said nothing about the contract.
- The Content Validator had a logic error of its own, so the layer meant to catch this was itself unverified against this case.
- Nothing about the defect was subtle. One bounds check turns a global outage into a logged error.

**Teach it as:** tests written from the implementation confirm the implementation; tests written from the contract can fail. Ask the room which kind an agent writes by default. The answer is the first kind, every time. Direct callback to the week-1 story ([SE and What AI Changes](se-and-ai.md)) and its "312 tests, 312 passing, all green if the whole feature is wrong" slide.

**Also lands here:** staged and canary rollout as a testing concern, not only an operations one. A 1% ring would have made this an incident rather than a catastrophe.

**Source:** CrowdStrike's external root cause analysis for Channel File 291 (August 2024) is public and readable. Assign the first few pages.

### Name the oracle (three minutes, and week 12 depends on it)

Say the word out loud in this module: an **oracle** is whatever decides that an execution was correct. A test is inputs plus an oracle, and the oracle is the only half that carries intent. Inputs decide what the code does; the oracle decides what "right" means.

This costs one slide and it is not new content, it is a label for the two things already taught here. CrowdStrike had inputs (test data that wildcarded the 21st field) and an oracle that agreed with the implementation, so the suite was green on a contract it never checked. The login ladder is the same lesson from the other side: the room's junior list is not short on inputs, it is short on any idea of what correct means beyond "it logged me in."

Once named, the CrowdStrike line becomes a definition rather than an aphorism: tests written from the implementation get their oracle from the implementation, which is why they cannot fail. That is also the answer to what an agent produces by default.

**Hand-off.** `MODULE-dynamic-analysis` (week 12) builds its oracle ladder on this word and teaches the in-source `assert` as an oracle over every execution rather than one example. Its section 4 assumes the word was named here. Skip these three minutes and week 12 has to define it cold.

**Keep the `assert` statement out of week 9.** It belongs beside fuzzing, where a stronger oracle is what turns a crash-finder into a bug-finder, and this week is a single Wednesday anyway (the midterm takes Monday). Week 9 owns the test assertion as an oracle for one input; week 12 owns the in-source assertion as an oracle for all of them.

### The opener: "how would you test the login?"

Carried forward from the 2025 deck (appendix), where it was buried behind the introduction lecture. It belongs here, and it is the best opener this module has.

Put a login form on the screen and ask the room to list test cases. Collect answers, then reveal the ladder they were climbing without knowing it:

- **Junior.** Correct username and password, does it work.
- **OK.** The combinatorics: wrong password, wrong username, both wrong, empty fields, one empty field, CAPTCHA correct and incorrect.
- **Experienced.** Case sensitivity. Password masked. Default-password reminders. Forgot username and forgot password. Length and complexity limits. CAPTCHA refresh. Session expiry after inactivity. Role-based redirects. Focus in the username field on load. Tab and Enter.
- **Super.** Password encrypted in transit and at rest. Expiry reminders. Direct URL access to protected pages without a session. Password readable from the clipboard or from view-source. SQL injection. XSS. Lockout after repeated failures. Same user on two browsers and on two devices. Login response time. A million concurrent logins. Browser and version matrix. Error messages that tell the user what to do next.

**Why it works:** every student produces the junior list, most produce the OK list, and almost nobody gets past it. The gap between "I can write this feature" and "I can say when this feature is done" is the whole module, visible in four minutes, with nobody needing to be told they are inexperienced.

**The AI-native turn, which is the reason to keep it:** run the same prompt against an agent live. It will produce something between the experienced and super lists in seconds, and better organized than the room's. Then ask the question that matters: which of these actually apply to *this* system, and which are ceremony? The agent generates the list. Deciding what is in scope, what the lockout threshold should be, and whether a million concurrent logins is a real requirement is the human's, and it is the delegation boundary in the one place students feel it.

**Time:** four to six minutes for the room, three for the agent comparison.
