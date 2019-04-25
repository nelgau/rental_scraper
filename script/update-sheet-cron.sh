#!/bin/bash
set -euo pipefail
source env/bin/activate
python3 update_google_sheet.py
