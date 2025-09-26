
---

## **Jira Test Case: Failed Login Flow**

**Summary:** Verify login fails with invalid credentials
**Priority:** High
**Requirement / Story:** User should not be able to log in with invalid credentials

### Steps

| Step # | Action                  | Test Data                                  | Expected Result                                                                     |
| ------ | ----------------------- | ------------------------------------------ | ----------------------------------------------------------------------------------- |
| 1      | Open login page         | `https://the-internet.herokuapp.com/login` | Login page loads successfully                                                       |
| 2      | Wait for the login form | -                                          | Username and Password fields are visible                                            |
| 3      | Enter Username          | `invalidUser`                              | Username is accepted                                                                |
| 4      | Enter Password          | `wrongPassword`                            | Password is accepted                                                                |
| 5      | Click Login button      | -                                          | Login request is submitted                                                          |
| 6      | Wait for error message  | -                                          | *“Your username is invalid!”* (or similar) is displayed; user remains on login page |

---
