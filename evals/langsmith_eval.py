import time

from langsmith import Client
from collections import defaultdict
from app.config import settings
from evals.run import CASES, PAUSE_SECONDS, REPEATS, find_problems, run_agent

DATASET_NAME = "abhimart-support-cases-v2"

client = Client()


def ensure_dataset() -> None:
    if client.has_dataset(dataset_name=DATASET_NAME):
        return
    dataset = client.create_dataset(DATASET_NAME)
    client.create_examples(
        dataset_id=dataset.id,
        examples=[
            {
                "inputs": {
                    "message": case["message"],
                    "customer_id": case.get("customer_id"),
                },
                "outputs": case,
                "metadata": {"category": case["category"]},
            }
            for case in CASES
        ],
    )


def target(inputs: dict) -> dict:
    start = time.perf_counter()
    tools, reply = run_agent(inputs["message"], inputs.get("customer_id"))
    seconds = time.perf_counter() - start
    time.sleep(PAUSE_SECONDS)
    return {"tools": tools, "reply": reply, "seconds": seconds}


def passed(outputs: dict, reference_outputs: dict) -> dict:
    problems = find_problems(reference_outputs, outputs["tools"], outputs["reply"])
    return {"key": "passed", "score": not problems, "comment": "; ".join(problems)}


def agent_seconds(outputs: dict) -> dict:
    return {"key": "agent_seconds", "score": outputs["seconds"]}


def print_summary(results) -> None:
    good = defaultdict(int)
    total = defaultdict(int)
    errors = 0
    for row in results:
        scores = [
            r.score for r in row["evaluation_results"]["results"] if r.key == "passed"
        ]
        if not scores:
            errors += 1
            continue
        category = row["example"].outputs["category"]
        total[category] += 1
        good[category] += int(scores[0])
    for category in total:
        print(f"{category}: {good[category]}/{total[category]}")
    print(f"errors (no verdict): {errors}")


if __name__ == "__main__":
    ensure_dataset()
    results = client.evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[passed, agent_seconds],
        experiment_prefix="after-ownership",
        num_repetitions=REPEATS,
        max_concurrency=1,
        metadata={"model": settings.gemini_model},
    )
    print_summary(results)
