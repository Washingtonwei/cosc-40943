"""Draw the deployment-shape spectrum for MODULE-architecture, section 4.7 (One deployable or several).

Monolith, modular monolith, and microservices side by side, drawn in the Team A and Team B style:
green arrows are in-process calls, amber dashed arrows cross a network. The strip underneath says
what moving a boundary and running the system cost in each. An informal figure, like the Team A and
Team B ones. The SVG this writes is committed; edit this script and rerun it from website/ rather
than hand-editing the output:

    python decks/figures/architecture_deployables.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from architecture_teams import (BG, SURF, RULE, INK, DIM, FAINT, ACC, OK, AMBER, SANS, MONO,  # noqa: E402
                                arrow, box_icon, card, cylinder, label, pill)

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "docs" / "slides" / "img"
W, H = 1200, 610
ALARM = "#FF4D4D"
COLS = (30, 420, 810)
CW = 360
LAYERS = (ACC, AMBER, OK)


def head():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d" font-family="{SANS}">
<title id="t">One deployable or several</title>
<desc id="d">Three deployment shapes side by side. A monolith: one deployable with no boundaries inside, its parts calling each other freely, one database; moving a boundary means untangling the code first. A modular monolith, marked as the one to aim for and as Project Pulse's shape: one deployable divided inside into domain packages (activity, team, evaluation), each layered, calling each other in-process through their services, one database; moving a boundary means moving a package, and there is one deployable to run. Microservices: activity, team, and evaluation as separate deployables, each with its own database, calling each other over the network; moving a boundary means migrating data between databases, and each service needs its own pipeline, monitoring, and on-call.</desc>
<defs>
  <marker id="net" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{AMBER}"/></marker>
  <marker id="call" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{OK}"/></marker>
  <marker id="req" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ACC}"/></marker>
  <filter id="sh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#000" flood-opacity="0.45"/></filter>
  <linearGradient id="cyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#26324A"/><stop offset="0.5" stop-color="#34425F"/><stop offset="1" stop-color="#26324A"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>
'''


def column_head(x, name, sub):
    return label(x + CW / 2, 50, name, INK, 19, weight="700") + label(x + CW / 2, 72, sub, DIM, 13)


def deployable(x, y, w, h, tag):
    """One deployable unit: a solid outlined box with a package icon and its tag."""
    return (f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{SURF}" stroke="{ACC}" stroke-width="2"/></g>'
            + box_icon(x + 22, y + 22) + label(x + 40, y + 27, tag, INK, 13.5, "start", "700"))


def cost(x, rows):
    s = ""
    y = 438
    for heading, value, color in rows:
        s += label(x + 14, y, heading, FAINT, 11, "start", "700").replace("<text", '<text letter-spacing="1.2"', 1)
        s += label(x + 14, y + 21, value, color, 14.5, "start", "700")
        y += 50
    return s


def monolith(x):
    s = column_head(x, "Monolith", "one deployable, no boundaries inside")
    s += deployable(x + 20, 96, CW - 40, 234, "one deployable")
    parts = [(78, 140), (190, 134), (296, 150), (104, 208), (222, 200), (306, 236), (84, 280), (196, 284)]
    pairs = [(0, 4), (1, 5), (2, 3), (3, 5), (4, 6), (6, 2), (7, 1), (0, 7), (5, 7), (1, 3), (0, 2)]
    for a, b in pairs:
        (x1, y1), (x2, y2) = parts[a], parts[b]
        s += f'<line x1="{x + x1}" y1="{y1}" x2="{x + x2}" y2="{y2}" stroke="{OK}" stroke-width="1.6" stroke-opacity="0.75"/>'
    for px, py in parts:
        s += f'<rect x="{x + px - 24}" y="{py - 11}" width="48" height="22" rx="5" fill="#2A3550" stroke="{DIM}" stroke-width="1.2"/>'
    s += arrow(x + CW / 2, 330, x + CW / 2, 348)
    s += cylinder(x + CW / 2 - 55, 350, 110, 50, "one database")
    s += cost(x, [("TO MOVE A BOUNDARY", "untangle the code first", ALARM), ("TO RUN IT", "one deployable", OK)])
    return s


def module(x, y, name):
    s = f'<rect x="{x}" y="{y}" width="80" height="172" rx="10" fill="none" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="5 4"/>'
    s += f'<text x="{x + 40}" y="{y + 22}" text-anchor="middle" fill="{INK}" font-size="12.5" font-weight="700" font-family="{MONO}">{name}</text>'
    for k, c in enumerate(LAYERS):
        s += f'<rect x="{x + 8}" y="{y + 36 + k * 44}" width="64" height="36" rx="5" fill="{c}" fill-opacity="0.38"/>'
    return s


def modular(x):
    s = f'<rect x="{x}" y="6" width="{CW}" height="{H - 94}" rx="16" fill="{ACC}" fill-opacity="0.07" stroke="{AMBER}" stroke-width="2"/>'
    s += column_head(x, "Modular monolith", "one deployable, divided inside by domain")
    s += deployable(x + 20, 96, CW - 40, 234, "one deployable")
    s += pill(x + CW - 104, 118, "aim here: Project Pulse", AMBER)
    xs = (x + 38, x + 140, x + 242)
    for mx, name in zip(xs, ("activity", "team", "evaluation")):
        s += module(mx, 146, name)
    ly = 146 + 36 + 44 + 18
    s += arrow(xs[0] + 72, ly, xs[1] + 8, ly, "call", OK)
    s += arrow(xs[2] + 8, ly, xs[1] + 72, ly, "call", OK)
    s += arrow(x + CW / 2, 330, x + CW / 2, 348)
    s += cylinder(x + CW / 2 - 55, 350, 110, 50, "one database")
    s += cost(x, [("TO MOVE A BOUNDARY", "move a package", OK), ("TO RUN IT", "one deployable", OK)])
    return s


def microservices(x):
    s = column_head(x, "Microservices", "one deployable per service, each with its data")
    team = (x + 130, 104)
    act = (x + 16, 226)
    eva = (x + 244, 226)
    for (cx, cy), name in ((team, "team"), (act, "activity"), (eva, "evaluation")):
        s += card(cx, cy, 100, 64, name, icon=box_icon(cx + 50, cy + 20), title_size=14)
    s += arrow(act[0] + 88, act[1], team[0] + 12, team[1] + 64, "net", AMBER, "5 4")
    s += arrow(eva[0] + 12, eva[1], team[0] + 88, team[1] + 64, "net", AMBER, "5 4")
    s += arrow(team[0] + 100, team[1] + 32, team[0] + 124, team[1] + 32)
    s += cylinder(team[0] + 126, team[1] + 8, 56, 48, "")
    for cx, cy in (act, eva):
        s += arrow(cx + 50, cy + 64, cx + 50, cy + 86)
        s += cylinder(cx + 22, cy + 88, 56, 48, "")
    s += label(x + CW / 2, 392, "a database each", DIM, 13)
    s += cost(x, [("TO MOVE A BOUNDARY", "migrate data between databases", ALARM),
                  ("TO RUN IT", "a pipeline, monitoring, on-call each", AMBER)])
    return s


def legend():
    s = f'<line x1="24" y1="{H - 72}" x2="{W - 24}" y2="{H - 72}" stroke="{RULE}"/>'
    y = H - 40
    x = 40
    items = [("dep", "deployable unit"), ("mod", "domain package, layered inside"), ("call", "in-process call"),
             ("net", "network call"), ("db", "database")]
    for kind, text in items:
        if kind == "dep":
            s += f'<rect x="{x}" y="{y - 11}" width="34" height="22" rx="5" fill="{SURF}" stroke="{ACC}" stroke-width="2"/>'
        elif kind == "mod":
            s += f'<rect x="{x}" y="{y - 11}" width="34" height="22" rx="5" fill="none" stroke="{ACC}" stroke-dasharray="4 3"/>'
        elif kind == "call":
            s += arrow(x, y, x + 34, y, "call", OK)
        elif kind == "net":
            s += arrow(x, y, x + 34, y, "net", AMBER, "5 4")
        elif kind == "db":
            s += cylinder(x + 6, y - 13, 22, 26, "")
        s += label(x + 44, y + 4, text, DIM, 13, "start")
        x += 44 + len(text) * 6.7 + 34
    return s


def figure():
    s = head()
    s += f'<line x1="24" y1="414" x2="{W - 24}" y2="414" stroke="{RULE}"/>'
    s += monolith(COLS[0]) + modular(COLS[1]) + microservices(COLS[2]) + legend()
    return s + "</svg>\n"


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "deployment-shapes.svg").write_text(figure(), encoding="utf-8")
    print("ok deployment-shapes.svg")
