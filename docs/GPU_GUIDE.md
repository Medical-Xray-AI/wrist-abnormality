# GPU usage guide

## Security first

- Receive VPN and Jupyter access details only through the approved private channel.
- Never paste private keys or tokens into GitHub issues, pull requests, notebooks, screenshots, or chat messages.
- Keep WireGuard configuration files outside this repository.
- Do not commit the access instruction document.
- If one WireGuard identity was provided for the whole team, do not use it concurrently on several devices unless the administrator confirms that this is supported. Prefer separate member configurations or a team schedule.

## Connecting

1. Install WireGuard from its official source.
2. Import the configuration supplied by the administrator.
3. Activate the tunnel.
4. Open the private JupyterLab address supplied by the administrator.
5. Enter the supplied token only in the Jupyter authentication page.

Do not copy secret connection values into this guide.

## First environment audit

Run these commands in a JupyterLab terminal before installing or upgrading packages:

```bash
nvidia-smi
python --version
python -c "import torch; print('torch:', torch.__version__); print('cuda runtime:', torch.version.cuda); print('cuda available:', torch.cuda.is_available()); print('device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
python -c "import torchvision; print('torchvision:', torchvision.__version__)"
```

Record the results in a team note. Do not replace the server's PyTorch installation until compatibility has been checked.

## Shared storage convention

Keep one shared extracted copy of MURA on the GPU server. Point each working copy to it using a private `.env` file:

```env
XRAY_DATA_ROOT=/path/provided/by/admin/MURA-v1.1
XRAY_OUTPUT_ROOT=/path/provided/by/admin/team5_outputs
XRAY_NUM_WORKERS=4
```

Use relative paths inside manifests. Do not place raw data or outputs inside the Git repository.

## Running experiments

Before a run:

1. Pull the reviewed code.
2. Record the commit SHA with `git rev-parse HEAD`.
3. Choose a committed config and seed.
4. Create a unique run ID such as `20260904_member3_densenet_s42`.
5. Add the planned run to `docs/experiment_registry.csv`.
6. Check GPU availability with `nvidia-smi`.

During a run:

- Run only one full training job at a time unless the team has confirmed sufficient memory.
- Use mixed precision when supported.
- Save checkpoints frequently enough to resume after interruption.
- Monitor GPU memory; do not occupy the GPU with abandoned notebooks.

After a run:

- Save config, metrics, history, logs, and validation predictions in the run directory.
- Update the experiment registry.
- Stop unused kernels and processes.
- Commit only code, configuration, aggregate metrics, and small safe figures.

## Troubleshooting

- `torch.cuda.is_available()` is false: confirm the GPU kernel/environment and compare the installed PyTorch build with the server CUDA setup.
- Out-of-memory error: stop duplicate kernels, reduce batch size, then record the change in the run notes.
- Disconnected session: resume from the most recent checkpoint instead of restarting without a record.
- Cannot reach JupyterLab: verify the WireGuard tunnel, then contact the administrator without sharing secrets publicly.
