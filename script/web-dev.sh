#!/bin/bash
set -euo pipefail
export FLASK_DEBUG=1
export FLASH_ENV=development
exec python3 wsgi.py
