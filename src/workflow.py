"""Composition of LLM agents and root workflow."""

from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.tools import AgentTool, google_search

from src.providers import (
    search_buses_tool,
    search_db_tool,
    search_flights_tool,
    search_pkp_tool,
    search_uz_tool,
)
from src.routing import (
    build_routes_tool,
    normalize_segments_tool,
    score_routes_tool,
)

GEMINI_MODEL = "gemini-2.5-flash-lite"

# --- Search agents (run in parallel) ---------------------------------


rail_search_agent = LlmAgent(
    name="RailSearchAgent",
    model=GEMINI_MODEL,
    description=(
        "Searches DB, PKP, and UZ for rail segments between origin and "
        "destination."
    ),
    instruction=(
        "You are a rail search specialist.\n"
        "- Use the DB, PKP, and UZ tools to fetch rail segments for the "
        "trip.\n"
        "- Always request segments using the provided origin, destination, "
        "and date.\n"
        "- Merge all segments into a single list.\n"
        "- Return ONLY JSON with key 'rail_segments', no extra text."
    ),
    tools=[search_db_tool, search_pkp_tool, search_uz_tool],
    output_key="rail_segments",
)

flight_search_agent = LlmAgent(
    name="FlightSearchAgent",
    model=GEMINI_MODEL,
    description=(
        "Searches flights from origin to regional hubs "
        "(e.g., Bucharest, Chisinau)."
    ),
    instruction=(
        "You are a flight search specialist.\n"
        "- Use the flights tool to get flight segments from origin to nearby "
        "hubs.\n"
        "- Return ONLY JSON with key 'flight_segments'."
    ),
    tools=[search_flights_tool],
    output_key="flight_segments",
)

bus_search_agent = LlmAgent(
    name="BusSearchAgent",
    model=GEMINI_MODEL,
    description=(
        "Searches cross-border buses from hubs into target country."
    ),
    instruction=(
        "You are a long-distance bus search specialist.\n"
        "- Use the buses tool to get bus segments that connect hubs to the "
        "destination region.\n"
        "- Return ONLY JSON with key 'bus_segments'."
    ),
    tools=[search_buses_tool],
    output_key="bus_segments",
)

search_parallel_agent = ParallelAgent(
    name="ProviderSearchParallel",
    sub_agents=[rail_search_agent, flight_search_agent, bus_search_agent],
)

# --- Normalization + connection builder ------------------------------


normalization_agent = LlmAgent(
    name="NormalizationAgent",
    model=GEMINI_MODEL,
    description=(
        "Normalizes raw segments from multiple providers into a unified "
        "schema."
    ),
    instruction=(
        "You are a normalization engine.\n"
        "- Read raw segments from state keys: rail_segments, flight_segments, "
        "bus_segments.\n"
        "- Combine them into a single Python list.\n"
        "- Call the 'normalize_segments' tool once with that list.\n"
        "- Return ONLY JSON with key 'normalized_segments'.\n"
        "If there are no segments, return {'normalized_segments': []}."
    ),
    tools=[normalize_segments_tool],
    output_key="normalized_segments",
)

connection_builder_agent = LlmAgent(
    name="ConnectionBuilderAgent",
    model=GEMINI_MODEL,
    description="Builds feasible candidate routes from normalized segments.",
    instruction=(
        "You are a connection builder.\n"
        "- Read 'normalized_segments' from session state.\n"
        "- Use the 'build_candidate_routes' tool to construct feasible routes "
        "from origin to destination using that list.\n"
        "- Use the origin and destination from the user message or state keys "
        "'origin' and 'destination' if present.\n"
        "- Return ONLY JSON with key 'candidate_routes'."
    ),
    tools=[build_routes_tool],
    output_key="candidate_routes",
)

# --- Optimization / scoring agent ------------------------------------


optimization_agent = LlmAgent(
    name="OptimizationAgent",
    model=GEMINI_MODEL,
    description=(
        "Scores candidate routes for fastest, cheapest, and fewest transfers."
    ),
    instruction=(
        "You are a routing optimizer.\n"
        "- Read 'candidate_routes' from session state.\n"
        "- Use the 'score_routes' tool to compute the fastest, cheapest, and "
        "fewest transfers routes.\n"
        "- Return ONLY JSON with keys: 'fastest', 'cheapest', "
        "'fewest_transfers'."
    ),
    tools=[score_routes_tool],
    output_key="ranked_routes",
)

# --- Optional: Google Search agent as a tool (border status) ----------


border_info_agent = LlmAgent(
    name="BorderInfoAgent",
    model=GEMINI_MODEL,
    description=(
        "Looks up current border status, disruptions, or safety advisories "
        "along the route."
    ),
    instruction=(
        "You are a border and disruption information specialist.\n"
        "Use Google Search to check for recent news on border closures, "
        "strikes, or war-related disruptions that might affect the suggested "
        "route.\n"
        "Summarize only the most critical points briefly."
    ),
    tools=[google_search],
    output_key="border_notes",
)

border_info_tool = AgentTool(agent=border_info_agent)

advisor_agent = LlmAgent(
    name="AdvisorAgent",
    model=GEMINI_MODEL,
    description=(
        "Turns raw scores + border info into a user-friendly itinerary "
        "summary."
    ),
    instruction=(
        "You are a travel advisor.\n"
        "- Read 'ranked_routes' from state and optionally call the "
        "border_info agent tool.\n"
        "- Generate a concise explanation of:\n"
        "    * fastest route\n"
        "    * cheapest route\n"
        "    * route with fewest transfers\n"
        "  including total time, price, and number of transfers.\n"
        "- If border_notes are available, append a short warning/safety "
        "paragraph.\n"
        "- Output should be clear, bullet-pointed, and human-readable."
    ),
    tools=[border_info_tool],
)

# --- Root multi-agent workflow ---------------------------------------


root_agent = SequentialAgent(
    name="MultiModalTravelPlanner",
    sub_agents=[
        search_parallel_agent,
        normalization_agent,
        connection_builder_agent,
        optimization_agent,
        advisor_agent,
    ],
)

__all__ = ["root_agent"]
