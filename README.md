# COSC 40943 Software Engineering — course website

Source for the Software Engineering / Senior Design course site at Texas Christian University, taught by Bingyang Wei. Built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and published to GitHub Pages by a GitHub Actions workflow.

The site carries the syllabus, the week-by-week schedule, the Friday studio format, the senior-design project requirements, the individual assignments, the AI policy, the method the course teaches, and the course modules.

## Build it locally

Python 3.9 or newer.

```bash
python -m venv .venv          # somewhere outside a synced folder if you use one
. .venv/Scripts/activate      # Windows;  source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt

mkdocs serve                  # http://127.0.0.1:8000/cosc-40943/
mkdocs build --strict         # exactly what CI runs
```

`mkdocs serve` watches `docs/` and `mkdocs.yml` and reloads on save.

## Found a mistake? Send a pull request

Typos, broken links, wrong dates, a setup step that does not work on your machine: fix it and open a pull request. Every pull request is built and checked automatically. You do not need to run anything locally to propose a small edit; use the pencil icon on any page to edit it in the browser.

Course-content questions belong in Slack or office hours rather than in an issue.

## Conventions

Four rules keep the site consistent. A pull request that breaks one will fail CI or get comments.

- **`strict: true`.** A link that does not resolve fails the build rather than shipping. Fix the link; never relax the flag.
- **No YAML front matter in `docs/*.md`.** Page titles come from the `<h1>`, and nav order lives in `mkdocs.yml`. Adding a page means adding a `nav:` line by hand.
- **Link between pages with relative `.md` paths**, not URLs: `[Schedule](schedule.md)`, `[SE and What AI Changes](modules/se-and-ai.md)`.
- **Never add `{ target="_blank" }` to a link.** The `privacy` plugin already opens every external link in a new tab.

## Publishing

`.github/workflows/pages.yml` builds on every push and pull request, and deploys only from `main`. Do not use `mkdocs gh-deploy`; it fills the history with bot commits, and the real `git log` gets read in class.

## Layout

```
docs/
  index.md          syllabus.md    schedule.md     studio.md
  project.md        assignments.md ai.md           method.md
  resources.md
  modules/          one page per course topic, linked from the schedule
mkdocs.yml          site config and nav
requirements.txt    pinned mkdocs-material
```

Modules go up as they are written, so some are still in progress and say so at the top.
