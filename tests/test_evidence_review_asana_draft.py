import unittest

from project_agent.integrations.evidence_review import make_asana_task_draft


class AsanaDraftTests(unittest.TestCase):
    def make_envelope(self):
        digest = "a" * 64
        return {
            "schema_version": "evidence-review/v1",
            "source_project": "EXAMPLE-PROJECT",
            "evidence_type": "survey_reconciliation",
            "evidence_sha256": digest,
            "idempotency_key": f"EXAMPLE-PROJECT:survey_reconciliation:{digest}",
            "review_gate": "READY_FOR_SURVEYOR_REVIEW",
            "engineering_approved": False,
            "approval_required": True,
            "transport_state": "DRAFT_NOT_SYNCED",
        }

    def test_creates_safe_asana_draft_without_external_write(self):
        draft = make_asana_task_draft(self.make_envelope())
        self.assertEqual(draft["sync_state"], "DRAFT_ONLY_NOT_SENT")
        self.assertEqual(draft["asana_request"]["name"], "Review EXAMPLE-PROJECT survey reconciliation")
        self.assertIn("Human review required", draft["asana_request"]["notes"])
        self.assertTrue(draft["approval_required"])
        self.assertEqual(draft["source_key"], self.make_envelope()["idempotency_key"])
        self.assertNotIn("project_gid", draft["asana_request"])

    def test_preflight_not_engineering_approval(self):
        bad = self.make_envelope()
        bad["engineering_approved"] = True
        with self.assertRaises(ValueError):
            make_asana_task_draft(bad)

    def test_forged_idempotency_key_rejected(self):
        bad = self.make_envelope()
        bad["idempotency_key"] = "forged"
        with self.assertRaises(ValueError):
            make_asana_task_draft(bad)

    def test_rejects_unexpected_sensitive_fields(self):
        bad = self.make_envelope()
        bad["site_coordinates"] = [6.4, 3.3]
        with self.assertRaises(ValueError):
            make_asana_task_draft(bad)

    def test_blocked_review_gate_is_never_silently_approved(self):
        bad = self.make_envelope()
        bad["review_gate"] = "BLOCKED"
        draft = make_asana_task_draft(bad)
        self.assertIn("Resolve", draft["asana_request"]["name"])
        self.assertTrue(draft["approval_required"])


if __name__ == "__main__":
    unittest.main()
