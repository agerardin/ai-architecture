# AI Architecture

Distributed AI agent system for robust, event-driven workflows with extensible infrastructure.

## Project Structure

- `src/ai_architecture/` — Main source code package
  - `infra/` — Infrastructure modules (event bus, context, logging, identity, LLM proxy)
  - `agents/` — Agent implementations
  - `workflows/` — Workflow orchestration (Prefect)
  - `sdk/` — SDKs for different languages
- `tests/` — Test suite
- `deploy/` — Deployment configs (Docker Compose, etc.)
- `LICENSE`, `NOTICE`, `README.md`, `pyproject.toml`, `pytest.ini` — Project metadata and config

## Setup

1. Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies (with dev/test extras):
   ```sh
   uv pip install --editable '.[dev]'
   ```

## Testing

Run all tests:
```sh
pytest
```

## Development Workflow
- All source code is under `src/ai_architecture/`.
- Use editable install for instant code/test feedback.
- Tests are auto-discoverable with `pytest.ini`.

## Features
- Async event bus abstraction (Redis backend)
- Context and session models (Pydantic)
- Agent orchestration and extensibility
- Identity, logging, and LLM proxy modules
- Workflow integration (Prefect)
- SDKs for multi-language support
- Docker Compose for local development

## Contributing
Pull requests and issues are welcome!

## License
Apache 2.0 — see LICENSE for details.

## Next Steps
- Build orchestrator agent
- Set up logging/monitoring
- Integrate LLM proxy
- Add identity management
- Integrate Prefect
- Prepare SDKs
