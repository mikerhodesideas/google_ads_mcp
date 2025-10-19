# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Context

This repository contains the Google Ads MCP server setup for Mike Rhodes' Google Ads accounts. The MCP server enables Claude to query Google Ads data through standardized tools.

## Account Aliases (accounts.json)

**IMPORTANT:** Always check `.claude/accounts.json` when the user refers to accounts by name or abbreviation.

The `accounts.json` file maps friendly names and aliases to Google Ads customer IDs:

**Manager Accounts**:
- **WebSavvy / Digital Divide** (997, websavvy, ddg) - `9978959108` - AUD - MCC
- **Mike Rhodes Ideas** (MRI, MCC) - `5407170017` - AUD - MCC

**Client Accounts** (under 997 MCC):
- **ButcherBox** (bb) - `9642575967` - USD
- **Kip&Co** (kip) - `4779792239` - AUD
- **BDO Furniture** (bdo) - `2827975704` - AUD
- **Swimwear Galore** (swg, swimwear) - `7415198088` - AUD

**Client Accounts** (under Mike Rhodes Ideas MCC):
- **Scottish Shutters** (SSC, Rocknowe Interiors) - `9882330267` - GBP
- **Mr Pool Man** (MPM, Pool Man) - `7435598264` - AUD

Load this file at the start of Google Ads queries to map names to customer IDs. Each entry in `accounts.json` includes aliases array for flexible name matching.

## Agent Skills

Skills in `.claude/skills/` provide Google Ads expertise:
- **gaql-query-builder/** - Constructs Google Ads Query Language (GAQL) queries with proper syntax, field selection, and filtering. Activates when building custom reports or troubleshooting GAQL syntax. Has access to `get_gaql_doc`, `get_reporting_view_doc`, and `execute_gaql` MCP tools.
- **google-ads-account-info/** - Retrieves account details, IDs, currency, timezone, manager status, and client account hierarchies. Activates when analyzing account structure or exploring MCC relationships. Has access to `list_accessible_accounts` and `execute_gaql` MCP tools.
- **google-ads-campaign-performance/** - Retrieves and analyzes campaign performance metrics (clicks, impressions, cost, conversions, CTR). Activates when analyzing campaign performance or generating performance reports. Has access to `execute_gaql` MCP tool.

These skills are **model-invoked** - Claude activates them automatically when the task matches their description. They use `allowed-tools` to restrict access to only the necessary Google Ads MCP tools.

### Skills vs Agents vs Commands vs Plugins

See `context/info-and-docs/agents-skills-plugins-commands.md` for detailed comparison.

**Quick summary**:
- **Commands** - User-invoked (you type `/command`) for manual workflows
- **Skills** - Model-invoked (Claude activates) for automatic expertise
- **Agents** - Mixed invocation (user or Claude) for specialist perspectives
- **Plugins** - Distribution mechanism for Commands + Skills + Agents + MCP

## MCP Server (Google Ads)

**Configuration**: `~/.claude/mcp_settings.json`

The Google Ads MCP server enables Claude to query Google Ads data through standardized tools. It provides:
- `list_accessible_accounts` - List all accessible Google Ads accounts
- `execute_gaql` - Execute GAQL queries against specific accounts
- `get_gaql_doc` - Get GAQL syntax documentation
- `get_reporting_view_doc` - Get field documentation for specific resources

**Location**: `/Users/mike/Projects/ads-mcp/google_ads_mcp/`
- This is Google's official implementation and should rarely be modified
- Credentials: `/Users/mike/Projects/ads-mcp/google_ads_mcp/google-ads.yaml`
- Server runs via `uv` with 30-second timeout

The MCP server is configured globally in `~/.claude/mcp_settings.json` and available across all Claude Code sessions.

## Account Aliases - Quick Reference

**Always check `.claude/accounts.json` for the complete, authoritative list.**

Common shortcuts in this project:
- "997" / "websavvy" / "ddg" → MCC 9978959108
- "swg" / "swimwear" → Account 7415198088 (AUD)
- "bb" / "butcherbox" → Account 9642575967 (USD)
- "kip" → Account 4779792239 (AUD)
- "bdo" → Account 2827975704 (AUD)
- "SSC" → Account 9882330267 (GBP)
- "MPM" → Account 7435598264 (AUD)
- "My MCC" → Account 5407170017 (manager account)

**Note:** General Google Ads query defaults and formatting rules are defined in `~/Projects/CLAUDE.md`.

## Project-Specific Configuration

This is a **project-specific** setup. The `.claude/` directory contains:
- `accounts.json` - Account aliases (project-specific)
- `skills/` - Google Ads Agent Skills (project-specific)
- `CLAUDE.md` - This file (project-specific)

These files provide context for working with Mike's Google Ads accounts in this repository.
