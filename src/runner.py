"""Local runner helper for manual testing."""

from dotenv import load_dotenv
load_dotenv()

import asyncio

from google.adk.runners import InMemoryRunner
from google.genai import types

from .workflow import root_agent


async def _run_once(
    query: str,
    origin: str = "Berlin",
    destination: str = "Pischanka",
    date: str = "2025-12-15",
) -> None:
    """Simple helper to run the pipeline locally with InMemoryRunner."""
    app_name = "multi_agent_travel"
    user_id = "demo-user-1"
    session_id = "session-1"

    runner = InMemoryRunner(agent=root_agent, app_name=app_name)
    session_service = runner.session_service

    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )

    session = await session_service.get_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )
    session.state["origin"] = origin
    session.state["destination"] = destination
    session.state["date"] = date

    user_content = types.Content(
        role="user",
        parts=[
            types.Part(
                text=(
                    f"{query}\n\n"
                    f"Origin: {origin}\n"
                    f"Destination: {destination}\n"
                    f"Date: {date}\n"
                    "Return the recommended routes as described in your "
                    "instructions."
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
    await _run_once(
        query="Find me the fastest, cheapest, and fewest-transfer routes.",
        origin="Berlin",
        destination="Pischanka",
        date="2025-12-15",
    )


__all__ = ["_run_once", "run_demo"]


if __name__ == "__main__":
    asyncio.run(run_demo())
