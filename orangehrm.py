import pytest
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
        username_input.send_keys("Admin")
        password_input.send_keys("admin123")
        password_input.send_keys(Keys.RETURN)
            
        # Verify login
        WebDriverWait(driver, 10).until(
            EC.title_contains("OrangeHRM")
        )
        assert "OrangeHRM" in driver.title

    def test_search_employee(self, setup):
        driver = setup
        # Go to PIM page
        pim_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))
        )
        pim_menu.click()

        # Found employee name field and keyin employee_name
        employee_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type for hints...']"))
        )
        employee_name_input.send_keys("manda akhil user")

        # Click Search button
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit' and contains(@class, 'oxd-button--secondary')]"))
        )
        search_button.click()

        # Check result is match
        try:
            # Use "presence_of_element_located" and wait timeout as 60s
            result = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(text(), 'Full-Time Permanent')]")
                )
            )
            assert result.is_displayed(), "Result include 'Full-Time Permanent'"
        except TimeoutException:
            print(driver.page_source)  #Output HTML page
            pytest.fail("Result not include 'Full-Time Permanent'")
