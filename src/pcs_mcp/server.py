"""MCP server exposing ProCyclingStats (PCS) teams, riders, and races data.

Each tool wraps a scraping class from the `procyclingstats` library and takes
a relative PCS URL path, mirroring the site's own URL structure. This keeps
the server thin and lets a caller dig into any season, race edition, or
rider/team page PCS exposes without the server hardcoding every variant.
"""

from typing import Any, Literal

from mcp.server.fastmcp import FastMCP
from procyclingstats import Race, RaceStartlist, Rider, RiderResults, Stage, Team

mcp = FastMCP("pcs-mcp")

StageResultType = Literal["results", "gc", "points", "kom", "youth", "teams", "climbs"]


def _parse(scraper_cls: type, url: str) -> dict[str, Any]:
    try:
        return scraper_cls(url).parse()
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}", "url": url}


@mcp.tool()
def get_rider(url: str) -> dict[str, Any]:
    """Fetch a rider's profile from ProCyclingStats.

    url: relative PCS path, e.g. "rider/tadej-pogacar" for the career
    profile (bio, team history, points per season/specialty), or
    "rider/tadej-pogacar/2023" for that season's results (read the
    'season_results' field of the response).
    """
    return _parse(Rider, url)


@mcp.tool()
def get_rider_results(url: str) -> dict[str, Any]:
    """Fetch a rider's full results history from ProCyclingStats.

    url: relative PCS path, e.g. "rider/tadej-pogacar/results" for all
    career results, or "rider/tadej-pogacar/results/final-5k-analysis"
    for final-5km climbing analysis.
    """
    return _parse(RiderResults, url)


@mcp.tool()
def get_team(url: str) -> dict[str, Any]:
    """Fetch a team's roster and season info from ProCyclingStats.

    url: relative PCS path including the season, e.g.
    "team/bora-hansgrohe-2024".
    """
    return _parse(Team, url)


@mcp.tool()
def get_race(url: str) -> dict[str, Any]:
    """Fetch a race edition's overview from ProCyclingStats.

    Returns stages, stage winners, and prior editions for stage races,
    or basic race info for one-day races.

    url: relative PCS path, e.g. "race/tour-de-france/2024" (stage race)
    or "race/milano-sanremo/2024" (one-day race).
    """
    return _parse(Race, url)


@mcp.tool()
def get_race_startlist(url: str) -> dict[str, Any]:
    """Fetch the startlist for a race edition from ProCyclingStats.

    url: relative PCS path, e.g. "race/tour-de-france/2024/startlist".
    """
    return _parse(RaceStartlist, url)


@mcp.tool()
def get_stage(url: str, result_type: StageResultType = "results") -> dict[str, Any]:
    """Fetch a results table for a single stage or one-day race.

    url: relative PCS path, e.g. "race/tour-de-france/2024/stage-18", or
    "race/milano-sanremo/2024/result" for a one-day race.
    result_type: which table to return - "results" (finishers), "gc"
    (general classification), "points", "kom", "youth", "teams", or
    "climbs". Not every result_type exists on every page.
    """
    try:
        stage = Stage(url)
        method = getattr(stage, result_type)
        return {result_type: method()}
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}", "url": url}


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
