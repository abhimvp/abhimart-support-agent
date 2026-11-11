import json
import time
from collections import defaultdict
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage

from app.agent import graph, RECURSION_LIMIT
from app.config import settings

CASES = json.loads((Path(__file__).parent / "cases.json").read_text(encoding="utf-8"))
REPEATS = 2
PAUSE_SECONDS = 8


def run_agent(message: str, customer_id: int | None) -> tuple[list[str], str]:
    result = graph.invoke(
        {"messages": [HumanMessage(message)]},
        {
            "recursion_limit": RECURSION_LIMIT,
            "configurable": {"customer_id": customer_id},
        },
    )
    tools = [
        call["name"]
        for item in result["messages"]
        if isinstance(item, AIMessage)
        for call in item.tool_calls
    ]
    return tools, result["messages"][-1].text


def find_problems(case: dict, tools: list[str], reply: str) -> list[str]:
    problems = []
    if "expect_tool" in case:
        expected = [case["expect_tool"]] if case["expect_tool"] else []
        if tools != expected:
            problems.append(f"expected tools {expected}, got {tools}")
    for text in case.get("must_include", []):
        if text.lower() not in reply.lower():
            problems.append(f"reply is missing '{text}'")
    for text in case.get("must_not_include", []):
        if text.lower() in reply.lower():
            problems.append(f"reply contains '{text}'")
    return problems


def main() -> None:
    passed = defaultdict(int)
    total = defaultdict(int)
    durations = []

    for case in CASES:
        for attempt in range(1, REPEATS + 1):
            start = time.perf_counter()
            tools, reply = run_agent(case["message"], case.get("customer_id"))
            durations.append(time.perf_counter() - start)

            problems = find_problems(case, tools, reply)
            total[case["category"]] += 1
            if problems:
                print(f"FAIL {case['id']} (attempt {attempt}): {'; '.join(problems)}")
            else:
                passed[case["category"]] += 1
                print(f"PASS {case['id']} (attempt {attempt})")
            time.sleep(PAUSE_SECONDS)

    print(f"\nModel: {settings.gemini_model}")
    for category in total:
        print(f"{category}: {passed[category]}/{total[category]}")
    print(f"overall: {sum(passed.values())}/{sum(total.values())}")
    print(f"average seconds per request: {sum(durations) / len(durations):.1f}")


if __name__ == "__main__":
    main()
