from pathlib import Path
import os

PROJECT_ROOT = Path(os.getcwd())
config_path = PROJECT_ROOT / "config.env"
if not config_path.exists():
    raise FileNotFoundError("Mangler config.env")

def load_env(path: Path):
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env

def expand(value: str, env: dict) -> str:
    out = value
    for _ in range(10):
        changed = False
        for k, v in env.items():
            token = "${" + k + "}"
            if token in out:
                out = out.replace(token, v)
                changed = True
        if not changed:
            break
    return out

env = load_env(config_path)
env["PROJECT_ROOT"] = str(PROJECT_ROOT)
for k in list(env.keys()):
    env[k] = expand(env[k], env)

repo_dir = Path(env["SEUTAO_REPO_DIR"])

# Patch 2D settings.py
settings_2d = repo_dir / "2DNet" / "src" / "settings.py"
settings_2d.write_text(
    "train_png_dir = r'" + str(repo_dir / "2DNet" / "train_png") + "/'\n"
    "test_png_dir = r'" + str(repo_dir / "2DNet" / "test_png") + "/'\n"
)

# Patch SequenceModel/settings.py
seq_settings = repo_dir / "SequenceModel" / "settings.py"
seq_settings.write_text(
    "csv_root = r'" + str(repo_dir / "SequenceModel" / "csv") + "'\n"
    "feature_path = r'" + str(repo_dir / "SequenceModel" / "features") + "'\n"
    "final_output_path = r'" + str(repo_dir / "FinalSubmission") + "'\n"
)

# Patch hardcoded concat paths in predict.py
predict_py = repo_dir / "2DNet" / "src" / "predict.py"
text = predict_py.read_text()

old_train = "/home1/kaggle_rsna2019/process/train_concat_3images_256/"
old_test = "/home1/kaggle_rsna2019/process/stage2_test_concat_3images/"

new_train = str(repo_dir / "2DNet" / "train_concat_3images_256") + "/"
new_test = str(repo_dir / "2DNet" / "stage2_test_concat_3images") + "/"

text = text.replace(old_train, new_train)
text = text.replace(old_test, new_test)

predict_py.write_text(text)

print("Patchede 2D settings, Sequence settings og predict.py")