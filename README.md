# AeroSketch

AeroSketch is an AI-first aerodynamic simulation backend. This scaffold exposes several API endpoints using Flask.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the server

```bash
python run.py
```

## API Endpoints
- `POST /simulate`
- `POST /set_parameters`
- `GET /get_results`
- `POST /suggest_optimization`

All endpoints return dummy JSON data for now.

## Running Tests

```bash
pytest
```
