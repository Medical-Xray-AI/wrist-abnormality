# Data manifests

The data owner will generate:

- `train.csv`
- `validation.csv`
- `test.csv`

Each row represents one X-ray image.

## Required columns

| Column | Description |
|---|---|
| `image_path` | Path relative to `XRAY_DATA_ROOT` |
| `patient_id` | Patient identifier parsed from the MURA path |
| `study_id` | Study identifier |
| `study_uid` | Unique patient and study combination |
| `body_part` | Must be `XR_WRIST` |
| `label` | `0` for normal and `1` for abnormal |
| `split` | `train`, `validation`, or `test` |
| `source_split` | `official_train` or `official_valid` |

## Example

```csv
image_path,patient_id,study_id,study_uid,body_part,label,split,source_split
train/XR_WRIST/patient00001/study1_positive/image1.png,patient00001,study1,patient00001_study1,XR_WRIST,1,train,official_train
```

## Leakage checks

Before training, verify that:

- Patient IDs do not overlap between splits.
- Study IDs do not cross splits.
- Duplicate images do not cross splits.
- Every image path exists.
- Labels agree with the original MURA study labels.

Model evaluation is performed at study level by averaging the image probabilities belonging to the same `study_uid`.
