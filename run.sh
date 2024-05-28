#!/usr/bin/env bash

# If conda installed, run with conda, else if `xc-cup-env` exists, run with venv,
# else try to run with system python3
if command -v conda &> /dev/null; then
    if conda env list | grep -q "xc-cup-env"; then
        conda run -n xc-cup-env python xc-cup-ranker.py $@
    fi
elif [ -d "xc-cup-env" ]; then
    source xc-cup-env/bin/activate
    python xc-cup-ranker.py $@
    deactivate
else
    python3 xc-cup-ranker.py $@
fi
