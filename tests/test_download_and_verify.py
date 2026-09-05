from __future__ import annotations

import shutil
from pathlib import Path

from src.data.audit_data import audit_dataset
from src.data.download import (
    DATASET_HANDLE,
    ensure_local_dataset,
    locate_dataset_root,
    update_env_data_root,
    validate_dataset_inventory,
)
from src.data.split_data import create_manifests
from src.data.verify import verify_local_dataset


FIXTURE_COUNTS = {
    ("train", "NORMAL"): 4,
    ("train", "PNEUMONIA"): 4,
    ("val", "NORMAL"): 2,
    ("val", "PNEUMONIA"): 2,
    ("test", "NORMAL"): 2,
    ("test", "PNEUMONIA"): 2,
}


def test_existing_local_dataset_is_reused_without_download(
    dataset_root: Path,
    monkeypatch,
) -> None:
    monkeypatch.delenv("XRAY_DATA_ROOT", raising=False)

    def fail_downloader(handle: str, output_dir: str) -> str:
        raise AssertionError("Downloader must not run for a valid existing dataset")

    root, downloaded_now = ensure_local_dataset(
        data_root=dataset_root,
        expected_counts=FIXTURE_COUNTS,
        downloader=fail_downloader,
    )
    assert root == dataset_root.resolve()
    assert downloaded_now is False
    assert (root / ".dataset_source.json").is_file()


def test_download_branch_uses_pinned_handle_and_validates_result(
    dataset_root: Path,
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.delenv("XRAY_DATA_ROOT", raising=False)
    destination = tmp_path / "download"
    calls: list[tuple[str, str]] = []

    def fake_downloader(handle: str, output_dir: str) -> str:
        calls.append((handle, output_dir))
        copied = Path(output_dir) / "chest_xray"
        shutil.copytree(dataset_root, copied)
        return str(Path(output_dir))

    root, downloaded_now = ensure_local_dataset(
        download_dir=destination,
        expected_counts=FIXTURE_COUNTS,
        downloader=fake_downloader,
    )
    assert downloaded_now is True
    assert calls == [(DATASET_HANDLE, str(destination.resolve()))]
    assert root == (destination / "chest_xray").resolve()
    assert sum(validate_dataset_inventory(root, FIXTURE_COUNTS).values()) == 16


def test_locator_prefers_canonical_root_over_nested_and_macos_copies(
    dataset_root: Path,
    tmp_path: Path,
) -> None:
    destination = tmp_path / "download" / "chest_xray"
    shutil.copytree(dataset_root, destination)
    shutil.copytree(dataset_root, destination / "chest_xray")
    shutil.copytree(dataset_root, destination / "__MACOSX" / "chest_xray")

    assert locate_dataset_root(destination.parent, FIXTURE_COUNTS) == destination.resolve()


def test_env_update_preserves_other_settings(dataset_root: Path, tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "XRAY_OUTPUT_ROOT=outputs\nXRAY_DATA_ROOT=C:/old/path\nXRAY_NUM_WORKERS=4\n",
        encoding="utf-8",
    )
    update_env_data_root(dataset_root, env_file)
    content = env_file.read_text(encoding="utf-8")
    assert content.count("XRAY_DATA_ROOT=") == 1
    assert dataset_root.resolve().as_posix() in content
    assert "XRAY_OUTPUT_ROOT=outputs" in content
    assert "XRAY_NUM_WORKERS=4" in content


def test_frozen_manifests_match_every_local_image_and_hash(
    dataset_root: Path,
    tmp_path: Path,
) -> None:
    audit_dir = tmp_path / "audit"
    manifest_dir = tmp_path / "manifests"
    audit_dataset(dataset_root, audit_dir, near_threshold=0)
    create_manifests(audit_dir / "file_manifest.csv", manifest_dir, seed=42)
    result = verify_local_dataset(
        dataset_root,
        manifest_dir=manifest_dir,
        full_hash_check=True,
        require_manifests=True,
        expected_counts=FIXTURE_COUNTS,
    )
    assert result["image_count"] == 16
    assert result["manifests_verified"] is True
    assert result["manifest_verification"]["hash_mismatches"] == 0
