# Contributing

## Case standard

A benchmark case must be:

- synthetic or redistributable under the repository license;
- small enough for a person to audit;
- domain-realistic without containing personal or confidential data;
- explicit about which proposition each source can support;
- falsifiable through structured claims, gaps, decisions, and forbidden outputs;
- hard for the right reason, such as conflicting versions, agent-authored material, missing evidence, redaction, or caller authority.

Do not add cases that reward a particular vendor's internal object names. Example vocabularies may be domain-specific, but the scorer contract stays neutral.

## Adding a case

1. Add a JSON case under `domains/<domain>/cases/`.
2. Run `emb validate`.
3. Regenerate the reference predictions with `emb reference --output examples/reference-predictions.jsonl`.
4. Run `python -m unittest discover -s tests -v`.
5. Explain the failure mode the case catches in the pull request.

Changing an existing label or expected result is a benchmark-version change. Preserve old tagged releases so published results remain reproducible.
