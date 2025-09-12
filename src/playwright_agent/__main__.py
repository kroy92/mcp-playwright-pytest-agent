from __future__ import annotations
import argparse
from pathlib import Path
from src.playwright_agent.runtime.base import BaseFlowRunner
from src.playwright_agent.schemas.results import RunResult

def main() -> None:
    parser = argparse.ArgumentParser(description="Run a Playwright MCP Agent flow.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--steps-file", help="Path to text/markdown/JSON flow steps")
    group.add_argument("--steps", help="Steps as a single string (quoted)")
    args = parser.parse_args()

    runner = BaseFlowRunner()
    steps_text = Path(args.steps_file).read_text(encoding="utf-8") if args.steps_file else args.steps
    result = runner.run_flow(steps_text, RunResult)

    try:
        print(result.model_dump_json(indent=2))  # pydantic v2
    except AttributeError:
        import json
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
