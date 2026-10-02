# Adapter protocol, v0.1

An adapter translates the benchmark's neutral timeline into a system under test and returns one JSON object per case.

## Input

Run `emb export --output workset.jsonl`. Each line contains a case with its `expected` block removed.

Process timeline events in order:

- `capture`: admit the record and preserve the supplied raw string;
- `supersede`: mark the earlier record as no longer current, without pretending it never existed;
- `redact`: destroy readable content for the named record while preserving the permitted audit tombstone.

Then ask `query.text` as `caller` at `query.as_of`.

## Output

Write one JSON object per line:

```json
{
  "case_id": "manufacturing.lot-release.001",
  "observed_sources": [
    {"record_id": "mfg.sensor.17", "sha256": "..."}
  ],
  "retrieved_record_ids": ["mfg.sensor.17"],
  "claims": [
    {"id": "temperature_in_range", "cited_record_ids": ["mfg.sensor.17"]}
  ],
  "gaps": ["qa_release_missing"],
  "decision": "withhold",
  "answer": "Optional free-form answer; not scored in v0.1."
}
```

`observed_sources` proves what the adapter saw at capture time. For a later-redacted record, the digest may survive in the audit tombstone even though the raw string may not.

`retrieved_record_ids` is ranked, highest first. The scorer reads the first five.

`claims` and `gaps` use the public labels in each case. This keeps v0.1 deterministic and avoids using one model to judge another model's prose.

## Rules

- Emit exactly one prediction per case.
- Do not read the `expected` block during an evaluated run.
- Do not manually change individual predictions after seeing their score.
- If the system cannot represent a field, leave the corresponding list empty and disclose the limitation.
- Keep the system's free-form answer in `answer` when useful, but v0.1 does not score its style.
