# Agent Guide for iot-monitoring-demo

This repository is a small demo stack for Elasticsearch and Kibana driven by
`docker compose` and `make`. Use this document as the single source of truth
for building, running, linting, testing, and making changes safely.

## Quick Facts

- Primary entrypoint: `makefile`
- Core runtime: Docker Compose (Elasticsearch + Kibana)
- Language tooling: none detected (no `package.json` or `pyproject.toml`)
- Config lives under `config/` and `docker-compose.yaml`

## Build, Run, Lint, Test

There are no app build, lint, or unit-test commands in this repo today. The
primary “build/run” workflow is starting the Docker stack.

### Start / Stop / Inspect the Stack

- Start: `make docker-infra-up`
- Stop: `make docker-infra-down`
- Status: `make docker-infra-status`
- Logs: `make docker-infra-logs`

### Docker Compose Directly

- Up: `docker compose -f docker-compose.yaml up -d`
- Down: `docker compose -f docker-compose.yaml down`
- Logs: `docker compose -f docker-compose.yaml logs -f`

### Single Test / Targeted Check

There is no test harness. If you need a focused check, use targeted
infrastructure or service health checks instead:

- Elasticsearch health: `curl -s http://localhost:9200 | grep -q 'cluster_name'`
- Kibana health: `curl -s -I http://localhost:5601 | grep -q 'HTTP/1.1 302 Found'`

If you add tests in the future, update this section with a single-test command
format (e.g., `pytest tests/foo_test.py::test_name`).

## Environment and Configuration

- `makefile` includes `.envrc` via `include .envrc`.
  - Ensure `.envrc` exists and is populated before running `make` targets.
  - If you use `direnv`, run `direnv allow` after editing `.envrc`.
- Docker env files:
  - `config/elastic-search/container-vars-elastic.env`
  - `config/kibana/container-vars-kibana.env`
- Do not store secrets in the repo. If you add credentials, keep them in a
  local `.envrc` or an ignored `.env` file and document required keys here.

## Code Style and Conventions

This repository is mostly configuration. Follow these conventions when editing
YAML, env files, and Makefiles.

### Formatting

- Use 2-space indentation for YAML.
- Keep keys ordered logically (service definition -> image -> restart -> ports
  -> volumes -> limits -> env -> healthchecks -> dependencies).
- Keep line lengths reasonable (<= 100 chars where possible) and wrap with
  indentation rather than trailing comments.
- Use LF line endings and UTF-8 (ASCII only unless a file already uses Unicode).

### Imports and Dependencies

- No code imports are present. If you add code, follow the conventions of the
  language’s standard tooling and update this file accordingly.
- Prefer explicit versions for Docker images via `.envrc` or environment
  variables used in `docker-compose.yaml`.

### Naming Conventions

- Service names use kebab-case (e.g., `elastic-search`, `kibana`).
- Environment variables use SCREAMING_SNAKE_CASE.
- Volume names use kebab-case (e.g., `elastic-data`).
- Make targets use kebab-case and map to a single action.

### Types and Data

- YAML scalars: use clear types (`true/false` for booleans, unquoted numbers
  for numeric values) unless the tool requires strings.
- Env files: use `KEY=value` pairs without quotes unless the value contains
  spaces or special characters.

### Error Handling and Safety

- Prefer “safe by default” settings; do not enable security-bypassing options
  without a note explaining why.
- When editing health checks, keep them deterministic and quick (avoid long
  sleeps or non-idempotent calls).
- Avoid deleting volumes unless explicitly requested; data loss is irreversible.

## File-Specific Notes

- `docker-compose.yaml` is the source of truth for runtime behavior.
- `makefile` is the preferred interface; keep targets simple and non-interactive.
- `config/elastic-search/container-vars-elastic.env` and
  `config/kibana/container-vars-kibana.env` are runtime configs for containers.

## Cursor / Copilot Rules

No Cursor rules found in `.cursor/rules/` or `.cursorrules`.
No Copilot instructions found in `.github/copilot-instructions.md`.

## When Adding New Tooling

- Add explicit commands for build/lint/test and a single-test format.
- Include required versions and setup steps in this file.
- Keep this guide close to 150 lines by replacing outdated content rather than
  appending indefinitely.
