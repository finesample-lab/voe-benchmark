# Voe Benchmark

Can a company-memory system show what it knows, why it believes it, and what it still cannot prove?

Voe Benchmark is a public, deterministic benchmark for evidence-native company memory. It tests the path from source capture to a governed answer: source preservation, retrieval, claim support, gap reporting, lifecycle, and action restraint.

The fixtures are synthetic. The scorer is system-neutral. You do not need a Voe account, Voe's private source, or network access to run it.

## First run

Requirements: Python 3.11 or newer. There are no third-party runtime dependencies.

```bash
PYTHONPATH=src python3 -m emb validate
PYTHONPATH=src python3 -m emb score examples/reference-predictions.jsonl
```

The reference predictions score 100 by construction. They verify the corpus and scorer; they are not a product result.

Create an empty submission template:

```bash
PYTHONPATH=src python3 -m emb template --output predictions.jsonl
```

Export cases without their expected answers for an adapter:

```bash
PYTHONPATH=src python3 -m emb export --output workset.jsonl
```

After your system processes the workset, populate `predictions.jsonl` and run:

```bash
PYTHONPATH=src python3 -m emb score predictions.jsonl --json
```

An editable install is optional: `python3 -m pip install -e .` provides the shorter `emb` command.

See [ADAPTER-PROTOCOL.md](ADAPTER-PROTOCOL.md) for the submission format and [BENCHMARK.md](BENCHMARK.md) for the scoring contract.

## What is measured

| Dimension | Question |
| --- | --- |
| Capture fidelity | Did the system preserve the bytes that arrived? |
| Retrieval | Did it find the records needed for the question? |
| Claim accuracy | Did it make the labeled claims and avoid invented ones? |
| Provenance | Does each claim cite evidence capable of supporting it? |
| Gaps | Did it name the evidence the record still lacks? |
| Decision | Did it answer, withhold, deny, or propose action correctly? |
| Lifecycle | Did redacted, superseded, or unauthorized material stay out of the answer? |

A composite score cannot hide an evidence failure. A release pass also requires per-dimension floors and zero critical failures.

## Domain examples

The first corpus contains eleven cases across:

- manufacturing quality and supplier certificates;
- contracts, amendments, invoices, and payments;
- hiring offers and background checks;
- incident recovery and bot-authored status;
- customer-support refunds;
- construction change orders;
- cross-domain redaction and access control.

Manufacturing, contracts, and hiring also include example domain vocabularies. They are explanatory artifacts, not a schema a competing system must adopt.

## What a result means

A passing result means the submitted predictions met the published labels and safety floors for this small synthetic corpus. It does not establish production accuracy, latency, security, legal compliance, model quality, or performance on a private company's data.

The corpus and labels are public, so this is a transparent conformance benchmark rather than a hidden leaderboard. Publish the exact commit, adapter, system version, and prediction file with any result.

## Public and private boundary

This repository contains benchmark code, synthetic fixtures, schemas, and examples. Voe's product source remains private. The benchmark is MIT-licensed; that license does not apply to Voe container images, binaries, services, or fineSample trademarks.

Voe is one implementation of the evidence infrastructure this benchmark is
designed to exercise. Its public product and operator documentation is at
[docs.runvoe.com](https://docs.runvoe.com/). The benchmark contract remains
system-neutral: using Voe is not required, and Voe receives no scoring
privilege.

## Contributing

New cases must include a falsifiable expected result, synthetic or properly licensed evidence, and a reason the case cannot be passed by plausible prose alone. See [CONTRIBUTING.md](CONTRIBUTING.md).
