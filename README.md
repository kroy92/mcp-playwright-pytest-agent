# mcp-playwright-pytest-agent- [mcp-playwright-pytest-agent](#mcp-playwright-pytest-agent)
- [mcp-playwright-pytest-agent- mcp-playwright-pytest-agent](#mcp-playwright-pytest-agent--mcp-playwright-pytest-agent)
  - [Why This Project?](#why-this-project)
  - [Key Features](#key-features)
  - [Challenges \& Learning Goals](#challenges--learning-goals)
  - [**Getting Started**](#getting-started)
    - [1. Install Python, uv and Node.js](#1-install-python-uv-and-nodejs)
    - [2. Clone the Repository](#2-clone-the-repository)
    - [3. Copy the Sample .env File](#3-copy-the-sample-env-file)
    - [4. Fill in the Details in `.env` File](#4-fill-in-the-details-in-env-file)
    - [5. Run Your First Test](#5-run-your-first-test)
  - [**Basics**](#basics)
    - [1. Imports](#1-imports)
    - [2. Create the Runner](#2-create-the-runner)
    - [3. Define the Test Function](#3-define-the-test-function)
    - [4. Write the Steps](#4-write-the-steps)
    - [5. Run the Steps](#5-run-the-steps)
    - [6. Print the Result](#6-print-the-result)
    - [7. Assert the Test Passed](#7-assert-the-test-passed)
  - [**Data-Driven Test: Running Multiple Flows from Files**](#data-driven-test-running-multiple-flows-from-files)
    - [Improving Reusability with Fixtures](#improving-reusability-with-fixtures)
      - [**Example with Fixture**](#example-with-fixture)
  - [**Default Assertions**](#default-assertions)
    - [Example](#example)
    - [What’s Happening Here](#whats-happening-here)
  - [**Custom Assertions**](#custom-assertions)
    - [Solution: Custom Assertions](#solution-custom-assertions)
  - [**Bring Your Own Tools**](#bring-your-own-tools)
  - [**Bring Your Own MCP Server**](#bring-your-own-mcp-server)
    - [Key Concepts](#key-concepts)
      - [1. **Configuring the External MCP Server**](#1-configuring-the-external-mcp-server)
      - [2. **Launching and Using the MCP Server in Your Test**](#2-launching-and-using-the-mcp-server-in-your-test)
      - [3. **Assertions and Step Results**](#3-assertions-and-step-results)
  - [Full Example: test\_example\_with\_dataverse\_mcp.py](#full-example-test_example_with_dataverse_mcppy)


**mcp-playwright-pytest-agent** is an experimental project that combines **Playwright** for browser automation, **Pytest** for structured testing, and the **Model Context Protocol (MCP)** for context-aware orchestration. It’s designed for developers who want to explore **next-gen automation** while learning and having fun.

<img src="mcp-playwright-pytest-agents.png" alt="Architecture Diagram" width="800"/>


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


## **Getting Started**


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

### Example
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

### What’s Happening Here

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

### Solution: Custom Assertions

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



## **Bring Your Own Tools**

Sometimes the default agent capabilities may not be enough. For example, you may need to generate an MFA code, fetch values from an external service, or create dynamic test data. In such cases, you can bring your own tools and plug them into the flow runner.

A tool is a normal Python function decorated with `@function_tool`. Once registered, the agent can **autonomously decide** to call it whenever required by the test steps.

```python
from agents.tool import function_tool # Import the decorator

# Define a tool to generate TOTP codes for MFA
@function_tool()
def get_totp() -> str:
    """Generate a MFA code for Login."""
    mfa_key = os.getenv("D365_MFA_KEY")  # Not required by default
    if not mfa_key:
        raise ValueError("MFA key is not configured.")
    return pyotp.TOTP(mfa_key).now()
```

The above function reads the secret key from `D365_MFA_KEY` and returns a one-time code.

The tool is then passed into the flow runner:

```python
result = flow_runner.run_flow(steps, RunResult, tools=[get_totp])
```

This ensures the agent generates the code just-in-time, instead of relying on an expired value. Calling the function directly and placing the result in your test steps file will not work, because the code will expire before the step is executed.

This behavior can be demonstrated by running:

```bash
uv run pytest .\tests\e2e\test_example_using_tools.py
```

use - s flag to see result of all steps

```bash
uv run pytest .\tests\e2e\test_example_using_tools.py
```

**How It Works Under the Hood**

When you decorate a function with `@function_tool`, the Agent SDK does several things automatically:

1. **Wraps the function with a schema definition** so the agent knows what inputs and outputs to expect.
2. **Passes this schema to the LLM** when running your flow, so the model can understand the function signature.
3. **Calls the function** whenever the agent decides it is needed during the flow.
4. **Feeds the result back to the LLM**, allowing the agent to continue execution with the updated value — all without any extra code from you.

This means that by just using the decorator, your function becomes a fully integrated tool that the agent can **autonomously decide** to call during test execution.

## **Bring Your Own MCP Server**


While this framework is primarily designed around Playwright MCP, you can **bring in other MCP servers** to support your tests whenever your scenario requires interaction with external systems (such as Dataverse, Azure DevOps (ADO), JIRA, or custom business process MCPs). This makes your automation extensible and ready for complex, cross-system flows.


**For example:**  
You can use **Dataverse MCP** to quickly create an opportunity record (your test data) right in your enterprise database—Dataverse, in this case—as the first step of your test. This means your test can focus on what really matters: checking the actual business process, like moving through all the BPF stages and closing the opportunity as "Won." You don’t have to waste time on setup or pre-requisite steps. This way, your automation is more reliable, efficient, and truly tests the real user journey—not just the data setup.


### Key Concepts

#### 1. **Configuring the External MCP Server**

To connect to an external system, you define the server parameters using `StdioServerParameters`. For example, to launch a Dataverse MCP server:

```python
# Key import for this snippet:
from mcp import StdioServerParameters

dataverse_mcp_param = StdioServerParameters(
    command="Microsoft.PowerPlatform.Dataverse.MCP",
    args=[
        f"--ConnectionUrl={connection}",
        "--MCPServerName=DataverseMCPServer",
        f"--TenantId={tenant}",
        "--EnableHttpLogging=true",
        "--EnableMsalLogging=false",
        "--Debug=false",
        "--BackendProtocol=HTTP",
    ],
)
```
- **Purpose:** This block specifies how to start the Dataverse MCP server, passing all required connection and logging arguments.
- **Why:** It enables the agent to interact with Dataverse as part of your test flow.

#### 2. **Launching and Using the MCP Server in Your Test**

The test launches the MCP server as a context manager and passes it to the agent runner:

```python
# Key imports for this snippet:
from agents.mcp.server import MCPServerStdio, MCPServerStdioParams
from agents.mcp import create_static_tool_filter

async with MCPServerStdio(
    params=MCPServerStdioParams(dataverse_mcp_param),
    client_session_timeout_seconds=120,
    tool_filter=create_static_tool_filter(allowed_tool_names=["create_record"])
) as dataverse_mcp:
    result = await flow_runner._run_agent_flow(
        steps,
        RunResult,
        tools=[get_totp],
        mcp_servers=[dataverse_mcp],  # Here we use Dataverse MCP
    )
```
- **What’s new:**  
  - The MCP server is started only for the duration of the test, ensuring clean resource management.
  - The `tool_filter` restricts the agent to only the tools you want to expose (here, just `create_record`).
  - The `mcp_servers` argument allows you to pass one or more MCP server instances to the agent, making it possible to orchestrate actions across multiple systems.

#### 3. **Assertions and Step Results**

The rest of the test asserts that the flow and each step passed, as in your previous examples.



**This pattern—configuring, launching, and passing an external MCP server to your agent—is how you extend your Playwright MCP framework to support any system with an MCP interface.**

This is demonstrated in the file **test_example_with_dataverse_mcp.py**.



## Full Example: test_example_with_dataverse_mcp.py



```python
import os
import pathlib
from datetime import date

import pyotp
import pytest
from dotenv import load_dotenv

# Key imports for MCP server integration:
from agents.mcp.server import MCPServerStdio, MCPServerStdioParams
from agents.mcp import create_static_tool_filter
from mcp import StdioServerParameters

from agents.tool import function_tool
from playwright_agent.runtime.base import BaseFlowRunner
from playwright_agent.schemas.results import RunResult

@function_tool()
def get_totp() -> str:
    """Generate a MFA code for Login."""
    mfa_key = os.getenv("D365_MFA_KEY")
    if not mfa_key:
        raise ValueError("MFA key is not configured.")
    return pyotp.TOTP(mfa_key).now()

@pytest.fixture
def flow_runner():
    """Fixture to provide a BaseFlowRunner instance."""
    return BaseFlowRunner()

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "steps_path",
    [
        "tests/data/flows/business_process_flow.md",
    ],
)
async def test_business_process_opportunity(flow_runner, steps_path):
    """
    Tests User is able to navigate all BPF stages of an opportunity.
    """
    load_dotenv(override=True)

    url = os.getenv("DYNAMICS_CRM_URL")
    username = os.getenv("D365_USERNAME")
    password = os.getenv("D365_PASSWORD")
    connection = os.getenv("DATAVERSE_CONNECTION_URL")
    tenant = os.getenv("DATAVERSE_TENANT_ID")

    if not all([url, username, password, connection, tenant]):
        pytest.skip("Required environment variables for D365/Dataverse are not set.")

    opp_name = "OCR extraction of Polling Booth records for ECI India"
    today_str = str(date.today())

    steps_template = pathlib.Path(steps_path).read_text(encoding="utf-8")
    steps = steps_template.format(
        url=url,
        username=username,
        password=password,
        OpportunityName=opp_name,
        today=today_str,
    )

    dataverse_mcp_param = StdioServerParameters(
        command="Microsoft.PowerPlatform.Dataverse.MCP",
        args=[
            f"--ConnectionUrl={connection}",
            "--MCPServerName=DataverseMCPServer",
            f"--TenantId={tenant}",
            "--EnableHttpLogging=true",
            "--EnableMsalLogging=false",
            "--Debug=false",
            "--BackendProtocol=HTTP",
        ],
    )

    async with MCPServerStdio(
        params=MCPServerStdioParams(dataverse_mcp_param),
        client_session_timeout_seconds=120,
        tool_filter=create_static_tool_filter(allowed_tool_names=["create_record"])
    ) as dataverse_mcp:
        result = await flow_runner._run_agent_flow(
            steps,
            RunResult,
            tools=[get_totp],
            mcp_servers=[dataverse_mcp],
        )

    assert result.status == "PASS", f"Flow failed: {result.exception} at {result.failed_step_id}"
    for step in result.steps:
        print(step, '\n')
        assert (
            step.status == "PASS"
        ), f"Step {step.step_id} failed: {step.exception}. Expected: {step.expected_result}, Actual: {step.actual_result}"
```

This behavior can be demonstrated by running:
   ```bash
   uv run pytest -s .tests\e2e\test_example_with_dataverse_mcp.py
   ```
   - The `-s` flag will print step-by-step results to the console.



**Tip:**  
For a detailed HTML report of your test results, run your tests with this flag:
```bash
uv run pytest --html=reports/test_example.html .tests\e2e\
```
This will generate a user-friendly report you can easily review and share.

