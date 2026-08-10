# Lark data route

Use capability discovery at runtime. Domain names and readable fields depend on the active Lark CLI profile, user scopes, and tenant configuration. Read the relevant Lark domain skill or shortcut reference before using an unfamiliar command; inspect `lark-cli schema` before a raw API call.

| Need | Lark route | Evidence value | Boundary |
|---|---|---|---|
| Target identity and organization | contact / user lookup | Resolves the employee and formal context | Identity does not prove work observation |
| Shared meetings and speech | `vc` search → meeting detail → note/transcript | Attributable discussion, decisions, actions | Attendance alone is weak |
| Business conversations | `im` message search → chat/thread context | Direct collaboration and follow-up | Use only visible, authorized content |
| Work execution | task / project / approval | Ownership, dependency, milestones, decisions | Assignment alone is not outcome evidence |
| Shared artifacts | docs / drive / wiki / sheets / base | Authorship, substantive edits, comments | View-only access is weak |
| Objectives and contribution | OKR | Shared objective, contributor, progress, outcome | An aligned objective alone is not observation |
| Formal coordination | calendar / mail | Scope, responsibility, follow-up | Administrative CC is supporting context |
| Review context | docs / sheets / base / mail | Cycle, period, previous reviewer context when authorized | If unavailable, disclose the gap |

## Retrieval discipline

1. Use `lark-cli auth status --json --verify` before every new run.
2. Keep company and personal profiles separate.
3. Prefer user identity for personal or collaboration evidence.
4. Use shortcuts before raw API calls.
5. Page to completion and retain `has_more`, truncations, denied sources, and transient errors.
6. Prefer raw transcripts or attributable messages over AI summaries for behavioral claims.
7. Keep source references and minimal facts; do not pass full private conversations to the host by default.

## Evidence strength

- `high`: primary, attributable, substantive, and inside the observation period.
- `medium`: primary with partial context, or derived material corroborated by primary evidence.
- `low`: administrative or indirect; useful for coverage diagnostics and insufficient on its own.

