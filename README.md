# pcs-mcp

MCP server exposing [ProCyclingStats](https://www.procyclingstats.com) teams,
riders, and races data, built on top of the
[`procyclingstats`](https://github.com/themm1/procyclingstats) scraping
library. Intended for digging into historical results and building custom
rankings on top of raw PCS data.

PCS has no official API, so this server scrapes site pages. URLs may break
if PCS changes its HTML; keep the `procyclingstats` dependency up to date.

## Tools

Every tool takes a relative PCS URL path (the same paths you'd see in your
browser, minus the domain) so you can reach any season, race edition, or
rider/team page PCS exposes.

| Tool | Example `url` | Returns |
|---|---|---|
| `get_rider` | `rider/tadej-pogacar` or `rider/tadej-pogacar/2023` | Bio, team history, points per season/specialty, or a specific season's results |
| `get_rider_results` | `rider/tadej-pogacar/results` | Full career results history |
| `get_team` | `team/bora-hansgrohe-2024` | Roster and season info |
| `get_race` | `race/tour-de-france/2024` | Stages, stage winners, prior editions |
| `get_race_startlist` | `race/tour-de-france/2024/startlist` | Startlist |
| `get_stage` | `race/tour-de-france/2024/stage-18` | Results / GC / points / KOM / youth / teams / climbs table |

## Setup

```bash
pip install -e .
```

## Run

```bash
pcs-mcp
```

Or point an MCP client (e.g. Claude Desktop / Claude Code) at it directly:

```json
{
  "mcpServers": {
    "pcs": {
      "command": "pcs-mcp"
    }
  }
}
```
