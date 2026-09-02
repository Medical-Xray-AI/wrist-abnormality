# Data

This repository does not contain raw or processed medical images.

## Dataset

The project uses the wrist subset of MURA:

- Dataset version: MURA-v1.1
- Body part: `XR_WRIST`
- Labels: `normal` and `abnormal`
- Task: Binary classification

Official source:
https://stanfordmlgroup.github.io/competitions/mura/

## Expected dataset structure

The directory referenced by `XRAY_DATA_ROOT` should contain:

```text
MURA-v1.1/
|-- train/
|-- valid/
|-- train_image_paths.csv
|-- train_labeled_studies.csv
|-- valid_image_paths.csv
`-- valid_labeled_studies.csv
```

## Local configuration

Each team member must copy `.env.example` as `.env` and set:

```env
XRAY_DATA_ROOT=C:/path/to/MURA-v1.1
```

The `.env` file must never be committed.

## Split policy

- Only `XR_WRIST` images are used.
- The official training set is divided into internal train and validation sets.
- The internal division must be performed at patient level.
- All images and studies belonging to one patient must remain in the same split.
- The official validation set is reserved as the locked final test set.
- Final test data must not be used for model or threshold selection.

## Repository policy

Allowed in Git:

- Relative-path manifests
- Dataset statistics
- Data audit reports
- Small aggregate plots without patient information

Not allowed in Git:

- X-ray images
- Archives containing the dataset
- Absolute local paths
- Patient-identifiable information
