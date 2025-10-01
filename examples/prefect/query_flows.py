import asyncio
from prefect.client.orchestration import get_client
from prefect.client.schemas.filters import FlowFilter


async def list_deployments_by_flow_name(flow_name):
    async with get_client() as client:
        flow_filter = FlowFilter(name={"any_": [flow_name]})
        deployments = await client.read_deployments(flow_filter=flow_filter)
        for dep in deployments:
            print(dep.name, dep.id)


# Replace with your actual flow name
flow_name = "your-flow-name"
asyncio.run(list_deployments_by_flow_name(flow_name))


async def list_flows():
    async with get_client() as client:
        flows = await client.read_flows()
        print("Flows:")
        for flow in flows:
            print(f"- {flow.name} (ID: {flow.id})")


async def list_deployments_for_flow(flow_name):
    async with get_client() as client:
        flows = await client.read_flows()
        flow = next((f for f in flows if f.name == flow_name), None)
        if not flow:
            print(f"Flow '{flow_name}' not found.")
            return
        deployments = await client.read_deployments()
        print(f"Deployments for flow '{flow_name}':")
        for dep in deployments:
            print(f"- {dep.name} (ID: {dep.id})")


if __name__ == "__main__":
    asyncio.run(list_flows())
    # Replace 'my-flow' with your flow's name (hyphens, not underscores)
    asyncio.run(list_deployments_for_flow("my-flow"))
    asyncio.run(list_deployments_by_flow_name("my-flow"))
