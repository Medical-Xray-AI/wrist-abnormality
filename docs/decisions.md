# Decision log

Record decisions that affect more than one project component. Do not silently change a shared contract in implementation code.

## Current decisions

| Date | Decision | Rationale | Status |
|---|---|---|---|
| 2026-09-05 | Use the Kermany pediatric chest X-ray dataset distributed as `paultimothymooney/chest-xray-pneumonia`. | It directly matches the required pneumonia-versus-normal chest X-ray task and is practical for the available time and compute. | Accepted |
| 2026-09-05 | Define the target as image-level `NORMAL` versus `PNEUMONIA`. | The selected distribution provides image folders and binary labels, not reliable study groupings. | Accepted |
| 2026-09-05 | Treat bacterial/viral filename information as audit metadata, not as the target. | The project remains a binary pneumonia detection task. | Accepted |
| 2026-09-05 | Do not use the provided 16-image validation folder as final validation. | It is too small for stable model, early-stopping, or threshold selection. | Accepted |
| 2026-09-05 | Create `split_v1` at patient level, using duplicate groups as a fallback when patient identity is uncertain. | This reduces identity and duplicate leakage. | Accepted |
| 2026-09-05 | Retain the provided test folder only after confirming no patient or duplicate overlap. | A contaminated test split would overestimate generalization. | Accepted |
| 2026-09-05 | Compare a custom CNN with pretrained DenseNet121. | This satisfies the baseline-versus-transfer-learning comparison while fitting the available compute budget. | Accepted |
| 2026-09-05 | Start at 224 x 224, preserve aspect ratio, pad, and replicate grayscale to three channels. | This is a compute-efficient starting point compatible with ImageNet-pretrained weights. | Accepted |
| 2026-09-05 | Use image-level Macro F1 as the primary metric and pneumonia sensitivity as the clinical metric. | Macro F1 exposes both imbalanced classes; sensitivity exposes pneumonia false negatives. | Accepted |
| 2026-09-05 | Select the classification threshold on validation data only. | Test-driven threshold tuning would leak final evaluation information. | Accepted |

## Superseded decisions

| Date | Previous decision | Reason superseded | Status |
|---|---|---|---|
| 2026-09-03 | Use the `XR_WRIST` subset of MURA for study-level abnormality classification. | The team switched datasets before model development to align directly with the original pneumonia project brief. | Superseded |
| 2026-09-03 | Aggregate multiple wrist views by study-level mean probability. | The selected pneumonia distribution is evaluated per chest X-ray image and has no equivalent study contract. | Superseded |

## Proposed changes

For a new decision, add a row with status `Proposed` and explain supporting evidence in the related pull request. Change it to `Accepted` only after team review.
