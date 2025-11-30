"""Public entry point for the travel planner."""

from dotenv import load_dotenv
load_dotenv()

from .runner import _run_once, run_demo
from .workflow import root_agent

__all__ = ["root_agent", "_run_once", "run_demo"]


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_demo())
