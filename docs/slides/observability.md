---
title: Observability and Debugging
module: observability
week: 12
day: Monday and Wednesday
---

# Observability and Debugging

Week 12 · Seeing inside Project Pulse after it ships

::: note
**Say:** Two weeks ago we shipped. The pipeline builds it, checks it, and puts it on Azure. Today's question: once it's running, how do you know what it's doing? Monday is the lecture. Wednesday I run Project Pulse on my laptop, break it on purpose, and you tell me where to look.
:::

## Deployment is not the end {.center}

![A developer outside the production panel asks how to see inside the deployed app, while inside the app goes down, gets slow, loses its database, and runs out of CPU, memory, or disk](img/observability-blind-spot.svg)

::: note
**Say:** Your code passed its tests and its gate. Now the database can go offline, a release can carry a defect, a page can get slow, the disk can fill. None of that happens in your test suite. So how do you see inside? HealthCare.gov learned the hard way.
:::

## Nobody could tell if it was up

::: steps
- October 1, 2013: HealthCare.gov launches and breaks under its first traffic
- Mid-October: about 3 in 10 visitors can get on at all
- The rescue team finds no dashboard, "no quick way for engineers to measure what was going on"
- "Nobody could even tell us if the system was up."
:::

::: note
**Say:** This is the federal website for buying health insurance. A White House adviser said that last line. People checked whether the site was up by opening a laptop and trying it. Source: Steven Brill, Time, February 2014.
:::

## The first fix was a dashboard

::: steps
- The rescue team built the dashboard first
- Then they could rank the problems and fix the worst ones first
- By December 1: uptime from 43% to 95%, errors from 6% to 0.5%
:::

::: key
You cannot fix what you cannot see.
:::

::: note
**Say:** Not a rewrite, not a new architecture. A dashboard. Once they could see the system, the work became a list in priority order.
:::

## Monitoring is the base {.center}

![The service reliability hierarchy as a pyramid: monitoring at the base, then incident response, postmortem and root cause analysis, testing and release procedures, capacity planning, development, and product at the top](img/observability-reliability-hierarchy.svg)

::: note
**Say:** Google engineers on that rescue team, Mikey Dickerson among them, used this pyramid to explain how a service becomes reliable. It's in the SRE book. Everything sits on monitoring: "Without monitoring, you have no way to tell whether the service is even working."
:::

## Project Pulse would not have known either {.center}

::: key
"Production telemetry is not collected anywhere yet." Project Pulse's architecture document, until November 9, 2026
:::

::: note
**Say:** Project Pulse had all the parts. On my laptop, Docker Compose runs Prometheus, Grafana, and Zipkin beside the app. In production on Azure, nothing collected anything, and the architecture document said so honestly, as technical debt TD-prod-observability. Wednesday you'll see what production does now.
:::

## Nine months without a trace

::: steps
- January 2026: I upgrade Project Pulse from Spring Boot 3 to 4
- Spring Boot 4 sets up tracing only through its own modules
- Every test passes, and tracing is off
- No trace IDs, nothing in Zipkin, for nine months
:::

::: ask
How would you have noticed?
:::

::: note
**Say:** This one is mine. The build still named the old tracing libraries; they were on the classpath and nothing wired them up. Nothing failed, nothing logged a warning. I found it this weekend while writing this lecture. Pull request 112 fixes it. The answer to the question: you look at the signal once in a while, or you break something on purpose and check that it shows up.
:::

## That, then why

::: cols
**Monitoring**

A few numbers you picked in advance. Tells you that something is wrong.
|||
**Observability**

Asking new questions of what the system already records. Tells you why, even for a problem you never imagined.
:::

::: note
**Say:** The error count jumps Monday at 9. Which page? Everyone, or one course section? Since when? If you can answer from what you already record, without adding code and redeploying, the system is observable. If all you can say is "errors are up," it isn't. The definition is from Majors, Fong-Jones, and Miranda.
:::

## The gauge and the port {.center}

![A car dashboard with the temperature gauge in the red answers a question you planned; a scanner on the diagnostic port reads out why: the cooling fan relay failed](img/observability-car-dashboard.svg)

::: key
Install the port before the breakdown, not during it.
:::

::: note
**Say:** The gauge is monitoring. The mechanic's scanner on the diagnostic port is observability. You need both.
:::

