from prefect import flow, task, pause_flow_run
from prefect.context import get_run_context
import redis


@task
def send_alert():
    print("ALERT: Please review and approve to continue.")


@flow
async def wait_for_human_approval():
    ctx = get_run_context()
    flow_run_id = str(ctx.flow_run.id)
    print(f"Paused flow run ID written to Redis: {flow_run_id}")
    # Connect to Redis (adjust host/port/db as needed)
    r = redis.Redis(host="localhost", port=6379, db=0)
    r.set("paused_flow_run_id", flow_run_id)
    print(f"Paused flow run ID written to Redis: {flow_run_id}")
    await pause_flow_run()
    print("Flow resumed after human approval.")
    return "approved"


@flow
def human_in_loop_flow():
    send_alert()
    import asyncio

    decision = asyncio.run(wait_for_human_approval())
    print("Decision:", decision)


if __name__ == "__main__":
    human_in_loop_flow()
