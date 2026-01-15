# Third-Period Comeback Tracker

This repository is the foundation for a website + automated data pipeline that tracks NHL games where
multi-goal third-period leads shrink into overtime or a shootout. It includes:

- A FastAPI web app with a ticker-style homepage and JSON API.
- A scraper scaffold for ingesting public data sources.
- Dockerized deployment primitives.

> **Disclaimer:** This project is unaffiliated with the NHL, teams, or sportsbook partners.

---

## Repository layout

```
app/                # FastAPI application, HTML templates, and CSS
scraping/           # Scraper scaffolding and data parsing
scripts/            # Helper shell scripts
data/events.json    # Placeholder events data consumed by the app
Dockerfile          # Production image
Docker-compose.yml  # Local dev convenience
requirements.txt    # Python dependencies
```

---

## Quick start (local dev)

### 1) Requirements

- Python 3.11+
- pip

### 2) Setup a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Run the web app

```bash
uvicorn app.main:app --reload
```

Visit: `http://localhost:8000`

### 4) Run the scraper (placeholder)

The scraper currently fetches HTML and returns an empty list (it is a scaffold).
When your parsing logic is ready, it will populate `data/events.json`.

```bash
python scraping/scraper.py --source https://www.nhl.com/
```

---

## Docker development

```bash
docker compose up --build
```

Visit: `http://localhost:8000`

---

## Production deployment

### Option A: Docker container

1. Build the image:

```bash
docker build -t comeback-tracker:latest .
```

2. Run the container:

```bash
docker run -p 8000:8000 comeback-tracker:latest
```

### Option B: VM + systemd

1. Provision a VM (Ubuntu 22.04 recommended).
2. Install Python 3.11 and create a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`.
4. Create a systemd service file:

```ini
[Unit]
Description=Comeback Tracker
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/comeback-tracker
ExecStart=/opt/comeback-tracker/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

5. Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable comeback-tracker
sudo systemctl start comeback-tracker
```

6. Configure Nginx or Caddy as a reverse proxy (optional) with HTTPS.

---

## Data pipeline concept

1. **Scrape:** Fetch public data from NHL.com, Puckpedia, or other partners.
2. **Parse:** Identify games where a team loses a multi-goal lead in the third.
3. **Store:** Write normalized events to `data/events.json` (or a database later).
4. **Serve:** The site reads `events.json` and publishes an API at `/api/events`.

### Scraper expansion checklist

- [ ] Replace `parse_events()` with real selectors and parsing logic.
- [ ] Add unit tests around parsing.
- [ ] Introduce a database (SQLite/Postgres) once volume grows.
- [ ] Schedule scraper in cron / GitHub Actions.
- [ ] Add tweet automation (separate process) after data validation.

---

## Environment variables

| Variable | Description | Default |
| --- | --- | --- |
| `PORT` | Web server port | `8000` |

---

## Contributing guidelines

- Keep scraping logic modular and tested.
- Avoid aggressive scraping or any terms-of-service violations.
- Update `data/events.json` schema changes in both scraper + web app.

---

## Roadmap (suggested)

- Build the trend analysis article pages.
- Add charting for comeback frequency over time.
- Add a "tip line" contact page and legal disclaimer.
- Add a real-time ticker with WebSockets.
- Extend dataset to tag penalty timing, coach challenges, and score effects.

---

## Support

If you need help wiring the scraper or automating Twitter/X posting, open an issue with:

- Target data source(s)
- Parsing rules for third-period lead criteria
- Hosting constraints (AWS, GCP, Render, etc.)
