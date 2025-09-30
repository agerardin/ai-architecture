import time
from prefect import flow


@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello, {name}!")
    time.sleep(10)
    print("Flow complete!")


if __name__ == "__main__":
    my_flow.deploy(
        name="my-deployment-2",
        work_pool_name="docker-pool",
        image="my-registry.com/my-docker-image:my-tag",
        push=False,  # switch to True to push to your image registry
    )
