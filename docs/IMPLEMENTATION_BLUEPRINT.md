# PROJECT-AGENT — Implementation and Execution Blueprint
Version: 0.1 (planning baseline) | 2026-11-13
Status: Proposed architecture; not implemented or certified.

## Mission
Build an open-source, multi-tenant, multi-domain agentic project execution engine with human-governed workforce orchestration, model-provider choice, standards-aware workflows, evidence-backed digital monitoring/reporting/verification (dMRV), and auditable delivery.

## Execution workflow
1. Intake: establish organization, project, jurisdiction, domain, scope, stakeholders, budget, schedule, risk class, data classification and model choice.
2. Requirements: map project requirements to versioned PMI/ISO/GRI and domain-specific controls, acceptance criteria and evidence obligations.
3. Plan: generate WBS, dependencies, schedule, cost baseline, risk register, communications plan, RACI, quality plan and change-control policy.
4. Compose workforce: discover, propose, sandbox-test, vet, approve, version, assign, supervise, suspend and retire agents.
5. Execute: durable event-driven tasks, tool permission checks, least privilege, budget limits, approval gates, idempotent operations and compensation.
6. Observe: ingest trusted evidence from authorized sources with timestamps, units, provenance, consent/licensing, validation and immutable audit references.
7. Verify: machine-checkable invariants, deterministic calculations, independent review and human sign-off for consequential decisions.
8. Deliver: project artifacts, dashboards, reports, visualizations, communication records and traceable release/closeout.
9. Improve: capture approved feedback and evaluation datasets; never silently change production agent authority.

## Reference architecture
- apps/web: responsive project workspace and onboarding UI
- apps/api: typed HTTP API, auth, RBAC/ABAC and tenant boundaries
- apps/worker: durable workflow execution and task queues
- packages/contracts: versioned schemas and generated API clients
- packages/orchestrator: task DAG, agent lifecycle, policies and approvals
- packages/models: hosted and local LLM adapters, routing, evaluations, token/cost accounting
- packages/connectors: MCP client/server boundaries and SaaS adapters
- packages/standards: licensed/linked standards registry, control mappings and versioning
- packages/evidence: dMRV ingestion, provenance, signed artifacts and audit trail
- packages/verification: state-machine invariants, policy checks and verification receipts
- packages/domains: construction, ESG, agriculture, food, finance, healthcare, events, aerospace
- packages/research: source-aware retrieval, citations, freshness and confidence
- packages/visuals: charts, maps, diagrams and document generation
- packages/comms: notifications, conversations, channels and escalation
- infra: containers, migrations, secrets, observability, deployment templates
- docs: architecture decisions, threat model, operator guide, contributor guide, API and runbooks

## Proposed technology baseline (to validate in ADRs)
TypeScript strict mode, Next.js frontend, Node API, Python isolated analytics workers where needed, PostgreSQL with row-level isolation, object storage, Redis-backed queues or Temporal, OpenTelemetry, OIDC, Docker Compose for local development, container deployment for production. Keep hosting portable; Vercel may host the frontend, while durable workers and databases require appropriate separate runtime.

## Verification strategy
- Define formal state transitions and invariants for approvals, permissions, agent registration, tenant isolation, evidence integrity and financial authorization.
- Use TLA+/PlusCal or equivalent model checking for concurrency-critical workflows; property-based and contract tests for implementation refinement.
- Validate deterministic computations independently of LLM output.
- Run unit, integration, end-to-end, security, accessibility, load and failure-injection tests in CI.
- Require traceability: requirement -> control -> code -> test -> evidence -> release.
- Formal verification applies to explicitly modeled properties, not blanket claims of correctness, medical safety, financial compliance or certification.

## Domain policy
Core orchestration is general-purpose. Every high-risk domain uses an independently versioned policy pack and jurisdiction-aware controls. Construction, medical, financial and aerospace outputs are decision support unless explicitly authorized by competent human professionals and applicable regulations. No autonomous physical safety-critical actuation or clinical decision without separate certified integration and approvals.

