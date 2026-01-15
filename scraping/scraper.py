from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import httpx
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "events.json"
DEFAULT_SOURCE = "https://www.nhl.com/"


@dataclass
class TrackedEvent:
    date: str
    matchup: str
    summary: str
    lead: str
    tied_at: str
    source: str


def fetch_html(url: str) -> str:
    response = httpx.get(url, timeout=20.0)
    response.raise_for_status()
    return response.text


def parse_events(html: str, source: str) -> Iterable[TrackedEvent]:
    soup = BeautifulSoup(html, "html.parser")
    _ = soup.title
    return []


def load_payload() -> dict:
    if DATA_PATH.exists():
        with DATA_PATH.open("r", encoding="utf-8") as file_handle:
            return json.load(file_handle)
    return {"events": []}


def save_events(events: list[TrackedEvent]) -> None:
    payload = load_payload()
    payload["generated_at"] = datetime.utcnow().isoformat() + "Z"
    payload["events"] = [event.__dict__ for event in events]
    DATA_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_scrape(source: str) -> None:
    html = fetch_html(source)
    events = list(parse_events(html, source))
    save_events(events)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape NHL comeback data sources.")
    parser.add_argument(
        "--source",
        default=DEFAULT_SOURCE,
        help="URL of the public source to parse.",
    )
    args = parser.parse_args()
    run_scrape(args.source)
