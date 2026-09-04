# Data manifests

The data owner will generate:

- `train.csv`
- `validation.csv`
- `test.csv`

Each row represents one chest X-ray image.

## Required columns

| Column | Description |
|---|---|
| `image_path` | Path relative to `XRAY_DATA_ROOT` |
| `patient_id` | Patient identifier parsed from the filename when reliable |
| `group_id` | Leakage-control group used for splitting; patient ID or duplicate-cluster fallback |
| `label` | `0` for normal and `1` for pneumonia |
| `pneumonia_subtype` | `normal`, `bacterial`, `viral`, or `unknown`; audit metadata only |
| `split` | `train`, `validation`, or `test` |
| `source_split` | Original Kaggle folder: `provided_train`, `provided_val`, or `provided_test` |
| `sha256` | Exact image-content hash |

## Example

```csv
image_path,patient_id,group_id,label,pneumonia_subtype,split,source_split,sha256
train/NORMAL/IM-0115-0001.jpeg,IM-0115,IM-0115,0,normal,train,provided_train,REPLACE_WITH_REAL_HASH
```

The example row documents the schema only. Generated manifests must contain hashes calculated from the actual files.

## Leakage checks

Before training, verify that:

- `group_id` values do not overlap between splits.
- Inferred patient IDs do not cross split boundaries.
- Exact hashes do not cross split boundaries.
- Near-duplicate images do not cross split boundaries.
- Every relative image path exists below `XRAY_DATA_ROOT`.
- Folder labels and manifest labels agree.
- Every row has exactly one split assignment.

## Prediction level

Evaluation is performed per image. Pneumonia subtype is retained for audit and subgroup error analysis but is not used as the binary training target.
