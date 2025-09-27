# AI Architecture

This project is a distributed semi-autonomous agent system. Agents communicate via an abstracted event bus/message broker, coordinate workflows, and support extensible identity, logging, and LLM proxying.

## Structure
- `agents/` - Individual agent implementations
- `infra/` - Infrastructure modules (event bus, context, logging, identity, LLM proxy)
- `workflows/` - Workflow orchestration (Prefect)
- `sdk/` - SDKs for different languages
- `tests/` - Test suite

## Next Steps
- Implement event bus abstraction
- Define context object
- Build orchestrator agent
- Set up logging/monitoring
- Integrate LLM proxy
- Add identity management
- Integrate Prefect
- Prepare SDKs
