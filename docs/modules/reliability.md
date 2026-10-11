# Reliability

**Slides:** [Reliability](../slides/reliability.html) (the fast version).

> **Purpose (one line):** turn an availability or performance requirement into an objective you can measure, make every call across a network fail the way your specification says it should, and learn from a failure without blaming whoever was at the keyboard.

## 1. Learning objectives

By the end of this module, a student can:

1. Tell a fault from an error and an error from a failure, tell reliability from availability, and compute availability from the mean time between failures and the mean time to repair.
2. Turn a quality-attribute requirement into a service level indicator, a service level objective, and an error budget.
3. For each external dependency, name its timeout, its retry policy, and the degradation the specification requires, and find the one an agent left out.
4. Explain how a retry without idempotency or backoff turns a small failure into a larger one.
5. Write a blameless postmortem: impact, timeline, contributing causes, and actions that change the system rather than a person.

## 2. Where it fits

- **Prerequisites:** [Software Architecture, Just Enough](architecture.md), where availability and robustness entered your specification as quality attributes with numbers.
- **Leads into:** Wednesday's observability lecture, which is how you see whether the objective set here is being met, and [Checkpoint 3](../project.md#checkpoints), where your team shows one objective measured and one dependency failing on purpose.
- **How it's taught:** Monday of week 12; whatever the lecture does not reach, read here. Your team does the hands-on out of class and shows it at Checkpoint 3.
- **Course outcome it delivers:** [building, testing, and shipping a working MVP](../syllabus.md#learning-outcomes) (outcome 4). Shipping includes knowing whether it stays up.

## 3. Motivation

**Fourteen hours and thirty-two minutes.** On October 19, 2025, at 11:48 PM Pacific, DynamoDB in AWS's `us-east-1` region began failing. Two copies of its DNS automation raced: one applied a plan late, the other applied a newer plan and then deleted the older one as stale, and the service's regional endpoint was left with no IP addresses. AWS restored the DNS record about two and a half hours later. The outage did not end there.

| Time (PDT) | What happened |
|---|---|
| Oct 19, 11:48 PM | DynamoDB's regional endpoint resolves to nothing; requests fail |
| Oct 20, about 2:25 AM | DNS record restored; DynamoDB recovers |
| until 5:28 AM | The EC2 lease manager, which depends on DynamoDB, tries to renew leases for the whole fleet at once; leases time out before they complete; manual intervention ends the "congestive collapse" |
| until 2:09 PM | Network Load Balancer health checks fail on new instances, removing and restoring them |
| 2:20 PM | All services recovered |

The first two and a half hours were a defect. The next twelve were the system's own recovery: a dependency nobody drew on a diagram, and a retry that every server ran at once. Recovery is a behavior you design, or one you discover.

**Project Pulse promises something it cannot check.** Its specification says `AVL-uptime`: available at least 99% of each academic term, with deadlines prioritized. Its own architecture document lists, under known gaps, "No **alerting** rules or **SLOs**" and production telemetry "not collected anywhere yet." If Project Pulse were down every Monday morning when weekly activity reports are due, nothing in it would notice. A requirement nobody measures is a wish with an identifier.

## 4. Core concepts

### 4.1 Fault, error, failure

Three words, one chain (Avižienis, Laprie, Randell, and Landwehr 2004):

| Term | Meaning | In Project Pulse's invitations, before September 10, 2026 |
|---|---|---|
| **Fault** | The cause: a defect in code, configuration, or the environment | An exception for one undeliverable address escaped the method that sends a batch of invitations |
| **Error** | The fault's effect on the system's state | The transaction around the batch rolled back, deleting invitation rows for students already emailed |
| **Failure** | The system does something its specification says it must not | Students received an invitation and were then told they had not been invited |

A fault that never reaches an error is harmless; an error caught before it reaches a user is handled. Reliability work is putting catches in that chain.

### 4.2 Reliability and availability

**Reliability** is the probability the system does what its specification says for a stated period. **Availability** is the fraction of time it is ready to. They differ: a system that crashes for one second every minute is highly available and not reliable.

```text
availability = MTBF / (MTBF + MTTR)
```

MTBF is the mean time between failures; MTTR, the mean time to repair. A team of students on one Azure container cannot make failures rare. It can make repair fast, which raises availability just as much. Project Pulse's staging slot is an MTTR decision: a bad release is undone by swapping the slots back, in seconds, without a rebuild.

### 4.3 From requirement to measurement: SLI, SLO, error budget

Google's site reliability engineers (Beyer et al. 2016) split a reliability promise into three parts:

| Part | Definition | `AVL-uptime`, made measurable |
|---|---|---|
| **Service level indicator (SLI)** | A measured ratio of good events to all events | The fraction of one-minute probes of the health endpoint that return healthy |
| **Service level objective (SLO)** | The target for the indicator over a window | At least 99% over the term |
| **Error budget** | What the target lets you spend | 1% of a 16-week term: 112 days × 24 hours × 0.01 ≈ **27 hours** |

The budget is the useful part. Twenty-seven hours is a day; one bad Friday deploy that takes the site down until Monday spends two-thirds of the term's budget. While budget remains, a team can ship risky changes; when it runs out, the next release is a reliability fix.

"With deadlines prioritized" is a second objective, not a footnote: a stricter SLO over the windows that matter, such as Monday mornings before weekly activity reports are due.

**The probe has to check the right thing.** Project Pulse's architecture document records that production answers unknown paths with its single-page app and `200 text/html`, so a probe that checks only the status code reports "up" for an endpoint that does not exist. Only the content type distinguishes the real health response. An SLI that cannot fail measures nothing.

Project Pulse's performance requirements are already SLO-shaped: `PER-report-load` asks for the dashboard and report views within 500 milliseconds at the 95th percentile. Its availability requirement is the one with no indicator. Wednesday's observability lecture is where the measurement gets built.

### 4.4 Failing well: timeout, retry, isolation, degradation

Every call that leaves your process (the database, the mail server, an LLM, a client's API) can be slow, can fail, or can succeed without your knowing. Each one needs four decisions, and the agent will make none of them unless you specify them:

**Timeout: how long to wait.** Project Pulse's mail configuration sets no SMTP timeout, and Jakarta Mail documents its default as infinite, so a Gmail server that accepts a connection and never answers holds a request thread until someone restarts the app. Timeouts also have to agree across layers. Project Pulse's browser client gives every request 10 seconds. Inviting a course section sends one email per student before the server answers, which takes longer. The browser gave up and showed a failure toast; the server went on and delivered every invitation. "Failed" in the browser did not mean "did not happen" on the server.

**Retry: whether to try again.** Only retry an operation that is safe to repeat (*idempotent*). The course admin who saw that failure toast would reasonably send the same list again. Each re-invitation minted a fresh token over the row keyed by the student's email, so every link already delivered stopped working. The fix, in commit [`40cf96d`](https://github.com/Washingtonwei/project-pulse/commit/40cf96d), reuses an existing invitation's token, which makes re-inviting idempotent, and gives the invite routes their own 180-second timeout. When a retry is safe, space it out: exponential backoff with random jitter, so a thousand clients do not retry in the same millisecond (Brooker 2015). The EC2 lease manager in [the motivation](#3-motivation) is what happens without that: recovery traffic large enough to keep the system down, a *metastable failure* (Bronson et al. 2021).

**Isolation: how far one failure spreads.** Project Pulse's [`WeeklyReminderScheduler`](https://github.com/Washingtonwei/project-pulse/blob/main/backend/src/main/java/team/projectpulse/system/WeeklyReminderScheduler.java) catches twice: once per student, so one rejected address no longer aborts "the whole morning at the first bad one," and once per course section, so a section that cannot be read does not skip every section after it. Its comment explains why: the run is unattended, so whatever fails has to be logged and stepped over rather than surfaced to a caller. Nygard (2018) calls the pattern a *bulkhead*, after the walls that keep one flooded compartment from sinking a ship.

**Degradation: what the user sees instead.** The specification decides this, not the code. Project Pulse's `AVL-llm-degradation` says that while the LLM is unavailable, everything else keeps working and the AI features say clearly that they are unavailable; `PER-ai-response-time` bounds the wait at 15 seconds. The reminder's design returns a `failed` list naming who was not reached (use case extension 6a in [`not.md`](https://github.com/Washingtonwei/project-pulse/blob/main/docs/design/not.md)). A degradation nobody specified is whatever the agent happened to write.

### 4.5 Dependencies that are sometimes wrong

A mail server fails loudly: an exception, a timeout. An LLM can also fail quietly, by answering quickly with something plausible and wrong. That third failure mode is not reliability in the uptime sense, but it reaches users the same way. Project Pulse specifies two defenses for its AI assistants, which are specified but not yet built: requests and responses use a structured JSON schema (`SI-llm-json`), so a response that does not parse is a detectable failure rather than text shown to a student, and the instructor can disable an assistant per course section (`FR-AI-enablement`), a switch that turns a misbehaving dependency off without a deploy. If your client's system calls a model, it needs the same three things as any dependency (a timeout, a degradation, an off switch) plus a check on the shape of what comes back.

### 4.6 Incidents and blameless postmortems

Something will fail in production this year. The difference between a team that learns from it and one that repeats it is the postmortem: a short written account of what happened, why, and what changes. It is **blameless**: it asks what about the system let a reasonable person make that mistake, because the person who made it is the one who knows how it happened, and a blamed person stops telling you (Allspaw 2012; Beyer et al. 2016, chapter 15).

Project Pulse's invitation failures, fixed on September 10, 2026, the day invitations went to a 77-student section, as a postmortem:

| Section | Content |
|---|---|
| **Summary** | Three defects in one path: a single bad address rolled back invitations already emailed; the browser timed out on a batch the server completed; a re-sent batch invalidated every link already delivered. |
| **Impact** | Students could be told they were not invited after receiving an invitation, or hold a link that no longer worked. |
| **Timeline** | First fix (commit [`41d306c`](https://github.com/Washingtonwei/project-pulse/commit/41d306c)): catch per address and report invited and failed lists. Code review of that fix found that its advice (invite in batches of about 20) could not work under the 10-second client timeout, and traced the re-send that broke tokens. Second fix (`40cf96d`) seven minutes later. |
| **Contributing causes** | Email is not transactional but sat inside a transaction; one timeout for every route regardless of how long the route takes; a non-idempotent operation the interface invites users to repeat; a test that stayed green against a broken mail path because delivery failures had become payload data. |
| **What went well** | Review of the first fix caught the second and third defects; the new tests were checked against the reverted code to confirm they fail without the fix. |
| **Actions** | Per-address and per-section isolation; idempotent re-invitation; a per-route timeout; tests that assert the invited and failed lists. One finding left open and recorded (`OI-54`: inviting instructors still aborts its batch). |

Every action changes the system. None of them is "be more careful."

## 5. The AI-native lens

- **Delegate to AI:** applying a policy you wrote down. Given "every outbound call has a timeout of N seconds, retries only idempotent calls, at most three times, with exponential backoff and jitter," an agent can find every call site and apply it. It can also draft a postmortem's timeline from commits, pull requests, and logs.
- **Keep human:** the objective and the degradation. How much downtime your client can tolerate, and what a user should see when the mail server is down, are client decisions recorded in the specification. So is which operations are safe to repeat: idempotency is a property of the business operation, not the code.
- **Context to supply:** the quality attributes with their numbers, each external dependency and how it fails, and which operations are idempotent. An agent asked to "add error handling" without these writes a `catch` that logs and continues, which is the right answer for the reminder scheduler and the wrong one for a payment.
- **How to verify:** a test that makes the dependency fail and asserts the specified degradation, checked against the code with the fix reverted, so you know it can fail. Then read every retry loop for a cap, a backoff, and an idempotent target. Project Pulse's first invitation fix was written with an agent and passed its tests; review of the fix found the timeout flaw.

## 6. Risks & mitigations

| Risk (classic + AI-introduced) | Human judgment that catches it | Mitigation |
|---|---|---|
| **Classic:** a reliability requirement nobody measures | Asking "how would we know?" of every `AVL-*` and `PER-*` requirement | An SLI and SLO for each, with a probe that can fail |
| **AI-introduced:** generated code calls a network service with no timeout and a tight retry loop, because the happy path is what it was asked for | Reading every outbound call for its timeout, retry, and fallback | A written policy in the charter; a degradation test per dependency |
| **AI-amplified:** an agent "handles" an error by catching and logging it, so a failure the user should see becomes silent | Asking what the user sees when this call fails, and finding it in the specification | The specified degradation, asserted by a test |

## 7. Hands-on (studio + optional individual assignment)

**Studio (team, own project)**

- **Goal:** your system's reliability promise is measured, and one of its dependencies fails the way your specification says.
- **On your own project, out of class:** turn one availability or performance requirement in your specification into an SLO: name its SLI, its window, its target, and its error budget, and write them under the requirement. Then write one automated test that makes an external dependency fail (an email service, a client API, a model) by throwing or timing out, and asserts the degradation your specification requires. If your specification never says what happens when that dependency fails, write that requirement first. Run the test once against code with the handling removed, to see it fail.
- **Deliverable & assessment:** at [Checkpoint 3](../project.md#checkpoints), show the SLO with its current measured value (the observability you built that week supplies it) and the degradation test, red against the reverted code and green against yours.

**Individual assignment (Project Pulse):** none.

## 8. Summary / key takeaways

- A fault causes an error; an error not caught becomes a failure a user sees. Reliability work puts catches in that chain.
- A requirement becomes a promise you can keep only with an indicator, an objective, and a budget. A probe that cannot fail measures nothing.
- Every call across a network needs a timeout, a retry policy, an isolation boundary, and a specified degradation. An agent will supply none of them unless you do.
- Retry only what is safe to repeat, and space retries out. Recovery traffic can keep a system down longer than the original fault.
- Postmortems are blameless and end in changes to the system.

## 9. Key papers & further reading

- Avižienis, A., Laprie, J.-C., Randell, B., and Landwehr, C. "Basic Concepts and Taxonomy of Dependable and Secure Computing." *IEEE Transactions on Dependable and Secure Computing* 1, no. 1 (2004): 11–33.
- Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds. *Site Reliability Engineering: How Google Runs Production Systems*. O'Reilly, 2016. Chapter 4 (service level objectives) and chapter 15 (postmortem culture). Free at <https://sre.google/sre-book/table-of-contents/>.
- Nygard, M. T. *Release It! Design and Deploy Production-Ready Software*. 2nd ed. Pragmatic Bookshelf, 2018. Timeouts, circuit breakers, bulkheads.
- Brooker, M. "Exponential Backoff and Jitter." AWS Architecture Blog, 2015. <https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/>
- Bronson, N., Aghayev, A., Charapko, A., and Zhu, T. "Metastable Failures in Distributed Systems." *HotOS* 2021.
- Allspaw, J. "Blameless PostMortems and a Just Culture." Code as Craft (Etsy), 2012.
- Amazon Web Services. "Summary of the Amazon DynamoDB Service Disruption in the Northern Virginia (US-EAST-1) Region." October 2025. <https://aws.amazon.com/message/101925/>

## 10. Self-check

1. A student's weekly activity report saves, but the confirmation email never arrives because Gmail rejected it. Name the fault, the error, and the failure, and say whether the failure is one your specification should allow.
2. Your client's system must be "available 99.5% during the semester." Write the SLI, the SLO, and the error budget for a 15-week semester.
3. Your agent wrote a loop that retries a failed payment request every 100 milliseconds until it succeeds. Name two things wrong with it.
4. The course admin's browser shows "invitation failed," and the admin clicks Send again. Before `40cf96d`, what happened to the students already invited, and what property was missing?
5. A postmortem's only action item is "developers must test more carefully." Rewrite it as an action that changes the system.

## Related

- [Software Architecture, Just Enough](architecture.md): where availability and robustness became quality attributes with numbers.
- [Project](../project.md): Checkpoint 3, where the SLO and the degradation test are shown.
- [Schedule](../schedule.md): when this is taught.

<!--
## Drafting notes (raw: distribute into template sections, then delete before `stable`)

### Sources to check before `stable`

- AWS timeline: start 11:48 PM PDT Oct 19, end 2:20 PM Oct 20, the race (two DNS Enactors, clean-up deleting the older plan), DWFM congestive collapse to 5:28 AM, checked against The Register's reading of the post-event summary and the instructor's 2025 deck; the AWS page itself refused the connection on 2026-10-10. NLB "until 2:09 PM" and DynamoDB recovery "about 2:25 AM" from the summary via secondary sources and the instructor's deck. Confirm all against https://aws.amazon.com/message/101925/.
- Jakarta Mail: confirm "Default is infinite timeout" for mail.smtp.connectiontimeout and mail.smtp.timeout in the com.sun.mail.smtp package summary.
- Avižienis et al. 2004 pages; Beyer et al. chapter numbers; Bronson et al. author list; Allspaw 2012 date.
- Project Pulse facts checked against `main` at `8768a1d` on 2026-10-10: AVL-uptime, PER-report-load, PER-ai-response-time, AVL-llm-degradation, SI-llm-json, FR-AI-enablement (SRS); "No alerting rules or SLOs", production telemetry not collected, the 200 text/html SPA fallback (architectural-design.md, Known gaps); no SMTP timeout in application-prod.yml; the 10-second Axios timeout and 180-second invitation timeout (frontend/src/utils/request.ts, frontend/src/apis/section/index.ts); WeeklyReminderScheduler's two catches; commits 41d306c and 40cf96d; OI-54.
- Ask the instructor: did the invitation failures reach real students on September 10, 2026, or were they found in review first? If they reached students, the Impact row can say so.
-->
