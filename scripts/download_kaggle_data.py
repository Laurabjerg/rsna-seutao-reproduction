#!/usr/bin/env python
"""
Download RSNA Intracranial Hemorrhage Detection dataset via kagglehub.

Requires:
  pip install kagglehub
  Kaggle credentials set up (KAGGLE_USERNAME + KAGGLE_KEY env vars, or ~/.kaggle/kaggle.json)

Creates symlinks from the kagglehub cache into data/rsna_raw/ so the pipeline
can find stage_1_train_images, stage_1_test_images, stage_2_test_images.
"""

import os
import sys
from pathlib import Path

try:
    import kagglehub
except ImportError:
    print("kagglehub ikke installeret. Kør: pip install kagglehub", file=sys.stderr)
    sys.exit(1)


def main():
    project_root = Path(os.environ.get("PROJECT_ROOT", ".")).resolve()
    raw_dir = project_root / "data" / "rsna_raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    print("=== Downloader RSNA dataset via kagglehub ===")
    print("(Dette kan tage lang tid ved første kørsel)")
    dataset_path = kagglehub.competition_download("rsna-intracranial-hemorrhage-detection")
    dataset_path = Path(dataset_path)
    print(f"Dataset hentet til: {dataset_path}")

    # kagglehub returnerer roden af det downloadede datasæt.
    # Vi forventer undermapper: stage_1_train_images, stage_1_test_images, stage_2_test_images
    expected_dirs = [
        "stage_1_train_images",
        "stage_1_test_images",
        "stage_2_test_images",
    ]

    for dirname in expected_dirs:
        src = dataset_path / dirname
        dst = raw_dir / dirname
        if dst.exists() or dst.is_symlink():
            print(f"  [skip] {dst} findes allerede")
            continue
        if src.exists():
            os.symlink(src, dst)
            print(f"  [link] {src} -> {dst}")
        else:
            # Prøv at finde mappen i undermapper
            matches = list(dataset_path.rglob(dirname))
            if matches:
                os.symlink(matches[0], dst)
                print(f"  [link] {matches[0]} -> {dst}")
            else:
                print(f"  [WARN] Kunne ikke finde {dirname} i {dataset_path}")
                print(f"         Indhold: {list(dataset_path.iterdir())}")

    # Kopiér også CSV-filer hvis de ligger i roden
    for csv_name in ["stage_1_train.csv", "stage_2_train.csv", "stage_2_sample_submission.csv"]:
        src = dataset_path / csv_name
        dst = raw_dir / csv_name
        if dst.exists() or dst.is_symlink():
            continue
        if src.exists():
            os.symlink(src, dst)
            print(f"  [link] {src} -> {dst}")
        else:
            matches = list(dataset_path.rglob(csv_name))
            if matches:
                os.symlink(matches[0], dst)

    print("Kaggle data klar.")


if __name__ == "__main__":
    main()
