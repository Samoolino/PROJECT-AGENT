# Evidence-review to Asana task-draft integration

Status: offline integration implemented and locally tested. Live Asana authorization, synchronization and production approval are NOT configured.

PROJECT-AGENT accepts a minimal evidence-review/v1 envelope and prepares a draft Asana task. Domain projects retain raw measurements, survey geometry, identities, reports and approvals in authorized private evidence stores.

The envelope allows exactly: schema_version, source_project, evidence_type, evidence_sha256, idempotency_key, review_gate, engineering_approved, approval_required, transport_state.

The first release supports schema_version evidence-review/v1, evidence_type survey_reconciliation, lowercase 64-hex SHA-256 evidence digest, review_gate BLOCKED or READY_FOR_SURVEYOR_REVIEW, engineering_approved false, approval_required true and transport_state DRAFT_NOT_SYNCED. Project aliases contain uppercase letters, digits, underscores or hyphens and must be 3 to 50 characters. The idempotency key is project alias, evidence type and original artifact digest joined with colons.

Any extra field is rejected. The adapter only constructs deterministic task name/notes, sync_state DRAFT_ONLY_NOT_SENT, approval_required true and source_key. It never creates a task, approves design, authorizes field work, or calls Asana.

Testing: set PYTHONPATH=src and run python -m unittest discover -s tests -v.

Before live activation: connect an authorized Asana workspace; map project/assignee identifiers server-side; validate scopes; store access tokens in a secret manager; implement a persistent idempotency-key to Asana task ID crosswalk and outbound audit log; exercise retry, outage, wrong-tenant, and revoked-access cases; obtain human approval for writeback. Asana must not be treated as the authoritative engineering approval register.

Hash identity is not a digital signature, source verification, or engineering certification. Private source artifacts stay outside Asana, with independent evidence custody.
