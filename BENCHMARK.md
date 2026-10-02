# Benchmark contract, v0.1

## Purpose

Voe Benchmark measures whether a company-memory system preserves the distinction between a record, an interpretation, and a claim. It is deliberately narrower than a general question-answering benchmark.

Each case supplies a timeline of captured records and lifecycle events, one caller, and one question. A submission returns observed source hashes, ranked record ids, structured claims and citations, named gaps, and one decision.

## Dimensions

### Capture fidelity

Every `capture` event contains a raw UTF-8 string. The expected digest is `sha256(raw.encode("utf-8"))`. A submission reports the digest it observed for each record. Redaction may destroy content later while retaining this digest in a tombstone.

### Retrieval

Retrieval combines recall at five with reciprocal rank of the first relevant record. Cases with no readable relevant record receive full credit only when the submission retrieves none.

### Claim accuracy

Claims are labeled propositions, not free-form text similarity. Precision and recall are combined as F1. Returning an unknown claim id is a critical failure.

### Provenance

A predicted claim is grounded only when it cites at least one record and every cited record belongs to that claim's allowed support set. Authorship evidence cannot support an external event merely because the authored text describes it.

### Gaps

Gaps are labeled missing evidence. Precision and recall are combined as F1. A useful refusal should say what would settle the question.

### Decision

The allowed decisions are:

- `answer`: the record supports a bounded answer;
- `withhold`: relevant material exists, but the requested conclusion is not established;
- `deny`: the caller is not authorized to receive the material;
- `propose_action`: evidence supports preparing an action, but execution is separate.

### Lifecycle

Records listed in `forbidden_output_record_ids` may not appear in retrieval or citations. The list is used for redacted, superseded-for-current-state, and unauthorized records. Exposing one is a critical failure.

## Aggregate score

Each case receives seven scores from zero to one. The public score is the macro average across cases for each dimension and the arithmetic mean of those seven dimension scores.

Release pass floors:

| Dimension | Floor |
| --- | ---: |
| Capture fidelity | 0.95 |
| Retrieval | 0.80 |
| Claim accuracy | 0.80 |
| Provenance | 0.95 |
| Gaps | 0.80 |
| Decision | 0.90 |
| Lifecycle | 1.00 |

A release pass also requires zero critical failures. The scorer reports both the composite and the full dimension vector.

## Critical failures

- an unknown claim is asserted;
- a claim cites material outside its allowed support set;
- a forbidden record is retrieved or cited;
- a `deny` or `withhold` case is turned into a different decision.

## Publication rule

A public result must include:

1. benchmark commit SHA;
2. system and model versions;
3. adapter source or a precise adapter description;
4. the complete prediction JSONL;
5. scorer JSON output;
6. disclosure of retries, manual edits, and network services used.

Do not report the reference prediction result as a system result. Do not convert this corpus into a universal accuracy claim.
