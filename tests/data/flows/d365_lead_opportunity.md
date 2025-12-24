
NOTE: DEFAULT STEP TIMEOUT : 30 SECONDS> Please try till 30 seconds for each step before failing.
    NOTE: If any unexpected popups appear, close them and continue.

   ## **Test**: Verify User is able to Convert the Lead to Opportunity
NOTE: DEFAULT STEP TIMEOUT : 30 SECONDS > Please try till 30 seconds for each step before failing.  
NOTE: If any unexpected popups appear, close them and continue.

## **Test**: Verify User is able to Convert the Lead to Opportunity

| **Step No** | **Test Step**                                                                 | **Test Data**                       | **Expected Result**                                                                 |
|-------------|-------------------------------------------------------------------------------|-------------------------------------|-------------------------------------------------------------------------------------|
| 1           | Launch URL and log in (enter username, click **Next**, enter password, click **Sign in**) | `{url}`, `{username}`, `{password}` | MFA prompt / Stay signed in / Main page should be visible                           |
| 2           | If prompted for MFA, enter the current code                                   | Use tools to fetch latest MFA code  | Main page should load successfully                                                  |
| 3           | If prompted "Stay signed in?", click **No** and wait for main page            | N/A                                 | Main page should be visible                                                         |
| 4           | Navigate to **Leads** and wait Copilot chat to fully load                                                      | N/A                                 | **Leads** view should be displayed                                                  |
| 5           | Click on **Read Only Grid** menuitem on Lead Commands to hide it                     | N/A                                 |After click  **Read Only Grid** menuitem should not be visible on Lead Commands                                          |
| 6           | Click close button in Copilot                | N/A                                 | Copilot chat should be closed (text *"Welcome to Copilot. Select one of the suggestions below to get started"* not visible) |
| 7           | Click **Create a New Lead Record** Menuitem  on Lead Commands                                | N/A                                 | Lead creation form should be displayed                                              |
| 8           | Enter topic name, first name, and last name in the lead creation form         | `{lead_name}`, `{FIRST_NAME}`, `{LAST_NAME}` | Fields should accept and display entered values                                     |
| 9           | Click **Save** image                                                          | N/A                                 | Lead should be saved successfully                                                   |
| 10          | Verify Lead’s Name in header                                                  | `{FIRST_NAME} {LAST_NAME}`          | Header should match entered name                                                    |
| 11          | Click **Phone** image under Lead Commands,  | N/A                                 | A **Qualify Lead** dialog should appear; no Duplicate dialogs should appear       
|12 |Click **Qualify** button on  **Qualify Lead** dialog    | N/A | **Finish** button should appear
| 13          | Click **Finish** button                                                       | N/A                                 | **Opportunity** page should be displayed                                            |
| 14          | Close the browser                                                             | N/A                                 | Browser should be closed, no instance running                                       |
