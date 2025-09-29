from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field

class StepResult(BaseModel):
    """Result schema for an individual step in a web flow."""
    step_id: str = Field(description="Identifier of the step")
    description: str = Field(description="Description of the current step")
    previous_step: str = Field(description="Description of did you completed previous step and what you did in previous step, or 'FIRST STEP' if this is the first step")
    expected_result: str = Field(description="What should have happened in this step")
    actual_result: str = Field(
        description="What actually happened in this step (None if not executed)"
    )
    status: Literal["PASS", "FAIL", "BLOCKED"] = Field(
        description=(
            "PASS if Expected == Actual. "
            "FAIL if Expected != Actual. "
            "BLOCKED if this step was not executed because a previous step failed."
        )
    )
    exception: str | None = Field(
        description="Exception or error details if this step failed"
    )
    locator: list[str] = Field(description="List of locators used in the step, if any")
    next_step: str = Field(description="considering you are a tester, Think again deeply if it PASS or FAIL , did you hallucinated and what to do next")


class RunResult(BaseModel):
    """Generic result schema for a web flow run."""
    status: Literal["PASS", "FAIL"] = Field(
        description="PASS only if all steps have status PASS. "
                    "FAIL if any step has status FAIL or BLOCKED."
    )
    failed_step_id: str | None = Field(
        None, description="Identifier of the first failed step, if any"
    )
    proof_of_pass: str  = Field(
        None, description="Final screenshot or artifact path if run passed or screenshot of failure point"
    )
    steps: list[StepResult] = Field(
        ..., description="Detailed results of all steps in execution order"
    )
    exception: str | None = Field(
        description="Concise tester-style explanation of why the run passed or failed"
    )
    summary: str | None = Field(
        description="Concise tester-style summary of the entire run"
    )   

