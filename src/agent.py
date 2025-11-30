"""Convenience entry points for the travel planner."""

from __future__ import annotations

import asyncio

from src import root_agent
from src.runner import run_demo, run_once

__all__ = ["root_agent", "run_demo", "run_once"]


if __name__ == "__main__":
    asyncio.run(run_demo())
