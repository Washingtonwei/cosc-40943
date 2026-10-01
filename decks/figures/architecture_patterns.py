"""Draw the eight architectural-pattern figures for MODULE-architecture, 4.8.

Informal figures, not technical diagrams: they are the exception to the mermaid rule, and the
module says so in section 4.4. The SVGs this writes are committed; edit this script and rerun
it from website/ rather than hand-editing the output:

    python decks/figures/architecture_patterns.py
"""
import math
import sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "docs" / "slides" / "img"
W, H = 1000, 420
BG, SURF, SURF2, RULE = "#0F1420", "#171E2E", "#1E273A", "#2C374E"
INK, DIM, FAINT = "#F2EDE3", "#9AA3B5", "#5C6780"
ACC, OK, AMBER, ALARM = "#9B6BD6", "#6FCF57", "#FFB443", "#FF4D4D"
SANS = "'Instrument Sans','Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'IBM Plex Mono',Consolas,Menlo,monospace"
COLORS = {"acc": ACC, "ok": OK, "amber": AMBER, "alarm": ALARM, "dim": DIM}


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def head(name, tag, title, desc):
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d" font-family="{SANS}">
<title id="t">{esc(title)}</title>
<desc id="d">{esc(desc)}</desc>
<defs>
'''
    for k, c in COLORS.items():
        s += (f'  <marker id="m-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
              f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>\n')
    s += f'''  <filter id="sh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#000" flood-opacity="0.45"/></filter>
  <linearGradient id="zone" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ACC}" stop-opacity="0.10"/><stop offset="1" stop-color="{ACC}" stop-opacity="0.03"/></linearGradient>
  <linearGradient id="cyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#26324A"/><stop offset="0.5" stop-color="#34425F"/><stop offset="1" stop-color="#26324A"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>
