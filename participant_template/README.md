# Healthcare Triage Participant (Purple Agent)

This repository contains the **Healthcare Triage Participant**, a standalone A2A agent designed to simulate a consumer-facing medical assistant. It focuses on safety-first triage by identifying potential medical emergencies.

## Architecture
This project follows the official [agent-template](https://github.com/RDI-Foundation/agent-template).

- `src/agent.py`: Integrated Healthcare Triage logic (Emergency vs. Non-Emergency).
- `src/server.py`: Standardized A2A server and Agent Card configuration.
- `src/messenger.py`: A2A messaging utilities for communicating with other agents.

## Getting Started

### 1. Install Dependencies
This project uses `uv` for fast dependency management:
```bash
uv sync
```

### 2. Run Locally
```bash
uv run src/server.py
```
The agent starts on port `9009` by default.

## Docker Support
The repository includes a `Dockerfile` and a GitHub Actions workflow that automatically publishes a Docker image to GHCR upon pushing to `main`.

To build locally:
```bash
docker build -t healthcare-triage-participant .
```

## Testing
Run A2A conformance tests:
```bash
uv sync --extra test
uv run pytest --agent-url http://localhost:9009
```

---
*Disclaimer: This agent is a synthetic benchmark tool and does not provide real medical advice.*
