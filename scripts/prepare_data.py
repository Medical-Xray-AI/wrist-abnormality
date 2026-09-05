"""Download, audit, split, and verify the dataset for split_v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from src.data.audit_data import audit_dataset  # noqa: E402
from src.data.download import ensure_local_dataset, update_env_data_root  # noqa: E402
from src.data.split_data import create_manifests  # noqa: E402
from src.data.verify import verify_local_dataset  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--download-dir",
        type=Path,
        default=REPOSITORY_ROOT / "data" / "raw" / "kaggle",
    )
    parser.add_argument("--data-root", type=Path, default=None)
    parser.add_argument(
        "--audit-dir",
        type=Path,
        default=REPOSITORY_ROOT / "docs" / "data_audit",
    )
    parser.add_argument(
        "--manifest-dir",
        type=Path,
        default=REPOSITORY_ROOT / "data" / "manifests",
    )
    parser.add_argument("--near-threshold", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root, downloaded_now = ensure_local_dataset(
        download_dir=args.download_dir,
        data_root=args.data_root,
    )
    env_path = update_env_data_root(root, REPOSITORY_ROOT / ".env")
    audit = audit_dataset(root, args.audit_dir, near_threshold=args.near_threshold)
    split = create_manifests(
        args.audit_dir / "file_manifest.csv",
        args.manifest_dir,
        seed=args.seed,
        validation_fraction=0.15,
        rebuild_ratios=(0.70, 0.15, 0.15),
        version="split_v1",
    )
    verification = verify_local_dataset(
        root,
        manifest_dir=args.manifest_dir,
        full_hash_check=False,
        require_manifests=True,
    )
    print(
        json.dumps(
            {
                "dataset_root": str(root),
                "downloaded_now": downloaded_now,
                "env_file_updated": str(env_path),
                "audit": audit,
                "split": split,
                "verification": verification,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
