#!/bin/bash
set -euo pipefail
source env/bin/activate
exec flock -xn /run/rental_scraper/update-sheet.lock -c script/update-sheet.sh
