# Team workflow

## Shared objective

Build and compare a custom CNN baseline and a pretrained DenseNet121 for study-level normal-versus-abnormal classification on the `XR_WRIST` subset of MURA.

The shared data contract is `configs/data.yaml`. Changes to labels, split policy, image handling, aggregation, or primary metrics require a documented team decision and pull request.

## Responsibilities

### Member 1: data and audit

- Download and verify MURA through the approved source.
- Filter `XR_WRIST` studies.
- Audit counts, corrupt files, labels, and duplicates.
- Generate deterministic patient-level manifests.
- Implement the dataset and DataLoader contract.

Deliverables: manifests, audit summary, split checks, and data-loading code.

### Member 2: preprocessing and baseline

- Implement preprocessing and conservative augmentation.
- Implement the custom CNN baseline.
- Run a small-subset overfit test and baseline experiments.
- Document class-imbalance handling.

Deliverables: baseline model, training evidence, config, and validation results.

### Member 3: pretrained model and training

- Implement pretrained DenseNet121.
- Implement the training loop, AMP, checkpointing, and resume support.
- Record training time and peak GPU memory.

Deliverables: reusable trainer, best validation checkpoint reference, and run logs.

### Member 4: evaluation and interpretation

- Implement study-level aggregation and metrics.
- Select the decision threshold using validation data only.
- Produce confusion matrix, ROC/PR results, ablations, error analysis, and Grad-CAM examples.

Deliverables: evaluation tables, aggregate figures, and analysis notes.

### Member 5: integration and reproducibility

- Maintain the repository contracts and team instructions.
- Implement inference and the final `run_all.py` entry point.
- Finalize pinned requirements after the GPU audit.
- Verify a clean-clone run, latency, model size, demo, report integration, and release package.

Deliverables: reproducible end-to-end command, inference output, final release, and submission QA.

## Review chain

1. Member 2 reviews Member 1.
2. Member 3 reviews Member 2.
3. Member 4 reviews Member 3.
4. Member 5 reviews Member 4.
5. Member 1 reviews Member 5.

At least one approval is required before merge.

## Integration gates

### Gate 1: repository and data contract

- Skeleton is on `main`.
- Credentials and raw data are ignored.
- Dataset location is environment-based.
- Roles and PR rules are understood.

### Gate 2: split freeze

- Audit is complete.
- Patient overlap is zero.
- Manifest schema is valid.
- Split seed and `split_v1` are recorded.

No member may create a personal alternative split after this gate.

### Gate 3: smoke tests

- One batch loads correctly.
- Image and label shapes match the contract.
- Baseline and DenseNet forward passes work.
- A small subset can be intentionally overfit.

### Gate 4: full experiments

- Runs use registered configs and commit SHAs.
- Checkpoints and logs are stored outside Git.
- Only validation results are used for model selection.

### Gate 5: final evaluation and release

- Model and threshold are frozen.
- Locked test is evaluated once for the final comparison.
- A clean clone can reproduce inference.
- Report, presentation, and repository contain no secrets or patient data.

## Daily status format

Each member reports:

1. Completed result and PR/commit link
2. Evidence produced
3. Next measurable result
4. GPU time needed
5. Blocker, if any

Avoid percentage-only updates such as "80% complete" without evidence.

## Artifact contract

Each experiment directory should contain:

```text
<run_id>/
|-- config.yaml
|-- metrics.json
|-- history.csv
|-- train.log
`-- predictions_val.csv
```

Large run directories remain outside Git. Register every meaningful run in `docs/experiment_registry.csv`.
