import argparse
from pathlib import Path
import pandas as pd
import cv2
from tqdm import tqdm

def build_concat(df: pd.DataFrame, png_dir: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    for study, sdf in tqdm(df.groupby("study_instance_uid"), desc=f"build {out_dir.name}"):
        sdf = sdf.copy()
        sdf["slice_num"] = sdf["slice_id"].astype(str).str.split("_").str[-1].astype(int)
        sdf = sdf.sort_values("slice_num").reset_index(drop=True)

        files = sdf["filename"].tolist()
        for i, fname in enumerate(files):
            prev_f = files[i - 1] if i > 0 else fname
            next_f = files[i + 1] if i < len(files) - 1 else fname

            img_prev = cv2.imread(str(png_dir / prev_f), 0)
            img_cur = cv2.imread(str(png_dir / fname), 0)
            img_next = cv2.imread(str(png_dir / next_f), 0)

            if img_prev is None or img_cur is None or img_next is None:
                raise FileNotFoundError(f"Mangler PNG omkring {fname}")

            img_prev = cv2.resize(img_prev, (512, 512))
            img_cur = cv2.resize(img_cur, (512, 512))
            img_next = cv2.resize(img_next, (512, 512))

            merged = cv2.merge([img_prev, img_cur, img_next])
            merged = cv2.resize(merged, (256, 256))
            cv2.imwrite(str(out_dir / fname), merged)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    stage1_csv = repo_root / "2DNet" / "data" / "stage1_train_cls.csv"
    stage2_csv = repo_root / "2DNet" / "data" / "stage2_test_cls.csv"

    train_png = repo_root / "2DNet" / "train_png"
    test_png = repo_root / "2DNet" / "test_png"

    train_out = repo_root / "2DNet" / "train_concat_3images_256"
    test_out = repo_root / "2DNet" / "stage2_test_concat_3images"

    df1 = pd.read_csv(stage1_csv)
    df2 = pd.read_csv(stage2_csv)

    build_concat(df1, train_png, train_out)
    build_concat(df2, test_png, test_out)

if __name__ == "__main__":
    main()