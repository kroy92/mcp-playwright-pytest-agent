## **Test**: Verify User is able to Convert the Lead to Opportunity  
**NOTE:** DEFAULT STEP TIMEOUT: 30 SECONDS → Retry each step for up to 30 seconds before failing.  
**NOTE:** If any unexpected popups appear, close them and continue.

---

### **Steps**

| **Step No** | **Test Step** | **Test Data** | **Expected Result** |
|-------------|---------------|---------------|----------------------|
| 1 | Launch `{url}` and log in: <br>• Enter username in **username textbox** <br>• Click **Next button** <br>• Enter password in **Password textbox** <br>• Click **Sign in button** | `{url}`, `{username}`, `{password}` | MFA prompt / Stay signed in / Main page should be visible |
| 2 | If prompted for MFA: <br>• Enter code in **MFA code textbox** <br>• Click **Verify button** | Use tools to fetch latest MFA code | Main page should load successfully |
| 3 | If prompted **Stay signed in?**, click **No button** | N/A | Main page should be visible |
| 4 | Navigate to **Leads**: <br>• Click **Leads navigation item** <br>• Wait for Copilot chat to fully load | N/A | Leads view should be displayed and Copilot chat fully loaded |
| 5 | Click **Read Only Grid menu item** on Lead Commands to hide it | N/A | Menu item should no longer be visible |
| 6 | Close Copilot: <br>• Click **Copilot Close button** | N/A | Copilot chat should be closed (welcome text not visible) |
| 7 | Click **New menu item** on Lead Commands | N/A | Lead creation form should be displayed |
| 8 | Enter values in Lead form: <br>• Topic in **Topic input** <br>• First Name in **First Name input** <br>• Last Name in **Last Name input** | `{lead_name}`, `{FIRST_NAME}`, `{LAST_NAME}` | Fields should accept and display entered values |
| 9 | Click **Save button** | N/A | Lead should be saved successfully |
| 10 | Verify Lead header matches `{FIRST_NAME} {LAST_NAME}` | `{FIRST_NAME} {LAST_NAME}` | Header should match entered name |
| 11 | Click **Qualify menu item** under Lead Commands | N/A | **Qualify Lead** dialog should appear; no duplicate dialogs |
| 12 | Click **Qualify button** in Qualify dialog | N/A | **Finish button** should appear |
| 13 | Click **Finish button** | N/A | Opportunity page should be displayed (URL contains `etn=opportunity`) |
| 14 | Take final screenshot and close browser | N/A | Browser should be closed, no instance running |

