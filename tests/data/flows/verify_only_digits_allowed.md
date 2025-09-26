

# **Test Case: Verify that the Phone Field Accepts Only Digits on Create Lead Form**

| Step No | Action                  | Test Data                                                    | Expected Result                                                                               |
| ------- | ----------------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| 1       | Launch CRM URL          | `https://crm.zoho.in/crm/org60048002059/`                    | CRM login page is displayed                                                                   |
| 2       | Login                   | Username: `{username}`<br>Password: `{password}`  | User is logged in and dashboard is displayed                                                  |
| 3       | Click the **Leads** tab | -                                                            | Leads page is opened                                                                          |
| 4       | Click **Create Lead**   | -                                                            | Create Lead form is opened                                                                    |
| 5       | Enter Last Name         | `Roy`                                                        | Last Name is accepted                                                                         |
| 6       | Enter Company           | `TestCompany`                                                | Company field is accepted                                                                     |
| 7       | Enter Phone number      | `123ABC456`                                                  | Only digits are allowed; non-digit characters are rejected or error message displayed         |
| 8       | Click **Save**          | -                                                            | Lead is **not created**; validation message is shown: "Phone number must contain digits only" |
