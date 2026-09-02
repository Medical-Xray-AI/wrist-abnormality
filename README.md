\# Wrist X-ray Abnormality Classification



A deep-learning project for classifying wrist X-ray studies as normal or abnormal using the MURA dataset.



\## Project objective



The project compares:



\- A custom CNN baseline

\- A pretrained DenseNet121 model



The final prediction is produced at study level by aggregating predictions from all images belonging to the same study.



\## Dataset



\- Dataset: MURA

\- Body part: Wrist (`XR\_WRIST`)

\- Task: Binary classification (`normal` / `abnormal`)

\- Split strategy: Patient-level split

\- Raw dataset files are not stored in this repository.



Official dataset source:

https://stanfordmlgroup.github.io/competitions/mura/



\## Evaluation



Primary metric:



\- Macro F1 score



Additional metrics:



\- Abnormal sensitivity

\- Specificity

\- ROC-AUC

\- PR-AUC

\- Cohen's kappa

\- Confusion matrix



\## Planned model configuration



\- Main model: Pretrained DenseNet121

\- Input size: 224 × 224

\- Input channels: Grayscale converted to 3 channels

\- Study aggregation: Mean probability

\- Validation threshold: Selected using validation data only



\## Repository structure



\- `configs/` — experiment configurations

\- `data/` — data documentation and manifests

\- `docs/` — team and GPU instructions

\- `scripts/` — utility scripts

\- `src/data/` — dataset and preprocessing code

\- `src/models/` — model definitions

\- `tests/` — automated tests

\- `report/` — report-related files

\- `presentation/` — presentation-related files



\## Data policy



Do not commit:



\- Raw or processed medical images

\- Patient information

\- Model checkpoints

\- GPU/VPN credentials

\- Kaggle credentials

\- Local `.env` files



\## Status



Project setup is currently in progress.

