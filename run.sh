#!/usr/bin/env bash

# If conda installed, run with conda, else run with python
if command -v conda &> /dev/null; then
    conda run -n xc-cup-env python xc-cup-ranker.py $@
else
    python3 xc-cup-ranker.py $@
fi
