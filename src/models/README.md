# Model module contract

This package contains the custom CNN baseline and pretrained DenseNet121 for pediatric pneumonia classification.

Planned modules:

- `baseline.py` - small CNN baseline
- `densenet.py` - pretrained DenseNet121 with a binary head
- `factory.py` - config-driven model construction

Model contract:

- Input shape: `[batch, 3, 224, 224]`
- Output shape: `[batch]` or `[batch, 1]` containing pneumonia logits
- Target mapping: normal `0`, pneumonia `1`
- Training loss: weighted binary cross-entropy with logits
- Sigmoid is applied only when probabilities are required
- Checkpoint paths and pretrained downloads must not be committed

Architecture or input-contract changes require an update to the relevant config and decision log.