<text x="28" y="38" fill="{ACC}" font-size="15" font-weight="800" letter-spacing="2">{esc(name.upper())}</text>
'''
    if tag:
        s += f'<text x="{W-28}" y="38" text-anchor="end" fill="{AMBER}" font-size="14" font-weight="700">{esc(tag)}</text>\n'
    return s


def text(x, y, t, color=INK, size=16, anchor="middle", weight="500", mono=False, italic=False):
    f = f' font-family="{MONO}"' if mono else ""
    it = ' font-style="italic"' if italic else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-size="{size}" font-weight="{weight}"{f}{it}>{esc(t)}</text>'


def card(x, y, w, h, title, sub=None, code=None, accent=ACC, fill=SURF, size=17, dashed=False, faded=False, top=False):
    op = ' opacity="0.45"' if faded else ""
    dash = ' stroke-dasharray="6 5"' if dashed else ""
    s = f'<g{op}><g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{RULE}"{dash}/></g>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="5" rx="2.5" fill="{accent}"/>'
    n = 1 + (1 if code else 0) + (len(sub.split(chr(10))) if sub else 0)
    y0 = y + 36 if top else y + h / 2 - (n - 1) * 10 + 6
    s += text(x + w / 2, y0, title, INK, size, weight="700")
    k = 1
    if code:
        s += text(x + w / 2, y0 + 21 * k, code, "#C9B3EE", 13.5, mono=True, weight="500")
        k += 1
    if sub:
        for ln in sub.split("\n"):
            s += text(x + w / 2, y0 + 20 * k, ln, DIM, 14, italic=True)
            k += 1
    return s + "</g>"


def line(x1, y1, x2, y2, c="acc", dash=None, w=2.2):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{COLORS[c]}" stroke-width="{w}"{d} marker-end="url(#m-{c})"/>'


def path(d, c="acc", dash=None, w=2.2, end=True):
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#m-{c})"' if end else ""
    return f'<path d="{d}" fill="none" stroke="{COLORS[c]}" stroke-width="{w}"{dd}{m}/>'


def pill(x, y, t, c=AMBER, size=13.5, fill=BG):
    w = len(t) * size * 0.56 + 18
    return (f'<rect x="{x-w/2}" y="{y-12}" width="{w}" height="24" rx="12" fill="{fill}" stroke="{c}" stroke-width="1.4"/>'
            + text(x, y + 5, t, c, size, weight="700"))


def cylinder(x, y, w, h, label, size=15, sub=None, faded=False):
    e = min(h * 0.14, 14)
    op = ' opacity="0.45"' if faded else ""
    s = (f'<g{op}><path d="M{x},{y+e} v{h-2*e} a{w/2},{e} 0 0 0 {w},0 v{-(h-2*e)}" fill="url(#cyl)" stroke="{DIM}" stroke-width="1.4"/>'
         f'<ellipse cx="{x+w/2}" cy="{y+e}" rx="{w/2}" ry="{e}" fill="#3B4A69" stroke="{DIM}" stroke-width="1.4"/>')
    lines = label.split("\n")
    ty = y + h / 2 + e / 2 + 5 - (len(lines) - 1) * size * 0.6 - (9 if sub else 0)
    for k, ln in enumerate(lines):
        s += text(x + w / 2, ty + k * size * 1.2, ln, INK, size, weight="700")
    if sub:
        s += text(x + w / 2, ty + len(lines) * size * 1.2 + 2, sub, DIM, 13, italic=True)
    return s + "</g>"


def zone(x, y, w, h, name, color=ACC):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="url(#zone)" stroke="{color}" '
            f'stroke-width="1.5" stroke-dasharray="7 6"/>' + text(x + 16, y + 24, name, INK, 14.5, "start", "700"))


def xmark(cx, cy, r=13):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BG}" stroke="{ALARM}" stroke-width="2"/>'
            f'<path d="M{cx-5},{cy-5} l10,10 M{cx+5},{cy-5} l-10,10" stroke="{ALARM}" stroke-width="2.4"/>')


def caption(t):
    return text(W / 2, H - 20, t, DIM, 15, italic=True)


# ---------------------------------------------------------------------------
def layered():
    s = head("Layered", "Project Pulse · the activity package",
             "Layered pattern in Project Pulse",
             "A request enters ActivityController, which calls ActivityService, which calls ActivityRepository, "
             "which talks to the database. Each layer calls only the one below; a controller never skips to the repository.")
    s += zone(150, 62, 690, 262, "activity package: one domain, three layers inside")
    s += pill(78, 204, "HTTP request", ACC)
    X = [178, 400, 622]
    L = [("Presentation", "Controller", "ActivityController", "receives the request"),
         ("Domain logic", "Service", "ActivityService", "applies the business rules"),
         ("Data access", "Repository", "ActivityRepository", "talks to the database")]
    for x, (layer, t, code, sub) in zip(X, L):
        s += text(x + 95, 112, layer.upper(), ACC, 13, weight="800")
        s += card(x, 144, 190, 120, t, sub, code)
    s += line(118, 204, 174, 204)
    s += line(368, 204, 396, 204)
    s += line(590, 204, 618, 204)
    s += line(812, 204, 866, 204)
    s += text(382, 196, "", DIM, 12)
    s += cylinder(870, 150, 106, 110, "Database", 16)
    s += path("M273,264 C273,318 717,318 717,268", "alarm", "6 5")
    s += xmark(495, 305)
    s += text(495, 348, "a controller never skips to the repository", ALARM, 14.5, weight="700")
    s += caption("Each layer knows only the one below it.")
    return s + "</svg>\n"


def pipes():
    s = head("Pipes and filters", "Spring Security in Project Pulse",
             "Pipes and filters: the Spring Security filter chain",
             "An HTTP request passes through CORS, authentication, and authorization filters in order before it reaches the "
             "controller. Each filter can pass the request on or reject it. A second strip shows a machine learning pipeline, "
             "the same pattern on data.")
    s += pill(62, 150, "HTTP request", ACC, size=12.5)
    s += line(112, 150, 146, 150)
    F = [("CORS", "right origin?", "blocked"), ("Authentication", "who are you?", "401"),
         ("Authorization", "may you?", "403"), ("… more filters", "", "")]
    x = 150
    for i, (t, sub, rej) in enumerate(F):
        w = 146
        s += (f'<g filter="url(#sh)"><path d="M{x},{100} h{w} l-18,50 l18,50 h-{w} l18,-50 z" fill="{SURF}" stroke="{RULE}"/></g>'
              f'<path d="M{x},{100} h{w}" stroke="{ACC}" stroke-width="5"/>')
        s += text(x + w / 2 + 2, 148, t, INK, 16, weight="700")
        if sub:
            s += text(x + w / 2 + 2, 170, sub, DIM, 14, italic=True)
        if rej:
            s += line(x + w / 2, 206, x + w / 2, 244, "alarm")
            s += pill(x + w / 2, 262, rej, ALARM)
        x += w + 12
    s += line(x - 8, 150, x + 34, 150, "ok")
    s += card(x + 38, 102, 150, 96, "Controller", "your code")
    s += text(W / 2 + 40, 86, "every request, in this order", DIM, 14, italic=True)
    s += pill(x - 62, 222 + 0, "", AMBER, fill=BG) if False else ""
    s += text(890, 232, "No rule matched?", AMBER, 14.5, weight="700")
    s += text(890, 252, "the last rule decides", AMBER, 14.5, weight="700")
    s += text(890, 272, "(section 4.9)", AMBER, 13.5)
    # ML strip
    s += f'<line x1="28" y1="306" x2="{W-28}" y2="306" stroke="{RULE}"/>'
    s += text(28, 334, "SAME PATTERN ON DATA", FAINT, 12.5, "start", "800")
    steps = ["raw data", "clean", "extract features", "train", "evaluate"]
    x = 230
    for i, st in enumerate(steps):
        w = len(st) * 8.6 + 30
        s += f'<rect x="{x}" y="318" width="{w}" height="32" rx="8" fill="{SURF2}" stroke="{RULE}"/>' + text(x + w / 2, 339, st, INK, 14.5)
        if i < len(steps) - 1:
            s += line(x + w + 4, 334, x + w + 30, 334, "dim", w=1.8)
        x += w + 34
    s += caption("Each filter takes input, does one job, and passes it on or stops it.")
    return s + "</svg>\n"


def broker():
    s = head("Broker", "illustrative",
             "Broker pattern",
             "Clients ask the broker for a service by name. The broker looks up a live instance in its registry and "
             "forwards the request; a failed instance is dropped and a new one registered, and the clients never change.")
    C = ["Web app", "Mobile app", "Nightly job"]
    for i, c in enumerate(C):
        s += card(34, 84 + i * 92, 150, 70, c)
        s += line(188, 119 + i * 92, 346, 211 - 20 + i * 20)
    s += text(266, 104, "“send this to grading”", DIM, 14, italic=True)
    s += card(350, 96, 250, 236, "Broker", None, top=True)
    s += f'<rect x="370" y="190" width="210" height="120" rx="8" fill="{SURF2}" stroke="{RULE}"/>'
    s += text(475, 212, "REGISTRY", ACC, 12.5, weight="800")
    rows = [("grading", "10.0.1.8", OK), ("grading", "10.0.1.7", ALARM), ("email", "10.0.2.3", OK)]
    for i, (n, a, c) in enumerate(rows):
        yy = 240 + i * 26
        s += text(386, yy, n, INK, 14, "start", mono=True)
        s += text(566, yy, a, c, 14, "end", mono=True)
    s += text(475, 164, "finds a live instance", DIM, 14, italic=True)
    s += card(700, 70, 250, 72, "grading #1", "10.0.1.7 · down", accent=ALARM, faded=True)
    s += xmark(950, 80)
    s += card(700, 170, 250, 72, "grading #2", "10.0.1.8 · replaced #1", accent=OK)
    s += card(700, 270, 250, 72, "email #1", "10.0.2.3")
    s += line(604, 206, 696, 206, "ok")
    s += text(650, 196, "forwards", OK, 13.5, weight="600")
    s += caption("Clients know the broker, never the addresses.")
    return s + "</svg>\n"


def pubsub():
    s = head("Publish-subscribe", "illustrative Project Pulse extension",
             "Publish-subscribe pattern",
             "The evaluation service publishes an EvaluationSubmitted event to a channel. Email, grade, and audit subscribers "
             "each receive it independently; a new analytics subscriber can be added later without changing the publisher.")
    s += card(30, 150, 200, 110, "Evaluation service", "the publisher", size=16)
    s += line(234, 205, 300, 205, "amber")
    s += pill(390, 176, "EvaluationSubmitted", AMBER)
    s += text(390, 238, "the event, fired once", DIM, 14, italic=True)
    s += f'<rect x="496" y="70" width="36" height="300" rx="10" fill="{SURF2}" stroke="{AMBER}" stroke-width="1.6"/>'
    s += line(480, 205, 492, 205, "amber")
    s += (f'<text x="514" y="220" text-anchor="middle" fill="{AMBER}" font-size="14" font-weight="800" '
          f'transform="rotate(-90 514 220)" letter-spacing="2">CHANNEL</text>')
    subs = [("Email notifier", "tells the student", False), ("Grade calculator", "updates the average", False),
            ("Audit log", "records who did what", False), ("Analytics", "added next year", True)]
    for i, (t, sub, new) in enumerate(subs):
        y = 66 + i * 78
        s += line(536, y + 32, 626, y + 32, "amber", "6 5" if new else None)
        s += card(630, y, 250, 64, t, sub, dashed=new, accent=AMBER if not new else FAINT)
    s += text(940, 336, "no change to", DIM, 13.5, weight="600")
    s += text(940, 354, "the publisher", DIM, 13.5, weight="600")
    s += caption("The publisher does not know who is listening.")
    return s + "</svg>\n"


def queue():
    s = head("Message queue", "illustrative",
             "Message queue pattern",
             "A user asks for a term report. The web app puts a job on the queue and answers 202 Accepted at once. "
             "Workers take jobs off the queue at their own pace and email the result later.")
    s += card(28, 140, 150, 96, "Instructor", "“term report”")
    s += line(182, 188, 238, 188)
    s += card(242, 140, 160, 96, "Web app", "enqueues a job")
    s += path("M290,236 C290,280 140,280 140,240", "ok")
    s += pill(215, 290, "202 Accepted, in 50 ms", OK)
    s += line(406, 188, 452, 188, "amber")
    s += f'<rect x="456" y="150" width="236" height="76" rx="38" fill="{SURF2}" stroke="{AMBER}" stroke-width="1.6"/>'
    for i in range(5):
        s += f'<rect x="{474 + i*42}" y="168" width="34" height="40" rx="6" fill="#2A2418" stroke="{AMBER}"/>'
        s += text(491 + i * 42, 194, "job", AMBER, 12, weight="700")
    s += text(574, 128, "QUEUE: waits, in order", AMBER, 13.5, weight="800")
    s += line(696, 188, 752, 150, "amber")
    s += line(696, 188, 752, 236, "amber")
    s += card(756, 106, 190, 76, "Worker 1", "takes the next job")
    s += card(756, 204, 190, 76, "Worker 2", "at its own pace")
    s += path("M851,280 C851,392 40,392 40,240", "dim", "6 5")
    s += text(560, 366, "report emailed when done", DIM, 14, italic=True)
    s += caption("Sender and receiver no longer have to be busy at the same moment.")
    return s + "</svg>\n"


def replica():
    s = head("Source-replica", "illustrative",
             "Source-replica pattern",
             "The application sends every write to the source database and spreads reads across two replicas, which "
             "copy the source's changes. If the source fails, a replica is promoted.")
    s += card(30, 150, 180, 110, "Application", None)
    s += cylinder(330, 145, 170, 120, "Source", 17, "every write")
    s += cylinder(640, 62, 160, 104, "Replica 1", 16, "reads")
    s += cylinder(640, 250, 160, 104, "Replica 2", 16, "reads")
    s += line(214, 205, 324, 205, "acc")
    s += pill(268, 186, "writes · 5%", ACC, size=12.5)
    s += path("M120,150 C120,70 400,60 634,100", "ok")
    s += path("M120,260 C120,350 400,350 634,306", "ok")
    s += pill(330, 72, "reads · 95%", OK)
    s += path("M504,190 C560,180 590,130 634,122", "amber", "6 5")
    s += path("M504,220 C560,230 590,280 634,288", "amber", "6 5")
    s += text(566, 212, "copies", AMBER, 14, "middle", "700")
    s += card(830, 150, 150, 110, "If Source fails", "promote a\nreplica", accent=ALARM, size=15)
    s += caption("Scale the reads and survive a failure; every write still goes to one place.")
    return s + "</svg>\n"


def mainworker():
    s = head("Main-worker", "illustrative",
             "Main-worker pattern",
             "A main process splits a job of 1,000 test suites into four chunks, sends one to each identical worker, "
             "and merges the four results into one report.")
    s += card(28, 150, 160, 100, "The job", "1,000 test suites")
    s += line(192, 200, 236, 200)
    s += card(240, 130, 160, 140, "Main", "splits, then\nmerges")
    for i in range(4):
        y = 64 + i * 78
        s += line(404, 200, 516, y + 30, "acc", w=1.8)
        s += f'<rect x="440" y="{y+10}" width="0" height="0"/>'
        s += card(520, y, 190, 60, f"Worker {i+1}", f"suites {i*250+1}–{(i+1)*250}", size=15)
        s += path(f"M714,{y+30} C780,{y+30} 790,200 846,200", "ok", w=1.8)
    s += card(850, 150, 126, 100, "Report", "merged")
    s += caption("Split one big job into identical pieces, run them in parallel, combine.")
    return s + "</svg>\n"


def gateway():
    s = head("API gateway", "Team A had one",
             "API gateway pattern",
             "Browser, mobile, and partner clients all call one gateway, which authenticates, rate-limits, logs, and routes "
             "each request to one of several services.")
    C = ["Browser", "Mobile app", "Partner script"]
    for i, c in enumerate(C):
        s += card(30, 84 + i * 96, 160, 72, c)
        s += line(194, 120 + i * 96, 316, 214 - 24 + i * 24)
    s += card(320, 70, 250, 290, "API gateway", None, top=True)
    chips = ["authenticate", "rate-limit", "log", "route"]
    for i, cpt in enumerate(chips):
        y = 180 + i * 42
        s += f'<rect x="352" y="{y}" width="186" height="32" rx="16" fill="{SURF2}" stroke="{ACC}"/>' + text(445, y + 21, cpt, INK, 15)
    s += text(445, 146, "one entry point", DIM, 14, italic=True)
    S = ["Activity service", "Evaluation service", "Team service", "… four more"]
    for i, t in enumerate(S):
        y = 66 + i * 78
        s += line(574, 214, 716, y + 30, "acc", "6 5" if i == 3 else None, 1.8)
        s += card(720, y, 250, 60, t, size=15, faded=(i == 3))
    s += caption("Cross-cutting concerns in one place, so each service does not reinvent them.")
    return s + "</svg>\n"


FIGS = {"layered": layered, "pipes-and-filters": pipes, "broker": broker, "publish-subscribe": pubsub,
        "message-queue": queue, "source-replica": replica, "main-worker": mainworker, "api-gateway": gateway}
OUT.mkdir(parents=True, exist_ok=True)
for k, f in FIGS.items():
    (OUT / f"pattern-{k}.svg").write_text(f(), encoding="utf-8")
print("ok", len(FIGS))
