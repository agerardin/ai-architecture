import asyncio
from prefect.client.orchestration import get_client
import redis


async def resume_paused_flow(flow_run_id, reason="approved"):
    async with get_client() as client:
        await client.resume_flow_run(flow_run_id=flow_run_id)
        print(f"Resumed flow run {flow_run_id} with reason: {reason}")


r = redis.Redis(host="localhost", port=6379, db=0)
flow_run_id = r.get("paused_flow_run_id")
if flow_run_id:
    flow_run_id = flow_run_id.decode().strip()  # decode from bytes to str
    print(f"Decoded flow run ID: {flow_run_id}")
    # Use flow_run_id directly in your Prefect resume call
else:
    print("No paused flow run ID found in Redis.")
asyncio.run(resume_paused_flow(flow_run_id))
