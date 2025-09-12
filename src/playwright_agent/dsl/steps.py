"""
Placeholder for a future structured steps DSL.

Example JSON to support later:
{
  "steps": [
    {"action": "open", "url": "https://example.com"},
    {"action": "type", "selector": {"role": "textbox", "name": "Search"}, "text": "Playwright MCP Agent"},
    {"action": "press", "key": "Enter"},
    {"action": "wait_for", "text": "Results"},
    {"action": "click", "selector": {"role": "link", "nth": 0}},
    {"action": "screenshot", "full_page": true}
  ]
}
"""
