#!/usr/bin/env bash

cd -- "$(dirname -- "${BASH_SOURCE[0]}")" || exit 1
python run_infer_idea.py --port 12372 "$@"
