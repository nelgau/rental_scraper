#!/bin/bash
set -euo pipefail
source env/bin/activate
scrapy crawl search
