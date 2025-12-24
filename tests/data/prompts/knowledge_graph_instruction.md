**Locator Handling with Knowledge Graph Hints**

1. **Before Execution**
   - Load locator hints from Knowledge Graph for all steps (use as first attempt only).

2. **During Execution**
   - Try the hinted locator first.
   - If it fails within the default timeout, **fallback to dynamic discovery** (updated attributes, text, roles, etc.).
   - If a new locator works, **update the Knowledge Graph with this new locator** (replace the old one).

3. **Rule**
   - Only update after a successful fallback.
   - After Test Completed, Check If you need updates to locators

