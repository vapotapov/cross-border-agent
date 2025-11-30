"""Utilities for normalizing segments, building routes, and scoring them."""

from __future__ import annotations

from typing import Any, Dict, List

from google.adk.tools import FunctionTool

Segment = Dict[str, Any]
SegmentList = List[Segment]
Route = Dict[str, Any]
RouteList = List[Route]


def normalize_segments(raw_segments: SegmentList) -> SegmentList:
    """Normalize provider-specific segments into a shared schema."""
    normalized = []
    for seg in raw_segments:
        # NOTE: in real code parse timestamps properly and compute duration.
        norm = {
            "provider": seg.get("provider", "unknown"),
            "from": seg.get("from", ""),
            "to": seg.get("to", ""),
            "dep": seg.get("dep", ""),
            "arr": seg.get("arr", ""),
            "mode": seg.get("mode", "unknown"),
            "price_eur": float(seg.get("price_eur", 0.0)),
            "transfers": int(seg.get("transfers", 0)),
            "currency": seg.get("currency", "EUR"),
            # toy heuristics
            "duration_hours": 4.0,
            "transfer_penalty": 0.5 * int(seg.get("transfers", 0)),
        }
        normalized.append(norm)
    return normalized


def build_candidate_routes(
    raw_segments: SegmentList, origin: str, destination: str
) -> RouteList:
    """Build route candidates from raw provider segments."""

    segments = normalize_segments(raw_segments)  # <-- automatic normalization

    if not segments:
        return []

    total_price = sum(seg["price_eur"] for seg in segments)
    total_transfers = sum(seg["transfers"] for seg in segments)
    total_duration = sum(seg["duration_hours"] for seg in segments)

    return [{
        "id": "route_1",
        "origin": origin,
        "destination": destination,
        "segments": segments,
        "total_price_eur": round(total_price, 2),
        "total_transfers": total_transfers,
        "total_duration_hours": total_duration,
    }]

def score_routes(routes: RouteList) -> Dict[str, Any]:
    """Score candidate routes on fastest / cheapest / fewest transfers."""
    if not routes:
        return {"fastest": None, "cheapest": None, "fewest_transfers": None}

    # Filter out malformed routes to avoid KeyError.
    valid_routes = [
        r
        for r in routes
        if {"total_duration_hours", "total_price_eur", "total_transfers"}.issubset(r.keys())
    ]
    if not valid_routes:
        return {"fastest": None, "cheapest": None, "fewest_transfers": None}

    fastest = min(valid_routes, key=lambda r: r.get("total_duration_hours", float("inf")))
    cheapest = min(valid_routes, key=lambda r: r.get("total_price_eur", float("inf")))
    fewest_transfers = min(valid_routes, key=lambda r: r.get("total_transfers", float("inf")))

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
