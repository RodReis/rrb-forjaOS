#!/usr/bin/env python3
"""roadmap.py — fonte única: docs/roadmap/roadmap.json → docs/STATUS.md + docs/roadmap/index.html

Uso:
  python3 scripts/roadmap.py validate
  python3 scripts/roadmap.py build [--check]
  python3 scripts/roadmap.py add-delivery --pr N --items ID1,ID2 --summary "texto" [--date AAAA-MM-DD]

Só stdlib. Os arquivos gerados nunca são editados à mão (METHODOLOGY §0.7).
Schema do roadmap.json:
  project, updated_at (AAAA-MM-DD),
  phases[]: id, name, weeks, dod, status (todo|doing|done|blocked)
  items[]:  id, fr[], phase, title, status, pr?, merged_at?, notes?
  deliveries[]: date, pr (int|null), items[], summary
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html as _html
import json
import sys
from pathlib import Path

STATUSES = ("todo", "doing", "done", "blocked")
STATUS_LABEL = {"todo": "a fazer", "doing": "em andamento", "done": "feito", "blocked": "bloqueado"}
GEN_MD = "<!-- GERADO por scripts/roadmap.py a partir de docs/roadmap/roadmap.json — NÃO EDITAR À MÃO -->"
GEN_HTML = "<!-- GERADO por scripts/roadmap.py a partir de docs/roadmap/roadmap.json — NÃO EDITAR À MÃO -->"


# ---------------------------------------------------------------- io
def paths(root: Path) -> dict[str, Path]:
    return {
        "json": root / "docs" / "roadmap" / "roadmap.json",
        "status": root / "docs" / "STATUS.md",
        "html": root / "docs" / "roadmap" / "index.html",
        "template": root / "scripts" / "roadmap_template.html",
    }


def load(root: Path) -> dict:
    return json.loads(paths(root)["json"].read_text(encoding="utf-8"))


def save(root: Path, data: dict) -> None:
    paths(root)["json"].write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- validate
def validate(data: dict) -> list[str]:
    errors: list[str] = []
    for key in ("project", "updated_at", "phases", "items", "deliveries"):
        if key not in data:
            errors.append(f"campo obrigatório ausente: {key}")
    if errors:
        return errors
    try:
        _dt.date.fromisoformat(data["updated_at"])
    except ValueError:
        errors.append(f"updated_at inválido: {data['updated_at']!r}")
    phase_ids: set[str] = set()
    for p in data["phases"]:
        for key in ("id", "name", "weeks", "dod", "status"):
            if key not in p:
                errors.append(f"fase sem campo {key}: {p}")
        if p.get("id") in phase_ids:
            errors.append(f"id de fase duplicado: {p.get('id')}")
        phase_ids.add(p.get("id"))
        if p.get("status") not in STATUSES:
            errors.append(f"fase {p.get('id')}: status inválido {p.get('status')!r}")
    item_ids: set[str] = set()
    for it in data["items"]:
        for key in ("id", "fr", "phase", "title", "status"):
            if key not in it:
                errors.append(f"item sem campo {key}: {it}")
        if it.get("id") in item_ids:
            errors.append(f"id de item duplicado: {it.get('id')}")
        item_ids.add(it.get("id"))
        if it.get("status") not in STATUSES:
            errors.append(f"item {it.get('id')}: status inválido {it.get('status')!r}")
        if it.get("phase") not in phase_ids:
            errors.append(f"item {it.get('id')}: phase desconhecida {it.get('phase')!r}")
        if not isinstance(it.get("fr"), list):
            errors.append(f"item {it.get('id')}: fr deve ser lista")
    for d in data["deliveries"]:
        for key in ("date", "items", "summary"):
            if key not in d:
                errors.append(f"delivery sem campo {key}: {d}")
        for ref in d.get("items", []):
            if ref not in item_ids:
                errors.append(f"delivery {d.get('date')}: item {ref} não existe")
    return errors


# ---------------------------------------------------------------- queries
def current_phase(data: dict) -> dict | None:
    for status in ("doing", "todo"):
        for p in data["phases"]:
            if p["status"] == status:
                return p
    return data["phases"][-1] if data["phases"] else None


def next_task(data: dict) -> dict | None:
    phase = current_phase(data)
    if not phase:
        return None
    for status in ("todo", "blocked"):
        for it in data["items"]:
            if it["phase"] == phase["id"] and it["status"] == status:
                return it
    # fase atual esgotada: primeiro todo de qualquer fase posterior
    for it in data["items"]:
        if it["status"] == "todo":
            return it
    return None


def counts(data: dict) -> dict[str, int]:
    c = {s: 0 for s in STATUSES}
    for it in data["items"]:
        c[it["status"]] += 1
    c["total"] = len(data["items"])
    c["pct_done"] = round(100 * c["done"] / c["total"]) if c["total"] else 0
    return c


def phase_name(data: dict, pid: str) -> str:
    for p in data["phases"]:
        if p["id"] == pid:
            return p["name"]
    return pid


# ---------------------------------------------------------------- render: STATUS.md
def _md_item(data: dict, it: dict) -> str:
    frs = ", ".join(it["fr"]) if it["fr"] else "—"
    extra = []
    if it.get("pr"):
        extra.append(f"PR #{it['pr']}")
    if it.get("merged_at"):
        extra.append(it["merged_at"])
    if it.get("notes"):
        extra.append(it["notes"])
    tail = f" — {' · '.join(extra)}" if extra else ""
    return f"- `{it['id']}` {it['title']} ({frs}) · fase {it['phase']}{tail}"


def render_status(data: dict) -> str:
    c = counts(data)
    phase = current_phase(data)
    nxt = next_task(data)
    lines = [
        GEN_MD,
        "",
        f"# Status — {data['project']}",
        "",
        f"**Atualizado em:** {data['updated_at']} · **Itens:** {c['done']}/{c['total']} feitos ({c['pct_done']} %) · "
        f"{c['doing']} em andamento · {c['todo']} a fazer · {c['blocked']} bloqueados",
        "",
        "Regenerar: `python3 scripts/roadmap.py build`. Visual: `docs/roadmap/index.html`. Fonte: `docs/roadmap/roadmap.json`.",
        "",
        "## Fase atual",
        "",
    ]
    if phase:
        lines += [f"**Fase {phase['id']} — {phase['name']}** (semanas {phase['weeks']}) · DoD: {phase['dod']}", ""]
    lines += ["## Próxima tarefa", ""]
    if nxt:
        lines += [
            f"**`{nxt['id']}` — {nxt['title']}**",
            "",
            f"- Requisitos: {', '.join(nxt['fr']) if nxt['fr'] else '—'}",
            f"- Fase: {nxt['phase']} — {phase_name(data, nxt['phase'])}",
            f"- Estado: {STATUS_LABEL[nxt['status']]}" + (f" — {nxt['notes']}" if nxt.get("notes") else ""),
            "",
            "Comece pelo gate *plan* (`docs/dev/METHODOLOGY.md §1`).",
            "",
        ]
    else:
        lines += ["Nenhuma tarefa pendente.", ""]
    lines += ["## Em andamento", ""]
    doing = [it for it in data["items"] if it["status"] == "doing"]
    lines += [_md_item(data, it) for it in doing] or ["- (nada em andamento)"]
    lines += ["", "## Bloqueios", ""]
    blocked = [it for it in data["items"] if it["status"] == "blocked"]
    lines += [_md_item(data, it) for it in blocked] or ["- (nenhum)"]
    lines += ["", "## Feito", ""]
    done = [it for it in data["items"] if it["status"] == "done"]
    lines += [_md_item(data, it) for it in done] or ["- (nada ainda)"]
    lines += ["", "## A fazer (por fase)", ""]
    for p in data["phases"]:
        todo = [it for it in data["items"] if it["phase"] == p["id"] and it["status"] == "todo"]
        if todo:
            lines.append(f"### Fase {p['id']} — {p['name']} ({STATUS_LABEL[p['status']]})")
            lines.append("")
            lines += [_md_item(data, it) for it in todo]
            lines.append("")
    lines += ["## Entregas (mais recentes primeiro)", ""]
    for d in list(reversed(data["deliveries"]))[:10]:
        pr = f"PR #{d['pr']}" if d.get("pr") else "sem PR"
        lines.append(f"- **{d['date']}** · {pr} · {d['summary']} · itens: {', '.join(d['items'])}")
    if not data["deliveries"]:
        lines.append("- (nenhuma)")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------- render: HTML
def _e(s) -> str:
    return _html.escape(str(s), quote=True)


def _pill(status: str) -> str:
    return f'<span class="pill pill-{status}">{_e(STATUS_LABEL[status])}</span>'


def _item_row(data: dict, it: dict) -> str:
    frs = ", ".join(it["fr"]) if it["fr"] else "—"
    pr = f'#{it["pr"]}' if it.get("pr") else "—"
    when = it.get("merged_at") or "—"
    notes = it.get("notes") or ""
    return (
        f'<tr data-phase="{_e(it["phase"])}" data-status="{_e(it["status"])}">'
        f'<td><code>{_e(it["id"])}</code></td>'
        f'<td>{_e(it["title"])}{(" <span class=note>" + _e(notes) + "</span>") if notes else ""}</td>'
        f'<td class="mono">{_e(frs)}</td>'
        f'<td class="mono">{_e(it["phase"])}</td>'
        f'<td>{_pill(it["status"])}</td>'
        f'<td class="mono">{_e(pr)}</td>'
        f'<td class="mono">{_e(when)}</td></tr>'
    )


def _rows(data: dict, status: str) -> str:
    rows = [_item_row(data, it) for it in data["items"] if it["status"] == status]
    return "\n".join(rows) or '<tr><td colspan="7" class="empty">— nenhum item —</td></tr>'


def _phases_nav(data: dict) -> str:
    out = []
    for p in data["phases"]:
        done = sum(1 for it in data["items"] if it["phase"] == p["id"] and it["status"] == "done")
        total = sum(1 for it in data["items"] if it["phase"] == p["id"])
        out.append(
            f'<a href="#fase-{_e(p["id"])}" class="nav-item" data-phase="{_e(p["id"])}">'
            f'<span class="dot dot-{_e(p["status"])}"></span>Fase {_e(p["id"])} · {_e(p["name"])}'
            f'<span class="count">{done}/{total}</span></a>'
        )
    return "\n".join(out)


def _phase_cards(data: dict) -> str:
    out = []
    for p in data["phases"]:
        items = [it for it in data["items"] if it["phase"] == p["id"]]
        done = sum(1 for it in items if it["status"] == "done")
        total = len(items)
        pct = round(100 * done / total) if total else 0
        out.append(
            f'<section class="card phase-card" id="fase-{_e(p["id"])}">'
            f'<div class="phase-head"><span class="phase-num">{_e(p["id"])}</span>'
            f'<div><h3>{_e(p["name"])}</h3><p class="meta">semanas {_e(p["weeks"])} · {_pill(p["status"])}</p></div></div>'
            f'<p class="dod"><strong>DoD:</strong> {_e(p["dod"])}</p>'
            f'<div class="bar"><span style="width:{pct}%"></span></div>'
            f'<p class="meta">{done}/{total} itens · {pct} %</p>'
            f'</section>'
        )
    return "\n".join(out)


def _deliveries(data: dict) -> str:
    out = []
    for d in reversed(data["deliveries"]):
        pr = f'PR #{d["pr"]}' if d.get("pr") else "sem PR"
        out.append(
            f'<li><span class="tl-date mono">{_e(d["date"])}</span>'
            f'<div><strong>{_e(d["summary"])}</strong><br>'
            f'<span class="meta">{_e(pr)} · itens: {_e(", ".join(d["items"]))}</span></div></li>'
        )
    return "\n".join(out) or "<li><span class='meta'>nenhuma entrega registrada</span></li>"


def render_html(data: dict, template: str) -> str:
    c = counts(data)
    phase = current_phase(data)
    nxt = next_task(data)
    repl = {
        "GEN": GEN_HTML,
        "PROJECT": _e(data["project"]),
        "UPDATED": _e(data["updated_at"]),
        "PHASE_ID": _e(phase["id"]) if phase else "—",
        "PHASE_NAME": _e(phase["name"]) if phase else "—",
        "PHASE_DOD": _e(phase["dod"]) if phase else "—",
        "PHASE_WEEKS": _e(phase["weeks"]) if phase else "—",
        "NEXT_ID": _e(nxt["id"]) if nxt else "—",
        "NEXT_TITLE": _e(nxt["title"]) if nxt else "nenhuma tarefa pendente",
        "NEXT_FR": _e(", ".join(nxt["fr"])) if nxt and nxt["fr"] else "—",
        "COUNTS_DONE": str(c["done"]), "COUNTS_DOING": str(c["doing"]), "COUNTS_TODO": str(c["todo"]),
        "COUNTS_BLOCKED": str(c["blocked"]), "COUNTS_TOTAL": str(c["total"]), "PCT_DONE": str(c["pct_done"]),
        "PHASES_NAV": _phases_nav(data),
        "PHASE_CARDS": _phase_cards(data),
        "DONE_ROWS": _rows(data, "done"),
        "DOING_ROWS": _rows(data, "doing"),
        "TODO_ROWS": _rows(data, "todo"),
        "BLOCKED_ROWS": _rows(data, "blocked"),
        "DELIVERIES": _deliveries(data),
        "DATA_JSON": json.dumps(data, ensure_ascii=False).replace("</", "<\\/"),
    }
    out = template
    for k, v in repl.items():
        out = out.replace("{{" + k + "}}", v)
    if "{{" in out:
        raise SystemExit("roadmap: placeholder não substituído no template: " + out[out.index("{{"):out.index("{{") + 40])
    return out


# ---------------------------------------------------------------- commands
def build(root: Path) -> None:
    p = paths(root)
    data = load(root)
    errors = validate(data)
    if errors:
        for e in errors:
            print("roadmap: " + e, file=sys.stderr)
        raise SystemExit(2)
    p["status"].parent.mkdir(parents=True, exist_ok=True)
    p["status"].write_text(render_status(data), encoding="utf-8")
    p["html"].write_text(render_html(data, p["template"].read_text(encoding="utf-8")), encoding="utf-8")
    print(f"roadmap: escrito {p['status'].relative_to(root)} e {p['html'].relative_to(root)}")


def check(root: Path) -> int:
    p = paths(root)
    data = load(root)
    errors = validate(data)
    if errors:
        for e in errors:
            print("roadmap: " + e, file=sys.stderr)
        return 2
    drift = 0
    expected = {
        p["status"]: render_status(data),
        p["html"]: render_html(data, p["template"].read_text(encoding="utf-8")),
    }
    for path, content in expected.items():
        actual = path.read_text(encoding="utf-8") if path.exists() else None
        if actual != content:
            print(f"roadmap: {path.relative_to(root)} difere do gerado — rode `python3 scripts/roadmap.py build`")
            drift = 1
    if not drift:
        print("roadmap: OK (gerados em dia)")
    return drift


def add_delivery(root: Path, pr: int | None, items: list[str], summary: str, date: str | None = None) -> None:
    data = load(root)
    date = date or _dt.date.today().isoformat()
    known = {it["id"]: it for it in data["items"]}
    unknown = [i for i in items if i not in known]
    if unknown:
        raise SystemExit(f"roadmap: itens desconhecidos: {', '.join(unknown)}")
    for i in items:
        known[i]["status"] = "done"
        known[i]["pr"] = pr
        known[i]["merged_at"] = date
    data["deliveries"].append({"date": date, "pr": pr, "items": items, "summary": summary})
    data["updated_at"] = date
    errors = validate(data)
    if errors:
        raise SystemExit("roadmap: " + "; ".join(errors))
    save(root, data)
    print(f"roadmap: entrega registrada ({date}, PR {pr}, {len(items)} item(ns)). Agora rode `build`.")


def main(argv: list[str] | None = None) -> int:
    root = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    b = sub.add_parser("build")
    b.add_argument("--check", action="store_true", help="não escreve; falha se gerados diferem")
    a = sub.add_parser("add-delivery")
    a.add_argument("--pr", type=int, default=None)
    a.add_argument("--items", required=True, help="IDs separados por vírgula")
    a.add_argument("--summary", required=True)
    a.add_argument("--date", default=None)
    ns = ap.parse_args(argv)
    if ns.cmd == "validate":
        errors = validate(load(root))
        for e in errors:
            print("roadmap: " + e, file=sys.stderr)
        print("roadmap: OK" if not errors else f"roadmap: {len(errors)} erro(s)")
        return 2 if errors else 0
    if ns.cmd == "build":
        if ns.check:
            return check(root)
        build(root)
        return 0
    if ns.cmd == "add-delivery":
        add_delivery(root, ns.pr, [s.strip() for s in ns.items.split(",") if s.strip()], ns.summary, ns.date)
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
