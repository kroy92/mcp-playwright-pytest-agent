# Test Case: Verify successful login with valid credentials  

**ID:** TC_Login_001  
**Priority:** High  
**Requirement:** User should be able to log in with valid credentials  

---

## Steps  

| Step # | Action | Expected Result |
|--------|--------|-----------------|
| 1 | Open `https://the-internet.herokuapp.com/login` | Login page loads successfully |
| 2 | Wait for the login form to appear | Username and Password fields are visible |
| 3 | Enter `tomsmith` in the **Username** field | Username is accepted |
| 4 | Enter `SuperSecretPassword!` in the **Password** field | Password is accepted |
| 5 | Click the **Login** button | Login request is submitted |
| 6 | Wait for message *“You logged into a secure area!”* | User is redirected to the secure area |
