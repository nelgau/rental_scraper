#!/bin/bash
set -euo pipefail
source env/bin/activate
exec scrapy crawl search
