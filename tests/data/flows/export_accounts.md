NOTE: DEFAULT STEP TIMEOUT : 30 SECONDS > Please try till 30 seconds for each step before failing.  
NOTE: If any unexpected popups appear, close them and continue.

## **Test**: Verify User is able to Export All Accounts (Select All)

| **Step No** | **Test Step**                                   | **Test Data**                         | **Expected Result**                         |
|-------------|-------------------------------------------------|---------------------------------------|---------------------------------------------|
| 1           | Launch URL and log in (enter username, password, click **Sign in**) | `{url}`, `{username}`, `{password}`   | Main page should be visible                 |
| 2           | Navigate to **Accounts**                        | N/A                                   | **Accounts** view should be displayed       |
| 3           | From the view dropdown, select **All Accounts** | N/A                                   | Grid should refresh with all accounts shown |
| 4           | Click **Select All** checkbox in grid header    | N/A                                   | All account rows should be selected         |
| 5           | Click **More Commands (…)** | N/A                                 | **More Commands** list should appear         
| 6          | Click **Export to Excel**                                | N/A                                   | Excel file with all accounts should download |
