# cross-border-agent

A multi-agent travel optimizer designed for complex, multi-country, multi-modal trips where no single data source is sufficient.

## Project layout
- `pyproject.toml` – package metadata, dependencies, lint/test tooling
- `src/` – library code (models + orchestrator skeleton)
- `tests/` – pytest-based smoke tests

## Models
- Default LLM: `gemini-2.5-flash-lite` (set as `GEMINI_MODEL` in `src/workflow.py` and used by all agents).
- All agents currently share the same model; swap to a different Gemini family ID or provider by changing the `GEMINI_MODEL` constant and re-running.
- Agents: RailSearchAgent, FlightSearchAgent, BusSearchAgent, NormalizationAgent, ConnectionBuilderAgent, OptimizationAgent, AdvisorAgent.

## What’s implemented (Google ADK)
- Multi-agent with LLMs: sequential root agent orchestrating parallel provider searches, normalization, scoring, and advisory.
- Parallel agents: rail/flight/bus search run in `ParallelAgent`.
- Sequential agents: overall flow in `SequentialAgent`.
- Sessions & state: uses ADK `InMemoryRunner`/`SessionService`; seeds state keys in `src/runner.py`.

## How to run
1. Use Python 3.11+ and create a virtual environment: `python -m venv .venv && . .venv/Scripts/Activate.ps1` (or `source .venv/bin/activate` on POSIX).
2. Install the package in editable mode: `python -m pip install -e .`.
3. Run project: `python -m src.runner`.
