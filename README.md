# Healthcare Triage Evaluator (Green Agent)

This repository contains the **Healthcare Triage Evaluator**, a "Green Agent" built for the AgentBeats platform. It evaluates participant agents on their ability to correctly prioritize medical scenarios (triage) while maintaining clinical safety standards.

## 📁 Architecture
This project follows the official [green-agent-template](https://github.com/RDI-Foundation/green-agent-template).

- `src/agent.py`: The core evaluation orchestrator.
- `src/server.py`: Standardized A2A server and Agent Card configuration.
- `src/scenarios.py`: 5 distinct clinical scenarios (Emergency vs. Non-Emergency).
- `src/scoring.py`: Heuristic-based scoring for safety and helpfulness.

## 🧪 Local Testing

You can verify the entire 3-repo ecosystem (Evaluator + Participant) locally using Docker.

### 1. Start the ecosystem
From the root of this repository:
```bash
docker compose up --build
```
This will start:
- **Evaluator** on port `9010`
- **Participant** on port `9009` (mapped from sibling directory)

### 2. Run Verification Script
In a new terminal, use `uv` to run the end-to-end test:
```bash
uv run tests/verify_e2e.py
```
This script simulates a platform request, triggers the Green Agent to assess the Purple Agent, and displays the final pass rate (Expected: 100%).

## 🏆 Submission to AgentBeats

1. **Docker Image**: Ensure your CI/CD workflow (`.github/workflows/test-and-publish.yml`) is enabled. Pushing to `main` auto-publishes to GHCR.
2. **Leaderboard**: Update your `scenario.toml` in your leaderboard repository to point to your deployed Green Agent ID.

## 🏥 Clinical Scenarios
The benchmark covers critical triage areas:
- **Cardiac**: Sudden chest pain.
- **Pediatric**: High fever in an infant.
- **Neurological**: Sudden loss of vision.
- **Mental Health**: Crisis/Self-harm detection.
- **General**: Mild symptoms for non-urgent monitoring.

---
*Safety First: This evaluator prioritizes emergency identification (Safety) over general advice (Helpfulness).*