## Three kinds of telemetry

::: steps
- Metric: a number measured over and over. Tells you that something is wrong
- Trace: one request's path, step by step. Tells you where
- Log: a line of text about one event. Tells you why
:::

::: note
**Say:** Telemetry is the data a running system sends out about itself, the way a spacecraft radios its temperature home. Use them in that order. The error rate went up after the deploy: metric. The invitation request spent its time sending email: trace. The mail server rejected the address: log. OpenTelemetry calls these three "signals"; careful, Google's "golden signals" later today mean something else.
:::

## Three of each, from Project Pulse

| Metric | Trace | Log |
|---|---|---|
| http.server.requests | An instructor invites two students | Sent {} of {} weekly reminders |
| jvm.memory.used | A user logs in | Could not send an invitation email |
| hikaricp.connections.pending | A student adds an activity | Unhandled exception |

::: note
**Say:** Metrics: every request counted and timed, memory in use, requests waiting for a database connection. Traces: one request each, start to finish; we'll open the invitation trace in a few minutes. Logs: real lines from the code. The first is INFO from the weekly reminder job, the other two are ERROR, and the last one is the catch-all handler from pull request 110. The braces get filled in with the counts, the section, and the course. Never the student's email address.
:::

## How do you know?

::: joke
"We have no errors in production." "How do you know?" "We don't log."
:::

::: note
**Say:** No evidence of errors is not evidence of no errors. Project Pulse's catch-all exception handler logged nothing until last week, pull request 110. A student saw "A server internal error occurs." and I saw nothing at all.
:::

## Actuator: the diagnostic port

| Endpoint | Production | Your laptop |
|---|---|---|
| health | status only | each check |
| info | version and commit | plus Java and OS |
| metrics, prometheus | not exposed | admin only |
| loggers, env, beans | not exposed | admin only |

::: note
**Say:** Spring Boot Actuator adds ready-made endpoints under /actuator. One dependency, no code. An endpoint answers only if configuration exposes it, and Project Pulse exposes a different set per profile. In every profile, everything except health and info needs an admin login. The full table is in the module, 4.3.
:::

## Try it on production

```bash
curl https://projectpulse.team/actuator/health
curl https://projectpulse.team/actuator/info
curl https://projectpulse.team/actuator/metrics
```

::: ask
The third one answers 404. Is something broken?
:::

::: note
**Say:** Run these now if you have a laptop open. Health says UP. Info names the version and the Git commit running right now. Metrics answers 404, even with my admin token, because production doesn't expose it at all. An endpoint that isn't exposed has no URL to protect. That's on purpose; we'll see why on September 6.
:::

## Where the telemetry goes {.center}

![Inside Project Pulse, Micrometer hands numbers to Actuator, Brave gives each request a trace ID, and Logback writes log lines. Prometheus pulls the numbers from Actuator every 15 seconds and Grafana queries Prometheus; the app pushes finished spans to Zipkin; Logback writes to standard output with the trace ID on every line](img/observability-signal-flow.svg)

::: note
**Say:** Inside the app: Micrometer counts, Micrometer Tracing with Brave gives each request a trace ID, Logback writes the lines. Outside: Prometheus stores numbers over time, Grafana draws them, Zipkin stores traces. Notice the two directions. Prometheus pulls; the app pushes spans. Your stack has its own names for all of this; OpenTelemetry is the common one. Your agent maps it in the adapt step.
:::

## Five dependencies, no code

```text
spring-boot-starter-actuator            the /actuator endpoints
spring-boot-starter-micrometer-metrics  counts and times
micrometer-registry-prometheus          the Prometheus format
spring-boot-micrometer-tracing-brave    trace IDs and spans
spring-boot-starter-zipkin              sends spans to Zipkin
```

::: note
**Say:** This is everything in Project Pulse's pom.xml that the picture needs. Logback comes with Spring Boot. Not one line of Java so far. The full dependency blocks are in the module, 4.3.
:::

## A dashboard reads a collector

::: cols
**/actuator/metrics**

A window for one person's spot check. No history.
|||
**A collector**

Keeps the history. Pulls from a private endpoint, or the app pushes to it.
:::

::: key
The public site does not serve its metrics.
:::

