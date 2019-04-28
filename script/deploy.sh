#!/bin/bash
set -euo pipefail
ssh ubuntu@rentals.nelgau.io <<EOF
  cd /home/web/rental_scraper;
  sudo su web -c 'git pull origin master';
  sudo systemctl restart rental_scraper.service
EOF
