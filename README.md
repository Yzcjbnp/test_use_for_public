# Use python to create templates for automatic testing at [OrangeHRM](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login)

### Test Case Name
Search Employee exist in Full-Time Permanent employee list.

### Expected Result
Employee status is displayed as full-time employee, in the sample code, we use "manda akhil user" as the search criteria.

### Unexpected result
Employee cannot be found or the status is displayed as part-time employee.

### Test Steps
1. Login OrangeHRM system(https://opensource-demo.orangehrmlive.com/web/index.php/auth/login). 
2. Go to PIM page, fillout "manda akhil user" and click search button.
3. Check result Employment Status as "Full-Time Permanent".

### How to run
```
pytest orangehrm.py
```

### Q&A
TBD
