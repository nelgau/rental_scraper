#!/bin/bash
set -euo pipefail
source env/bin/activate
exec flock -xn /run/rental_scraper/crawl-search.lock -c script/crawl-search.sh
