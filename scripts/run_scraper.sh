#!/usr/bin/env bash
set -euo pipefail

SOURCE_URL=${1:-"https://www.nhl.com/"}
python scraping/scraper.py --source "$SOURCE_URL"