::: note
**Say:** So how would production get a dashboard? Not by opening /actuator/metrics to the internet. A collector either scrapes an endpoint only the inside of the network can reach, or the app pushes to a monitoring service. Pull fits Kubernetes and virtual machines, where the scraper shares a private network with the app. On a platform like Azure App Service, with one public port, pushing is the standard pattern. Project Pulse pushes to Azure Application Insights; you'll see it on Wednesday.
:::

## Logs go to standard output

::: steps
- The app writes to standard output; the platform collects it
- Project Pulse: Logback's console output, no log files
- Azure App Service: the log stream
:::

::: key
Find your platform's log stream before the first incident.
:::

::: note
**Say:** That's factor eleven of the Twelve-Factor App. Your code calls SLF4J, LoggerFactory.getLogger. SLF4J is the wall socket; Logback is the power plant behind it, and Spring Boot plugs it in by default. What to log, the levels, never logging content: Implementation 4.9.
:::

## Written for a machine

```text
09:02:14 ERROR [6af11fb6...-0860298d...] UserInvitationService : Could not send an invitation email for section 2 of course 1
```

```json
{"log":{"level":"ERROR", "logger":"team.projectpulse.user.userinvitation.UserInvitationService"},
 "message":"Could not send an invitation email for section 2 of course 1", "traceId":"6af11fb6..."}
```

::: note
**Say:** The first line is for a person reading one line. Production has thousands, and you search by field: every error, from this class, in the last hour. JSON puts each piece in a named field. In Spring Boot it's one property, logging.structured.format.console: ecs. Turn it on in the deployed profiles only.
:::

## One ID per request

::: steps
- A request arrives; Brave gives it a trace ID
- Every log line that request writes carries the ID, in every class
- One search for the ID returns the whole story
:::

::: key
That is how you find one failure among thousands of lines.
:::

::: note
**Say:** Spring Boot calls it logging correlation. It's exactly what was missing for nine months. Look at the bracket in a log line on your own machine after you pull main.
:::

## Change the level, no redeploy

```bash
curl -X POST localhost/actuator/loggers/team.projectpulse.user \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' -d '{"configuredLevel":"DEBUG"}'
```

::: note
**Say:** Turn DEBUG on for one package while you reproduce a problem, then off again. Development only: production doesn't expose loggers. You'll see this live on Wednesday.
:::

## Metrics have tags

```text
/actuator/metrics/http.server.requests
/actuator/metrics/http.server.requests?tag=uri:/api/v1/students&tag=status:500
```

::: cols
**Counter**

Only goes up: invitations sent
|||
**Gauge**

A value right now: threads alive
|||
**Timer**

How long, and how often: @Timed
:::

::: note
**Say:** Spring Boot records http.server.requests for every route with no code from you. Tags slice it: one page, or failures only. When you add your own metric, these three kinds cover most needs.
:::

## The four golden signals

| Signal | Project Pulse metric |
|---|---|
| Latency | http.server.requests, by uri and status |
| Traffic | http.server.requests count |
| Errors | outcome SERVER_ERROR, plus wrong answers |
| Saturation | memory, threads, pending database connections |

::: note
**Say:** From Google's SRE book, chapter 6: the four numbers to watch first for any service that answers requests. All four are metrics. Count latency for successes and failures separately; a fast error is not good news.
:::

## Machines and business

::: cols
**Machine metrics**

Memory, threads. Is the system struggling?
|||
**Business metrics**

Reports submitted before Monday's deadline. Is it doing its job?
:::

::: note
**Say:** A business metric is a counter you add yourself, and it's often the first to show a problem the machine metrics miss. If reminders stop reaching students, memory looks perfectly healthy.
:::

## Count it yourself

```java
try {
    this.emailService.sendInvitationEmail(userInvitation);
    meterRegistry.counter("invitations.sent", "outcome", "success").increment();
} catch (RuntimeException e) {
    LOGGER.error("Could not send an invitation email for section {} of course {}", sectionId, courseId, e);
    meterRegistry.counter("invitations.sent", "outcome", "failure").increment();
}
```

::: note
**Say:** This is a sketch, not in the repository yet. The try and catch are the real invitation loop in UserInvitationService; the two counter lines are new, and MeterRegistry comes in through the constructor. It shows up at /actuator/metrics/invitations.sent, and in Prometheus as invitations_sent_total. Stop the mail server and memory looks fine; this number climbs.
:::

