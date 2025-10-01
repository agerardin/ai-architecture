from time import sleep
from uuid import UUID

from prefect import flow, task
from prefect.artifacts import (
    create_progress_artifact,
    update_progress_artifact,
)


def fetch_batch(i: int):
    # Simulate fetching a batch of data
    sleep(2)


@task
def fetch_in_batches():
    progress_artifact_id = create_progress_artifact(
        progress=0.0,
        description="Indicates the progress of fetching data in batches.",
    )
    for i in range(1, 11):
        fetch_batch(i)
        if isinstance(progress_artifact_id, UUID):
            update_progress_artifact(artifact_id=progress_artifact_id, progress=i * 10)


@flow
def etl():
    fetch_in_batches()


if __name__ == "__main__":
    etl()
