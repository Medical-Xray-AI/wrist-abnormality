<div align="center">

# Pediatric Pneumonia Detection from Chest X-rays

**Image-level normal vs. pneumonia classification using the Kermany pediatric chest X-ray dataset**

![Task](https://img.shields.io/badge/task-binary%20classification-4C78A8)
![Dataset](https://img.shields.io/badge/dataset-Kermany%20Pediatric%20CXR-6F4E7C)
![Models](https://img.shields.io/badge/models-CNN%20%7C%20DenseNet121-2E8B57)
![Status](https://img.shields.io/badge/status-in%20development-F2C94C)

</div>

---

## Overview

This project develops a reproducible deep-learning pipeline for classifying a pediatric chest X-ray as **normal** or **pneumonia**. It compares a custom convolutional neural network with an ImageNet-pretrained DenseNet121 under the same leakage-aware evaluation protocol.

> **Scope:** The dataset contains chest radiographs from children aged approximately 1-5 years. Results must not be generalized to adults or other clinical settings without external validation.

## Project at a glance

| Item | Selection |
|---|---|
| Dataset | Kermany pediatric chest X-rays, distributed on Kaggle |
| Source population | Guangzhou Women and Children's Medical Center, ages 1-5 |
| Task | Binary classification: normal / pneumonia |
| Prediction level | Image |
| Baseline | Custom small CNN |
| Main model | Pretrained DenseNet121 |
| Initial input | 224 x 224, aspect ratio preserved and padded |
| Input channels | Grayscale replicated to 3 channels |
| Split unit | Patient ID, with duplicate-group fallback |
| Primary metric | Macro F1 |
| Clinical metric | Pneumonia sensitivity |

## Pipeline

```mermaid
flowchart LR
    A[Kermany pediatric CXR] --> B[Path, label and duplicate audit]
    B --> C[Patient or duplicate groups]
    C --> D[Leakage-aware split]
    D --> E[Resize, pad and normalize]
    E --> F1[Custom CNN]
    E --> F2[DenseNet121]
    F1 --> G[Image probability]
    F2 --> G
    G --> H[Validation-selected threshold]
    H --> I[Image-level evaluation]
```

## Dataset caveats and split policy

The Kaggle archive contains `train`, `val`, and `test` folders, but the provided validation directory contains only 16 images. It is therefore not used as the project's model-selection validation set.

Before training, the data owner must audit patient identifiers, exact hashes, and potential near-duplicates across all provided folders.

Preferred protocol:

1. Combine the provided `train` and `val` folders for development.
2. Create a new patient/group-level internal validation split using seed 42.
3. Keep the provided `test` folder locked only if the audit confirms no patient or duplicate overlap with development data.
4. If overlap is found, pool all images and rebuild train/validation/test at patient or duplicate-group level using the ratios in `configs/data.yaml`.
5. Select the model, early-stopping point, and decision threshold using validation data only.

Reported image-level metrics:

- Macro F1
- Pneumonia sensitivity
- Specificity
- ROC-AUC
- PR-AUC
- Confusion matrix

## Repository structure

```text
.
|-- .github/
|   `-- pull_request_template.md
|-- configs/
|   |-- data.yaml
|   |-- baseline.yaml
|   `-- densenet121.yaml
|-- data/
|   |-- manifests/
|   `-- README.md
|-- docs/
|   |-- TEAM_WORKFLOW.md
|   |-- GPU_GUIDE.md
|   |-- decisions.md
|   `-- experiment_registry.csv
|-- presentation/
|-- report/
|-- scripts/
|-- src/
|   |-- data/
|   `-- models/
|-- tests/
|-- .env.example
|-- .gitignore
|-- CONTRIBUTING.md
|-- requirements.txt
`-- run_all.py
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/Medical-Xray-AI/pneumonia-xray.git
cd pneumonia-xray
```

### 2. Configure local paths

Copy the environment template:

```bash
# Windows CMD
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

Edit `.env` and point it to the extracted `chest_xray` directory and a machine-local or shared output directory:

```env
XRAY_DATA_ROOT=/path/to/chest_xray
XRAY_OUTPUT_ROOT=outputs
XRAY_NUM_WORKERS=4
```

The real `.env` file must remain local and must never be committed.

### 3. Check the GPU environment

Before installing or upgrading PyTorch on the shared GPU server, follow [`docs/GPU_GUIDE.md`](docs/GPU_GUIDE.md). Dependency versions remain provisional until the server's Python, CUDA, PyTorch, and torchvision versions have been audited.

### 4. Verify the repository entry point

```bash
python run_all.py --check
```

The complete training and inference commands will be connected to `run_all.py` as reviewed modules are integrated.

## Dataset

Download the archive outside this Git repository and extract it so that `XRAY_DATA_ROOT` points to:

```text
chest_xray/
|-- train/
|   |-- NORMAL/
|   `-- PNEUMONIA/
|-- val/
|   |-- NORMAL/
|   `-- PNEUMONIA/
`-- test/
    |-- NORMAL/
    `-- PNEUMONIA/
```

Official and distribution resources:

- [Kaggle: Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
- [Original Mendeley Data release](https://data.mendeley.com/datasets/rscbjbr9sj/3)
- [Kermany et al., Cell (2018)](https://doi.org/10.1016/j.cell.2018.02.010)

See [`data/README.md`](data/README.md) for the data policy and [`data/manifests/README.md`](data/manifests/README.md) for the manifest contract.

## Reproducibility

Every meaningful experiment must record:

- Git commit SHA
- Config file and random seed
- Split version
- Device and peak GPU memory
- Training duration and best epoch
- Validation metrics
- External checkpoint location

Runs are tracked in [`docs/experiment_registry.csv`](docs/experiment_registry.csv). Large outputs and checkpoints remain outside Git.

## Team workflow

Development is branch- and pull-request-based. Direct development on `main` is avoided after the initial bootstrap, and each pull request requires at least one teammate review.

- [Team roles and integration gates](docs/TEAM_WORKFLOW.md)
- [Contribution and review rules](CONTRIBUTING.md)
- [Technical decision log](docs/decisions.md)

## Project status

- [x] Repository structure and security rules
- [x] Shared data and experiment configurations
- [x] Team workflow and GPU guidance
- [ ] Dataset audit and leakage-safe manifests
- [ ] Custom CNN baseline
- [ ] DenseNet121 training pipeline
- [ ] Image-level evaluation and interpretation
- [ ] End-to-end inference and clean-clone verification
- [ ] Final report and presentation

## Security and data policy

Do **not** commit raw X-rays, processed datasets, patient information, model checkpoints, `.env` files, VPN configurations, private keys, Jupyter tokens, or Kaggle credentials.

## Disclaimer

This repository is an educational research project. Its outputs are not validated for clinical use and must not be used for medical diagnosis or treatment decisions.
