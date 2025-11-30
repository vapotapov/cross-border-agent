# cross-border-agent

A multi-agent travel optimizer designed for complex, multi-country, multi-modal trips where no single data source is sufficient.

## Project layout
- `pyproject.toml` – package metadata, dependencies, lint/test tooling
- `src/cross_border_agent/` – library code (models + orchestrator skeleton)
- `tests/` – pytest-based smoke tests

## Getting started
1. Use Python 3.11+ and create a virtual environment: `python -m venv .venv && . .venv/Scripts/Activate.ps1` (or `source .venv/bin/activate` on POSIX).
2. Install the package in editable mode with dev tools: `pip install -e .[dev]`.
3. Run tests: `pytest`.

## Next steps
- Wire up specialized agents (search, scoring, constraints) behind `Orchestrator.plan`.
- Add adapters for data sources (GDS, rail APIs, bus feeds, mapping/routing).
- Model constraints/preferences (visas, transit rules, layovers, carbon, budget) in `TravelRequest`.
- Introduce routing/optimization heuristics and caching for multi-modal legs.
