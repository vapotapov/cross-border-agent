"""Local runner helper for manual testing."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Final

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types

# Load environment variables early so Google ADK sees API credentials.
load_dotenv()  # project root .env if present
load_dotenv(Path(__file__).with_name(".env"))  # src/.env fallback

from src.workflow import root_agent

DEFAULT_APP: Final[str] = "cross-border-agent"
DEFAULT_USER: Final[str] = "demo-user-1"
DEFAULT_SESSION: Final[str] = "session-1"

async def run_once(
    query: str,
    origin: str = "Berlin",
    destination: str = "Pischanka",
    date: str = "2025-12-15",
    *,
    app_name: str = DEFAULT_APP,
    user_id: str = DEFAULT_USER,
    session_id: str = DEFAULT_SESSION,
) -> None:
    """Run the workflow a single time with the given parameters."""
    runner = InMemoryRunner(agent=root_agent, app_name=app_name)
    session_service = runner.session_service

    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )

    session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )
    session.state["origin"] = origin
    session.state["destination"] = destination
    session.state["date"] = date
    # Seed expected state keys so instruction templating doesn't fail if upstream tools return nothing.
    session_defaults = {
        "rail_segments": [],
        "flight_segments": [],
        "bus_segments": [],
        "normalized_segments": [],
        "candidate_routes": [],
        "ranked_routes": {},
        "border_notes": "",
    }
    for key, value in session_defaults.items():
        session.state.setdefault(key, value)

    user_content = types.Content(
        role="user",
        parts=[
            types.Part(
                text=(
                    f"{query}\n\n"
                    f"Origin: {origin}\n"
                    f"Destination: {destination}\n"
                    f"Date: {date}\n"
                    "Return the recommended routes as described in your instructions."
                )
            )
        ],
    )

    print(">>> USER:", query)
    print("-----------------------------------------------------")

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(">>> AGENT:")
            print(event.content.parts[0].text.strip())


async def run_demo() -> None:
    """Convenience wrapper that runs a sample request."""
    await run_once(
        query="Find me the fastest, cheapest, and fewest-transfer routes.",
        origin="Berlin",
        destination="Pischanka",
        date="2025-12-15",
    )


__all__ = ["run_once", "run_demo"]


if __name__ == "__main__":
    asyncio.run(run_demo())
