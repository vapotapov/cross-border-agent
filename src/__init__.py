from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

# Load environment variables once on package import so runners/agents
# see credentials without duplicated calls.
# Try project root .env first, then src/.env fallback.
load_dotenv()
load_dotenv(Path(__file__).with_name(".env"))

from src.workflow import root_agent  # noqa: E402

__all__ = ["__version__", "root_agent"]
__version__ = "0.1.0"
