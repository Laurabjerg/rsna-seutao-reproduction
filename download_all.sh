#!/usr/bin/env bash
set -euo pipefail

if [ ! -f config.env ]; then
  echo "Mangler config.env. Kør: cp config.env.example config.env"
  exit 1
fi

source config.env

mkdir -p "${DOWNLOAD_DIR}" "${PRETRAIN_DIR}" "${AUX_DATA_DIR}" external

if [ ! -d "${SEUTAO_REPO_DIR}" ]; then
  echo "=== Kloner originalrepo ==="
  git clone https://github.com/SeuTao/RSNA2019_Intracranial-Hemorrhage-Detection.git "${SEUTAO_REPO_DIR}"
else
  echo "Originalrepo findes allerede: ${SEUTAO_REPO_DIR}"
fi

echo "RSNA dataset skal allerede være downloadet."
echo "Angiv paths i config.env"

python scripts/download_gdrive.py \
  --download-root "${AUX_DATA_DIR}" \
  --pretrained-root "${PRETRAIN_DIR}"

python scripts/unpack_downloads.py

echo "Næste trin: bash smoke_test.sh"