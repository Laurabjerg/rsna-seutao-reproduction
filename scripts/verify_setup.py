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

required_keys = [
    "SEUTAO_REPO_DIR",
    "DOWNLOAD_DIR",
    "PRETRAIN_DIR",
    "AUX_DATA_DIR",
    "RSNA_STAGE1_TRAIN_DIR",
    "RSNA_STAGE1_TEST_DIR",
    "RSNA_STAGE2_TEST_DIR",
]

for key in required_keys:
    if key not in env or not env[key]:
        raise RuntimeError(f"Mangler env-var i config.env: {key}")

required_paths = [
    Path(env["SEUTAO_REPO_DIR"]),
    Path(env["RSNA_STAGE1_TRAIN_DIR"]),
    Path(env["RSNA_STAGE1_TEST_DIR"]),
    Path(env["RSNA_STAGE2_TEST_DIR"]),
]

for p in required_paths:
    if not p.exists():
        raise FileNotFoundError(f"Mangler path: {p}")

repo_dir = Path(env["SEUTAO_REPO_DIR"])
must_exist = [
    repo_dir / "2DNet" / "src" / "prepare_data.py",
    repo_dir / "2DNet" / "src" / "predict.py",
    repo_dir / "SequenceModel" / "main.py",
]
for p in must_exist:
    if not p.exists():
        raise FileNotFoundError(f"Mangler repo-fil: {p}")

aux_dir = Path(env["AUX_DATA_DIR"])
pre_dir = Path(env["PRETRAIN_DIR"])

expected_downloads = [
    aux_dir / "data.zip",
    aux_dir / "csv.zip",
    pre_dir / "densenet121_512",
    pre_dir / "densenet169_256",
    pre_dir / "seresnext101_256",
]
for p in expected_downloads:
    if not p.exists():
        raise FileNotFoundError(f"Mangler forventet download: {p}")

try:
    import torch
    print(f"torch ok: {torch.__version__}")
    print(f"cuda available: {torch.cuda.is_available()}")
except Exception as e:
    raise RuntimeError(f"Torch import fejlede: {e}")

print("Alle setup-tjek er bestået.")