from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field

class RunResult(BaseModel):
    """Generic result schema for a web flow run."""
    status: Literal["PASS", "FAIL"] = Field(..., description="Overall test result - PASS if all steps  completed and all **Success conditions** met, else FAIL")
    exception: str | None = Field(None, description="Exception message if failed")
    failed_step_id: str | None = Field(None, description="Identifier of failed step, if any")
    proof_of_pass: str | None = Field(None, description="Final screenshot path")
