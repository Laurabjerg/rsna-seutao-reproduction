#!/usr/bin/env bash
set -euo pipefail

if [ ! -f config.env ]; then
  echo "Opretter config.env fra config.env.example ..."
  cp config.env.example config.env
fi

export PROJECT_ROOT="$(pwd)"
source config.env

python scripts/verify_setup.py
echo "Smoke test bestået."