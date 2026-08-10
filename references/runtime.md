# Agent runtime contract

This file expands the short contract in the README. `SKILL.md` remains the normative instruction file.

## Trigger

Use this Skill when the user asks for 环评人、360 评估人、绩效反馈人、reviewer nomination, or a ranked reviewer shortlist based on observable collaboration.

## First action

1. Read `SKILL.md`.
2. Read `references/host-bootstrap.md`.
3. Identify the host: Doubao Enterprise, Codex, or Claude Code.
4. Verify the read-capable Lark route before retrieving any employee evidence.

## Access gate

For Codex and Claude Code, run:

```bash
command -v lark-cli
lark-cli --help
lark-cli auth status --json --verify
```

Continue only when the intended tenant is active and the result reports `identity: user` and `verified: true`. Missing CLI, failed verification, bot-only identity, or an unavailable required scope is a stop condition.

For Doubao Enterprise, use the built-in enterprise Lark capability or an approved Lark CLI bridge. Do not ask for a local CLI when the built-in capability is available.

## Request contract

Resolve:

- employee identity and organization context;
- explicit review cycle or date range, when provided;
- requested reviewer count; default is 10;
- role mix, if the user specifies one.

If a cycle is unavailable, use a disclosed six-month observation window for a direct recommendation request. Keep the limitation in the result.

## Evidence contract

Search shared work through the narrowest authorized Lark routes. Page until the source reports completion and retain truncation, denied-source, deleted-content, and unreadable-artifact flags.

Prefer, in order:

1. shared deliverables, tasks, decisions, action items, milestones, substantive edits, OKRs, approvals, and formal feedback;
2. attributable messages and raw transcripts;
3. AI meeting summaries corroborated by primary evidence;
4. attendance, mentions, views, and administrative CC only as supporting context.

Each recommendation needs a relationship, observed work fact, date, dimension, source reference, evidence strength, and material limitation. Do not send full private conversations to the reasoning model by default; pass minimal facts and opaque candidate aliases.

## Output contract

Lead with a human-readable ranking from high to low. Each row states:

- candidate and observed relationship;
- why the person can provide useful feedback;
- evidence range and strength;
- confidence and material limitation.

When JSON is requested, validate it with `scripts/validate_output.py`. Always retain `human_review_required: true`, source coverage, evidence references, excluded candidates, data gaps, and audit metadata.

## Hard boundaries

- Read-only recommendation is the default.
- Never assign reviewers, send invitations, or write performance records in the recommendation step.
- Never use a bot or browser search as a substitute for the intended user's authorized evidence.
- Never promote a cross-tenant collaborator into the final submit-ready list without an explicit eligibility check.
- Return `blocked` or `insufficient_evidence` when access or evidence is inadequate; do not fill the requested quota with weak candidates.
