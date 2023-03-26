import pytest
import time
import logging
from datetime import datetime
import os,sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture(params=["chrome", "firefox"])
def browser(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError("Invalid browser name")
    yield driver
    driver.quit()

def take_screenshot(browser, exception):
    screenshot_folder = os.path.join(os.getcwd(), "screenshots")
    os.system(f'rm -R {screenshot_folder}/*')
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H-%M-%S")
    filename = f"test_failed_{timestamp}.png"
    screenshot_path = os.path.join(os.getcwd(), "screenshots", filename)
    browser.save_screenshot(screenshot_path)
    logging.info(f'{exception}. Screenshot is saved to {screenshot_path}')

def test_insider_careers(browser):
    #Visit Insider home page
    logging.info("Visiting Insider home page")
    browser.maximize_window()
    browser.get("https://useinsider.com/")
    assert "Insider" in browser.title, take_screenshot(browser, f"Insider page not opened in {browser.name} browser")
    wait = WebDriverWait(browser, 10)

    #Select Careers page from More menu
    logging.info('Selecting "Careers" from "More" menu')
    cookie = browser.find_element(By.ID, 'wt-cli-accept-all-btn')
    cookie.click()
    more_menu = browser.find_element(By.XPATH, '//*[@id="navbarNavDropdown"]/ul[1]/li[6]')
    more_menu.click()
    careers_link = browser.find_element(By.XPATH, '//*[@id="navbarNavDropdown"]/ul[1]/li[6]/div/div[1]/div[3]/div/a/h5')
    careers_link.click()

    logging.info('Checking "Location", "Teams" and "Life at insider" titles in the page')
    locations = browser.execute_script('return document.getElementById("career-our-location")')    
    teams = browser.execute_script('return document.evaluate(\'//*[@id="career-find-our-calling"]/div/div/a\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;');
    life_at_insider = browser.execute_script("return document.evaluate('/html/body/div[1]/div/div/section[4]/div/div/div/div/div/div[1]/div/h2', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;")

    assert locations.is_displayed(), take_screenshot(browser, f"Locations block not displayed in {browser.name} browser")
    assert teams.is_displayed(), take_screenshot(browser, f"Teams block not displayed in {browser.name} browser")
    assert life_at_insider.is_displayed(), take_screenshot(browser, f"Life at Insider block not displayed in {browser.name} browser")

    #Select Quality Assurance jobs in Istanbul, Turkey
    logging.info('Selecting Quality Assurance part')
    scroll_to_teams = browser.execute_script('return document.evaluate(\'//*[@id="career-find-our-calling"]/div/div/div[2]/div[3]/div[4]/p\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;');
    browser.execute_script("arguments[0].scrollIntoView();", scroll_to_teams)
    time.sleep(2)
    teams.click()

    wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="career-find-our-calling"]/div/div/div[2]/div[12]/div[2]/a/h3')))
    quality_assurance = browser.execute_script('return document.evaluate(\'//*[@id="career-find-our-calling"]/div/div/div[2]/div[12]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;');
    browser.execute_script("arguments[0].scrollIntoView();", quality_assurance)
    time.sleep(2)
    quality_assurance.click()
    wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="page-head"]/div/div/div[1]/div/div/a')))
    see_all_qa_jobs = browser.execute_script('return document.evaluate(\'//*[@id="page-head"]/div/div/div[1]/div/div/a\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;');
    see_all_qa_jobs.click()

    #Check Istanbul, Turkey location in the list
    logging.info('Checking Quality Assurance positions in Istanbul, Turkey location')
    wait.until(EC.visibility_of_element_located((By.ID, "select2-filter-by-location-container")))
    location_filter = browser.execute_script('return document.getElementById("select2-filter-by-location-container")')
    location_filter.click()
    wait.until(EC.visibility_of_element_located((By.ID, "select2-filter-by-location-results")))
    location_list = browser.find_element(By.ID, "select2-filter-by-location-results").text
    assert "Istanbul, Turkey" in location_list, take_screenshot(browser, "Istanbul, Turkey location couldnt find in the list")

    locations = browser.find_elements(By.XPATH,'//*[@class="select2-results__option"]')
    for item in locations:
        if item.text == "Istanbul, Turkey":
            item.click()
            break
            
    #Check Quality Assurance department in the list
    department_filter = browser.execute_script('return document.getElementById("select2-filter-by-department-container")')
    department_filter.click()
    department_list = browser.find_element(By.ID, "select2-filter-by-department-results").text
    assert "Quality Assurance" in department_list, take_screenshot(browser, "Quality Assurance department couldnt find in the list")
    
    #Check any jobs are found
    logging.info('Checking search results')
    department_filter.click()
    scroll_to_job = browser.execute_script('return document.evaluate(\'//*[contains(@class, "col-12 d-flex flex-column")]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;');
    browser.execute_script("arguments[0].scrollIntoView();", scroll_to_job)
    wait.until(EC.visibility_of_element_located((By.XPATH,'//*[contains(@class, "position-list-item-wrapper")]')))
    time.sleep(2)

    jobs = browser.find_elements(By.XPATH,'//*[contains(@class, "position-list-item-wrapper")]')
    assert len(jobs) > 0, take_screenshot(browser, "No jobs found in the selected location and department")

    #Check job details
    positions = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "position-title")]')))
    for position in positions:
        assert "Quality Assurance" in position.text, take_screenshot(browser, f"{position.text} is not a QA position")

    departments = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "position-department")]')))
    for department in departments:
        assert "Quality Assurance" in department.text, take_screenshot(browser, f"{department.text} is not in the QA department")

    locations = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "position-location")]')))
    for location in locations:
        assert "Istanbul, Turkey" in location.text, take_screenshot(browser, f"{location.text} is not in Istanbul, Turkey")

    #Clicking apply button
    logging.info('Clicking application button and checking its form')
    position = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@class, "position-location")]')))
    ActionChains(browser).move_to_element(position).perform()
    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="jobs-list"]/div/div/a')))
    assert apply_button.is_displayed(), take_screenshot(browser, "Apply Now button not displayed")

    #Check application form link
    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="jobs-list"]/div/div/a')))
    apply_button.click()
    main_window = browser.current_window_handle
    all_openned_window = browser.window_handles
    for window in all_openned_window:
        if window != main_window:
            browser.switch_to.window(window)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@class, "posting-headline")]')))
    assert "lever" in browser.current_url, take_screenshot(browser, "Lever application form not opened")
    logging.info("Test Scenario is completed successfully")

    
