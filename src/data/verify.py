"""Verify a local dataset copy and, when present, the frozen manifests."""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import pandas as pd

from .common import CANONICAL_COLUMNS, relative_posix, resolve_image_path, sha256_file
from .download import EXPECTED_COUNTS, list_dataset_images, validate_dataset_inventory


SOURCE_TO_FOLDER = {
    "provided_train": "train",
    "provided_val": "val",
    "provided_test": "test",
}
LABEL_TO_FOLDER = {0: "NORMAL", 1: "PNEUMONIA"}


def _cross_split_count(frame: pd.DataFrame, column: str) -> int:
    known = frame.loc[frame[column].astype(str).str.strip() != ""]
    return int((known.groupby(column)["split"].nunique() > 1).sum())


def verify_frozen_manifests(
    root: str | Path,
    manifest_dir: str | Path,
    full_hash_check: bool = True,
) -> dict[str, Any]:
    resolved_root = Path(root).resolve()
    directory = Path(manifest_dir)
    frames: list[pd.DataFrame] = []
    for split_name in ("train", "validation", "test"):
        path = directory / f"{split_name}.csv"
        if not path.is_file():
            raise FileNotFoundError(f"Missing frozen manifest: {path}")
        frame = pd.read_csv(path, keep_default_na=False)
        missing = sorted(set(CANONICAL_COLUMNS) - set(frame.columns))
        if missing:
            raise ValueError(f"{path} is missing columns: {missing}")
        if set(frame["split"]) != {split_name}:
            raise ValueError(f"{path} contains rows assigned to another split")
        frames.append(frame[CANONICAL_COLUMNS])

    combined = pd.concat(frames, ignore_index=True)
    combined["label"] = pd.to_numeric(combined["label"], errors="raise").astype(int)
    if combined["image_path"].duplicated().any():
        raise ValueError("Frozen manifests contain duplicate image_path rows")

    manifest_paths: set[str] = set()
    hash_mismatches: list[str] = []
    for row in combined.itertuples(index=False):
        relative = str(row.image_path)
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts:
            raise ValueError(f"Unsafe or non-portable image_path: {relative}")
        image_path = resolve_image_path(resolved_root, relative)
        if not image_path.is_file():
            raise FileNotFoundError(f"Manifest image does not exist: {relative}")
        if len(pure.parts) < 3:
            raise ValueError(f"Unexpected dataset path structure: {relative}")
        expected_source_folder = SOURCE_TO_FOLDER.get(str(row.source_split))
        if pure.parts[0] != expected_source_folder:
            raise ValueError(f"source_split disagrees with image_path: {relative}")
        if pure.parts[1].upper() != LABEL_TO_FOLDER[int(row.label)]:
            raise ValueError(f"label disagrees with image folder: {relative}")
        if full_hash_check and sha256_file(image_path) != str(row.sha256):
            hash_mismatches.append(relative)
        manifest_paths.add(relative)

    if hash_mismatches:
        raise ValueError(f"Image hash mismatches: {hash_mismatches[:5]}")
    local_paths = {relative_posix(path, resolved_root) for path in list_dataset_images(resolved_root)}
    if manifest_paths != local_paths:
        missing_from_manifests = sorted(local_paths - manifest_paths)[:5]
        missing_locally = sorted(manifest_paths - local_paths)[:5]
        raise ValueError(
            "Frozen manifests and local dataset differ; "
            f"unlisted local examples={missing_from_manifests}, missing local examples={missing_locally}"
        )

    leakage = {
        "group_overlap": _cross_split_count(combined, "group_id"),
        "patient_overlap": _cross_split_count(combined, "patient_id"),
        "sha256_overlap": _cross_split_count(combined, "sha256"),
    }
    if any(leakage.values()):
        raise ValueError(f"Frozen manifest leakage checks failed: {leakage}")
    return {
        "manifest_rows": int(len(combined)),
        "full_hash_check": bool(full_hash_check),
        "hash_mismatches": 0,
        "leakage": leakage,
    }


def verify_local_dataset(
    root: str | Path,
    manifest_dir: str | Path | None = None,
    full_hash_check: bool = True,
    require_manifests: bool = False,
    expected_counts: Mapping[tuple[str, str], int] = EXPECTED_COUNTS,
) -> dict[str, Any]:
    inventory = validate_dataset_inventory(root, expected_counts)
    result: dict[str, Any] = {
        "dataset_root": "<XRAY_DATA_ROOT>",
        "image_count": int(sum(inventory.values())),
        "inventory": {
            f"{split}/{label}": count for (split, label), count in sorted(inventory.items())
        },
        "manifests_verified": False,
    }
    if manifest_dir is not None:
        directory = Path(manifest_dir)
        available = all((directory / f"{name}.csv").is_file() for name in ("train", "validation", "test"))
        if available:
            result["manifest_verification"] = verify_frozen_manifests(
                root,
                directory,
                full_hash_check=full_hash_check,
            )
            result["manifests_verified"] = True
        elif require_manifests:
            raise FileNotFoundError(f"Frozen manifests are not complete below {directory}")
    return result
