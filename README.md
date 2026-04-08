# vision-one-mxdr

A clean-slate HTML/Flask system inspired by the workflow of the existing vision1 project.

## Goals
- Keep secrets out of source code
- Allow runtime key/token input only when needed
- Start with a maintainable MVP structure
- Support future Vision One / MxDR investigation workflows

## Planned MVP
- Home dashboard
- Session-based settings page for API/token input
- Query page scaffold
- Report/result page scaffold

## Security principles
- No hardcoded API keys
- No committed credential files
- Prefer session-scoped secret handling
