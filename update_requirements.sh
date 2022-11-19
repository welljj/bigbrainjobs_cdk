#!/bin/bash
source .venv/bin/activate
python -m pip install -U --upgrade-strategy eager pip setuptools wheel
python -m pip install -U --upgrade-strategy eager -r requirements.txt -r requirements-dev.txt -r website/bigbrainjobs/requirements.txt
