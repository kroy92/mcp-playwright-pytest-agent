

# **Test Case: Verify that a user cannot Create Lead Without Company**

## **Test Steps**

| Step No | Action                                  | Test Data                                                    | Expected Result                                         |
| ------- | --------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------- |
| 1       | Launch CRM URL                          | `https://crm.zoho.in/crm/org60048002059/`                    | CRM login page is displayed                             |
| 2       | Login                                   | Username: `{username}`<br>Password: `{password}`<br> Click Sign in             | User is logged in and dashboard is displayed            |
| 3       | Click the **Leads** tab                 | -                                                            | Leads page is opened                                    |
| 4       | Click **Create Lead**                   | -                                                            | Create Lead form is opened                              |
| 5       | Enter Last Name and leave Company empty | **Last Name**: `Roy`<br>**Company**: *(leave empty)*                 | Last Name is entered; Company field is empty            |
| 6       | Click **Save**                          | -                                                            | Error message is displayed: "Company name is mandatory"  or Something similar|

---
