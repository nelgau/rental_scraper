#!/bin/bash
set -euo pipefail
export FLASH_ENV=production
exec python3 wsgi.py
