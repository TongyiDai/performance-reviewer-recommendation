---
name: performance-reviewer-recommendation
description: Recommend human-reviewable 360-degree performance reviewers from authorized Feishu/Lark work evidence through Lark CLI. Use when asked for 环评人、360评估人、绩效反馈人、reviewer nomination, or a reviewer shortlist with reasons based on meetings, messages, tasks, documents, OKRs, approvals, calendars, or other observable collaboration records.
---

# Performance Reviewer Recommendation

## One job

Recommend people who have directly observed an employee’s work during a specified period, and explain why each person is a suitable 360 reviewer. Use Lark CLI as the data access layer. Use the current Agent host—Doubao Enterprise, Codex, or Claude Code—as the reasoning layer.

This Skill does not score the employee’s performance, assign reviewers, send invitations, write performance records, or infer private traits.

## Default user experience

Accept requests such as:

> 给张三推荐本周期 10 位 360 环评人，并说明每个人的推荐原因。

Resolve the employee, review period, requested count, and role mix. Use an explicit review cycle or date range when provided. If the current cycle cannot be established from authorized Lark evidence, use a disclosed six-month observation window for a direct recommendation request; ask for the period only when it would materially change the candidate pool or the user requests a formal-cycle result. Default to ten candidates when count is omitted. Include manager, peer, and cross-functional perspectives when the request does not specify a mix; include direct reports when the employee is a manager and the review design calls for downward feedback.

Ask one concise clarification when an ambiguity would materially change the candidate pool. Do not delay the task for preferences that can be reported as assumptions.

## Host and access gate

Read [host-bootstrap.md](references/host-bootstrap.md) before any Feishu retrieval.

- **Doubao Enterprise**: use its built-in Lark tool or approved Lark CLI bridge. If neither is available, stop with `blocked`.
- **Codex / Claude Code**: require local `lark-cli`. If it is missing, tell the user to install or enable it, then stop.
- Prefer `lark-cli auth status --json --verify` to verify the intended tenant, profile, and user identity. When the current CLI build does not expose the `auth` subcommand, fall back to `contact +get-user --as user` and, if needed, `task +get-my-tasks --as user` as a read-only compatibility probe. Treat `contact` as resolved current user, treat `task` as user-context only, and do not turn compatibility mode into a write-capable or subject-binding claim.
- Never silently use a bot identity, a different Feishu profile, browser search, or manually guessed records as a substitute.

Record the host, Lark profile, identity type, token status, scopes, and check time without recording credentials.

## Retrieval sequence

Use [data-source-map.md](references/data-source-map.md) for the source route. Prefer the narrowest read-only query that answers the request, then paginate completely.

1. **Resolve the target**: identify the employee and confirm the organization context.
2. **Resolve the period**: use the explicit cycle or observation dates; retain the assumption if a default is used.
3. **Find shared work**: search the target’s substantive collaboration across meetings, transcripts, messages and threads, tasks, documents, OKRs, projects, approvals, calendars, and mail when authorized.
4. **Build candidate edges**: connect the employee to people who jointly delivered work, made decisions, owned follow-up, reviewed artifacts, or participated in attributable business discussions.
5. **Preserve boundaries**: record source, date, access status, pagination, truncation, deleted material, and unreadable artifacts. A meeting title, attendee list, message mention, or document view alone does not prove observation.

Prefer primary evidence in this order:

1. shared deliverables, task ownership, decisions, action items, milestones, substantive edits/comments, OKRs, approvals, and formal feedback;
2. attributable message or transcript content with context;
3. AI-generated meeting summaries corroborated by primary material;
4. co-attendance, group membership, mentions, views, and administrative CC as supporting context only.

## Candidate rules

Exclude or flag the employee, duplicate identities, inactive or departed users, people outside the permitted population, policy-defined conflicts, and anyone without substantive evidence in the period.

Treat cross-tenant collaborators as eligibility-flagged candidates even when their direct evidence is strong. Confirm that the target review system accepts them before placing them in the submit-ready shortlist.

Do not use message volume, meeting count, attendance, reactions, leave, compensation, health, age, gender, ethnicity, disability, private relationships, or inferred personality as positive evidence.

Require two independent evidence items when available, with at least one substantive primary item. Keep confidence separate from rank: a high-ranked candidate with incomplete evidence remains low confidence.

Select for perspective coverage, not popularity. Avoid over-concentration in one team or one type of relationship. Leave a role unfilled when the evidence does not support it.

## Evidence representation

Normalize each usable observation into the contract in [evidence.schema.json](references/evidence.schema.json). Keep raw snapshots and the candidate-name map local. Give the host model opaque candidate aliases and minimal facts with source references.

Each evidence edge must answer:

- Who observed whom?
- What work fact was observed?
- Which dimension does it support?
- When did it occur?
- What source can a reviewer inspect?
- Is the fact primary, derived, administrative, restricted, or unknown?

## Recommendation logic

Use a transparent, provisional rubric when no organization policy is provided:

```text
work relevance       30
observation depth    25
recency              15
evidence breadth     10
role complementarity 10
review reliability   10
```

Store the rubric version in the audit record. Calculate components from evidence edges, not raw event counts. Apply explicit flags for sparse evidence, conflict, duplicated perspective, and historical concentration. Do not let the model override an access block or an insufficient-evidence state.

## Default output

Lead with a concise human-readable shortlist:

| 候选人 | 角色 | 推荐原因 | 证据范围 | 置信度 |
|---|---|---|---|---|
| 某人 | 跨团队协作 | 基于共同交付、关键决策和后续验收，对目标员工的交付与协作有直接观察 | 会议、任务、文档 | 中 |

Each reason must state the observed work relationship, supported dimensions, and material limitation. Do not copy private messages or present model-generated claims as source facts.

When machine-readable output is needed, return JSON matching [output.schema.json](references/output.schema.json) and validate it with:

```bash
python3 scripts/validate_output.py path/to/result.json
```

Always include source coverage, evidence references, excluded candidates, data gaps, confidence, host audit metadata, and `human_review_required: true`.

## Completion boundary

The normal endpoint is a recommendation draft for HR or the responsible manager. Do not assign reviewers or write back to a performance system. If the user later explicitly requests a write, require a dry-run preview, confirmation, idempotency protection, and exact readback; keep the recommendation and human decision as separate records.

## Quality checks

Use synthetic or redacted fixtures to test missing Lark CLI, expired user identity, bot-only access, incomplete pagination, unreadable transcripts, attendance-only candidates, duplicate identities, conflict flags, role gaps, contradictory evidence, sparse evidence, and invalid model JSON. Report `blocked` or `insufficient_evidence` explicitly instead of filling the quota.
