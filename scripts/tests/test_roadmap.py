"""Testes de scripts/roadmap.py — só stdlib (unittest)."""
import json, re, shutil, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import roadmap  # noqa: E402

SAMPLE = {
    "project": "ForjaOS", "updated_at": "2026-11-08",
    "phases": [
        {"id": "0", "name": "Fundação", "weeks": "1–2", "dod": "Imagem builda no Actions", "status": "doing"},
        {"id": "1", "name": "Imagem instalável", "weeks": "3–8", "dod": "Pendrive → dual boot", "status": "todo"},
    ],
    "items": [
        {"id": "GOV-001", "fr": ["ADR-026"], "phase": "0", "title": "Metodologia", "status": "done", "pr": None, "merged_at": "2026-11-08"},
        {"id": "F0-001", "fr": ["FR-001"], "phase": "0", "title": "Containerfile mínimo", "status": "todo"},
        {"id": "F0-002", "fr": ["FR-002"], "phase": "0", "title": "check-branding real", "status": "blocked", "notes": "depende do F0-001"},
        {"id": "F1-001", "fr": ["FR-010"], "phase": "1", "title": "ISO", "status": "todo"},
    ],
    "deliveries": [{"date": "2026-11-08", "pr": None, "items": ["GOV-001"], "summary": "Governança"}],
}


def copy(d):
    return json.loads(json.dumps(d))


class RoadmapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "docs" / "roadmap").mkdir(parents=True)
        (self.tmp / "scripts").mkdir()
        shutil.copy(ROOT / "scripts" / "roadmap_template.html", self.tmp / "scripts" / "roadmap_template.html")
        self.json = self.tmp / "docs" / "roadmap" / "roadmap.json"
        self.json.write_text(json.dumps(SAMPLE, ensure_ascii=False), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    # --- validate ---
    def test_validate_ok(self):
        self.assertEqual(roadmap.validate(SAMPLE), [])

    def test_validate_bad_status(self):
        bad = copy(SAMPLE); bad["items"][0]["status"] = "maybe"
        self.assertTrue(any("status" in e for e in roadmap.validate(bad)))

    def test_validate_unknown_phase(self):
        bad = copy(SAMPLE); bad["items"][0]["phase"] = "9"
        self.assertTrue(any("phase" in e for e in roadmap.validate(bad)))

    def test_validate_duplicate_id(self):
        bad = copy(SAMPLE); bad["items"][1]["id"] = "GOV-001"
        self.assertTrue(any("duplicado" in e for e in roadmap.validate(bad)))

    def test_validate_delivery_unknown_item(self):
        bad = copy(SAMPLE); bad["deliveries"][0]["items"] = ["NOPE-1"]
        self.assertTrue(any("NOPE-1" in e for e in roadmap.validate(bad)))

    # --- queries ---
    def test_current_phase_is_first_doing(self):
        self.assertEqual(roadmap.current_phase(SAMPLE)["id"], "0")

    def test_next_task_is_first_todo_of_current_phase(self):
        self.assertEqual(roadmap.next_task(SAMPLE)["id"], "F0-001")

    def test_next_task_falls_back_to_blocked(self):
        d = copy(SAMPLE); d["items"][1]["status"] = "done"
        self.assertEqual(roadmap.next_task(d)["id"], "F0-002")

    # --- render ---
    def test_status_md_contains_sections(self):
        md = roadmap.render_status(SAMPLE)
        for s in ("GERADO", "Fase atual", "Feito", "Em andamento", "Próxima tarefa", "F0-001", "Bloqueios", "F0-002"):
            self.assertIn(s, md)

    def test_html_is_self_contained_and_has_data(self):
        tpl = (ROOT / "scripts" / "roadmap_template.html").read_text(encoding="utf-8")
        html = roadmap.render_html(SAMPLE, tpl)
        self.assertNotIn("cdn.tailwindcss.com", html)
        self.assertIn('type="application/json"', html)
        self.assertIn("F0-001", html)
        self.assertNotIn("{{", html)
        self.assertIn("&lt;", roadmap.render_html({**copy(SAMPLE), "items": [{**SAMPLE["items"][0], "title": "<b>x</b>"}]}, tpl))

    def test_template_colors_come_from_palette(self):
        palette = (ROOT / "brand" / "palette.json").read_text(encoding="utf-8").lower()
        allowed = set(re.findall(r"#[0-9a-f]{6}\b", palette))
        tpl = (ROOT / "scripts" / "roadmap_template.html").read_text(encoding="utf-8").lower()
        used = set(re.findall(r"#[0-9a-f]{6}\b", tpl))
        self.assertTrue(used, "template sem cores?")
        self.assertEqual(used - allowed, set(), f"cores fora do palette: {used - allowed}")

    # --- build / check / add-delivery ---
    def test_build_writes_and_check_detects_drift(self):
        roadmap.build(self.tmp)
        status = self.tmp / "docs" / "STATUS.md"
        self.assertTrue(status.exists())
        self.assertTrue((self.tmp / "docs" / "roadmap" / "index.html").exists())
        self.assertEqual(roadmap.check(self.tmp), 0)
        status.write_text(status.read_text(encoding="utf-8") + "\nedit manual\n", encoding="utf-8")
        self.assertEqual(roadmap.check(self.tmp), 1)

    def test_add_delivery_marks_items_done(self):
        roadmap.add_delivery(self.tmp, pr=7, items=["F0-001"], summary="Containerfile", date="2026-11-09")
        d = json.loads(self.json.read_text(encoding="utf-8"))
        item = next(i for i in d["items"] if i["id"] == "F0-001")
        self.assertEqual(item["status"], "done")
        self.assertEqual(item["pr"], 7)
        self.assertEqual(item["merged_at"], "2026-11-09")
        self.assertEqual(d["deliveries"][-1]["pr"], 7)
        self.assertEqual(d["updated_at"], "2026-11-09")

    def test_add_delivery_rejects_unknown_item(self):
        with self.assertRaises(SystemExit):
            roadmap.add_delivery(self.tmp, pr=8, items=["NOPE"], summary="x", date="2026-11-09")

    def test_build_fails_on_invalid_json(self):
        bad = copy(SAMPLE); bad["items"][0]["status"] = "maybe"
        self.json.write_text(json.dumps(bad), encoding="utf-8")
        with self.assertRaises(SystemExit):
            roadmap.build(self.tmp)


if __name__ == "__main__":
    unittest.main()
