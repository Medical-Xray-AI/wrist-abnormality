# Decision log

Record decisions that affect more than one project component. Do not silently change a shared contract in implementation code.

| Date | Decision | Rationale | Status |
|---|---|---|---|
| 2026-09-03 | Use the `XR_WRIST` subset of MURA. | It supports an interesting musculoskeletal abnormality task with patient and study structure. | Accepted |
| 2026-09-03 | Define the task as normal versus abnormal, not fracture diagnosis. | MURA supplies study-level normal/abnormal labels and does not provide reliable abnormality subtypes. | Accepted |
| 2026-09-03 | Split development data at patient level. | Keeping every study and image from a patient in one split prevents identity leakage. | Accepted |
| 2026-09-03 | Use official train for development and reserve official valid as the locked final test. | Model and threshold selection must remain separate from final evaluation. | Accepted |
| 2026-09-03 | Compare a custom CNN with pretrained DenseNet121. | This satisfies the baseline-versus-transfer-learning comparison while fitting the available compute budget. | Accepted |
| 2026-09-03 | Start at 224 x 224, preserve aspect ratio, pad, and replicate grayscale to three channels for DenseNet. | This is a compute-efficient starting point compatible with ImageNet-pretrained weights. | Accepted |
| 2026-09-03 | Use study-level mean probability across views. | MURA labels are study-level and a study may contain multiple images. | Accepted |
| 2026-09-03 | Use study-level Macro F1 as the primary metric and abnormal sensitivity as the clinical metric. | Macro F1 treats both classes explicitly; sensitivity exposes abnormal false negatives. | Accepted |
| 2026-09-03 | Select the classification threshold on validation data only. | Test-driven threshold tuning would leak final evaluation information. | Accepted |

## Proposed changes

For a new decision, add a row with status `Proposed` and explain supporting evidence in the related pull request. Change it to `Accepted` only after team review.
