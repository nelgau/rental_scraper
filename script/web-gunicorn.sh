#!/bin/bash
set -euo pipefail
export FLASH_ENV=production
exec gunicorn --bind 127.0.0.1:5000 wsgi:app
