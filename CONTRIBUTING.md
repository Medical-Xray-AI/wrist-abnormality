# Contributing

This repository is shared by a five-person project team. Keep changes small, reproducible, and reviewable.

## Initial setup

1. Clone the repository.
2. Copy `.env.example` to `.env`.
3. Set `XRAY_DATA_ROOT` and `XRAY_OUTPUT_ROOT` for the current machine or GPU workspace.
4. Do not commit `.env`, VPN files, Kaggle credentials, datasets, or model checkpoints.

Dependency versions in `requirements.txt` are provisional until the GPU environment audit is complete. Record the working Python, CUDA, PyTorch, and torchvision versions before pinning them.

## Branches

Do not develop directly on `main`. Suggested branches are:

- `feature/data-audit`
- `feature/baseline-cnn`
- `feature/densenet-training`
- `feature/evaluation`
- `feature/inference-repro`

Use additional short-lived branches when a task needs to be split further.

## Pull requests

Every pull request must:

- Explain the change and its scope.
- Include exact verification commands.
- Identify the config, seed, split version, and commit SHA for experiments.
- Receive at least one teammate review before merge.
- Avoid unrelated formatting or refactoring.

Direct pushes, force pushes, and branch deletion on `main` should be disabled in GitHub branch protection after the initial repository bootstrap.

## Commit messages

Use concise, action-oriented messages, for example:

- `Add leakage-aware manifest generator`
- `Implement baseline CNN training`
- `Report image-level validation metrics`

## Data and security

The repository may contain relative manifests and aggregate statistics, but must not contain:

- Raw or processed chest X-ray images
- Patient-identifiable information
- Dataset archives
- Model checkpoints
- Absolute machine-specific paths
- WireGuard configurations, private keys, Jupyter tokens, or Kaggle credentials

Immediately notify the team lead if a secret is committed. Removing it in a later commit is not sufficient because it remains in Git history.

## Experiment records

Each meaningful run must be recorded in `docs/experiment_registry.csv`. Store large artifacts outside Git and reference their shared path in the registry.

Do not evaluate the locked final test set until the team has selected the final model and decision threshold using development data only.

## Review chain

- Data work: reviewed by the baseline owner
- Baseline work: reviewed by the pretrained-model owner
- Pretrained-model work: reviewed by the evaluation owner
- Evaluation work: reviewed by the inference/reproducibility owner
- Inference/reproducibility work: reviewed by the data owner
