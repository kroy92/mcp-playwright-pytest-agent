# mcp-playwright-pytest-agent

**mcp-playwright-pytest-agent** is an experimental project that combines **Playwright** for browser automation, **Pytest** for structured testing, and the **Model Context Protocol (MCP)** for context-aware orchestration. It’s designed for developers who want to explore **next-gen automation** while learning and having fun.



## Why This Project?

- **Context switching** between tools and workflows  
- **Dynamic environments** with popups, MFA, and flaky UI elements  
- **Integrating AI-driven orchestration** into existing test ecosystems  

This project tries to leverage Playwright MCP to create **context-driven automation tests**



## Key Features

- ✅ **Playwright + Pytest Integration** – Combine modern browser automation with robust testing  
- ✅ **Custom Assertions** – Define domain-specific success conditions
- ✅ **Bring Your Own Tools** – Plug in custom Python functions   
- ✅ **Bring Your Own MCP Servers** – Connect to external MCP-based services for extended capabilities  
- ✅ **Modular Design** – Flexible architecture for experimentation  


## Challenges & Learning Goals

- Implementing **self-healing automation** when elements change or fail  
- Managing **timeouts and retries** in unpredictable UI flows  
- Orchestrating **multi-step, context-aware scenarios** with MCP  
- Exploring **how AI agents can assist in real-world test automation**  



This is not just a tool—it’s a **sandbox for ideas**. Perfect for anyone curious about **AI-assisted testing**, **context-aware automation**, and **modern testing workflows**. Whether you’re experimenting with MCP, building custom tools, or integrating advanced orchestration into your tests, this project gives you a starting point to learn and innovate.


## Getting Started


Follow these steps to set up your environment and run your first test.

### 1. Install Python, uv and Node.js

