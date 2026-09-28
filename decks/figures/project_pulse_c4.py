"""Draw Project Pulse's C4 diagrams as slide figures for MODULE-architecture's deck.

The source of truth is the mermaid C4 in Project Pulse's architecture-of-record, which the module
carries unchanged. Mermaid's C4 layout is unreadable when projected, so the deck shows these
redrawings instead: same elements, same descriptions, same relationships and labels, in the style
of the Team A and Team B figures. Students write mermaid; these SVGs are for presentation only.

The SVGs this writes are committed; edit this script and rerun it from website/ rather than
hand-editing the output:

    python decks/figures/project_pulse_c4.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from architecture_teams import (BG, SURF, SURF2, RULE, INK, DIM, FAINT, ACC, SANS, MONO,  # noqa: E402
                                cylinder, zone)

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "docs" / "slides" / "img"
BODY = "#C9CED8"
EXT = "#6B7890"


def head(w, h, title, desc):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" font-family="{SANS}">
<title id="t">{title}</title>
<desc id="d">{desc}</desc>
<defs>
  <marker id="req" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ACC}"/></marker>
  <filter id="sh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#000" flood-opacity="0.45"/></filter>
  <linearGradient id="zone" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ACC}" stop-opacity="0.10"/><stop offset="1" stop-color="{ACC}" stop-opacity="0.03"/></linearGradient>
  <linearGradient id="cyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#26324A"/><stop offset="0.5" stop-color="#34425F"/><stop offset="1" stop-color="#26324A"/></linearGradient>
</defs>
<rect width="{w}" height="{h}" rx="18" fill="{BG}"/>
<text x="{w/2}" y="30" text-anchor="middle" fill="{INK}" font-size="17" font-weight="700">{title}</text>
'''


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text, width, size):
    per = max(8, int(width / (size * 0.52)))
    out, line = [], ""
    for word in text.split():
        cand = (line + " " + word).strip()
        if len(cand) > per and line:
            out.append(line)
            line = word
        else:
            line = cand
    if line:
        out.append(line)
    return out


def txt(x, y, t, color=DIM, size=12, anchor="middle", weight="500", italic=False, mono=False):
    st = ' font-style="italic"' if italic else ""
    fm = f' font-family="{MONO}"' if mono else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-size="{size}" font-weight="{weight}"{st}{fm}>{esc(t)}</text>'


class Box:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def at(self, side, t=0.5):
        if side == "top":
            return (self.x + self.w * t, self.y)
        if side == "bottom":
            return (self.x + self.w * t, self.y + self.h)
        if side == "left":
            return (self.x, self.y + self.h * t)
        return (self.x + self.w, self.y + self.h * t)


def person_icon(cx, y, color=ACC):
    return (f'<circle cx="{cx}" cy="{y+7}" r="7" fill="none" stroke="{color}" stroke-width="2"/>'
            f'<path d="M{cx-11},{y+30} a11,12 0 0 1 22,0" fill="none" stroke="{color}" stroke-width="2"/>')


def element(b, name, kind, desc, ext=False, person=False, name_size=16, mono_name=False):
    """A C4 element as a house-style card: name, [kind], and its description."""
    accent = EXT if ext else ACC
    fill = SURF2 if ext else SURF
    s = f'<g filter="url(#sh)"><rect x="{b.x}" y="{b.y}" width="{b.w}" height="{b.h}" rx="12" fill="{fill}" stroke="{RULE}"/></g>'
    s += f'<rect x="{b.x}" y="{b.y}" width="{b.w}" height="5" rx="2.5" fill="{accent}"/>'
    cx = b.x + b.w / 2
    y = b.y + 26
    if person:
        s += person_icon(cx, b.y + 12, accent)
        y = b.y + 60
    s += txt(cx, y, name, INK, name_size, weight="700", mono=mono_name)
    y += 18
    s += txt(cx, y, f"[{kind}]", DIM, 11.5, italic=True)
    for ln in wrap(desc, b.w - 22, 12):
        y += 16
        s += txt(cx, y, ln, BODY, 12)
    return s


def database(b, name, kind, desc):
    e = b.h * 0.12
    s = (f'<path d="M{b.x},{b.y+e} v{b.h-2*e} a{b.w/2},{e} 0 0 0 {b.w},0 v{-(b.h-2*e)}" fill="url(#cyl)" stroke="{DIM}" stroke-width="1.3"/>'
         f'<ellipse cx="{b.x+b.w/2}" cy="{b.y+e}" rx="{b.w/2}" ry="{e}" fill="#3B4A69" stroke="{DIM}" stroke-width="1.3"/>')
    cx = b.x + b.w / 2
    y = b.y + 2 * e + 20
    s += txt(cx, y, name, INK, 16, weight="700")
    y += 18
    s += txt(cx, y, f"[{kind}]", DIM, 11.5, italic=True)
    for ln in wrap(desc, b.w - 26, 12):
        y += 16
        s += txt(cx, y, ln, BODY, 12)
    return s


def boundary(x, y, w, h, name, kind, at="top", nx=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="url(#zone)" stroke="{ACC}" stroke-width="1.6" stroke-dasharray="7 6"/>'
    ly = y + 22 if at == "top" else y + h - 12
    nx = x + 16 if nx is None else nx
    s += txt(nx, ly, name, INK, 14, "start", "700")
    s += txt(nx + len(name) * 7.6 + 8, ly, f"[{kind}]", DIM, 12, "start", italic=True)
    return s


def rel(points, label, tech=None, lx=None, ly=None, both=False, anchor="middle", width=1.8):
    """A labelled relationship along a polyline; the label sits on a background so crossings stay legible."""
    d = "M" + " L".join(f"{x},{y}" for x, y in points)
    start = ' marker-start="url(#req)"' if both else ""
    s = f'<path d="{d}" fill="none" stroke="{ACC}" stroke-width="{width}" stroke-linejoin="round" marker-end="url(#req)"{start}/>'
    if lx is None:
        (x1, y1), (x2, y2) = points[len(points) // 2 - 1], points[len(points) // 2]
        lx, ly = (x1 + x2) / 2, (y1 + y2) / 2
    lines = label.split("\n")
    if tech:
        lines.append(f"[{tech}]")
    wmax = max(len(ln) for ln in lines) * 6.3 + 12
    hh = 15 * len(lines) + 6
    bx = lx - wmax / 2 if anchor == "middle" else (lx - 6 if anchor == "start" else lx - wmax + 6)
    s += f'<rect x="{bx}" y="{ly - hh/2}" width="{wmax}" height="{hh}" rx="6" fill="{BG}" fill-opacity="0.92"/>'
    for k, ln in enumerate(lines):
        is_tech = tech and k == len(lines) - 1
        s += txt(lx, ly - hh / 2 + 15 + k * 15, ln, FAINT if is_tech else DIM, 11 if is_tech else 12, anchor,
                 "500", italic=bool(is_tech))
    return s


def legend(w, y, items):
    s = f'<line x1="24" y1="{y-18}" x2="{w-24}" y2="{y-18}" stroke="{RULE}"/>'
    x = 32
    for kind, text in items:
        if kind == "person":
            s += person_icon(x + 17, y - 14)
        elif kind in ("el", "ext"):
            c = EXT if kind == "ext" else ACC
            s += f'<rect x="{x}" y="{y-11}" width="34" height="22" rx="5" fill="{SURF2 if kind == "ext" else SURF}" stroke="{RULE}"/><rect x="{x}" y="{y-11}" width="34" height="4" rx="2" fill="{c}"/>'
        elif kind == "db":
            s += cylinder(x + 6, y - 13, 22, 26, "")
        elif kind == "zone":
            s += f'<rect x="{x}" y="{y-11}" width="34" height="22" rx="5" fill="url(#zone)" stroke="{ACC}" stroke-dasharray="5 4"/>'
        elif kind == "rel":
            s += f'<line x1="{x}" y1="{y}" x2="{x+34}" y2="{y}" stroke="{ACC}" stroke-width="2" marker-end="url(#req)"/>'
        s += txt(x + 44, y + 4, text, DIM, 13, "start")
        x += 44 + len(text) * 6.7 + 30
    return s


# ---------------------------------------------------------------- context
def context():
    W, H = 1200, 640
    s = head(W, H, "System Context Diagram for Project Pulse",
             "Project Pulse as one box: an instructor and a senior design student use it; it sends email through Gmail, "
             "which delivers it to both, and requests AI review from an LLM service. Redrawn from the mermaid C4 in "
             "Project Pulse's architecture-of-record.")
    ins = Box(40, 70, 250, 170)
    stu = Box(40, 360, 250, 150)
    pul = Box(470, 215, 260, 140)
    gm = Box(910, 70, 250, 120)
    llm = Box(910, 380, 250, 120)
    # Gmail delivers to both people: routed around the outside so they do not cross the system.
    s += rel([gm.at("top", 0.5), (gm.x + gm.w / 2, 50), (ins.x + ins.w / 2, 50), ins.at("top", 0.5)],
             "Sends emails to", lx=600, ly=50)
    s += rel([gm.at("right", 0.5), (1180, gm.y + gm.h / 2), (1180, 545), (stu.x + stu.w / 2, 545), stu.at("bottom", 0.5)],
             "Sends emails to", lx=600, ly=545)
    s += rel([ins.at("right", 0.6), (380, ins.y + ins.h * 0.6), (380, pul.y + 40), pul.at("left", 40 / pul.h)],
             "Manages courses;\nreviews requirements", lx=380, ly=205)
    s += rel([stu.at("right", 0.5), (380, stu.y + stu.h / 2), (380, pul.y + 100), pul.at("left", 100 / pul.h)],
             "Submits work;\nauthors requirements", lx=380, ly=395)
    s += rel([pul.at("right", 0.3), (820, pul.y + pul.h * 0.3), (820, gm.y + gm.h / 2), gm.at("left", 0.5)],
             "Sends emails using", lx=820, ly=205)
    s += rel([pul.at("right", 0.75), (820, pul.y + pul.h * 0.75), (820, llm.y + llm.h / 2), llm.at("left", 0.5)],
             "Requests AI review", lx=820, ly=370)
    s += element(ins, "Instructor", "Person",
                 "Teaches a course section; a course admin is an instructor who also runs the course", person=True)
    s += element(stu, "Senior Design Student", "Person", "Member of a team in a course section", person=True)
    s += element(pul, "Project Pulse", "Software System", "Tracks team performance and supports requirements authoring",
                 name_size=18)
    s += element(gm, "Gmail", "Software System", "Email system", ext=True)
    s += element(llm, "LLM Service", "Software System", "AI-assisted requirement review", ext=True)
    s += legend(W, 612, [("person", "person"), ("el", "the system"), ("ext", "external system"),
                         ("rel", "relationship")])
    return s + "</svg>\n"


# ---------------------------------------------------------------- containers
def container():
    W, H = 1200, 690
    s = head(W, H, "Container Diagram for Project Pulse",
             "Inside the Project Pulse boundary: the SPA in the browser, the REST API application, a MySQL database, "
             "and Azure Blob Storage. Instructors and students use the SPA; the API delivers it, serves its API calls, "
             "reads and writes the database, stores files in Blob Storage, sends email through Gmail, and requests AI "
             "review from an LLM service. Redrawn from the mermaid C4 in Project Pulse's architecture-of-record.")
    ins = Box(40, 55, 250, 150)
    stu = Box(330, 55, 250, 130)
    gm = Box(900, 55, 260, 110)
    llm = Box(900, 330, 260, 110)
    s += boundary(30, 240, 820, 385, "Project Pulse", "Software System", at="bottom")
    spa = Box(60, 290, 270, 130)
    api = Box(500, 290, 300, 130)
    db = Box(400, 455, 205, 145)
    blob = Box(630, 455, 205, 145)
    s += rel([gm.at("left", 0.35), stu.at("right", 0.35 * gm.h / stu.h + (gm.y - stu.y) / stu.h)], "Sends emails to",
             lx=740, ly=gm.y + gm.h * 0.35 - 14)
    s += rel([gm.at("bottom", 0.2), (gm.x + gm.w * 0.2, 222), (ins.x + 60, 222), ins.at("bottom", 60 / ins.w)],
             "Sends emails to", lx=300, ly=222)
    s += rel([ins.at("bottom", 0.6), spa.at("top", (ins.x + ins.w * 0.6 - spa.x) / spa.w)], "Uses", "HTTPS",
             lx=ins.x + ins.w * 0.6 + 8, ly=262, anchor="start")
    s += rel([stu.at("bottom", 0.4), (stu.x + stu.w * 0.4, 262), (spa.x + spa.w - 30, 262), spa.at("top", (spa.w - 30) / spa.w)],
             "Uses", "HTTPS", lx=stu.x + stu.w * 0.4 + 8, ly=258, anchor="start")
    s += rel([spa.at("right", 0.3), api.at("left", 0.3)], "API calls", "JSON/HTTPS", lx=415, ly=spa.y + spa.h * 0.3 - 20)
    s += rel([api.at("left", 0.75), spa.at("right", 0.75)], "Delivers", "HTTPS", lx=415, ly=spa.y + spa.h * 0.75 + 20)
    s += rel([api.at("bottom", 0.15), (api.x + api.w * 0.15, db.y - 2)], "Reads & writes", "JDBC",
             lx=api.x + api.w * 0.15 - 8, ly=438, anchor="end")
    s += rel([api.at("bottom", 0.7), (api.x + api.w * 0.7, blob.y - 2)], "Stores & reads files", "HTTPS",
             lx=api.x + api.w * 0.7 + 8, ly=438, anchor="start")
    s += rel([api.at("right", 0.25), (865, api.y + api.h * 0.25), (865, gm.y + gm.h * 0.8), gm.at("left", 0.8)],
             "Sends email", "SMTP", lx=865, ly=250)
    s += rel([api.at("right", 0.75), (870, api.y + api.h * 0.75), (870, llm.y + llm.h * 0.5), llm.at("left", 0.5)],
             "Requests\nAI review", "HTTPS", lx=850, ly=api.y + api.h * 0.75 - 30)
    s += element(ins, "Instructor", "Person",
                 "Teaches a course section; a course admin is an instructor who also runs the course", person=True)
    s += element(stu, "Senior Design Student", "Person", "Member of a team in a course section", person=True)
    s += element(gm, "Gmail", "Software System", "Email system", ext=True)
    s += element(llm, "LLM Service", "Software System", "AI-assisted requirement review", ext=True)
    s += element(spa, "SPA", "Container: Vue 3 / TypeScript",
                 "Runs in the browser; the user interface for performance tracking and requirements authoring")
    s += element(api, "REST API Application", "Container: Java 21 / Spring Boot",
                 "Delivers the SPA; serves the performance-tracking and RAM APIs")
    s += database(db, "Database", "Container: MySQL 8",
                  "Courses, teams, WARs, peer evaluations, and RAM artifacts, links, and documents")
    s += database(blob, "Blob Storage", "Container: Azure Blob Storage", "Uploaded project source material (PDF/PPTX)")
    s += legend(W, 664, [("person", "person"), ("el", "container"), ("db", "data store"), ("ext", "external system"),
                         ("zone", "system boundary"), ("rel", "relationship")])
    return s + "</svg>\n"


# ---------------------------------------------------------------- shared foundation
def foundation():
    W, H = 1400, 870
    s = head(W, H, "Component Diagram: shared foundation inside the REST API Application",
             "The REST API application's shared foundation: security, SPA serving, actuator, user, the org model, "
             "participants, rubric, and notifications, with the SPA, the database, and Gmail outside. Redrawn from the "
             "mermaid C4 in Project Pulse's architecture-of-record.")
    spa = Box(340, 50, 320, 110)
    s += boundary(30, 190, 1160, 450, "REST API Application (Spring Boot)", "Container", at="top", nx=700)
    web = Box(60, 225, 240, 125)
    sec = Box(340, 225, 320, 125)
    act = Box(700, 225, 200, 125)
    noti = Box(940, 225, 220, 140)
    gm = Box(1225, 530, 160, 100)
    peo = Box(55, 485, 210, 125)
    org = Box(295, 485, 230, 125)
    rub = Box(635, 485, 220, 125)
    usr = Box(895, 485, 270, 125)
    db = Box(420, 690, 360, 125)
    # entry points
    s += rel([web.at("top", 0.5), (web.x + web.w / 2, spa.y + 55), spa.at("left", 0.5)], "Delivers", "HTTPS", lx=240, ly=spa.y + 55)
    s += rel([spa.at("bottom", 0.5), sec.at("top", 0.5)], "Logs in; sends every\nAPI request through", "JSON/HTTPS",
             lx=spa.x + spa.w / 2 + 12, ly=192, anchor="start")
    s += rel([sec.at("right", 0.5), act.at("left", 0.5)], "Guards", lx=680, ly=sec.y + sec.h / 2 - 16)
    # security fans out to participants, the org model, rubric, and user
    s += rel([(360, sec.y + sec.h), (360, 400), (peo.x + peo.w / 2, 400), peo.at("top", 0.5)],
             "Passes authorized\nrequests to", lx=peo.x + peo.w / 2 - 8, ly=445, anchor="end")
    s += rel([(420, sec.y + sec.h), (420, org.y)],
             "Checks ownership and\nmembership in; passes\nauthorized requests to", lx=412, ly=452, anchor="end")
    s += rel([(645, sec.y + sec.h), (645, rub.y)],
             "Checks rubric ownership\nin; passes authorized\nrequests to", lx=653, ly=432, anchor="start")
    s += rel([(560, sec.y + sec.h), (560, 385), (1000, 385), (1000, usr.y)],
             "Loads the authenticated\nuser from; passes\nauthorized requests to", lx=992, ly=432, anchor="end")
    # inside the foundation
    s += rel([org.at("right", 0.5), rub.at("left", 0.5)], "Owns and\nassigns rubrics", lx=580, ly=org.y + org.h / 2)
    s += rel([(1150, usr.y), (1150, noti.y + noti.h)], "Sends invitation\nand reset emails via", lx=1158, ly=450, anchor="start")
    s += rel([(1040, noti.y + noti.h), (1040, 468), (480, 468), (480, org.y)],
             "Finds course sections\ndue a reminder in", lx=1048, ly=395, anchor="start")
    s += rel([noti.at("right", 0.5), (1305, noti.y + noti.h / 2), gm.at("top", 0.5)], "Sends email", "SMTP",
             lx=1313, ly=365, anchor="start")
    # every data component reads and writes the database
    s += rel([peo.at("bottom", 0.5), (peo.x + peo.w / 2, 752), db.at("left", 0.5)], "Reads & writes", "JDBC", lx=290, ly=752)
    s += rel([org.at("bottom", 0.7), (org.x + org.w * 0.7, db.y + 10)], "Reads & writes", "JDBC", lx=org.x + org.w * 0.7 - 8, ly=652, anchor="end")
    s += rel([rub.at("bottom", 0.25), (rub.x + rub.w * 0.25, db.y + 10)], "Reads & writes", "JDBC", lx=rub.x + rub.w * 0.25 + 8, ly=652, anchor="start")
    s += rel([usr.at("bottom", 0.5), (usr.x + usr.w / 2, 752), db.at("right", 0.5)], "Reads & writes", "JDBC", lx=930, ly=752)
    s += element(spa, "SPA", "Container: Vue 3 / TypeScript", "Course and team administration UI")
    s += element(web, "SPA serving", "Component: Spring MVC static resources", "Serves the bundled SPA; forwards UI routes to index.html")
    s += element(sec, "security", "Component: Spring Security filter chain",
                 "JWT login and request authentication; AuthorizationManagers check ownership and membership")
    s += element(act, "actuator", "Component: Spring Boot Actuator", "Health and info management endpoints")
    s += element(peo, "student · instructor", "Component: Spring MVC + Spring Data JPA", "Course participants and their roles")
    s += element(org, "course · section · team", "Component: Spring MVC + Spring Data JPA",
                 "Courses, course sections, teams: the org/enrollment model")
    s += element(rub, "rubric", "Component: Spring MVC + Spring Data JPA",
                 "Rubrics and criteria: owned by a course, assigned to course sections")
    s += element(usr, "user", "Component: Spring MVC + Spring Data JPA", "User accounts, invitations, password reset")
    s += element(noti, "notifications", "Component: Spring Mail + @Scheduled",
                 "EmailService; WeeklyReminderScheduler sends each week's reminders")
    s += element(gm, "Gmail", "Software System", "Email system", ext=True)
    s += database(db, "Database", "Container: MySQL 8", "Users, courses, course sections, teams, rubrics")
    s += legend(W, 848, [("el", "container or component"), ("db", "data store"), ("ext", "external system"),
                         ("zone", "container boundary"), ("rel", "relationship")])
    return s + "</svg>\n"


def rel_label(lx, ly, label, anchor="middle"):
    lines = label.split("\n")
    wmax = max(len(ln) for ln in lines) * 6.3 + 12
    hh = 15 * len(lines) + 6
    bx = lx - wmax / 2 if anchor == "middle" else (lx - 6 if anchor == "start" else lx - wmax + 6)
    s = f'<rect x="{bx}" y="{ly - hh/2}" width="{wmax}" height="{hh}" rx="6" fill="{BG}" fill-opacity="0.92"/>'
    for k, ln in enumerate(lines):
        s += txt(lx, ly - hh / 2 + 15 + k * 15, ln, DIM, 12, anchor)
    return s


# ---------------------------------------------------------------- performance tracking
def performance():
    W, H = 1300, 790
    s = head(W, H, "Component Diagram: performance-tracking components inside the REST API Application",
             "The performance-tracking feature area, activity and evaluation, on the shared foundation (security, the org "
             "model, rubric, notifications, drawn in grey), with the SPA and the database outside. Redrawn from the "
             "mermaid C4 in Project Pulse's architecture-of-record.")
    spa = Box(430, 50, 330, 110)
    s += boundary(30, 190, 1000, 520, "REST API Application (Spring Boot)", "Container", at="top")
    sec = Box(430, 225, 330, 120)
    act = Box(80, 420, 260, 110)
    eva = Box(470, 420, 280, 110)
    rub = Box(820, 225, 190, 120)
    noti = Box(820, 420, 190, 130)
    org = Box(260, 575, 330, 100)
    db = Box(1080, 380, 200, 150)
    s += rel([spa.at("bottom", 0.5), sec.at("top", 0.5)], "Submits and reviews WARs\nand peer evaluations", "JSON/HTTPS",
             lx=spa.x + spa.w / 2 + 12, ly=192, anchor="start")
    s += rel([sec.at("left", 0.5), (act.x + act.w / 2, sec.y + sec.h / 2), act.at("top", 0.5)],
             "Checks WAR ownership and\nteam membership in; passes\nauthorized requests to", lx=act.x + act.w / 2 + 10, ly=360, anchor="start")
    s += rel([sec.at("bottom", 0.5), eva.at("top", (sec.x + sec.w / 2 - eva.x) / eva.w)],
             "Checks evaluation ownership\nin; passes authorized\nrequests to", lx=sec.x + sec.w / 2 + 10, ly=383, anchor="start")
    s += rel([eva.at("right", 0.2), (790, eva.y + eva.h * 0.2), (790, rub.y + rub.h * 0.7), rub.at("left", 0.7)],
             "Scores peer\nevaluations against\ncriteria from", lx=915, ly=383)
    s += rel([eva.at("right", 0.75), noti.at("left", (eva.y + eva.h * 0.75 - noti.y) / noti.h)], "Sends\nconfirmation\nemail via",
             lx=785, ly=eva.y + eva.h + 45)
    s += rel([act.at("bottom", 0.7), (act.x + act.w * 0.7, org.y + org.h / 2), org.at("left", 0.5)],
             "Reads team members\nand instructors from", lx=act.x + act.w * 0.7 - 8, ly=562, anchor="end")
    s += rel([eva.at("bottom", 0.3), (eva.x + eva.w * 0.3, org.y + org.h / 2), org.at("right", 0.5)],
             "Reads course sections\nand students from", lx=eva.x + eva.w * 0.3 + 8, ly=560, anchor="start")
    s += rel([act.at("left", 0.5), (55, act.y + act.h / 2), (55, 690), (1180, 690), db.at("bottom", 0.5)],
             "Reads & writes", "JDBC", lx=700, ly=690)
    s += rel([eva.at("bottom", 0.85), (eva.x + eva.w * 0.85, 650), (1150, 650), db.at("bottom", 0.35)],
             "Reads & writes", "JDBC", lx=880, ly=650)
    s += element(spa, "SPA", "Container: Vue 3 / TypeScript", "Course management UI: WARs, peer evaluations, dashboards")
    s += element(sec, "security", "Component: Shared foundation", "Authenticates and authorizes every API request", ext=True)
    s += element(act, "activity", "Component: Spring MVC + Spring Data JPA", "Weekly activity reports")
    s += element(eva, "evaluation", "Component: Spring MVC + Spring Data JPA", "Peer evaluations and their scoring")
    s += element(rub, "rubric", "Component: Shared foundation", "Rubrics and criteria", ext=True)
    s += element(noti, "notifications", "Component: Shared foundation",
                 "Email; weekly WAR and peer evaluation reminders", ext=True)
    s += element(org, "course · section · team · student", "Component: Shared foundation", "The org/enrollment model", ext=True)
    s += database(db, "Database", "Container: MySQL 8", "WARs, peer evaluations")
    s += legend(W, 766, [("el", "container or component"), ("ext", "shared foundation"), ("db", "data store"),
                         ("zone", "container boundary"), ("rel", "relationship")])
    return s + "</svg>\n"


# ---------------------------------------------------------------- RAM
def ram():
    W, H = 1690, 1020
    s = head(W, H, "Component Diagram: RAM components inside the REST API Application",
             "The RAM module's ten components on the shared foundation (security, team and user, in grey), with the SPA, "
             "the database, Blob Storage, and the LLM service outside. Redrawn from the mermaid C4 in Project Pulse's "
             "architecture-of-record.")
    spa = Box(520, 50, 320, 110)
    s += boundary(30, 190, 1360, 610, "REST API Application (Spring Boot)", "Container", at="top", nx=880)
    val = Box(55, 230, 215, 120)
    glo = Box(310, 230, 215, 120)
    sec = Box(555, 230, 245, 120)
    exp = Box(830, 230, 220, 120)
    rev = Box(1100, 230, 240, 120)
    uc = Box(55, 440, 215, 130)
    req = Box(350, 440, 270, 130)
    doc = Box(760, 440, 260, 130)
    ai = Box(1100, 440, 240, 130)
    col = Box(420, 650, 240, 120)
    org = Box(800, 650, 180, 110)
    src = Box(1140, 650, 230, 120)
    llm = Box(1460, 445, 205, 120)
    blob = Box(1460, 640, 205, 140)
    db = Box(300, 840, 850, 125)
    # the entry path
    s += rel([spa.at("bottom", 0.5), (spa.x + spa.w / 2, sec.y)], "Sends every RAM\nrequest through", "JSON/HTTPS",
             lx=spa.x + spa.w / 2 + 10, ly=195, anchor="start")
    s += rel([(600, sec.y + sec.h), (600, req.y)], "Passes authenticated requests\nto (and to every other\nRAM component)",
             lx=608, ly=395, anchor="start")
    # into the requirements graph
    s += rel([val.at("right", 0.85), glo.at("left", 0.85)], "Checks terminology against", lx=285, ly=365)
    s += rel([(180, val.y + val.h), (180, 395), (370, 395), (370, req.y)], "Checks artifacts\nand links in", lx=275, ly=402)
    s += rel([(470, glo.y + glo.h), (470, req.y)], "Derives glossary\nterms from", lx=478, ly=398, anchor="start")
    s += rel([uc.at("right", 0.5), req.at("left", 0.5)], "Is a requirement\nartifact in", lx=310, ly=600)
    s += rel([req.at("right", 0.5), doc.at("left", 0.5)], "Places artifacts in\ndocument sections", both=True,
             lx=690, ly=req.y + req.h / 2 - 34)
    s += rel([(520, col.y), (520, req.y + req.h)], "Anchors comment\nthreads to", lx=512, ly=610, anchor="end")
    s += rel([col.at("right", 0.3), (775, col.y + col.h * 0.3), (775, doc.y + doc.h)], "Anchors comment\nthreads to",
             lx=718, ly=col.y + col.h * 0.3 + 30)
    # around the document
    s += rel([(900, exp.y + exp.h), (900, doc.y)], "Renders", lx=908, ly=385, anchor="start")
    s += rel([(1130, rev.y + rev.h), (1130, 410), (990, 410), (990, doc.y)], "Locks and submits", lx=1138, ly=383, anchor="start")
    s += rel([ai.at("left", 0.85), doc.at("right", 0.85)], "Reads context\nfrom; proposes\nedits to", lx=1060, ly=612)
    s += rel([(930, doc.y + doc.h), (930, org.y)], "Scopes documents\nto a team in", lx=922, ly=612, anchor="end")
    s += rel([(1260, ai.y + ai.h), (1260, src.y)], "Reads extracted\ntext from", lx=1268, ly=610, anchor="start")
    # beyond the database
    s += rel([ai.at("right", 0.5), llm.at("left", (ai.y + ai.h / 2 - llm.y) / llm.h)], "Proxies AI\nrequests", "HTTPS",
             lx=1417, ly=ai.y + ai.h / 2 - 32)
    s += rel([src.at("right", 0.5), blob.at("left", (src.y + src.h / 2 - blob.y) / blob.h)], "Stores &\nreads files", "HTTPS",
             lx=1417, ly=src.y + src.h / 2 - 32)
    # every component with tables reads and writes the database
    s += rel([(160, uc.y + uc.h), (160, db.y + db.h / 2), db.at("left", 0.5)], "Reads & writes", "JDBC", lx=230, ly=db.y + db.h / 2)
    s += rel([(375, req.y + req.h), (375, db.y + 8)], "Reads & writes", "JDBC", lx=367, ly=805, anchor="end")
    s += rel([(560, col.y + col.h), (560, db.y + 8)], "Reads & writes", "JDBC", lx=568, ly=805, anchor="start")
    s += rel([(1005, doc.y + doc.h), (1005, db.y + 8)], "Reads & writes", "JDBC", lx=997, ly=805, anchor="end")
    s += rel([(1120, ai.y + ai.h), (1120, db.y + 8)], "Reads & writes", "JDBC", lx=1112, ly=812, anchor="end")
    s += rel([rev.at("right", 0.5), (1372, rev.y + rev.h / 2), (1372, 820), (1135, 820), (1135, db.y + 8)],
             "Reads & writes", "JDBC", lx=1372, ly=395)
    s += rel([(1250, src.y + src.h), (1250, db.y + db.h / 2), db.at("right", 0.5)], "Stores references\nand extracted text", "JDBC",
             lx=1258, ly=db.y + db.h / 2 + 30, anchor="start")
    s += element(spa, "SPA", "Container: Vue 3 / TypeScript", "RAM authoring views; calls each component's REST API over JSON/HTTPS")
    s += element(val, "validation", "Component: Spring MVC", "ReqLint structural and consistency checks")
    s += element(glo, "glossary", "Component: Spring MVC", "Glossary terms and terminology invariants")
    s += element(sec, "security", "Component: Shared foundation", "Authenticates every API request", ext=True)
    s += element(exp, "export", "Component: Spring MVC", "Renders documents to PDF, DOCX, and Markdown")
    s += element(rev, "review", "Component: Spring MVC + Spring Data JPA", "Review and submission workflow")
    s += element(uc, "usecase", "Component: Spring MVC + Spring Data JPA", "Use cases: main steps, extensions, locking")
    s += element(req, "requirement", "Component: Spring MVC + Spring Data JPA",
                 "Requirement artifacts, artifact links and tracing, key-prefix sequences: the requirements graph")
    s += element(doc, "document", "Component: Spring MVC + Spring Data JPA",
                 "Requirement documents and document sections, templates and provisioning, section locking, autosave")
    s += element(ai, "ai", "Component: Spring MVC + Spring Data JPA", "AI configuration, AI assistants, LLM proxy")
    s += element(col, "collaboration", "Component: Spring MVC + Spring Data JPA",
                 "Comment threads; real-time presence and broadcast are a deferred layer")
    s += element(org, "team · user", "Component: Shared foundation", "Teams that own RAM content; users as authors", ext=True)
    s += element(src, "sourcematerial", "Component: Spring MVC + Spring Data JPA",
                 "Project source material: upload, storage, server-side text extraction")
    s += element(llm, "LLM Service", "Software System", "AI-assisted requirement review", ext=True)
    s += database(blob, "Blob Storage", "Container: Azure Blob Storage", "Uploaded project source material")
    s += database(db, "Database", "Container: MySQL 8",
                  "RAM artifacts, links, documents, document sections, comments, AI configuration")
    s += legend(W, 996, [("el", "container or component"), ("ext", "shared foundation or external"), ("db", "data store"),
                         ("zone", "container boundary"), ("rel", "relationship")])
    return s + "</svg>\n"


FIGS = {"pulse-c4-context.svg": context, "pulse-c4-containers.svg": container,
        "pulse-c4-foundation.svg": foundation, "pulse-c4-performance.svg": performance,
        "pulse-c4-ram.svg": ram}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FIGS.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
    print("ok", ", ".join(FIGS))
