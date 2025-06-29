# AeroSketch

AeroSketch is an AI-first aerodynamic simulation engine. This repository contains the backend service used for serving simulation results.

## Running locally

Create a virtual environment and install dependencies from `requirements.txt`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the Flask development server:

```bash
python -m aerosketch.app
```

The service exposes a `/simulate` endpoint that currently returns mocked pressure and velocity fields in base64-encoded form.
