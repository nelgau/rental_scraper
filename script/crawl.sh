#!/bin/bash
set -euo pipefail
scrapy crawl search
python3 update_google_sheet.py
