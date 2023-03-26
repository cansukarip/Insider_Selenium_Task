# Insider_Selenium_Task
  Project has 
  API test automation for "https://petstore.swagger.io/",
  UI test automation for "https://usensider.com", and 
  Load tests for "https://www.n11.com/" as the following structure.
  
        API_Test_Automation
          - test_petStoreApi.py
        UI_Test_Automation
          - screenshots
          - test_automation_WebUI.py
        Load_Tests
          - Load_Test_Scenarios.docx
    
## Prerequisites
    Python 3.10.10

#### Package - Version
    pip                 23.0.1
    pytest              7.2.2
    pytest-logger       0.5.1
    requests            2.28.2
    selenium            4.8.2
    chrome-webdriver    111.0.5563.111
    firefox-webdriver   111.0.1

## Test Scenarios Execution
Under project folder,
    - For run all test scenarios : pytest
    - For UI test scenario execution : pytest --log=INFO .\UI_Test_Automation\test_automation_WebUI.py
    - For API test scenario execution : pytest .\API_Test_Automation\test_petStoreApi.py
