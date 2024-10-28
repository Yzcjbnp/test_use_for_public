# Use python to create templates for automatic testing at [OrangeHRM](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login)

### Test Case Name
Search for employees that exist in the employee list.

### Expected Result
Employees can be added and can be searched on the PIM page.

### Unexpected result
The employee cannot be found or the employee cannot be added.

### Test Steps
1. Log in to the OrangeHRM system (https://opensource-demo.orangehrmlive.com/web/index.php/auth/login).
2. Enter the PIM page, click the add button, and enter an employee's information including First name, Last name and a six-digit random ID.
3. Return to the PIM page, enter the employee’s name, and click Search
4. The check result is that the employee exists.

### How to run
```
pytest orangehrm.py
```

### Q&A
TBD
