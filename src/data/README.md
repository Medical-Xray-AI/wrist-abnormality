# Data module contract

This package will own dataset discovery, manifest generation, patient-level splitting, preprocessing, and PyTorch data loading.

Planned modules:

- `audit.py` - dataset counts, path validation, corrupt-image checks, and duplicate checks
- `split.py` - deterministic patient-level train/validation manifests
- `dataset.py` - image loading and sample metadata
- `transforms.py` - resize/padding, normalization, and conservative augmentation

Each dataset sample should expose at least:

```text
image
label
patient_id
study_uid
image_path
```

Rules:

- Read the dataset root from `XRAY_DATA_ROOT`.
- Use paths relative to that root in committed manifests.
- Keep every patient in exactly one split.
- Apply stochastic augmentation to training data only.
- Preserve enough metadata for study-level aggregation.
