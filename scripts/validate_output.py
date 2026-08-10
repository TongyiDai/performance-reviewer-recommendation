#!/usr/bin/env python3
"""Validate the minimum safety and traceability contract for a result JSON."""

import json
import sys
from pathlib import Path


ALLOWED_STATUS = {"ready", "insufficient_evidence", "blocked"}
ALLOWED_ROLES = {
    "manager",
    "peer",
    "cross_functional",
    "direct_report",
    "project_owner",
    "customer_partner",
}
REQUIRED_RECOMMENDATION = {
    "candidate_ref",
    "role",
    "score",
    "confidence",
    "observed_dimensions",
    "reason",
    "evidence_refs",
    "counter_evidence",
    "risks",
    "next_action",
}


def fail(message):
    print(f"INVALID: {message}")
    raise SystemExit(1)


def main(path):
    try:
        payload = json.loads(Path(path).read_text())
    except Exception as exc:
        fail(f"cannot read JSON: {exc}")

    if not isinstance(payload, dict):
        fail("root must be an object")
    if payload.get("schema_version") != "reviewer-recommendation.v1":
        fail("unsupported schema_version")
    if payload.get("status") not in ALLOWED_STATUS:
        fail("status must be ready, insufficient_evidence, or blocked")
    if payload.get("human_review_required") is not True:
        fail("human_review_required must be true")
    for field in ("request", "coverage", "recommendations", "excluded_candidates", "data_gaps", "audit"):
        if field not in payload:
            fail(f"missing top-level field: {field}")
    if not isinstance(payload["recommendations"], list):
        fail("recommendations must be an array")

    seen_refs = set()
    for item in payload["recommendations"]:
        if not isinstance(item, dict):
            fail("each recommendation must be an object")
        missing = REQUIRED_RECOMMENDATION - set(item)
        if missing:
            fail(f"recommendation missing: {sorted(missing)}")
        if item["confidence"] not in {"high", "medium", "low"}:
            fail("confidence must be high, medium, or low")
        if item["role"] not in ALLOWED_ROLES:
            fail(f"unsupported role: {item['role']}")
        if not isinstance(item["score"], (int, float)) or not 0 <= item["score"] <= 100:
            fail("score must be a number from 0 to 100")
        if not isinstance(item["evidence_refs"], list):
            fail("evidence_refs must be an array")
        for ref in item["evidence_refs"]:
            if not isinstance(ref, str) or not ref:
                fail("evidence_refs must contain non-empty strings")
            seen_refs.add(ref)
        if not isinstance(item["counter_evidence"], list) or not isinstance(item["risks"], list):
            fail("counter_evidence and risks must be arrays")

    audit = payload["audit"]
    if not isinstance(audit, dict):
        fail("audit must be an object")
    for field in ("run_id", "source_manifest", "evidence_refs", "scoring_version", "model_backend"):
        if not audit.get(field):
            fail(f"audit missing: {field}")
    if not isinstance(audit["evidence_refs"], list):
        fail("audit.evidence_refs must be an array")
    known_evidence = set(audit["evidence_refs"])
    for item in payload["recommendations"]:
        unknown = set(item["evidence_refs"]) - known_evidence
        if unknown:
            fail(f"recommendation cites unknown evidence: {sorted(unknown)}")

    if payload["status"] == "ready" and not payload["recommendations"]:
        fail("ready result must contain at least one recommendation")
    print(f"VALID: {len(payload['recommendations'])} recommendation(s)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: validate_output.py result.json")
        raise SystemExit(2)
    main(sys.argv[1])
