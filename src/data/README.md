# Data module contract

This package owns dataset discovery, auditing, leakage-aware splitting, preprocessing, and PyTorch data loading for the pediatric pneumonia task.

Planned modules:

- `audit.py` - class counts, path validation, corrupt-image checks, hashes, and duplicate checks
- `split.py` - deterministic patient/group-level train, validation, and test manifests
- `dataset.py` - image loading and sample metadata
- `transforms.py` - resize/padding, normalization, and conservative augmentation

Each dataset sample should expose at least:

```text
image
label
patient_id
group_id
image_path
source_split
pneumonia_subtype
```

Rules:

- Read the dataset root from `XRAY_DATA_ROOT`.
- Use paths relative to that root in committed manifests.
- Keep every patient or duplicate group in exactly one split.
- Apply stochastic augmentation to training data only.
- Preserve subtype and source-folder metadata for auditing, not as binary targets.
- Do not use the locked test set for preprocessing statistics, threshold selection, or model selection.
