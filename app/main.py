from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "events.json"

app = FastAPI(title="Third-Period Comeback Tracker")
app.mount("/static", StaticFiles(directory=BASE_DIR / "app" / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")


def load_events() -> list[dict[str, Any]]:
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8") as file_handle:
        payload = json.load(file_handle)
    return payload.get("events", [])


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    events = load_events()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "events": events,
            "last_updated": datetime.utcnow().isoformat() + "Z",
        },
    )


@app.get("/api/events")
def api_events() -> dict[str, Any]:
    return {
        "events": load_events(),
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
