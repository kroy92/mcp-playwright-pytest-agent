from __future__ import annotations
import argparse
import asyncio
from pathlib import Path
from src.playwright_agent.runtime.base import BaseFlowRunner
from src.playwright_agent.schemas.results import RunResult


async def run_flow(steps_text: str) -> None:
    """Run the flow asynchronously."""
    runner = BaseFlowRunner()
    result = await runner.run(steps_text, RunResult)

    try:
        print(result.model_dump_json(indent=2))  # pydantic v2
    except AttributeError:
        import json
        print(json.dumps(result, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a Playwright MCP Agent flow.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--steps-file", help="Path to text/markdown/JSON flow steps")
    group.add_argument("--steps", help="Steps as a single string (quoted)")
    args = parser.parse_args()

    steps_text = Path(args.steps_file).read_text(encoding="utf-8") if args.steps_file else args.steps
    asyncio.run(run_flow(steps_text))


if __name__ == "__main__":
    main()
