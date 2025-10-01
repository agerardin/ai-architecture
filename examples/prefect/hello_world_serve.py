from random import randint
from prefect import flow, task
from prefect.deployments import run_deployment


@flow
def think():
    import time

    print("Thinking...")
    time.sleep(5)
    decision = randint(1, 2)
    if decision == 1:
        print("I have decided to say goodbye right away.")
    else:
        print("I have decided to run another workflow.")
    run_deployment("my-flow/my-deployment-2", parameters={"name": "Alice"})
    print("Done thinking!")


@flow
def hello(name):
    print(f"Hello {name} from Prefect! 🤗")


@task
def goodbye(name):
    print(f"Goodbye {name}! 👋")


@flow(log_prints=True)
def hello_world(name: str = "world", bye: bool = False):
    hello(name)
    think()
    if bye:
        goodbye(name)


if __name__ == "__main__":
    # creates a deployment and starts a long-running
    # process that listens for scheduled work
    hello_world.serve(
        name="my-first-deployment",
        tags=["onboarding"],
        parameters={"bye": True},
        interval=60,
    )
