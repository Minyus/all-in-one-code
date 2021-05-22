#!/bin/bash

set -eux

# Optionally install dependencies
pip --no-cache-dir install \
    pandas \
    pyinstrument \
    && true

# Run the entry main code
# python main.py
pyinstrument main.py

# Show environment info
printenv
python -V
pip freeze
