"""Fail-closed, offline Asana task-draft adapter for survey evidence.

No credentials, API calls, approvals, or external writes are performed.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

SCHEMA_VERSION = "evidence-review/v1"
EVIDENCE_TYPE = "survey_reconciliation"
ENVELOPE_FIELDS = frozenset({
    "schema_version", "source_project", "evidence_type",
    "evidence_sha256", "idempotency_key", "review_gate",
    "engineering_approved", "approval_required", "transport_state",
})
REVIEW_GATES = frozenset({"BLOCKED", "READY_FOR_SURVEYOR_REVIEW"})


def make_asana_task_draft(envelope: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a minimal handoff envelope and return an *unsent* Asana draft.

    The caller must later use a server-side, authenticated Asana connector,
    access-controlled project mapping, and an idempotency crosswalk. This
    function intentionally never accepts or forwards site-specific content.
    """
    if not isinstance(envelope, Mapping) or set(envelope) != ENVELOPE_FIELDS:
        raise ValueError("unexpected or missing handoff fields")
    if envelope["schema_version"] != SCHEMA_VERSION or envelope["evidence_type"] != EVIDENCE_TYPE:
        raise ValueError("unsupported handoff schema/evidence type")
    source_project = envelope["source_project"]
    if not isinstance(source_project, str) or re.fullmatch(r"[A-Z][A-Z0-9_-]{2,49}", source_project) is None:
        raise ValueError("invalid project alias")
    digest = envelope["evidence_sha256"]
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise ValueError("invalid evidence digest")
    expected_key = f"{source_project}:{EVIDENCE_TYPE}:{digest}"
    if envelope["idempotency_key"] != expected_key:
        raise ValueError("invalid evidence idempotency key")
    gate = envelope["review_gate"]
    if not isinstance(gate, str) or gate not in REVIEW_GATES:
        raise ValueError("unsupported review gate")
    if (envelope["engineering_approved"] is not False
            or envelope["approval_required"] is not True
            or envelope["transport_state"] != "DRAFT_NOT_SYNCED"):
        raise ValueError("cannot bypass human review or preflight boundaries")

    name = (f"Review {source_project} survey reconciliation"
            if gate == "READY_FOR_SURVEYOR_REVIEW"
            else f"Resolve {source_project} survey reconciliation blockers")
    notes = (
        f"Project alias: {source_project}\n"
        f"Evidence SHA-256: {digest}\n"
        f"Preflight gate: {gate}\n"
        "Human review required. This preflight is NOT engineering, "
        "survey, hydraulic, construction or billing approval. "
        "Locate evidence within the authorized private evidence store."
    )
    return {
        "asana_request": {"name": name, "notes": notes},
        "sync_state": "DRAFT_ONLY_NOT_SENT",
        "approval_required": True,
        "source_key": expected_key,
    }
