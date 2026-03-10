#!/usr/bin/env bash
set -euo pipefail

if [ ! -f config.env ]; then
  echo "Mangler config.env. Kør: cp config.env.example config.env"
  exit 1
fi

python scripts/verify_setup.py
echo "Smoke test bestået."