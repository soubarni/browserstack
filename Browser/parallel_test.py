import pytest
from selenium import webdriver
from main import run_scraper

# BrowserStack credentials
USERNAME = "soubarnikas_7IOvsS"
ACCESS_KEY = "GXUNrmpaJC4dfSPuMFdE"

# Correct W3C-compliant BrowserStack capabilities
@pytest.fixture(scope="function")
def driver():
    capabilities = {
        "browserName": "Chrome",
        "browserVersion": "120.0",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "local": "true",
            "seleniumVersion": "4.20.0",  # Match your local selenium version if needed
            "projectName": "BrowserStack Sample",
            "buildName": "bstack-demo",
            "sessionName": "Parallel Test",
            "debug": "true",
            "networkLogs": "true",
            "consoleLogs": "info"
        }
    }

    driver = webdriver.Remote(
        command_executor=f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
        desired_capabilities=capabilities
    )

    yield driver
    driver.quit()


def test_run_scraper(driver):
    try:
        run_scraper(driver)
    except Exception as e:
        pytest.fail(f"Test failed due to: {e}")
