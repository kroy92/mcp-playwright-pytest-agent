# MCP Playwright Test Agent (pytest + uv)

A **generic** test agent that uses an **LLM** to control a **Playwright MCP** server.
Write flows as plain text (or JSON) and execute them with **pytest**

## Features
- Pytest-first: idiomatic tests, fixtures, markers
- MCP Playwright browser control
- LLM agent executes human-readable steps deterministically
- Final screenshots + typed results for assertions
- Run from **steps file**, **inline string**, or **named pytest tests**

## Requirements
- Python 3.12+
- Node.js with `npx`
- Azure OpenAI (or compatible)
- OpenAI Agent SDK
  
