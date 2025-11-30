"""Mock provider search functions and FunctionTool wrappers."""

from __future__ import annotations

from typing import Any, Dict, List

from google.adk.tools import FunctionTool

SegmentList = List[Dict[str, Any]]


def search_db_trains(origin: str, destination: str, date: str) -> SegmentList:
    """Mock Deutsche Bahn search."""
    return [
        {
            "provider": "DB",
            "from": origin,
            "to": "Frankfurt (Oder)",
            "dep": f"{date}T07:00",
            "arr": f"{date}T09:00",
            "mode": "train",
            "price_eur": 29.0,
            "currency": "EUR",
            "transfers": 0,
        },
    ]


def search_pkp_trains(origin: str, destination: str, date: str) -> SegmentList:
    """Mock PKP (Poland) search."""
    return [
        {
            "provider": "PKP",
            "from": "Frankfurt (Oder)",
            "to": "Warszawa Centralna",
            "dep": f"{date}T10:00",
            "arr": f"{date}T15:00",
            "mode": "train",
            "price_eur": 40.0,
            "currency": "EUR",
            "transfers": 0,
        },
    ]


def search_uz_trains(origin: str, destination: str, date: str) -> SegmentList:
    """Mock Ukrzaliznytsia search."""
    return [
        {
            "provider": "UZ",
            "from": "Warszawa Centralna",
            "to": "Pischanka (via Kyiv hub)",
            "dep": f"{date}T18:00",
            "arr": f"{date}T+1T10:00",
            "mode": "train",
            "price_eur": 45.0,
            "currency": "EUR",
            "transfers": 1,
        },
    ]


def search_flights_to_hubs(origin: str, date: str) -> SegmentList:
    """Mock flights to regional hubs (e.g. Bucharest / Chisinau)."""
    return [
        {
            "provider": "FlightAPI",
            "from": "Berlin",
            "to": "Bucharest",
            "dep": f"{date}T09:30",
            "arr": f"{date}T12:30",
            "mode": "flight",
            "price_eur": 120.0,
            "currency": "EUR",
            "transfers": 0,
        },
        {
            "provider": "FlightAPI",
            "from": "Berlin",
            "to": "Chisinau",
            "dep": f"{date}T08:00",
            "arr": f"{date}T11:00",
            "mode": "flight",
            "price_eur": 110.0,
            "currency": "EUR",
            "transfers": 0,
        }
    ]


def search_cross_border_buses(
    origin: str, destination: str, date: str
) -> SegmentList:
    """Mock long-distance / cross-border buses."""
    return [
        {
            "provider": "BusCo",
            "from": "Bucharest",
            "to": "Vinnytsia",
            "dep": f"{date}T15:00",
            "arr": f"{date}T+1T06:00",
            "mode": "bus",
            "price_eur": 60.0,
            "currency": "EUR",
            "transfers": 0,
        },
    ]


search_db_tool = FunctionTool(func=search_db_trains)
search_pkp_tool = FunctionTool(func=search_pkp_trains)
search_uz_tool = FunctionTool(func=search_uz_trains)
search_flights_tool = FunctionTool(func=search_flights_to_hubs)
search_buses_tool = FunctionTool(func=search_cross_border_buses)

__all__ = [
    "search_buses_tool",
    "search_cross_border_buses",
    "search_db_tool",
    "search_db_trains",
    "search_flights_to_hubs",
    "search_flights_tool",
    "search_pkp_tool",
    "search_pkp_trains",
    "search_uz_tool",
    "search_uz_trains",
]