Download and install Python from the official site:  
[Install Python - Download Python | Python.org](https://www.python.org/downloads/)

[Install uv - Installation | uv](https://docs.astral.sh/uv/getting-started/installation/)

[Install Node from Node.js — Download Node.js](https://nodejs.org/en/download/)

### 2. Clone the Repository

```bash
git clone https://github.com/kroy92/mcp-playwright-pytest-agent.git
cd mcp-playwright-pytest-agent
````

### 3. Copy the Sample .env File

```bash
cp .env.example .env
```

### 4. Fill in the Details in `.env` File

Open the `.env` file in your editor and update the required values.

### 5. Run Your First Test

Once everything is set up, run:

```bash
uv run pytest .\tests\e2e\test_first_examples.py
```

To see detailed results of steps performed  use -s flag

```bash
uv run pytest -s .\tests\e2e\test_first_examples.py
```
## **Basics**

Here’s a simple, step-by-step explanation of your First test in plain words:



### 1. Imports

```python
from __future__ import annotations
from playwright_agent.runtime.base import BaseFlowRunner
from playwright_agent.schemas.results import RunResult
```

* `BaseFlowRunner`: The main engine that **runs your test steps**.
* `RunResult`: A structure to hold the **outcome of the test** (pass/fail, exceptions, etc.).
* `__future__ import annotations`: Helps with **type hinting**, nothing to worry about for basic usage.



### 2. Create the Runner

```python
runner = BaseFlowRunner()
```

* You create an **instance of the runner**, which will execute your test flow.



### 3. Define the Test Function

```python
def test_google_search_inline():
```

* `test_google_search_inline` is a **test case**.
* Pytest will automatically detect and run any function starting with `test_`.



### 4. Write the Steps

```python
steps = """
Open https://the-internet.herokuapp.com/login
Wait for the login form to appear
Type "tomsmith" into the Username field
Type "SuperSecretPassword!" into the Password field
Click the Login button
Wait for the message "You logged into a secure area!" to appear
"""
```

* You describe the **test steps in plain English**.
* The runner will **read these steps and perform them in the browser**.



### 5. Run the Steps

```python
result = runner.run_flow(steps, RunResult)
```

* The `run_flow` method **executes the steps**.
* It returns a `RunResult` object containing:

  * `status`: Did the test **pass** or **fail**?
  * `exception`: Any **error messages** if something failed.
  * `failed_step_id`: The **step that failed** (if any).


---

### 6. Print the Result

```python
print(result)
````

* Shows the **test result in the console**.
* In **pytest**, `print()` output is only shown if you run tests with the `-s` flag:


### 7. Assert the Test Passed

```python
assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"
```

* Checks that the test **succeeded**.
* If it **failed**, it will print which step failed and why.


## **Data-Driven Test: Running Multiple Flows from Files**

We can also **run the same test logic with different flow files** by using **Pytest’s `@pytest.mark.parametrize`** feature.

```python
@pytest.mark.parametrize("steps_path", [
    "tests/data/flows/failed_login.md",
    "tests/data/flows/demo_login.md",
])
def test_generic_web_flows(steps_path: str):
    steps = pathlib.Path(steps_path).read_text(encoding="utf-8")
    result = runner.run_flow(steps, RunResult)
    print(result)
    assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"
    assert result.proof_of_pass, "Missing proof_of_pass (screenshot path)"
```

* Each `steps_path` points to a **file with plain-English steps** (e.g., login failed, demo login).
* Pytest will **execute the test once for each file**, making it **data-driven**.
* The flow steps are read from the file, executed by the runner, and the results are validated.


### Improving Reusability with Fixtures
---

Instead of creating the `runner` inside every test, we can use a **Pytest fixture** to manage it in one place. Fixtures let you define reusable setup code and inject it automatically into test functions.

#### **Example with Fixture**

```python
import pathlib
import pytest
from playwright_agent.schemas.results import RunResult
from playwright_agent.runtime.base import BaseFlowRunner


# Fixture to create and return a reusable runner
@pytest.fixture
def flow_runner():
    return BaseFlowRunner()


@pytest.mark.e2e
@pytest.mark.parametrize("steps_path", [
    "tests/data/flows/failed_login.md",
    "tests/data/flows/demo_login.md",
])
def test_generic_web_flows(flow_runner, steps_path: str):
    steps = pathlib.Path(steps_path).read_text(encoding="utf-8")
    result = flow_runner.run_flow(steps, RunResult)
    print(result)
    assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"
```

* `flow_runner` is defined **once** as a fixture.
* Any test that needs it can simply **add `flow_runner` as an argument**.
* Pytest automatically **provides the fixture** when running the test.

✅ **Benefit:** Makes tests **cleaner and easier to maintain**. If the runner setup ever changes, you only update the fixture, not every test.

This is demonstrated in test_from_files.py

```bash
uv run pytest  .\tests\e2e\test_from_files.py
```


## **Default Assertions**

In **MCP Playwright tests**, the overall **PASS/FAIL status** is determined by the AI agent. While this is usually reliable, it’s important to **verify each step explicitly** to catch hidden issues. Default assertions help ensure **both the flow and individual steps passed**.


### 

```python
@pytest.mark.parametrize("steps_path", [
    "tests/data/flows/verify_company_name.md",
])
def test_verify_company_name(flow_runner, steps_path: str):
    # Read the markdown file with flow steps
    steps = pathlib.Path(steps_path).read_text(encoding="utf-8")

    # Run the flow
    result = flow_runner.run_flow(steps, RunResult)
    print(result)

    # Assert overall flow passed
    assert result.status == "PASS", f"Flow failed: {result.exception} at {result.failed_step_id}"

    # Assert each step passed individually
    for step in result.steps:
        print(step, '\n')  # Print each step result if -s flag is enabled
        assert step.status == "PASS", (
            f"Step {step.step_id} failed: {step.exception}. "
            f"Expected: {step.expected_result}, Actual: {step.actual_result}"
        )
```

---

### **What’s Happening Here**

1. **Overall Flow Check**

   ```python
   assert result.status == "PASS"
   ```

   Confirms the test completed without AI-detected errors.

2. **Step-by-Step Checks**

   ```python
   for step in result.steps:
       assert step.status == "PASS"
   ```

   Validates that **every single step** in the flow executed successfully.

3. **Helpful Failure Messages**
   Each step assertion prints:

   * Which **step failed** (`step.step_id`)
   * The **exception**, if any
   * The **expected result vs actual result**



✅ **Takeaway:**
Default assertions provide **step-level safety nets**, ensuring that even if the AI marks the flow as passed, no hidden failures go unnoticed.



This is demonstrated in `test_default_assertions.py`

```bash
uv run pytest  .\tests\e2e\test_default_assertions.py
```
To see result of each step, enable -s flag


```bash
uv run pytest -s .\tests\e2e\test_default_assertions.py
```

While these default assertions provide a safety net, there may be situations where the AI **may still mark a flow as PASS** even if **critical business rules are violated** (for example, a form accepting invalid data). Since we **never truly know how LLMs may interpret each step**, **custom assertions may be needed** (explained in the next section) — to enforce **specific validations** and ensure that your tests **strictly follow business rules**, even when the AI may consider the flow successful.






## **Custom Assertions**
In **MCP Playwright tests**, the overall **PASS/FAIL status is often determined by the underlying LLM (AI agent)** interpreting your test steps.

* This is powerful, but it’s also **hit-or-miss**: the AI may incorrectly mark a step as “PASS” even if a business rule is violated.
* Example: Your CRM allows alphanumeric phone numbers. The AI may still mark the flow as PASS because all steps technically completed, **even though invalid data was entered**.

---

### **Solution: Custom Assertions**

To ensure your tests **enforce business rules reliably**, we extend the default result with **custom assertions**:

* Add **boolean flags** for key business rules (e.g., `phone_validation_passed`).


```python
class CustomRunResult(RunResult):
        phone_validation_passed: bool = Field(description="True if phone validation message appeared, else False")
```

This ensures your automation **guides the AI and verifies critical validations**, making tests more robust and reliable.





* The field tracks whether the **phone validation actually triggered**.
* Even if the AI marks the flow as `PASS`, this **ensures the business rule is enforced**.

When running the flow:

```python
result = flow_runner.run_flow(steps, CustomRunResult)
```

* The `CustomRunResult` is passed to the agent
* We then assert:

```python
assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"
assert result.phone_validation_passed, "Phone field accepted non-digit characters, validation failed."
```

* First line checks overall flow completion.
* Second line is the **custom assertion** — it fails the test if invalid phone input was accepted.

✅ **Takeaway:** Custom assertions let you **guide the AI and verify critical validations**, ensuring business rules are enforced even if the flow steps pass.

This is demonstrated in test_custom_assertions.py

```python
from __future__ import annotations
import pathlib
import pytest
from playwright_agent.schemas.results import RunResult
from playwright_agent.runtime.base import BaseFlowRunner
from pydantic import  Field
import os
from dotenv import load_dotenv
load_dotenv(override=True)


# Define a fixture that creates and returns a runner instance
@pytest.fixture
def flow_runner():
    return BaseFlowRunner()

@pytest.mark.parametrize("steps_path", [
    "tests/data/flows/verify_only_digits_allowed.md",
])
def test_generic_phone_number(flow_runner, steps_path: str):
    username = os.environ.get("CRM_USERNAME")
    password = os.environ.get("CRM_PASSWORD")

    if not username or not password:
        pytest.skip("Environment variables CRM_USERNAME or CRM_PASSWORD not set")

    # Read markdown and inject credentials using f-string formatting
    steps_template = pathlib.Path(steps_path).read_text(encoding="utf-8")
    steps = steps_template.format(username=username, password=password)

    # Define a custom RunResult class to include additional validation results
    # Add boolean flags for key business rules (e.g., phone_validation_passed)
    class CustomRunResult(RunResult):
        phone_validation_passed: bool = Field(description="True if phone validation message appeared, else False")

    # Run the flow and get results in the custom result class
    result = flow_runner.run_flow(steps, CustomRunResult)

    print(result) # Print result, if -s flag is enabled
    assert result.status == "PASS", f"Failed: {result.exception} at {result.failed_step_id}"
    assert result.phone_validation_passed, "Phone field accepted non-digit characters, validation failed."
```

When we run this test with an incorrect phone number:

```bash
uv run pytest -s .\tests\e2e\test_from_files.py
```

We get the following **assertion error**:

```
collected 1 item

tests/e2e/test_custom_assertions.py::test_generic_phone_number[tests/data/flows/verify_only_digits_allowed.md] status='PASS' exception=None failed_step_id=None proof_of_pass='C:\\VSCodeProjects\\mcp-playwright-pytest-agent\\.screenshots\\success_20250925T000000.png' phone_validation_passed=False
FAILED

================================================================================= FAILURES ==================================================================================
_________________________________________________ test_generic_phone_number[tests/data/flows/verify_only_digits_allowed.md] _________________________________________________
tests\e2e\test_custom_assertions.py:40: in test_generic_phone_number
    assert result.phone_validation_passed, "Phone field accepted non-digit characters, validation failed."
E   AssertionError: Phone field accepted non-digit characters, validation failed.
E   assert False
E    +  where False = CustomRunResult(status='PASS', exception=None, failed_step_id=None, proof_of_pass='C:\\VSCodeProjects\\mcp-playwright-pytest-agent\\.screenshots\\success_20250925T000000.png', phone_validation_passed=False).phone_validation_passed
========================================================================== short test summary info ==========================================================================
FAILED tests/e2e/test_custom_assertions.py::test_generic_phone_number[tests/data/flows/verify_only_digits_allowed.md] - AssertionError: Phone field accepted non-digit characters, validation failed.
======================================================================= 1 failed in 107.31s (0:01:47) =======================================================================
```

> **Note:** The overall flow status still shows **PASS**, but the **custom assertion** correctly identifies that the phone validation failed.

This demonstrates **how custom assertions can catch business rule violations** even when the AI-marked status indicates success.

### Upcoming Sections
1. Bring your own Tools
2. Bring your own MCP servers on need basis
