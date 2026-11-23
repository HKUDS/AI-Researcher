#!/usr/bin/env bash

cd -- "$(dirname -- "${BASH_SOURCE[0]}")" || exit 1
python run_infer_plan.py --port 12380 "$@"
