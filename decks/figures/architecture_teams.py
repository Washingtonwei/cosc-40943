"""Draw the Team A and Team B container figures for MODULE-architecture, section 3 (Motivation).

Informal figures, not technical diagrams: they are the exception to the mermaid rule, and the
module says so in section 4.4. The SVGs this writes are committed; edit this script and rerun
it from website/ rather than hand-editing the output:

    python decks/figures/architecture_teams.py
"""
import sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "docs" / "slides" / "img"

W, H = 1200, 600
BG, SURF, SURF2, RULE = "#0F1420", "#171E2E", "#1E273A", "#2C374E"
INK, DIM, FAINT = "#F2EDE3", "#9AA3B5", "#5C6780"
ACC, OK, AMBER = "#9B6BD6", "#6FCF57", "#FFB443"
SANS = "'Instrument Sans','Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'IBM Plex Mono',Consolas,Menlo,monospace"

ROW_TOP, ROW_H, ROW_STEP = 58, 52, 64
def cy(i): return ROW_TOP + i * ROW_STEP + ROW_H / 2
MID = cy(3)


def head(title, desc):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d" font-family="{SANS}">
<title id="t">{title}</title>
<desc id="d">{desc}</desc>
<defs>
  <marker id="req" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ACC}"/></marker>
  <marker id="net" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{AMBER}"/></marker>
  <marker id="call" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{OK}"/></marker>
  <filter id="sh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#000" flood-opacity="0.45"/></filter>
  <linearGradient id="zone" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ACC}" stop-opacity="0.10"/><stop offset="1" stop-color="{ACC}" stop-opacity="0.03"/></linearGradient>
  <linearGradient id="cyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#26324A"/><stop offset="0.5" stop-color="#34425F"/><stop offset="1" stop-color="#26324A"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>
