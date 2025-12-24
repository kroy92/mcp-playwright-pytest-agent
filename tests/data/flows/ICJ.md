## **Test**: Verify User is able to Perform Inventory Counting and Create On-Hand Counting Journal  
**NOTE:** DEFAULT STEP TIMEOUT: 30 SECONDS → Please try till 30 seconds for each step before failing.  
**NOTE:** If any unexpected popups appear, close them and continue.

| **Step No** | **Test Step**                                                                 | **Test Data**                               | **Expected Result**                                                                 |
|-------------|-------------------------------------------------------------------------------|---------------------------------------------|-------------------------------------------------------------------------------------|
| 1           | Launch the application                                                        | `{url}`                                     | Application should launch successfully                                             |
| 2           | Enter username and click **Next**                                             | `{username}`                                | Username should be accepted                                                        |
| 3           | Enter password and click **Login**                                            | `{password}`                                | User should be logged in successfully                                              |
| 4           | Click on Search    
| 5           | Type  **Counting**                                     | 'Counting' |  **Inventory management > Journal entries > Item counting**  list item  should appear 
| 6          | Click **Inventory management > Journal entries > Item counting**    List item                              | N/A |  **Item Counting** page should be displayed 
| 7          | Click **New** to create a new journal                                         | N/A                                         | New journal creation form should be displayed    . Note the Journal Number                                 |
| 8           | Enter '003800' in  **Site**                                             | 003800                              | Selected site should be displayed in the form                                      |
| 9          | Click **OK** to create Inventory Journal                                      | N/A                                         | Inventory Journal should be created successfully                                   |
| 10           | Click **Create Lines** and select **On-hand**                                 | N/A                                         | 'Create on-hand counting journal' form should appear                                |                                      |
| 11          | Click **OK**                                     | N/A                                         | User should see a message 'The Create on-hand counting journal job is added to the batch queue.'                            |
| 12          | Click Back button                                                        | N/A                                         | Page should close without errors                                                   |
| 13          | Click BAck button                                                | N/A                                         |  page should be closed                                                         |
| 14          | Log off from the application                                                  | N/A                                         | User should be logged off successfully                                             |

**IMPORTANT**: Use Reasonable retries and think like a smart manual tester