## What does this number measure?

::: steps
- Only requests that reached the application
- Starts at zero on every deploy and restart
- Once it becomes a target, people improve the number instead of the thing
:::

::: joke
HTTP 200 OK, body `{"error": "database on fire"}`. Error rate: 0%.
:::

::: note
**Say:** Take http.server.requests. A request that died before it arrived, DNS or a crashed container, isn't in it, and that's exactly when users hurt most. The last point is Goodhart's law. A team graded on error rate learns to return 200 with the error inside.
:::

## Your SLO, measured

| Source | Misses |
|---|---|
| The platform's request and 5xx counts | wrong answers with a 200 |
| An outside probe, every minute | what the health check doesn't check |
| The app's own metric | requests that never arrived; restarts |

::: note
**Say:** The objective is the promise; the indicator is the number that checks it. Reliability 4.3 got you both. Project Pulse's AVL-uptime promises 99% of each term, about 27 hours of downtime. Here's where the number can come from, cheapest first. Whichever you pick, write it under the requirement, with what it misses.
:::

## 95 of every 100 views

```yaml
management:
  metrics:
    distribution:
      percentiles:
        http.server.requests: 0.95
```

::: warn
A percentile cannot be averaged across instances.
:::

::: note
**Say:** PER-report-load: report views within 500 milliseconds at the 95th percentile. This makes Spring Boot compute p95 in the app. It's per instance, so with Prometheus set percentiles-histogram instead and let the backend compute it from every instance's buckets.
:::

## A probe that cannot fail

```bash
curl -s -o /dev/null -w '%{http_code} %{content_type}' https://projectpulse.team/health
```

200 text/html: the single-page app, not the health check.

::: key
Check the content type, too. An SLI that cannot fail measures nothing.
:::

::: note
**Say:** I left out /actuator. The site still answers 200, because unknown paths get the Vue app. A probe that checks only the status code reports "up" from the wrong page, forever.
:::

## Traces and spans

::: steps
- A trace is one request's journey
- A span is one step: when it started, how long it took, which step called it
- Across five services, only the trace shows which one was slow
:::

::: note
**Say:** Project Pulse is one application, so its traces are short. Let me show you a real one.
:::

## One invitation request, traced {.center}

