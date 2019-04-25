#!/bin/bash
set -euo pipefail
source env/bin/activate
exec python3 update_google_sheet.py
