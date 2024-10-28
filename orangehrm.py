import pytest
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestOrangeHRM:
    @pytest.fixture(scope="class")
    def setup(self):
        # Setup chrome webDriver
        self.driver = webdriver.Chrome()
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        yield self.driver
        self.driver.quit()

    def test_login(self, setup):
        driver = setup
        # Login system
        username_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
        username_input.send_keys("Admin")
        password_input.send_keys("admin123")
        password_input.send_keys(Keys.RETURN)

        # Verify login
        WebDriverWait(driver, 10).until(
            EC.title_contains("OrangeHRM")
        )
        assert "OrangeHRM" in driver.title

    def test_change_page(self, setup):
        driver = setup

        pim_menu = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))
        )
        pim_menu.click()

        # Confirm to jump to the PIM page
        page_title = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h6[contains(@class, 'oxd-topbar-header-breadcrumb-module') and text()='PIM']"))
        )
        assert "PIM" in page_title.text, "PIM page title not found"

    def test_add_employee(self, setup):
        driver = setup
      # Click add button
        add_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'oxd-button--secondary') and .//i[contains(@class, 'bi-plus')]]"))
        )
        add_button.click()

        # Waiting for the new addition to be successful
        page_title = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(@class, 'orangehrm-main-title') and text()='Add Employee']"))
        )

        # Verify whether it jumps to the Add Employee page
        page_title = driver.find_element(By.XPATH, "//h6[contains(@class, 'orangehrm-main-title') and text()='Add Employee']")
        assert "Add Employee" in page_title.text, "Add Employee page failed to load successfully"

        # Enter data in the First Name and Last Name input boxes
        first_name_field = driver.find_element(By.NAME, "firstName")
        last_name_field = driver.find_element(By.NAME, "lastName")
        first_name_field.send_keys("Orange")
        last_name_field.send_keys("Testuser")

        # Generate a random 6-digit employee number and enter it into the number field
        employee_id = str(random.randint(100000, 999999))
        employee_id_field = driver.find_element(By.XPATH,
                                                "//input[@class='oxd-input oxd-input--active' and not(@name)]")
        employee_id_field.send_keys(employee_id)
        time.sleep(3)
        # Click save button
        save_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'oxd-button--secondary') and text()=' Save ']"))
        )
        save_button.click()

        # Confirm that you have been redirected to the Personal Details page
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h6[contains(@class, 'orangehrm-main-title') and text()='Personal Details']"))
        )

        # Click save button
        save_button_personal_details = driver.find_element(By.XPATH,
                                                           "//button[contains(@class, 'oxd-button--secondary') and text()=' Save ']")
        save_button_personal_details.click()

        # Verify whether the jump is successful and save
        assert "Personal Details" in driver.page_source, "Personal Details page did not load successfully"

    def test_query_employee(self, setup):
        driver = setup

        pim_menu = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))
        )
        pim_menu.click()
        time.sleep(3)

        # Found employee name field and enter employee_name
        employee_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type for hints...']"))
        )
        employee_name_input.send_keys("Orange Testuser")
        time.sleep(3)
        # Click search button
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit' and contains(@class, 'oxd-button--secondary')]"))
        )
        search_button.click()

        # Check the results to verify whether the employee was successfully added
        search_result = driver.page_source
        assert "No Records Found" not in search_result, "Failed to add an employee. No record of the employee was found."
        time.sleep(5)
