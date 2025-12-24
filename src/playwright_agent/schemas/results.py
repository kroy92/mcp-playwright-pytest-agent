"""
Result Schemas for Web Flow Execution
=====================================

This module defines Pydantic models for structured test results.
These schemas are used by the AI agent to report step-by-step
execution results in a consistent, parseable format.

Classes
-------
- `StepResult`: Result of a single test step (PASS/FAIL/BLOCKED)
- `RunResult`: Overall test run result containing all step results

Usage
-----
The schemas are passed to `run_flow()` as the output type:

    from playwright_agent import BaseFlowRunner, RunResult
    
    runner = BaseFlowRunner()
    result = runner.run_flow(steps, RunResult)  # Returns RunResult instance
    
    # Access results
    print(f"Overall: {result.status}")
    for step in result.steps:
        print(f"Step {step.step_id}: {step.status}")

Custom Assertions
-----------------
You can extend RunResult with custom fields for domain-specific checks:

    from pydantic import Field
    
    class LoginResult(RunResult):
        user_logged_in: bool = Field(description="True if login succeeded")
        dashboard_visible: bool = Field(description="True if dashboard loaded")
    
    result = runner.run_flow(steps, LoginResult)
    assert result.user_logged_in

"""

from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field


class StepResult(BaseModel):
    """
    Result schema for an individual step in a web flow.
    
    Each step in the test flow produces a StepResult with details about
    what was expected, what actually happened, and whether it passed.
    
    Attributes:
        step_id: Unique identifier for the step (e.g., "1", "2a")
        description: Human-readable description of the step action
        previous_step: Context from the previous step or "FIRST STEP"
        expected_result: What should happen if the step succeeds
        actual_result: What actually happened during execution
        status: PASS (expected==actual), FAIL (mismatch), BLOCKED (skipped)
        exception: Error details if the step failed
        locator: List of element locators used in this step
        next_step: AI reasoning about the result and next action
    """
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
    """
    Overall result schema for a complete web flow execution.
    
    This is the primary output type for `run_flow()`. It contains the
    overall pass/fail status plus detailed results for every step.
    
    Attributes:
        status: PASS only if ALL steps passed, otherwise FAIL
        failed_step_id: ID of the first step that failed (if any)
        proof_of_pass: Screenshot path or artifact for verification
        steps: List of StepResult objects in execution order
        exception: Summary explanation of pass/fail reason
        summary: High-level summary of the entire test run
    
    Example:
        result = runner.run_flow(steps, RunResult)
        
        if result.status == "FAIL":
            print(f"Failed at step: {result.failed_step_id}")
            print(f"Reason: {result.exception}")
        
        for step in result.steps:
            print(f"{step.step_id}: {step.status}")
    """
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

