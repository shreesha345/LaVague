
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time

# Constants
BASE_URL = 'https://www.laposte.fr/'

# Scenarios
scenarios('demo_laposte.feature')

# Fixtures
@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Steps
@given('I am on the homepage')
def go_to_homepage(browser):
    browser.get(BASE_URL)

@when('I click on "J\'accepte" to accept cookies')
def accept_cookies(browser):
    accept_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[2]/button"))
    )
    try:
        browser.execute_script("arguments[0].click();", accept_button)
    except ElementClickInterceptedException:
        pytest.fail("Failed to accept cookies")

@when('I click on "Envoyer un colis"')
def click_send_package(browser):
    send_package_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div[2]/div/main/div/div[2]/div[4]/div/div/a[3]"))
    )
    try:
        browser.execute_script("arguments[0].click();", send_package_button)
    except ElementClickInterceptedException:
        pytest.fail("Failed to click on 'Envoyer un colis'")

@when('I click on the "Format du colis" dropdown under "Dimension"')
def click_format_dropdown(browser):
    format_dropdown = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div/main/div/div[2]/div[2]/div/div/div/div/div/div/div/div[3]/div[2]/fieldset/div"))
    )
    try:
        browser.execute_script("arguments[0].click();", format_dropdown)
    except ElementClickInterceptedException:
        pytest.fail("Failed to click on 'Format du colis' dropdown")

@when('I click on "Volumineux & tube" from the dropdown results')
def select_large_package(browser):
    large_package_option = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div/main/div/div[2]/div[2]/div/div/div/div/div/div/div/div[3]/div[2]/fieldset/div[2]/div/label[2]"))
    )
    try:
        browser.execute_script("arguments[0].click();", large_package_option)
    except ElementClickInterceptedException:
        pytest.fail("Failed to select 'Volumineux & tube'")

@when(parsers.parse('I enter {weight} in the "Poids" field'))
def enter_weight(browser, weight):
    weight_field = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/main/div/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/div[2]/div/div/div/div/input"))
    )
    weight_field.clear()
    weight_field.send_keys(weight)

@when('I wait for the cost to update')
def wait_for_cost_update():
    time.sleep(3)

@then(parsers.parse('the cost should be "{expected_cost}"'))
def verify_cost(browser, expected_cost):
    try:
        cost_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='calculator__cta__price']"))
        )
        actual_cost = cost_element.text.strip()
        assert actual_cost == expected_cost, f"Expected cost to be {expected_cost}, but got {actual_cost}"
    except Exception as e:
        pytest.fail(f"Failed to verify cost: {str(e)}")
