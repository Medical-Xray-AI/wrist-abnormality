"""Verify the local dataset and the team's frozen manifests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from src.data.common import resolve_dataset_root  # noqa: E402
from src.data.verify import verify_local_dataset  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=None, help="Defaults to XRAY_DATA_ROOT")
    parser.add_argument(
        "--manifest-dir",
        type=Path,
        default=REPOSITORY_ROOT / "data" / "manifests",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Check paths and leakage metadata without recomputing every SHA-256 hash.",
    )
    parser.add_argument(
        "--require-manifests",
        action="store_true",
        help="Fail if train/validation/test manifests have not been frozen yet.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = resolve_dataset_root(args.data_root)
    result = verify_local_dataset(
        root,
        manifest_dir=args.manifest_dir,
        full_hash_check=not args.quick,
        require_manifests=args.require_manifests,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
