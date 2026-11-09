import time

from langsmith import Client

from app.config import settings
from evals.run import CASES, PAUSE_SECONDS, REPEATS, find_problems, run_agent

DATASET_NAME = "abhimart-support-cases"

client = Client()


def ensure_dataset() -> None:
    if client.has_dataset(dataset_name=DATASET_NAME):
        return
    dataset = client.create_dataset(DATASET_NAME)
    client.create_examples(
        dataset_id=dataset.id,
        examples=[
            {
                "inputs": {"message": case["message"]},
                "outputs": case,
                "metadata": {"category": case["category"]},
            }
            for case in CASES
        ],
    )


def target(inputs: dict) -> dict:
    tools, reply = run_agent(inputs["message"])
    time.sleep(PAUSE_SECONDS)
    return {"tools": tools, "reply": reply}


def passed(outputs: dict, reference_outputs: dict) -> dict:
    problems = find_problems(reference_outputs, outputs["tools"], outputs["reply"])
    return {"key": "passed", "score": not problems, "comment": "; ".join(problems)}


if __name__ == "__main__":
    ensure_dataset()
    client.evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[passed],
        experiment_prefix="baseline",
        num_repetitions=REPEATS,
        max_concurrency=1,
        metadata={"model": settings.gemini_model},
    )