## Standards and data sources
- PMI PMBOK/Process Groups: licensed guidance and cross-references, not redistributed copyrighted text.
- ISO 21502, 31000, 9001, 14001, 45001, 27001, 42001, 19650 and domain-specific standards: versioned control metadata; check licensing.
- GRI Standards, GHG Protocol, ISSB/IFRS S1/S2, SDGs, ESRS as applicable; track versions and jurisdiction.
- Source adapters: government procurement/open data, national statistics, World Bank, UN, FAOSTAT, OpenStreetMap, weather/climate providers, commodity exchanges, permitted market price feeds, FHIR clinical systems with consent, ERP/accounting systems, sensors, construction BIM and project SaaS.
- Every datum requires source ID, retrieval time, effective date, location, currency/units, license, quality, uncertainty and evidence link. No fabricated real-time pricing or compliance claims.

## Workforce and communication
Agent manifest: identifier, purpose, skills, model/tool requirements, inputs/outputs, scope, risk tier, permissions, evaluation suite, version, owner, approval and rollback policy. New agents enter quarantine, pass static and adversarial tests, then require approval before deployment. Messaging supports in-app threads and audited connectors to email, Slack, Teams, Telegram and other permitted APIs; categorize incident, approval, task, announcement and external notice; enforce RBAC, retention and consent.

## Model onboarding
Support hosted model credentials through server-side secrets and local model endpoints (e.g., Ollama/vLLM) through a provider-neutral adapter. Model selection considers capability, cost, privacy, latency, tool support and evaluated safety. A Hugging Face model artifact is not automatically runnable or licensed for every purpose.

## Deployment and UX
Web/PWA first; optional desktop packaging and mobile clients later. Guided onboarding: create workspace -> connect model -> select domain/standards -> import project -> review plan -> approve workforce -> execute -> inspect evidence -> export reports. Provide CLI and API for automation. Never embed provider API secrets in browser bundles.

## Delivery sequence and exit gates
P0 (weeks 1-2): repository scaffold, architecture decisions, threat model, schemas, CI, baseline tests and sample project. Gate: reproducible build and documented requirements.
P1 (weeks 3-5): identity, tenancy, workspace, projects, RBAC/ABAC, audit and model adapters. Gate: isolation and permission tests.
P2 (weeks 6-9): durable orchestration, agent registry/vetting, approvals, connectors and communication. Gate: model-checked critical transitions and adversarial tests.
P3 (weeks 10-13): evidence/dMRV, standards registry, research, dashboards and export. Gate: provenance and calculation reconciliation.
P4 (weeks 14-17): construction and ESG pilot templates, finance controls, visual outputs and operator guide. Gate: independently reviewed pilot acceptance.
P5 (weeks 18-22): hardening, observability, security review, deployment packaging, load tests and open-source release. Gate: documented residual risks and release sign-off.
These are planning estimates, not delivery commitments; reassess after scope and team sizing.

## Initial acceptance criteria
- One-click local developer startup with documented prerequisites.
- Authenticated users cannot read/write across tenants; tests demonstrate enforcement.
- No agent can gain a new permission or invoke a consequential tool without an approved policy transition.
- Every material project claim and metric links to provenance and validation status.
- Approval-gated actions cannot be bypassed by retries, prompt injection or workflow concurrency.
- Model-provider swap preserves typed interfaces and explicit evaluation thresholds.
- A sample ESG/construction project can be onboarded, planned, executed in simulation, verified and exported end-to-end.
- Accessibility, security, disaster recovery, operator documentation and open-source licensing are reviewed before release.

## Immediate next engineering tasks
1. Confirm baseline architecture and repo license.
2. Write ADRs, requirements catalog, domain risk matrix and threat model.
3. Bootstrap monorepo and local Docker development stack.
4. Define canonical project, task, agent, approval, evidence and verification schemas.
5. Implement minimal vertical slice with tests before broad domain expansion.
