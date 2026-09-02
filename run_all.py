"""Future end-to-end entry point for the wrist abnormality pipeline.

The executable contract is created during repository bootstrap. Training,
evaluation, and inference stages will be connected here after their reviewed
modules are merged.
"""

from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_CONFIG = Path("configs/densenet121.yaml")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser without importing training dependencies."""
    parser = argparse.ArgumentParser(
        description="Run the wrist X-ray abnormality pipeline."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Experiment configuration path (default: configs/densenet121.yaml).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check that the selected config exists without starting a run.",
    )
    return parser


def main() -> int:
    """Validate the current skeleton contract or report pending integration."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.config.is_file():
        parser.error(f"Config file not found: {args.config}")

    if args.check:
        print(f"Configuration found: {args.config}")
        print("Repository entry-point check passed.")
        return 0

    parser.error(
        "The end-to-end pipeline has not been integrated yet. "
        "Use --check to verify the repository skeleton."
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