'''


def card(x, y, w, h, title, sub=None, icon="", accent=ACC, title_size=16):
    s = f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{SURF}" stroke="{RULE}"/></g>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="5" rx="2.5" fill="{accent}"/>'
    s += icon
    lines = title.split("\n")
    ty = y + h / 2 + (12 if icon else 0) - (len(lines) - 1) * 10 - (8 if sub else 0) + 6
    for k, ln in enumerate(lines):
        s += f'<text x="{x + w/2}" y="{ty + k*20}" text-anchor="middle" fill="{INK}" font-size="{title_size}" font-weight="700">{ln}</text>'
    if sub:
        for k, ln in enumerate(sub.split("\n")):
            s += f'<text x="{x + w/2}" y="{ty + (len(lines)-1)*20 + 21 + k*16}" text-anchor="middle" fill="{DIM}" font-size="12.5" font-style="italic">{ln}</text>'
    return s


def people_icon(cx, y):
    s = ""
    for dx, r in ((-13, 1.0), (13, 1.0), (0, 1.15)):
        c = cx + dx
        s += f'<circle cx="{c}" cy="{y + 8*r}" r="{7*r}" fill="none" stroke="{ACC}" stroke-width="2"/>'
        s += f'<path d="M{c-11*r},{y+32*r} a{11*r},{12*r} 0 0 1 {22*r},0" fill="none" stroke="{ACC}" stroke-width="2"/>'
    return s


def browser_icon(cx, y):
    return (f'<rect x="{cx-22}" y="{y}" width="44" height="32" rx="4" fill="none" stroke="{ACC}" stroke-width="2"/>'
            f'<line x1="{cx-22}" y1="{y+9}" x2="{cx+22}" y2="{y+9}" stroke="{ACC}" stroke-width="2"/>'
            + "".join(f'<circle cx="{cx-16+k*6}" cy="{y+4.5}" r="1.6" fill="{ACC}"/>' for k in range(3))
            + f'<path d="M{cx-8},{y+16} l-5,5 5,5 M{cx+8},{y+16} l5,5 -5,5" fill="none" stroke="{DIM}" stroke-width="1.8"/>')


def gateway_icon(cx, y):
    return (f'<rect x="{cx-16}" y="{y}" width="32" height="32" rx="6" transform="rotate(45 {cx} {y+16})" fill="none" stroke="{ACC}" stroke-width="2"/>'
            f'<path d="M{cx-9},{y+16} h18 M{cx+4},{y+11} l5,5 -5,5" fill="none" stroke="{AMBER}" stroke-width="2"/>')


def app_icon(cx, y):
    return (f'<rect x="{cx-20}" y="{y}" width="40" height="34" rx="5" fill="none" stroke="{ACC}" stroke-width="2"/>'
            + "".join(f'<line x1="{cx-12}" y1="{y+9+k*8}" x2="{cx+12}" y2="{y+9+k*8}" stroke="{DIM}" stroke-width="2"/>' for k in range(3)))


def cylinder(x, y, w, h, label, size=12):
    e = h * 0.14
    s = (f'<path d="M{x},{y+e} v{h-2*e} a{w/2},{e} 0 0 0 {w},0 v{-(h-2*e)}" fill="url(#cyl)" stroke="{DIM}" stroke-width="1.3"/>'
         f'<ellipse cx="{x+w/2}" cy="{y+e}" rx="{w/2}" ry="{e}" fill="#3B4A69" stroke="{DIM}" stroke-width="1.3"/>')
    lines = label.split("\n")
    ty = y + h / 2 + e / 2 + 4 - (len(lines) - 1) * (size * 0.6)
    for k, ln in enumerate(lines):
        s += f'<text x="{x+w/2}" y="{ty + k*size*1.25}" text-anchor="middle" fill="{INK}" font-size="{size}" font-weight="600">{ln}</text>'
    return s


def arrow(x1, y1, x2, y2, marker="req", color=ACC, dash=None, width=2):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{d} marker-end="url(#{marker})"/>'


def label(x, y, text, color=DIM, size=12, anchor="middle", weight="500"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-size="{size}" font-weight="{weight}">{text}</text>'


def pill(x, y, text, color):
    w = len(text) * 6.6 + 14
    return (f'<rect x="{x - w/2}" y="{y-10}" width="{w}" height="20" rx="10" fill="{BG}" stroke="{color}" stroke-width="1.2"/>'
            f'<text x="{x}" y="{y+4}" text-anchor="middle" fill="{color}" font-size="11.5" font-weight="600">{text}</text>')


def zone(x, y, w, h, name, stats, icon):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="url(#zone)" stroke="{ACC}" stroke-width="1.6" stroke-dasharray="7 6"/>'
            + icon + label(x + 40, y + 24, name, INK, 14, "start", "700")
            + label(x + w - 16, y + 24, stats, AMBER, 13, "end", "700"))


def wheel_icon(cx, cyy):
    s = f'<circle cx="{cx}" cy="{cyy}" r="9" fill="none" stroke="{ACC}" stroke-width="2"/>'
    import math
    for k in range(7):
        a = 2 * math.pi * k / 7
        s += f'<line x1="{cx}" y1="{cyy}" x2="{cx + 9*math.sin(a):.1f}" y2="{cyy - 9*math.cos(a):.1f}" stroke="{ACC}" stroke-width="1.5"/>'
    return s


def box_icon(cx, cyy):
    return (f'<path d="M{cx-9},{cyy-4} l9,-5 9,5 v10 l-9,5 -9,-5 z M{cx-9},{cyy-4} l9,5 9,-5 M{cx},{cyy+1} v10" '
            f'fill="none" stroke="{ACC}" stroke-width="1.8" stroke-linejoin="round"/>')


def legend(items):
    s = f'<line x1="24" y1="532" x2="{W-24}" y2="532" stroke="{RULE}"/>'
    x = 32
    for kind, text in items:
        y = 562
        if kind == "req":
            s += arrow(x, y, x + 34, y)
        elif kind == "net":
            s += arrow(x, y, x + 34, y, "net", AMBER, "5 4")
        elif kind == "call":
            s += arrow(x, y, x + 34, y, "call", OK, None)
        elif kind == "db":
            s += cylinder(x + 6, y - 13, 22, 26, "")
        elif kind == "zone":
            s += f'<rect x="{x}" y="{y-11}" width="34" height="22" rx="5" fill="url(#zone)" stroke="{ACC}" stroke-dasharray="5 4"/>'
        s += label(x + 44, y + 4, text, DIM, 13, "start")
        x += 44 + len(text) * 6.7 + 34
    return s


ORDER = [("Activity", "activity"), ("Evaluation", "evaluation"), ("Team", "team"),
         ("Rubric", "rubric"), ("Section", "section"), ("Account", "user"), ("Requirements", "ram")]
CALLS = [(1, 2, 44, "team members?"), (0, 2, 92, "team members?"), (1, 3, 140, "which rubric?"), (2, 4, 188, "which section?")]

PEOPLE = (24, 164)
SPA = (204, 354)
CARD_Y, CARD_H = MID - 62, 124


def common(spa_sub):
    s = card(PEOPLE[0], CARD_Y, PEOPLE[1] - PEOPLE[0], CARD_H, "Instructor\nand students", "people", people_icon((PEOPLE[0]+PEOPLE[1])/2, CARD_Y + 18))
    s += card(SPA[0], CARD_Y, SPA[1] - SPA[0], CARD_H, "Single-page app", spa_sub, browser_icon((SPA[0]+SPA[1])/2, CARD_Y + 20))
    s += arrow(PEOPLE[1] + 4, MID, SPA[0] - 4, MID)
    s += label((PEOPLE[1] + SPA[0]) / 2, MID - 10, "uses", DIM, 12)
    s += label((PEOPLE[1] + SPA[0]) / 2, MID + 22, "HTTPS", FAINT, 11)
    return s


def team_a():
    s = head("Team A: seven services (container view)",
             "The same Project Pulse use cases built as seven services on Kubernetes. Browser app, API gateway, "
             "and one service per use case area, each owning its own database; four service-to-service calls cross the network.")
    s += zone(398, 20, 778, 494, "Kubernetes cluster", "7 deployables · 7 databases · 4 network hops", wheel_icon(420, 39))
    s += common("Vue.js,\nhosted on its own")
    GX0, GX1 = 420, 544
    s += card(GX0, CARD_Y, GX1 - GX0, CARD_H, "API gateway", "routes each\nrequest [HTTP]", gateway_icon((GX0+GX1)/2, CARD_Y + 18))
    s += arrow(SPA[1] + 4, MID, GX0 - 4, MID)
    s += label((SPA[1] + GX0) / 2 - 2, MID - 10, "requests", DIM, 12)
    s += label((SPA[1] + GX0) / 2 - 2, MID + 22, "REST", FAINT, 11)
    PX0, PX1 = 608, 964
    for i, (name, _) in enumerate(ORDER):
        y, c = ROW_TOP + i * ROW_STEP, cy(i)
        s += f'<path d="M{GX1},{MID} C{GX1+40},{MID} {PX0-40},{c} {PX0-4},{c}" fill="none" stroke="{ACC}" stroke-width="1.6" stroke-opacity="0.85" marker-end="url(#req)"/>'
        s += f'<g filter="url(#sh)"><rect x="{PX0}" y="{y}" width="{PX1-PX0}" height="{ROW_H}" rx="10" fill="{SURF}" stroke="{RULE}"/></g>'
        s += f'<rect x="{PX0}" y="{y}" width="5" height="{ROW_H}" rx="2.5" fill="{ACC}"/>'
        s += label(PX0 + 20, c - 2, f"{name} service", INK, 14.5, "start", "700")
        s += label(PX0 + 20, c + 15, "Spring Boot · own pipeline", DIM, 11, "start")
        s += arrow(PX0 + 196, c, PX0 + 226, c, width=1.5)
        s += label(PX0 + 211, c - 6, "SQL", FAINT, 9.5)
        s += cylinder(PX0 + 230, y + 6, 106, 40, f"{name} DB", 11.5)
    for a, b, depth, text in CALLS:
        ya, yb = cy(a) + 6, cy(b) - 6
        s += (f'<path d="M{PX1},{ya} C{PX1+depth},{ya} {PX1+depth},{yb} {PX1+4},{yb}" fill="none" stroke="{AMBER}" '
              f'stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#net)"/>')
    for a, b, depth, text in CALLS:
        s += pill(PX1 + depth * 0.75, (cy(a) + cy(b)) / 2, text, AMBER)
    s += legend([("req", "request [HTTP]"), ("net", "service calls service, over the network"),
                 ("db", "database"), ("zone", "deployment boundary")])
    return s + "</svg>\n"


def team_b():
    s = head("Team B: one deployable (container view)",
             "The same Project Pulse use cases built as one Spring Boot application in one Docker container, "
             "divided inside into seven domain packages that call each other in-process, with one relational database.")
    s += zone(398, 20, 574, 494, "One Docker container", "1 deployable · 1 database · 0 network hops", box_icon(420, 39))
    s += common("Vue.js,\nserved by the app")
    AX0, AX1 = 420, 950
    s += f'<g filter="url(#sh)"><rect x="{AX0}" y="54" width="{AX1-AX0}" height="448" rx="14" fill="{SURF}" stroke="{RULE}"/></g>'
    s += f'<rect x="{AX0}" y="54" width="{AX1-AX0}" height="5" rx="2.5" fill="{ACC}"/>'
    s += app_icon(482, MID - 58)
    s += label(482, MID + 2, "Spring Boot", INK, 16, "middle", "700")
    s += label(482, MID + 22, "application", INK, 16, "middle", "700")
    s += label(482, MID + 44, "Java · one build", DIM, 12.5)
    s += label(482, MID + 60, "one deployable", DIM, 12.5)
    s += arrow(SPA[1] + 4, MID, AX0 - 4, MID)
    s += label((SPA[1] + AX0) / 2 - 2, MID - 10, "requests", DIM, 12)
    s += label((SPA[1] + AX0) / 2 - 2, MID + 22, "REST", FAINT, 11)
    PX0, PX1 = 608, 850
    for i, (name, pkg) in enumerate(ORDER):
        y, c = ROW_TOP + i * ROW_STEP, cy(i)
        s += f'<rect x="{PX0}" y="{y+4}" width="{PX1-PX0}" height="{ROW_H-8}" rx="8" fill="{SURF2}" stroke="{RULE}"/>'
        s += f'<text x="{PX0+16}" y="{c+1}" fill="{INK}" font-size="14.5" font-weight="600" font-family="{MONO}">{pkg}</text>'
        s += label(PX0 + 16, c + 16, "controller · service · repository", DIM, 10.5, "start")
    for a, b, depth, _ in CALLS:
        ya, yb = cy(a) + 6, cy(b) - 6
        d = depth * 0.42
        s += (f'<path d="M{PX1},{ya} C{PX1+d},{ya} {PX1+d},{yb} {PX1+4},{yb}" fill="none" stroke="{OK}" '
              f'stroke-width="1.8" marker-end="url(#call)"/>')
    s += arrow(AX1 + 4, MID, 1022, MID)
    s += label(986, MID - 10, "JDBC", DIM, 12)
    s += cylinder(1026, MID - 80, 150, 160, "One relational\ndatabase", 15)
    s += legend([("req", "request"), ("call", "method call inside one process"),
                 ("db", "database"), ("zone", "deployment boundary")])
    return s + "</svg>\n"


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "architecture-team-a.svg").write_text(team_a(), encoding="utf-8")
    (OUT / "architecture-team-b.svg").write_text(team_b(), encoding="utf-8")
    print("ok")
