"""Utilities for normalizing segments, building routes, and scoring them."""

from typing import Any, Dict, List

from google.adk.tools import FunctionTool


def normalize_segments(
    raw_segments: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Normalize provider-specific segments into a shared schema.

    For demo: just ensure required keys are present and emit
    'duration_hours' and 'transfer_penalty'.
    """
    normalized = []
    for seg in raw_segments:
        # NOTE: in real code parse timestamps properly and compute duration.
        norm = {
            "provider": seg["provider"],
            "from": seg["from"],
            "to": seg["to"],
            "dep": seg["dep"],
            "arr": seg["arr"],
            "mode": seg["mode"],
            "price_eur": float(seg["price_eur"]),
            "transfers": int(seg.get("transfers", 0)),
            "currency": seg.get("currency", "EUR"),
            # toy heuristics
            "duration_hours": 4.0,
            "transfer_penalty": 0.5 * int(seg.get("transfers", 0)),
        }
        normalized.append(norm)
    return normalized


def build_candidate_routes(
    segments: List[Dict[str, Any]], origin: str, destination: str
) -> List[Dict[str, Any]]:
    """
    In a real system this would do graph search over segments.

    For demo: treat the full list of segments as a single linear route.
    """
    if not segments:
        return []

    total_price = sum(seg["price_eur"] for seg in segments)
    total_transfers = sum(seg["transfers"] for seg in segments)
    total_duration = sum(seg["duration_hours"] for seg in segments)

    return [
        {
            "id": "route_1",
            "origin": origin,
            "destination": destination,
            "segments": segments,
            "total_price_eur": round(total_price, 2),
            "total_transfers": total_transfers,
            "total_duration_hours": total_duration,
        }
    ]


def score_routes(
    routes: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Score candidate routes on:
      - fastest
      - cheapest
      - fewest transfers
    """
    if not routes:
        return {"fastest": None, "cheapest": None, "fewest_transfers": None}

    fastest = min(routes, key=lambda r: r["total_duration_hours"])
    cheapest = min(routes, key=lambda r: r["total_price_eur"])
    fewest_transfers = min(routes, key=lambda r: r["total_transfers"])

    return {
        "fastest": fastest,
        "cheapest": cheapest,
        "fewest_transfers": fewest_transfers,
    }


normalize_segments_tool = FunctionTool(func=normalize_segments)
build_routes_tool = FunctionTool(func=build_candidate_routes)
score_routes_tool = FunctionTool(func=score_routes)

__all__ = [
    "build_candidate_routes",
    "build_routes_tool",
    "normalize_segments",
    "normalize_segments_tool",
    "score_routes",
    "score_routes_tool",
]