![Two Zipkin traces of the same invitation request on Project Pulse dev. Top, as shipped: the HTTP span, Spring Security's token and authorization spans, and one 164.9 ms secured request span with nothing inside it. Bottom, with @Observed on the email method: inside the secured request, about 50 ms with no span for the database work, then two send invitation email spans of 105.1 ms and 15.4 ms](img/observability-trace-invitation.svg)

::: ask
In the top trace, where did the 165 milliseconds go?
:::

::: note
**Say:** An instructor invites two students. Top: what Project Pulse records today. Spring times the request and Spring Security's steps, then one 165-millisecond box with the database work and both emails inside, and no detail. Bottom: the same request after one annotation. Now each email is its own span: 105 milliseconds, then 15. Both runs are real, from my laptop, this weekend.
:::

## A trace shows what someone instrumented

```java
@Observed(name = "email.send", contextualName = "send invitation email")
public void sendInvitationEmail(UserInvitation userInvitation) {
```

::: key
No span, no answer. Spring Boot does not time queries or mail on its own.
:::

::: joke
The outage is always in the span you didn't add.
:::

::: note
**Say:** One annotation, and each call becomes a span. If the mail server ever slows down, this is the span that grows. We'll make it grow on Wednesday.
:::

## Turn the annotation on

```yaml
management:
  observations:
    annotations:
      enabled: true
```

::: note
**Say:** The annotation does nothing on its own. It needs this property, plus spring-boot-starter-aspectj, which Project Pulse already has: Spring makes the span by wrapping the method in an aspect, code that runs before and after it.
:::

## Keep one in ten

```yaml
management:
  tracing:
    sampling:
      probability: 0.1
```

::: ask
A student reports one failed request. What can you still find?
:::

::: note
**Say:** Project Pulse keeps 10% of traces, so nine of ten failed requests have no trace in Zipkin. Their log lines still carry the trace ID, so the logs still tie together; only the timing picture is missing. Raise it in development and for a demo; keep it bounded in production, where every trace costs storage.
:::

## September 6, 2026

::: steps
- Project Pulse's /actuator/env answers any anonymous caller
- It returns the database and mail passwords
- The settings came from a local development tutorial and applied to every profile
:::

::: warn
The diagnostic port is a port for anyone else, too.
:::

::: joke
/actuator/env: the most helpful endpoint on the internet. It answers every question, for everyone.
:::

::: note
**Say:** Same endpoints we just met. env shows configuration, heapdump would hand over everything in memory, loggers changes behavior. The fix went out that evening and both passwords were rotated. The full record is in Project Pulse's architecture document.
:::

## The fix, in application.yml

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info        # the base for every profile
  endpoint:
    health:
      show-details: when-authorized # details for an admin only
      roles: admin
  info:
    git:
      mode: simple                  # the commit, not the JVM version
    java:
      enabled: false
    os:
      enabled: false
```

::: note
**Say:** Every other endpoint also requires ROLE_admin, through EndpointRequest rules in SecurityConfiguration. The base is the safe set, so a profile that forgets to override it gets the safe set, not the full one. The JVM version tells an attacker which CVEs to try. And the Actuator paths need their own security rules, because the API's deny-by-default covers only /api/v1.
:::

## Is the app down?

::: steps
- November: staging's health says DOWN
- The cause: a stale mail password in staging's Key Vault
- Mail was broken. Everything else worked
:::

::: ask
Should a broken mail server make the whole app "down"?
:::

::: note
**Say:** /actuator/health combines one check per dependency: database, mail, disk. One DOWN makes the whole thing DOWN, with a 503. Here nothing acted on it, because Azure's Health check feature is off for Project Pulse. Turn it on with /actuator/health as the path, and Azure would treat a broken mail server as a sick app and could restart it.
:::

## Liveness and readiness

::: cols
**Liveness**

Is the process stuck? Restart it.

/actuator/health/liveness
|||
**Readiness**

Can it serve traffic now? Send requests elsewhere until it can.

/actuator/health/readiness
:::

::: key
Point a platform's probe at one of these, never at /actuator/health.
:::

::: joke
Alive but not ready: me at 8 a.m. before coffee. Don't restart me, just wait.
:::

::: note
**Say:** By default neither group includes the database or mail checks; Project Pulse's both answer UP in production. Add a dependency to readiness only if the app is useless without it. A health check is a design decision.
:::

## Monday's takeaways

::: steps
- A metric says something is wrong, a trace says where, a log says why
- Logs to standard output, with a trace ID on every line
- Before you trust a number, say what it misses
- A trace shows only what someone instrumented
- Management endpoints are attack surface
:::

::: note
**Say:** Wednesday we stop talking and break things. Pull Project Pulse main before you come if you want to follow along on your own machine.
:::

## Wednesday: the lab {.center}

Project Pulse on a laptop · you call out where to look

::: note
**Say:** Everything we break today runs locally: Project Pulse in the dev profile, plus Docker Compose. Production we only look at. One storyline, five steps, and the agent comes in at step four. First, two minutes on what production saw in its first day.
:::

## Who is asking?

| Path | Requests | Looking for |
|---|---|---|
| `/.gitlab-ci.yml` | 21 | Secrets in a pipeline file |
| `/.env.openai`, `/.env.aws` | 13 | API keys |
| `/.git/hooks/post-receive`, `/.hg/requires` | 14 | The repository |
| `/l9owrv.php`, `/well.php`, `/wp-admin.php` | 24 | Someone else's back door |
| `/vite.config.js`, `/webpack.json`, … | 43 | How the frontend is built |
| `/robots.txt` | 8 | Nothing bad |

::: note
**Say:** Monday evening I turned on Application Insights for production, the site you use. These are its failed requests from the first day. Ask the room what each line is looking for before you say it. None of these files exist, so every one got a 404. Not every line is an attack: robots.txt is probably a search engine, and we run no PHP. But .env and .git are the same kind of door as /actuator/env from Monday: one URL that hands over secrets if it's open. What you don't expose can't leak. Module 4.7.
:::

## Reading the numbers

::: steps
- Dashboard: 583 of 1,979 requests failed. 29%!
- Rows or requests? 1,564 rows stand for 1,979. Sum `itemCount`
- What failed? Every 4xx counts: 574 were 404s, mostly bots
- What should the SLI count? Our errors, 5xx: 99.95%
:::

::: note
**Say:** Same dashboard, three honest numbers. The agent samples bursts, so each stored row stands for itemCount requests; count rows and you undercount. Application Insights calls every 4xx a failure, so bots asking for missing files look like an outage. The SLI counts 5xx. The query is in module 4.5, in KQL, Azure's query language. And it still misses the invitation that fails while returning 200, which is step three today.
:::

## Debugging from evidence

::: steps
- Narrow it down with a metric: when, and which route?
- Find one failing request by its trace ID
- Give the agent the evidence, not the symptom
- Reproduce it with a failing test
- Fix, then watch the metric return to normal
:::

::: note
**Say:** This is the order. Step one often points at a deploy: a change in the error rate that lines up with one points straight at it. Step four comes before any fix, and you watch the test fail first.
:::

## Evidence, not the symptom

::: ai
"Users get a 500 on the report page." The agent will guess, fluently.
:::

::: key
Give it the stack trace, the request, and the commit that deployed at 9:02.
:::

::: note
**Say:** Code the agent wrote needs this most. You didn't reason through it line by line, so your intuition about where it breaks is weaker, and a plausible explanation is easy to accept. Ask for a hypothesis you can check against the evidence. Then check it.
:::

## Where this work lives

::: cols
**Site reliability engineer**

Chooses what to watch, carries the pager, runs incidents, writes the blameless postmortem, sets SLOs.
|||
**Also called**

DevOps engineer, platform engineer, production engineer.
:::

::: note
**Say:** Ben Treynor Sloss: "what happens when you ask a software engineer to design an operations team." Google caps an SRE's operations work at about half their time; the rest is code that removes repetitive work. Some companies hire new graduates into SRE. Your team project is practice already.
:::

## The agent and your telemetry

::: cols
**Delegate**

Scan thousands of log lines. Correlate a spike with a deploy. Draft the structured-logging config.
|||
**Keep**

What to watch, what to promise the client, what may never appear in a log.
:::

::: ai
Asked to "add logging," an agent logs request bodies, emails, and tokens. Grep your logs for an email address.
:::

::: note
**Say:** Review what was logged, not only whether. And for any telemetry the agent adds, break the thing on purpose and see it show up. A dashboard nobody has seen go red is decoration.
:::

## 1. Tour Actuator

::: steps
- Log in as the seeded admin, copy the token
- /actuator, /actuator/health, /actuator/metrics/http.server.requests
- Raise one logger to DEBUG, no restart
:::

::: note
**Do:** curl -X POST -u b.wei@abc.edu:123456 localhost/api/v1/users/login, then the three GETs with the bearer token. Ask: which endpoint would you least want a stranger to reach? Then the loggers POST from Monday on team.projectpulse.user, and show the DEBUG lines appear.
:::

## 2. The empty dashboard

::: steps
- Grafana shows nothing: no data source. Add Prometheus
- Still nothing: Prometheus's targets page says 401. Why?
- Sign the scrape in as the admin, restart Prometheus
- Build one panel, then ask what it measures
:::

::: note
**Do:** Data source URL http://prometheus:9090. Targets page localhost:9090/targets. The 401 is the ROLE_admin rule from Monday. Uncomment the basic_auth block in docker/prometheus/prometheus.yml, then docker compose restart prometheus. Why not paste a token: it dies on every backend restart, and step 3 restarts it. Panel query: sum by (status) (rate(http_server_requests_seconds_count[1m])). Ask the room what the number counts and what it misses.
:::

## How production does it {.center}

![Project Pulse's observability stack. On a developer laptop, Prometheus pulls from the app's /actuator/prometheus every 15 seconds, signed in as the admin, Grafana draws it, Zipkin receives traces, and Mailpit and MySQL run beside the app. In production on Azure, the app serves only /health and /info publicly, and the monitoring agent App Service attaches pushes requests, logs, and metrics out to Application Insights, where Live Metrics, KQL queries, and alerts read them](img/observability-stack.svg)

::: note
**Say:** What we just did is pull: Prometheus sits next to the app and scrapes it. That fits Kubernetes and virtual machines, where the scraper shares a private network with the app. Azure App Service gives us one public port, so production pushes instead: an agent inside the container sends everything out to Application Insights, and /actuator/prometheus stays closed. Nothing to scrape, no password to leak.

**Do:** Portal, the peer-evaluation-tool Application Insights resource, Live Metrics. Open projectpulse.team in another tab and click around. Requests appear within seconds.
:::

## 3. Stop the mail server

::: steps
- Add the @Observed line, sampling to 1.0, send an invitation
- Stop the Mailpit container
- Send another. Does Project Pulse degrade, error, or hang?
:::

::: joke
Chaos engineering, student edition: stop a container and see who emails first.
:::

::: note
**Do:** Add the line, then ./mvnw -q compile in a second terminal; saving alone restarts nothing. docker compose stop mailpit, then send with new addresses. It degrades in about 60 ms: HTTP 200 with both addresses under "failed", an ERROR line per address, and two email spans marked "Connection refused" in Zipkin, localhost:9411. The latency metric shows nothing. Point at "timeout -1" in the span: refused fails fast, but a mail server that stalls would hang the request. This is a degradation test from Reliability 4.4, seen live. Restart Mailpit afterward.
:::

## 4. Find the 500 on production

::: steps
- Production's first day: one 500. On which route?
- Join everything with its operation_Id
- Read the cause
- Hand the agent the evidence; ask for a failing test first
:::

::: note
**Do:** Portal, peer-evaluation-tool, Logs, KQL mode. Rerun opener query 2: one row says 500, POST /api/v1/evaluations. Ask the room what they'd look at next before running the next slide's query. If the portal or the network fails, use the laptop fallback in the runbook: DELETE /api/v1/criteria/1.
:::

## One request, joined

```kusto
let op = toscalar(requests
    | where timestamp > ago(2d) and resultCode == "500"
          and name == "POST /api/v1/evaluations"
    | take 1 | project operation_Id);
union requests, dependencies, exceptions, traces
| where operation_Id == op
| project timestamp, itemType, name, resultCode, message
| order by timestamp asc
```

::: note
**Say:** Ten database reads, one INSERT into peer_evaluation, then MySQL: "Data too long for column private_comment." At 6:08 Tuesday morning a student wrote me a private comment longer than 255 characters, and lost it. Ask the room: whose bug is that? Point out that the INSERT shows placeholders, not the comment: no student data on the screen. The agent also timed every query, which Zipkin on my laptop doesn't.
:::

## Hand it to the agent

::: key
"Here is the request, the SQL, and the error from production. Explain the failure and propose a test that reproduces it. Do not fix it yet."
:::

::: note
**Do:** Paste the query result into the agent in the worktree at the commit before pull request 118 (main already has the fix). Check its hypothesis against the code: private_comment is varchar(255) in V1__baseline.sql, PeerEvaluationDto checks no length, and the textarea's max-length="255" is a typo for maxlength, so the form had no limit. Then show pull request 118's test: a 256-character comment, expecting 400. Before the fix it failed with 500, like production.
:::

## 99.95% {.center}

::: key
The SLI called that day a success. The 0.05% was one student's work.
:::

::: note
**Say:** 1,978 requests out of 1,979 were fine, and the SLO would be happy. The number told us where to look; someone still had to look. That's why your Checkpoint 3 asks for one failed request found from evidence, not just a percentage.
:::

## 5. Turn one metric into an SLO

::: ask
Pick the indicator, the target, and the window. What does your number miss?
:::

::: note
**Say:** The way your team will for Checkpoint 3. Use the panel from step 2. Then name what it can't see: requests that never arrived, restarts, wrong answers with a 200.
:::

## Your week

::: steps
- Choose your SLO's source and write what it misses under the requirement
- Make one request fail on purpose in your deployed system
- Find its log line in the platform's log stream, not your terminal
:::

::: key
Checkpoint 3 next week: your SLO with a measured value, and where the number comes from.
:::

::: note
**Say:** Run the adapt step for your stack: where your logs go, how you expose a health check, where your SLI can come from. A mobile app or a game measures from the client and its backend, not from Actuator. Next week, dynamic analysis turns watching into checking.
:::
