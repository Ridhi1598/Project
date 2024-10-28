from behave import *
import difflib
import json
import random
import string
import time
import os
import sys
import ssl
import pysftp
import gzip
import shutil
from os.path import dirname, abspath
import jsonschema as jsonschema
import requests
import datetime
from selenium import webdriver
from behave import given, when, then, step
from jsonschema import validate
from requests import HTTPError
from selenium.webdriver import ActionChains

from features.steps.globalVar import GlobalVar
from features.steps.bi.bi_restApis import *
from features.steps.api_steps_general import *
from requests.auth import HTTPBasicAuth
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from features.steps.globalVar import GlobalVar
from features.steps.ui_steps_general import page_title_validation, change_currentPage
from selenium.webdriver.support.select import Select
from common.util.payloadGenerator import payloadGenerator
from selenium.webdriver.common.action_chains import ActionChains
from features.steps.globalVar import GlobalVar
from selenium.common.exceptions import TimeoutException

# declared variables
addUser = {}
regNewUser = {}
state = {}
roleAdmin = {}
roleRW = {}
roleRead = {}
loginStatus = False
requestIds = []
Errormsg = {}
RequestID = {}
testParams = {}
baseTest = None
readOnlyStatus = None
ConfigData = {}


@step('I fill registration details and should land on the Business Internet Portal')
def enter_new_user_registration_details(context):
    global regNewUser
    currentPage = "LandingPage"
    url = sys.argv[1] + 'URL_' + sys.argv[2]
    context.driver.get(context.config.get(url))

    pageHeadingXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'pageHeading')
    pageHeading = WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, pageHeadingXpath))).text

    if 'BI Service Dashboard' in pageHeading:
        pass
    else:
        LoginXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Login')
        WebDriverWait(context.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, LoginXpath)))
        time.sleep(10)
        context.baseReader.getElementByPropertyName(context, currentPage, 'Login').click()
        currentPage = 'KeycloakLoginPage'
        titleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'PageTitle')
        WebDriverWait(context.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, titleXpath)))
        regNewUser['TelusID'] = GlobalVar.testParams.get('RegNewUserID')
        regNewUser['Password'] = GlobalVar.testParams.get('RegNewUserPw')
        regNewUser['EmailID'] = GlobalVar.testParams.get('RegNewUserEmail')
        usernameXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'UserName')
        WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, usernameXpath))).send_keys(regNewUser['TelusID'])
        context.baseReader.getElementByPropertyName(context, currentPage, 'Password').send_keys(regNewUser['Password'])
        context.baseReader.getElementByPropertyName(context, currentPage, 'LoginButton').click()


@step('I verify the new user registration details and register')
def new_user_registration_details_verification(context):
    currentPage = GlobalVar.currentPage
    disabledTelusID = context.baseReader.getElementByPropertyName(context, currentPage, 'RegNewUserDisplayedName')
    disabledEmailID = context.baseReader.getElementByPropertyName(context, currentPage, 'RegNewUserDisplayedEmail')
    displayedNewUserTelusID = disabledTelusID.get_attribute('value')
    displayedNewUserEmailID = disabledEmailID.get_attribute('value')
    assert regNewUser['TelusID'] == displayedNewUserTelusID
    assert regNewUser['EmailID'] == displayedNewUserEmailID
    context.baseReader.getElementByPropertyName(context, currentPage, 'RegNewUserSelectRole').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'RegNewUserReadOnly').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'RegNewUserDisplayedEmail').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'RegisterButton').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'RegisterOKAlert').click()


@step('I should land on BI Home page')
def step_impl(context):
    global loginStatus
    currentPage = "LandingPage"
    url = sys.argv[1] + 'URL_' + sys.argv[2]
    context.driver.get(context.config.get(url))
    pageHeadingXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'pageHeading')
    pageHeading = WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, pageHeadingXpath))).text
    print(pageHeading)

    if pageHeading.lower() == 'transactions':
        pass
    else:
        LoginXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Login')
        WebDriverWait(context.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, LoginXpath)))
        time.sleep(10)
        context.baseReader.getElementByPropertyName(context, currentPage, 'Login').click()
        currentPage = 'KeycloakLoginPage'
        titleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'PageTitle')
        WebDriverWait(context.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, titleXpath)))
        readOnlyStatus = bool(GlobalVar.testParams.get('readOnly'))

        if readOnlyStatus:
            username = context.envReader.get('TestUserNameReadOnly')
            password = context.envReader.get('TestUserPassReadOnly')
        else:
            username = context.envReader.get("TestUserName")
            password = context.envReader.get('TestUserPass')

        usernameXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'UserName')
        WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, usernameXpath))).send_keys(username)
        context.baseReader.getElementByPropertyName(context, currentPage, 'Password').send_keys(password)
        context.baseReader.getElementByPropertyName(context, currentPage, 'LoginButton').click()
        titleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'title')
        WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, titleXpath)))


@step(u'I fill user details and save')
def fill_user_details(context):
    global addUser
    currentPage = GlobalVar.currentPage
    addUser['TelusID'] = GlobalVar.testParams.get("addUserID")

    LoadingWait = context.baseReader.getElementLocatorValue(context, currentPage, 'LoadingGif')
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, LoadingWait)))
    saveXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Save')
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, saveXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'UserTelusID').send_keys(addUser['TelusID'])
    context.baseReader.getElementByPropertyName(context, currentPage, 'SelectUserRole').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NewUserReadOnly').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'dropDownBtn').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'Save').click()


@step(u'I leave all the details empty and try to save')
def fill_user_details(context):
    currentPage = GlobalVar.currentPage
    LoadingWait = context.baseReader.getElementLocatorValue(context, currentPage, 'LoadingGif')
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, LoadingWait)))
    saveXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Save')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, saveXpath))).click()
    TelusIDValidation = context.baseReader.getElementByPropertyName(context, currentPage, 'NoTelusIDMessage')
    RoleValidation = context.baseReader.getElementByPropertyName(context, currentPage, 'NoRoleMessage')
    assert TelusIDValidation.text == GlobalVar.testParams.get('TelusIDValidation')
    assert RoleValidation.text == GlobalVar.testParams.get('RoleValidation')
    context.baseReader.getElementByPropertyName(context, currentPage, 'Cancel').click()
    LoadingWait = context.baseReader.getElementLocatorValue(context, currentPage, 'LoadingGif')
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, LoadingWait)))


@step(u'I fill details except user role and try to save')
def fill_user_details(context):
    global addUser
    currentPage = GlobalVar.currentPage
    addUser['TelusID'] = GlobalVar.testParams.get("addUserID")
    LoadingWait = context.baseReader.getElementLocatorValue(context, currentPage, 'LoadingGif')
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, LoadingWait)))
    saveXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Save')
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, saveXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'UserTelusID').send_keys(addUser['TelusID'])
    context.baseReader.getElementByPropertyName(context, currentPage, 'Save').click()
    RoleValidation = context.baseReader.getElementByPropertyName(context, currentPage, 'NoRoleMessage')
    assert RoleValidation.text == GlobalVar.testParams.get('RoleValidation')
    context.baseReader.getElementByPropertyName(context, currentPage, 'Cancel').click()
    LoadingWait = context.baseReader.readElementByPropertyName(currentPage, 'LoadingGif').get("value")
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, LoadingWait)))


@step(u'I fill details except TelusID and try to save')
def fill_user_details(context):
    global addUser
    currentPage = GlobalVar.currentPage
    LoadingWait = context.baseReader.getElementLocatorValue(context, currentPage, 'LoadingGif')
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, LoadingWait)))
    saveXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Save')
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, saveXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SelectUserRole').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NewUserReadOnly').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'dropDownBtn').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'Save').click()
    TelusIDValidation = context.baseReader.getElementByPropertyName(context, currentPage, 'NoTelusIDMessage')
    assert TelusIDValidation.text == GlobalVar.testParams.get('TelusIDValidation')
    context.baseReader.getElementByPropertyName(context, currentPage, 'Cancel').click()
    LoadingWait = context.baseReader.readElementByPropertyName(currentPage, 'LoadingGif').get("value")
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, LoadingWait)))


@step(u'User name should "{scenario}" displayed in the list of users')
def search_user(context, scenario):
    currentPage = GlobalVar.currentPage
    addUser['TelusID'] = GlobalVar.testParams.get("addUserID")
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noData")
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, noDataXpath)))
    searchObj = context.baseReader.getElementByPropertyName(context, currentPage, 'SearchUser')
    searchObj.clear()
    searchObj.send_keys(addUser['TelusID'])
    if 'not' in scenario:
        noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'UserSearchResultNegative')
        WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, noDataXpath)))
    else:
        firstResultXpath = context.baseReader.getElementLocatorValue(context, currentPage, "firstIdResult")
        WebDriverWait(context.driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, firstResultXpath), addUser['TelusID']))
        assert addUser['TelusID'] == WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, firstResultXpath))).text
        print(WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, firstResultXpath))).text)

@step(u'I change the account state to "{changeState}"')
def change_account_state(context, changeState):
    global state
    currentPage = GlobalVar.currentPage
    AccountStateValue = context.baseReader.getElementByPropertyName(context, currentPage, 'AccStateBtn')
    AccountStateColor = AccountStateValue.value_of_css_property('background-color')
    state['Before'] = False
    state['After'] = False
    if AccountStateColor == state['Green']:
        state['Before'] = True
    if AccountStateColor == state['Grey']:
        state['Before'] = False
    context.baseReader.getElementByPropertyName(context, currentPage, 'AccStateBtn').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'YesUserAccountChange').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'AccountStateChangeSuccessAlert').click()
    LoadingWait = context.baseReader.readElementByPropertyName(currentPage, 'LoadingGif').get("value")
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, LoadingWait)))


@step(u'I verify that the account state has been changed')
def change_account_state_verification(context):
    accountStateChange = False
    currentPage = GlobalVar.currentPage
    AccountStateValue = context.baseReader.getElementByPropertyName(context, currentPage, 'AccStateBtn')
    AccountStateColor = AccountStateValue.value_of_css_property('background-color')
    if AccountStateColor == state['Green']:
        state['After'] = True
    if AccountStateColor == state['Grey']:
        state['After'] = False
    if state['Before'] != state['After']:
        accountStateChange = True
    assert accountStateChange


@step(u'I delete the user')
def delete_user(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'Delete').click()
    confirmXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'confirmId')
    WebDriverWait(context.driver, 5).until(
        EC.text_to_be_present_in_element((By.XPATH, confirmXpath), addUser["TelusID"]))
    context.baseReader.getElementByPropertyName(context, currentPage, 'YesForDelete').click()


@step(u'I verify that the user has been deleted')
def verify_user_deletion(context):
    currentPage = GlobalVar.currentPage
    addUser['TelusID'] = GlobalVar.testParams.get("addUserID")
    searchObj = context.baseReader.getElementByPropertyName(context, currentPage, 'SearchUser')
    searchObj.clear()
    searchObj.send_keys(addUser['TelusID'])
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'UserSearchResultNegative')
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, noDataXpath)))
    time.sleep(5)


@step(u'I log out')
def log_out(context):
    global loginStatus
    currentPage = GlobalVar.currentPage
    accXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'UserAccountLogo')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, accXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'UserAccountLogo').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'LogoutBtn').click()


@step(u'I Set POST request Body "{body_key}" as "{body_value}"')
def step_impl(context, body_key, body_value):
    global body
    body[body_key] = body_value
    GlobalVar.api_dict['request_bodies'] = body


@step('Wait till the Contact support popup will shown up')
def wait_for_contact_support_popup(context):
    currentPage = GlobalVar.currentPage
    contactSupportHeadingXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                           'contactSupportHeading')
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, contactSupportHeadingXpath)), message='Element not visible')


@step('Validate the input validation messages for contact support email')
def validate_input_validation_for_contact_support_email(context):
    currentPage = GlobalVar.currentPage
    subjectValidationMessage = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                           'subjectInputValidation').text
    descriptionValidationMessage = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                               'descriptionInputValidation').text
    assert subjectValidationMessage == GlobalVar.testParams.get('subjectValidationMessage')
    assert descriptionValidationMessage == GlobalVar.testParams.get('descriptionValidationMessage')


@step('I send the contact support email')
def fill_contact_support_details(context):
    currentPage = GlobalVar.currentPage
    tempMessage = 'Test_Automation_' + str(''.join(random.choices(string.ascii_letters + string.digits, k=10)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'subject').send_keys(tempMessage)
    context.baseReader.getElementByPropertyName(context, currentPage, 'description').send_keys(tempMessage)
    context.baseReader.getElementByPropertyName(context, currentPage, 'contactSupportMailSave').click()
    sentSuccessMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'sentSuccessMessage')
    WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, sentSuccessMessageXpath)), message='Element not visible')
    context.baseReader.getElementByPropertyName(context, currentPage, 'okAlert').click()


@step('Fill the pre-existed user details')
def wait_for_new_user_form(context):
    global addUser
    currentPage = GlobalVar.currentPage
    addUser['TelusID'] = GlobalVar.testParams.get("addUserID")
    LoadingWait = context.baseReader.getElementLocatorValue(context, currentPage, 'LoadingGif')
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, LoadingWait)))
    saveXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Save')
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, saveXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'UserTelusID').send_keys(addUser['TelusID'])
    context.baseReader.getElementByPropertyName(context, currentPage, 'SelectUserRole').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NewUserReadOnly').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'dropDownBtn').click()
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, saveXpath))).click()


@step('Validate the alert message for "{messageType}"')
def validate_alert_message_for_existed_user(context, messageType):
    currentPage = GlobalVar.currentPage
    alertWindowXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alertWindow')
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, alertWindowXpath)), message='Element not visible')
    time.sleep(10)
    message = context.baseReader.getElementByPropertyName(context, currentPage, 'alertMessage').text
    assert message == GlobalVar.testParams.get(messageType + 'Message')
    context.baseReader.getElementByPropertyName(context, currentPage, 'OK').click()


@step('I iteratively validate the number of results displayed per page')
def validate_results_displayed_per_page(context):
    currentPage = GlobalVar.currentPage
    time.sleep(2)

    # Below part reads the total number of results
    resultLineArray = context.baseReader.getElementByPropertyName(context, currentPage, 'TotalResults')
    totalResults = int((resultLineArray.text).split()[0])
    print("Total number of results:", totalResults)

    dropDownResultsPerPage = [10, 20, 30, 40, 50]

    for i in dropDownResultsPerPage:
        time.sleep(2)

        print("Checking for results per page:", i)

        # Checking how many results per page option is selected from the dropdown
        select = Select(context.baseReader.getElementByPropertyName(context, currentPage, 'ResultNumberSelected'))
        resultsPerPageSelected = int((select.first_selected_option).text)
        print("Already results per page selected option:", resultsPerPageSelected)

        if i != resultsPerPageSelected:
            # Selecting number of results to display per page
            print("Selecting results per page:", i)
            select.select_by_value(str(i))
            time.sleep(2)

            # Verifying that the new selected value for results per page has been selected
            select = Select(context.baseReader.getElementByPropertyName(context, currentPage, 'ResultNumberSelected'))
            resultsPerPageSelected = int((select.first_selected_option).text)
            print("Now results per page selected option:", resultsPerPageSelected)
            assert i == resultsPerPageSelected

        # Checking how many rows are displayed
        rows = context.driver.find_elements_by_xpath("//*[@class= 'table table-bordered']/tbody/tr")
        rowsDisplayed = len(rows)
        print("Number of result rows displayed:", rowsDisplayed)
        if totalResults >= i:
            assert i == rowsDisplayed
        else:
            assert totalResults == rowsDisplayed


@step('I iteratively verify total number of pages displayed')
def validate_total_pages_displayed_against_results_per_page(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)

    # Below part reads the total number of results
    resultLineArray = context.baseReader.getElementByPropertyName(context, currentPage, 'TotalResults')
    totalResults = int((resultLineArray.text).split()[0])
    print("Total number of results:", totalResults)

    dropDownResultsPerPage = [10, 20, 30, 40, 50]

    for i in dropDownResultsPerPage:
        time.sleep(5)
        print("Checking for results per page:", i)

        if totalResults % i == 0:
            expectedTotalPages = totalResults // i
            print("Expected total pages:", expectedTotalPages)
        else:
            expectedTotalPages = (totalResults // i) + 1
            print("Expected total pages:", expectedTotalPages)

        # Checking how many results per page option is selected from the dropdown
        select = Select(context.baseReader.getElementByPropertyName(context, currentPage, 'ResultNumberSelected'))
        resultsPerPageSelected = int((select.first_selected_option).text)
        print("Already results per page selected option:", resultsPerPageSelected)

        if i != resultsPerPageSelected:
            # Selecting number of results to display per page
            print("Selecting results per page:", i)
            select.select_by_value(str(i))
            time.sleep(5)

            # Verifying that the new selected value for results per page has been selected
            select = Select(context.baseReader.getElementByPropertyName(context, currentPage, 'ResultNumberSelected'))
            resultsPerPageSelected = int((select.first_selected_option).text)
            print("Now results per page selected option:", resultsPerPageSelected)
            assert i == resultsPerPageSelected

        # Below part reads the last page number displayed
        resultLineArray = context.baseReader.getElementByPropertyName(context, currentPage, 'TotalResults')
        lastPageNumberDisplayed = int((resultLineArray.text).split()[-3])
        print("Last page number displayed:", lastPageNumberDisplayed)

        # Going to last page
        if lastPageNumberDisplayed > 1:
            print("Navigating to last page to check the last page displayed")
            context.baseReader.getElementByPropertyName(context, currentPage, 'LastPage').click()
            time.sleep(5)

        # Below part reads the last page number displayed
        resultLineArray = context.baseReader.getElementByPropertyName(context, currentPage, 'TotalResults')
        lastPageNumberDisplayed = int((resultLineArray.text).split()[-3])
        print("Last page number displayed:", lastPageNumberDisplayed)

        # Going to first page
        if lastPageNumberDisplayed > 1:
            print("Navigating to first page")
            context.baseReader.getElementByPropertyName(context, currentPage, 'FirstPage').click()
            time.sleep(5)
        print("Asserting if", expectedTotalPages, "=", lastPageNumberDisplayed)
        assert expectedTotalPages == lastPageNumberDisplayed


@step('I search for "{value}" Operation Result')
def search_Operation_Result(context, value):
    currentPage = GlobalVar.currentPage
    OperationResult = context.baseReader.getElementLocatorValue(context, currentPage, 'OperationResult')
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, OperationResult)),
                                            message='Element not visible')
    context.baseReader.getElementByPropertyName(context, currentPage, 'OperationResult').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'OperationResult').send_keys(value)


@step('Validate all Operation Result should be "{expectedValue}"')
def Validation_of_failed_operation_result(context, expectedValue):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    DashboardTableDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DashboardTableData')
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, DashboardTableDataXpath)))

    OperationResultValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'OperationResultcolumn')
    OperationResultcolumnList = context.driver.find_elements(By.XPATH, OperationResultValueXpath)

    for i in range(0, len(OperationResultcolumnList)):
        assert OperationResultcolumnList[i].text == expectedValue
    print('All operation results are {}'.format(expectedValue))


@step('I click on "{expectedText}" Operation Result text')
def click_on_operation_result_value(context, expectedText):
    currentPage = GlobalVar.currentPage
    OperationResultValue = context.baseReader.getElementLocatorValue(context, currentPage, 'OperationResultValue')
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, OperationResultValue)),
                                            message='Element not visible')
    assert expectedText in context.baseReader.getElementByPropertyName(context,
                                                                       currentPage, 'OperationResultValue').text
    context.baseReader.getElementByPropertyName(context, currentPage, 'OperationResultValue').click()


@step('I should see the reason for failure in a pop up bubble')
def reason_for_failure_in_a_pop_up_bubble(context):
    global Errormsg
    currentPage = GlobalVar.currentPage
    FailedOperation = context.baseReader.getElementByPropertyName(context, currentPage, 'FailedOperation')
    action = ActionChains(context.driver)
    action.move_to_element(FailedOperation).perform()
    FailedOperationResult = context.baseReader.getElementLocatorValue(context, currentPage, 'FailedOperationResult')
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, FailedOperationResult)),
                                            message='Element not visible')
    popupmsg = context.baseReader.getElementByPropertyName(context, currentPage, 'FailedOperationResult').text
    Errormsg['Old'] = popupmsg
    # print("Error in popup:", Errormsg['Old'])

@step('Validate alert Modal should open and display same reason for failure')
def reason_for_failure_in_alert_modal(context):
    global Errormsg
    currentPage = GlobalVar.currentPage
    FailedOperationMessage = context.baseReader.getElementLocatorValue(context, currentPage, 'FailedOperationMessage')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, FailedOperationMessage)),
                                            message='Element not visible')
    alertmessage = context.baseReader.getElementByPropertyName(context, currentPage, 'FailedOperationMessage').text
    Errormsg['error'] = alertmessage
    assert Errormsg['Old'] == Errormsg['error']


@step('Validate the same reason for failure display on alert Modal')
def Validate_failed_popup_and_alert_messages(context):
    global Errormsg
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    errormessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ErrorMessage').text
    Errormsg['New'] = errormessage
    assert Errormsg['Old'] == Errormsg['New']


@step('Close the error window')
def Close_error_window(context):
    currentPage = GlobalVar.currentPage
    AlertcloseButton = context.baseReader.getElementLocatorValue(context, currentPage, 'AlertcloseButton')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, AlertcloseButton)),
                                            message='Element not visible')
    context.baseReader.getElementByPropertyName(context, currentPage, 'AlertcloseButton').click()
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'PageTitle').text
    assert actualValue == 'BI Service Dashboard'


@step('I look for a "{value}" Operation Result of "{value2}" Operation')
def look_for_Completed_Operation_Result(context, value, value2):
    currentPage = GlobalVar.currentPage
    OperationType = context.baseReader.getElementLocatorValue(context, currentPage, 'OperationType')
    time.sleep(5)
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, OperationType)),
                                            message='Element not visible')
    context.baseReader.getElementByPropertyName(context, currentPage, 'OperationType').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'OperationType').send_keys(value2)
    OperationResult = context.baseReader.getElementLocatorValue(context, currentPage, 'OperationResult')
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, OperationResult)),
                                            message='Element not visible')
    context.baseReader.getElementByPropertyName(context, currentPage, 'OperationResult').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'OperationResult').send_keys(value)
    time.sleep(5)


@step('Validate that the Parameter information should be Available')
def validate_Parameter_information(context):
    currentPage = GlobalVar.currentPage
    ParameterInformationTitle = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                          'ParameterInformationTitle')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, ParameterInformationTitle)),
                                            message='Element not visible')
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'ParameterInformationTitle').text
    assert actualValue == 'Parameter Information'


@step('Validate that Parameter information should be "{expectedValue}"')
def validate_all_Parameter_information(context, expectedValue):
    currentPage = GlobalVar.currentPage
    DataNotAvailableText = context.baseReader.getElementLocatorValue(context, currentPage, 'DataNotAvailableText')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, DataNotAvailableText)),
                                            message='Element not visible')
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'DataNotAvailableText').text
    assert actualValue == expectedValue


@step('I look for a Customer Service ID')
def look_for_a_Customer_Service_ID(context):
    currentPage = GlobalVar.currentPage
    CustomerServiceID = context.baseReader.getElementLocatorValue(context, currentPage, 'CustomerServiceID')
    time.sleep(10)
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, CustomerServiceID)),
                                            message='Element not visible')
    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerServiceID').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerServiceID').send_keys(
        GlobalVar.testParams.get('serviceId'))
    time.sleep(10)
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerServiceIDValue').text
    assert actualValue == GlobalVar.testParams['serviceId']


@step('"{value}" should be "{expectedValue}"')
def Operation_validation(context, value, expectedValue):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, value).text
    # assert expectedValue.lower() == actualValue.lower()


@step('I search for the "{precedence}" "{element}" for "{scenarioType}" scenario from dashboard')
def look_for_associated_Request_ID(context, precedence, element, scenarioType):
    global RequestID
    currentPage = GlobalVar.currentPage
    RequestID[precedence + element] = context.baseReader.getElementByPropertyName(
        context, currentPage, element).text
    GlobalVar.reqId = RequestID[precedence + element]


@step('I click on "{value}" and "{expectedValue}" Modal should open')
def Operation_validation(context, value, expectedValue):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()
    expectedValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, expectedValue)
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, expectedValueXpath)))
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, expectedValue).text
    assert expectedValue in actualValue
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
    WebDriverWait(context.driver, 20).until(EC.invisibility_of_element_located((By.XPATH, noDataXpath)))


@step('I validate the "{precedence}" Request ID for "{scenarioType}" scenario')
def Validate_RequestId(context, precedence, scenarioType):
    currentPage = GlobalVar.currentPage
    reqID = context.baseReader.getElementByPropertyName(context, currentPage, 'RequestID').text
    assert reqID == RequestID[precedence + scenarioType]
    if precedence == 'old':
        RequestID['oldRequestID'] = reqID


@step('"{element}" should be available in "{column}" column for latest transaction')
def Validate_RollBack_button(context, element, column):
    currentPage = GlobalVar.currentPage
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, element)
    elementVal = WebDriverWait(context.driver, 5).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))

    if element == 'userID':
        try:
            assert elementVal.text == context.envReader.get("TestUserName")
        except:
            assert elementVal.text == GlobalVar.api_dict["request_params"]["user_id"]

    if element == 'requestId':
        assert elementVal.text == RequestID['execute']


@step('Wait for the operation to submit')
def Wait_for_processing_the_request_and_refresh_the_page(context):
    currentPage = GlobalVar.currentPage
    time.sleep(40)


@step('Validate that a new request id is generated')
def Validate_request_id(context):
    global RequestID
    currentPage = GlobalVar.currentPage
    time.sleep(10)
    RequestIDColumn = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                'RequestIDColumn')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, RequestIDColumn)),
                                            message='Element not visible')
    newOldReqID = context.baseReader.getElementByPropertyName(context, currentPage, 'RequestIDColumn').text
    # print(newOldReqID)
    RequestID['newOldReqID'] = newOldReqID
    assert RequestID['oldRequestID'] != RequestID['newOldReqID']


@step('Validate that the Customer Name and Network Element Name should be empty')
def Validate_Customer_Name_and_Network_Element(context):
    currentPage = GlobalVar.currentPage
    CustomerName = context.baseReader.getElementLocatorValue(context, currentPage, 'firstCustomerName')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, CustomerName)),
                                            message='Element not visible')
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'firstCustomerName').text
    # print(actualValue)
    assert actualValue == ''

    NetworkElementName = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                   'firstNetworkElementName')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, NetworkElementName)),
                                            message='Element not visible')
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'firstNetworkElementName').text
    # print(actualValue)
    assert actualValue == ''


@step('Wait for the "{value}" to "{expectedValue}" and refresh the page')
def Wait_for_processing_the_request_and_refresh_the_page(context, value, expectedValue):
    currentPage = GlobalVar.currentPage
    time.sleep(400)
    context.driver.refresh()

@step('I click on Close History Modal button')
def click_History_button(context):
    currentPage = GlobalVar.currentPage
    HistoryCloseButton = context.baseReader.getElementLocatorValue(context, currentPage, 'HistoryCloseButton')
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, HistoryCloseButton)),
                                            message='Element not visible')
    context.baseReader.getElementByPropertyName(context, currentPage, 'HistoryCloseButton').click()
    time.sleep(10)


@step('Validate RollBack config button should be available on action column')
def Validate_RollBack_config_button_should_be_available(context):
    currentPage = GlobalVar.currentPage
    buttonSymbol = context.baseReader.getElementByPropertyName(context, currentPage, 'RollBackButton').text
    # print(buttonSymbol)
    assert buttonSymbol == '+'


@step('I look for the associated network element name')
def Look_for_Customer_Name_and_Network_Element(context):
    currentPage = GlobalVar.currentPage
    global RequestID
    CustomerName = context.baseReader.getElementLocatorValue(context, currentPage, 'firstCustomerName')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, CustomerName)),
                                            message='Element not visible')
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'firstCustomerName').text
    RequestID['network element'] = actualValue

    NetworkElementName = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                   'firstNetworkElementName')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, NetworkElementName)),
                                            message='Element not visible')
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'firstNetworkElementName').text


@step('I look for the associated prefix value')
def Look_for_associated_prefixe_value(context):
    currentPage = GlobalVar.currentPage
    global RequestID
    IPV4ProviderPrefix1 = context.baseReader.getElementLocatorValue(context, currentPage, 'IPV4ProviderPrefix1')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, IPV4ProviderPrefix1)),
                                            message='Element not visible')
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage,
                                                              'IPV4ProviderPrefix1').get_attribute('value')
    RequestID['prefix value'] = actualValue


@step('I Wait for the Rollback Configuration Information to appear')
def Wait_for_Rollback_Configuration_Information(context):
    currentPage = GlobalVar.currentPage
    global RequestID
    time.sleep(600)
    RollbackConfigInfo = context.baseReader.getElementLocatorValue(context, currentPage, 'RollbackConfigInfo')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, RollbackConfigInfo)),
                                            message='Element not visible')
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'RollbackConfigInfo').text
    RequestID['Config Value'] = actualValue


@step('Validate that the associated "Customer Service ID" should be displayed')
def Validate_prefixe_value(context):
    currentPage = GlobalVar.currentPage
    global RequestID
    time.sleep(5)
    assert GlobalVar.testParams['serviceId'] in RequestID['Config Value']


@step('Validate that network element name should be same')
def Validate_network_element_name(context):
    currentPage = GlobalVar.currentPage
    global RequestID
    time.sleep(5)
    assert RequestID['network element'] in RequestID['Config Value']


@step('Validate that associated prefix value should be same')
def Validate_prefix_value(context):
    currentPage = GlobalVar.currentPage
    global RequestID
    time.sleep(5)
    assert RequestID['prefix value'] in RequestID['Config Value']


@step('Validate that Rollback Configuration Info should be "{expectedValue}"')
def validate_all_Parameter_information(context, expectedValue):
    currentPage = GlobalVar.currentPage
    RollbackConfigInfo = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                   'RollbackConfigInfo')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, RollbackConfigInfo)),
                                            message='Element not visible')
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage,
                                                              'RollbackConfigInfo').text
    assert actualValue == expectedValue


@step('Validate that associated prefix value should be displayed')
def Validate_prefix_value(context):
    currentPage = GlobalVar.currentPage
    global RequestID
    IPV4ProviderPrefix1 = context.baseReader.getElementLocatorValue(context, currentPage, 'IPV4ProviderPrefix1')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, IPV4ProviderPrefix1)),
                                            message='Element not visible')
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage,
                                                              'IPV4ProviderPrefix1').get_attribute('value')
    assert actualValue != RequestID['prefix value']


@step('I look for the "{value}" for "{scenario}" scenario')
def look_for_associated_Request_ID(context, value, scenario):
    currentPage = GlobalVar.currentPage
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, value).get_attribute('value')
    GlobalVar.ServiceParams[scenario + value] = actualValue


@step('Validate "NetworkElementName" and "CSIDValue" different after scenario')
def Validate_RequestId(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    assert GlobalVar.ServiceParams.get('beforeNetworkElementValue') != GlobalVar.ServiceParams.get(
        'afterNetworkElementValue')
    assert GlobalVar.ServiceParams.get('beforeCSIDValue') != GlobalVar.ServiceParams.get('afterCSIDValue')
    # assert ServiceParams['beforeNetworkElementValue'] != ServiceParams['afterNetworkElementValue']
    # assert ServiceParams['beforeCSIDValue'] != ServiceParams['afterCSIDValue']


@step('Validate that mwr device is not available in Rollback Configuration Information')
def Validate_RequestId(context):
    currentPage = GlobalVar.currentPage
    global ServiceParams
    global RequestID
    time.sleep(5)
    assert GlobalVar.ServiceParams.get('beforeNetworkElementValue') not in RequestID.get('Config Value')
    # assert RequestID.get('Config Value'] not in GlobalVar.ServiceParams.get('beforeNetworkElementValue')
    # assert ServiceParams['beforeCSIDValue'] not in RequestID['Config Value']


@step('Validate that mwr device is available in Rollback Configuration Information')
def Validate_RequestId(context):
    currentPage = GlobalVar.currentPage
    global ServiceParams
    global RequestID
    time.sleep(5)
    assert GlobalVar.testParams['NetworkElementName'] in RequestID.get('Config Value')


@step('"{value}" button should not be available in action column')
def Validate_RollBack_config_button_should_not_available(context, value):
    currentPage = GlobalVar.currentPage
    value = context.baseReader.getElementLocatorValue(context, currentPage, value)
    try:
        WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, value)),
                                                message='Element not visible')
        print("Element found")
        assert False
    except TimeoutException:
        print("Element no more found")


@step('Clear the required values of parameter information')
def Clear_required_values_of_parameter_information(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix1').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix1').clear()

    context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix2').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix2').clear()

    context.baseReader.getElementByPropertyName(context, currentPage, 'QOSIngress').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'QOSIngress').clear()

    context.baseReader.getElementByPropertyName(context, currentPage, 'QosEgress').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'QosEgress').clear()


@step('Update "invalid prefix value" of parameter information')
def Clear_required_values_of_parameter_information(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').send_keys(
        GlobalVar.testParams['InvalidPrefixValue'])


@step('Update "{value}" of parameter information')
def Clear_required_values_of_parameter_information(context, value):
    currentPage = GlobalVar.currentPage
    time.sleep(2)
    if value == 'InvalidPrefixFormat':
        context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').clear()
        context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').send_keys(
            GlobalVar.testParams['InvalidPrefix'])
    elif value == 'RemovingProviderPrefix':
        context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').clear()
        context.driver.find_element(By.XPATH, '//button/i').click()
    time.sleep(2)


@step('I Wait for next page to load')
def Wait_for_processing_the_request(context):
    currentPage = GlobalVar.currentPage
    time.sleep(60)


@step('Validate "{value}" button should be disable')
def Validate_button_should_disable(context, value):
    currentPage = GlobalVar.currentPage
    assert not context.baseReader.getElementByPropertyName(context, currentPage, value).is_enabled()


@step('"{value}" should be Displayed')
def Validate_button_should_disable(context, value):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, value).text
    Errormessage = GlobalVar.testParams['errorMessage']
    assert Errormessage in actualValue
    assert Errormessage == actualValue

    Errormessage = Errormessage[:3] + GlobalVar.testParams['InvalidPrefix'] + Errormessage[3:]


@step('I click on required parameters of Execution details form')
def click_details_execution_form(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    ReasonForChange = context.baseReader.getElementLocatorValue(context, currentPage, 'reasonForChange')
    WebDriverWait(context.driver, 5).until(EC.visibility_of_element_located((By.XPATH, ReasonForChange)),
                                           message='Element not visible').click()

    ExecutionDetails = context.baseReader.getElementLocatorValue(context, currentPage, 'ExecutionDetails')
    WebDriverWait(context.driver, 5).until(EC.visibility_of_element_located((By.XPATH, ExecutionDetails)),
                                           message='Element not visible').click()

    WorkOrderChange = context.baseReader.getElementLocatorValue(context, currentPage, 'workOrderChange')
    WebDriverWait(context.driver, 5).until(EC.visibility_of_element_located((By.XPATH, WorkOrderChange)),
                                           message='Element not visible').click()

    ExecutionDetails = context.baseReader.getElementLocatorValue(context, currentPage, 'ExecutionDetails')
    WebDriverWait(context.driver, 5).until(EC.visibility_of_element_located((By.XPATH, ExecutionDetails)),
                                           message='Element not visible').click()


@step('ErrorMessage should be displayed under required parameters')
def ErrorMessage_in_execution_form(context):
    currentPage = GlobalVar.currentPage
    ReasonForChangeError = context.baseReader.getElementByPropertyName(context, currentPage, 'ReasonForChangeError').text
    WorkOrderError = context.baseReader.getElementByPropertyName(context, currentPage, 'WorkOrderError').text

    assert GlobalVar.testParams['ReasonForChangeError'] == ReasonForChangeError
    assert GlobalVar.testParams['WorkOrderError'] == WorkOrderError


@step('Validate service id should present in table')
def Validate_service_should_present_table(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    serviceIdListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'CustServiceID')
    serviceIdList = context.driver.find_elements(By.XPATH, serviceIdListXpath)

    # index variable will store the row number in which the service is appearing
    index = None
    for i in range(0, len(serviceIdList)):
        if serviceIdList[i].text == GlobalVar.testParams.get('serviceId'):
            index = str(i + 1)
            break
    else:
        print('service not found')

    # read the xpath for the expandButton and replace the row number with the above index
    paramBoxXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'ExecuteBox')
    paramBoxXpath = paramBoxXpath.replace('index', index)
    time.sleep(5)
    context.driver.find_element(By.XPATH, paramBoxXpath).click()
    time.sleep(5)


@step('Validate Origin of the service should be "{originType}"')
def Validate_Origin_should_be_NC(context, originType):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    HistoryOrigin = context.baseReader.getElementLocatorValue(context, currentPage, 'HistoryOrigin')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, HistoryOrigin)),
                                            message='Element not visible')
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'HistoryOrigin').text
    assert actualValue == originType


@step('Validate the generated request id is displayed')
def Validate_RequestId(context):
    currentPage = GlobalVar.currentPage
    global RequestID
    time.sleep(5)
    NewReqID = context.baseReader.getElementByPropertyName(context, currentPage, 'RequestID').text
    RequestID['newRequestID'] = NewReqID
    assert RequestID['oldRequestID'] == RequestID['newRequestID']


@step('ProgressBar button should be disappear from action column')
def Validate_RollBack_config_button_should_not_available(context):
    currentPage = GlobalVar.currentPage
    AlertButton = context.baseReader.getElementLocatorValue(context, currentPage, 'AlertButton')
    try:
        element = WebDriverWait(context.driver, 5).until(EC.visibility_of_element_located((By.XPATH, AlertButton)))
        assert element
    except TimeoutException:
        print("Element no more found")


@step('Validate that the "{precedence}" generated "{element}" is displayed in "{location}"')
def Validate_generated_RequestId(context, precedence, element, location):
    global RequestID
    currentPage = GlobalVar.currentPage
    # if 'history' in location:
    #     element = element + precedence
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, element).text
    # print("Globalvar.requestId: {}".format(GlobalVar.requestId))
    # print("ActualValue: {}".format(actualValue))
    if GlobalVar.requestId is None:
        assert actualValue == RequestID[precedence + element]
    else:
        assert actualValue == GlobalVar.requestId
    RequestID[precedence + element] = actualValue


@step('Validate the generated request id is displayed in History Modal')
def Validate_RequestId(context):
    currentPage = GlobalVar.currentPage
    global RequestID
    time.sleep(5)
    HistoryReqID = context.baseReader.getElementByPropertyName(context, currentPage, 'HistoryRequestId').text
    RequestID['reqID'] = HistoryReqID
    assert GlobalVar.requestId == RequestID['reqID']


@step('Validate that History Modal "{element}" should be "{expectedValue}"')
def validate_History_Modal_data(context, element, expectedValue):
    currentPage = GlobalVar.currentPage
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'History' + element).text
    assert actualValue == expectedValue


@step('Validate parameter information should be available')
def Validate_parameter_information(context):
    currentPage = GlobalVar.currentPage
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'CSIDValue').get_attribute('value')
    try:
        assert actualValue.strip() == GlobalVar.testParams.get('serviceId').strip()
    except:
        assert actualValue.strip() == GlobalVar.testParams.get('mwrId').strip()


@step('RollBack button should be not available in action column')
def Validate_RollBack_config_button_should_not_available(context):
    currentPage = GlobalVar.currentPage
    RollBackButton = context.baseReader.getElementLocatorValue(context, currentPage, 'RollBackButton')
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, RollBackButton)),
                                                message='Element not visible')


@step('I read service id for UI testcase')
def read_service_id(context):
    GlobalVar.testParams['serviceId'] = GlobalVar.testParams.get('serviceId')
    GlobalVar.baseTest = GlobalVar.testParams.get('Testcase')
    print(GlobalVar.testParams['serviceId'])
    print(GlobalVar.baseTest)

@step('Search the selected service ID and click on the result')
def search_By_ServiceID(context):
    currentPage = GlobalVar.currentPage
    serviceIDSearchXpath = context.baseReader.readElementByPropertyName(currentPage, "serviceIDSearch").get("value")
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, serviceIDSearchXpath)))
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'serviceIDSearch').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'serviceIDSearch').send_keys(
        GlobalVar.testParams['serviceId'])
    time.sleep(5)


@step('Update the required values of parameter information for "{value}" scenario')
def update_parameter_information(context, value):
    currentPage = GlobalVar.currentPage
    dashboardLoadingImageXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                           "dashboardLoadingImage")
    WebDriverWait(context.driver, 20).until(
        EC.invisibility_of_element_located((By.XPATH, dashboardLoadingImageXpath)))

    # Add steps to check service exists before modify
    operationResult = context.baseReader.getElementByPropertyName(context, currentPage, "firstOperationResult").text
    operationType = context.baseReader.getElementByPropertyName(context, currentPage, "firstOperationType").text
    if operationResult == 'COMPLETED':
        assert operationType in ["modify service", "create service", "rollback service"]
    elif operationResult == 'CANCELLED':
        assert operationType == "modify service"

    context.baseReader.getElementByPropertyName(context, currentPage, 'positiveActionButton').click()
    dashboardLoadingImageXpath = context.baseReader.readElementByPropertyName(currentPage,
                                                                              "dashboardLoadingImage").get("value")
    WebDriverWait(context.driver, 20).until(
        EC.invisibility_of_element_located((By.XPATH, dashboardLoadingImageXpath)))

    if value == "success":
        successIPV4val = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                     'IPV4ProviderPrefix0').get_attribute('value')
        GlobalVar.testParams['OriginalPrefixValue'] = successIPV4val
        context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').clear()
        GlobalVar.testParams['ModifiedPrefixValue'] = generateNewPrefix(GlobalVar.testParams['OriginalPrefixValue'])
        context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').send_keys(
            GlobalVar.testParams['ModifiedPrefixValue'])

    elif value == "timeout":
        timeoutIPV4val = context.csvRead[0].get("")
        context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').send_keys(
            timeoutIPV4val)

    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Save').click()


def generateNewPrefix(originalPrefixValue):
    randomVal = str(random.randint(0, 9))
    if GlobalVar.tempVal is None:
        GlobalVar.tempVal = str(random.randint(0, 9))
    elif randomVal != GlobalVar.tempVal:
        GlobalVar.tempVal = randomVal
    else:
        while randomVal != GlobalVar.tempVal:
            GlobalVar.tempVal = randomVal

    index = None
    replaceValue = originalPrefixValue.split(".")[2]
    if len(replaceValue) == 1:
        index = 6
    elif len(replaceValue) == 2:
        index = 7

    modifiedPrefixValue = originalPrefixValue[:index] + GlobalVar.tempVal + originalPrefixValue[index + 1:]
    if modifiedPrefixValue == originalPrefixValue:
        modifiedPrefixValue = generateNewPrefix(originalPrefixValue)
    return modifiedPrefixValue


@step('Wait for next page to load and validate the configurations for "{value}" scenario')
def validate_configurations(context, value):
    counter = False
    currentPage = GlobalVar.currentPage
    dashboardLoadingImageXpath = context.baseReader.readElementByPropertyName(currentPage,
                                                                              "dashboardLoadingImage").get("value")
    WebDriverWait(context.driver, 20).until(
        EC.invisibility_of_element_located((By.XPATH, dashboardLoadingImageXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'okAlert').click()

    updatedServiceLoaderXpath = context.baseReader.readElementByPropertyName(currentPage,
                                                                             "updatedServiceLoader").get("value")
    WebDriverWait(context.driver, 500).until(
        EC.invisibility_of_element_located((By.XPATH, updatedServiceLoaderXpath)))

    currentConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'reviewUpdateConfig').text
    context.baseReader.getElementByPropertyName(context, currentPage, 'currentConfigButton').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'expectedConfigButton').click()
    expectedConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'reviewUpdateConfig').text

    if (GlobalVar.testParams['serviceId'] in currentConfig) and (
            GlobalVar.testParams['serviceId'] in expectedConfig):
        counter = True
        assert counter

    GlobalVar.testParams['updatedRequestId'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                           'updatedRequestId').text


@step('Update the "{value}" IPV4ProviderPrefixes in Parameter edit Form')
def click_button(context, value):
    currentPage = GlobalVar.currentPage
    time.sleep(10)
    if value == "success":
        successIPV4val = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                     'IPV4ProviderPrefix0').get_attribute('value')
        GlobalVar.testParams['OriginalPrefixValue'] = successIPV4val
        context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').clear()
        GlobalVar.testParams['ModifiedPrefixValue'] = generateNewPrefix(GlobalVar.testParams['OriginalPrefixValue'])
        context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').send_keys(
            GlobalVar.testParams['ModifiedPrefixValue'])

    elif value == "timeout":
        timeoutIPV4val = context.csvRead[0].get("")
        context.baseReader.getElementByPropertyName(context, currentPage, 'IPV4ProviderPrefix0').send_keys(
            timeoutIPV4val)
    time.sleep(5)


@step('I fill the required parameters for Execution details form')
def fill_details_execution_form(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'reasonForChange').send_keys('testAutomation')
    context.baseReader.getElementByPropertyName(context, currentPage, 'workOrderChange').send_keys('testAutomation')
    context.baseReader.getElementByPropertyName(context, currentPage, 'performButton').click()


@step('Status should be updated for "{value}" in the BI service dashboard table')
def validate_result_bi_service_dashboard(context, value):
    currentPage = GlobalVar.currentPage
    time.sleep(200)
    context.driver.refresh()
    serviceIdSearchBox = context.baseReader.getElementLocatorValue(context, currentPage, 'serviceIDSearch')
    WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, serviceIdSearchBox))).click()
    serviceId = GlobalVar.testParams['serviceId']
    context.baseReader.getElementByPropertyName(context, currentPage, 'serviceIDSearch').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'serviceIDSearch').send_keys(serviceId)
    dashboardLoadingImageXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                           "dashboardLoadingImage")
    WebDriverWait(context.driver, 20).until(
        EC.invisibility_of_element_located((By.XPATH, dashboardLoadingImageXpath)))
    operationTypeValue = context.baseReader.getElementByPropertyName(context, currentPage, 'operationType').text
    operationResultValue = context.baseReader.getElementByPropertyName(context, currentPage, 'operationResult').text
    assert operationTypeValue == "modify service"

    if value == "AcceptContinue":
        assert operationResultValue == "COMPLETED"
    elif value == "CancelScenario":
        assert operationResultValue == "CANCELLED"
        requestIdValue = context.baseReader.getElementByPropertyName(context, currentPage, 'requestIdValue').text
        assert requestIdValue == GlobalVar.testParams['updatedRequestId']


@step('I validate the request is successfully deleted from service queue')
def service_successfully_deleted(context):
    currentPage = GlobalVar.currentPage
    successfullyDeletedPopupXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                              "successfullyDeletedPopup")
    WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, successfullyDeletedPopupXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'okAlert').click()

    pageTitleXpath = context.baseReader.getElementLocatorValue(context, currentPage, "pageTitle")
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, pageTitleXpath)))

    try:
        elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
        WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))

    except:
        tableDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'tableData')
        WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, tableDataXpath)))
        requestIdListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'requestIdList')
        requestIdList = context.driver.find_elements(By.XPATH, requestIdListXpath)
        for i in range(0, len(requestIdList)):
            assert requestIdList[i].text != GlobalVar.testParams['updatedRequestId']


@step('I validate the customer service is not present in service update queue')
def service_not_present_in_Queue(context):
    currentPage = GlobalVar.currentPage
    try:
        tableDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'tableData')
        WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, tableDataXpath)))
        requestIdListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'requestIdList')
        requestIdList = context.driver.find_elements(By.XPATH, requestIdListXpath)
        for i in range(0, len(requestIdList)):
            assert requestIdList[i].text != GlobalVar.testParams['updatedRequestId']
            print("service id is not present")
    except:
        NoDataFound = context.baseReader.getElementLocatorValue(context, currentPage, "NoDataFound")
        WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, NoDataFound)))
        print("service id is not present")


@step('I set data values against testcase "{testCase}"')
def read_data(context, testCase):
    GlobalVar.testParams = context.csvRead[int(testCase) - 1]


@step('Filter and search the "{value}" for update request')
def filter_service(context, value):
    currentPage = GlobalVar.currentPage
    serviceIDSearchXpath = context.baseReader.readElementByPropertyName(currentPage, "serviceIDSearch").get("value")
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, serviceIDSearchXpath)))
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'serviceIDSearch').send_keys(Keys.ARROW_UP)
    context.baseReader.getElementByPropertyName(context, currentPage, 'serviceIDSearch').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'serviceIDSearch').send_keys(
        GlobalVar.testParams[value])
    firstResultXpath = context.baseReader.getElementLocatorValue(context, currentPage, "firstServiceResult")
    WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, firstResultXpath), GlobalVar.testParams[value]))


@step('Validate that "{element}" should be "{expectedValue}"')
def validate_data(context, element, expectedValue):
    currentPage = GlobalVar.currentPage
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, element).text
    assert actualValue.lower().strip() == expectedValue.lower().strip()


@step('Open "{element}" box by expanding the row')
def expand_row(context, element):
    currentPage = GlobalVar.currentPage
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'positiveActionButton').click()
    paramBoxXpath = context.baseReader.getElementLocatorValue(context, currentPage, "parameterInformation")
    temp = WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, paramBoxXpath), element))


@step('Update "{param}" value for the service')
def change_param(context, param):
    currentPage = GlobalVar.currentPage
    paramBoxXpath = context.baseReader.getElementLocatorValue(context, currentPage, param)
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, paramBoxXpath)))
    paramVal = 'test_' + param + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    context.baseReader.getElementByPropertyName(context, currentPage, param).click()
    context.baseReader.getElementByPropertyName(context, currentPage, param).clear()
    context.baseReader.getElementByPropertyName(context, currentPage, param).send_keys(paramVal)


@step('An "{popup}" box should open')
def popup_box(context, popup):
    currentPage = GlobalVar.currentPage
    paramBoxXpath = context.baseReader.getElementLocatorValue(context, currentPage, popup)
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, paramBoxXpath)))


@step('I validate the "{messageType}" message in the "{popupType}" box for "{scenario}"')
def alert_message(context, messageType, popupType, scenario):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    actualMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'alertMessage').text
    GlobalVar.testParams[messageType + '_message'] = actualMessage
    if messageType == 'confirm':
        expectedMessage = GlobalVar.testParams[messageType + "Message_" + scenario].format(RequestID['oldRequestID'])
    else:
        expectedMessage = GlobalVar.testParams[messageType + "Message_" + scenario]

    # assert GlobalVar.testParams[messageType + "_message"] == expectedMessage
    # assert actualMessage == expectedMessage
    print(actualMessage == expectedMessage)


@step('I refresh the page and wait for the dashboard to load')
def refresh_and_load(context):
    currentPage = GlobalVar.currentPage
    context.driver.refresh()
    # noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
    # WebDriverWait(context.driver, 40).until(EC.invisibility_of_element_located((By.XPATH, noDataXpath)))
    # elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, element)
    # WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))
    time.sleep(10)


@step('Validate same "{messageType}" message is displayed upon mouse hover on operation result link')
def validate_error(context, messageType):
    currentPage = GlobalVar.currentPage
    operationResultElement = context.baseReader.getElementByPropertyName(context, currentPage, messageType + 'Message')
    context.driver.find_element(By.XPATH, "//h3").click()
    ActionChains(context.driver).move_to_element(operationResultElement).perform()
    errorMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'errorPopUp')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, errorMessageXpath)))
    message = context.baseReader.getElementByPropertyName(context, currentPage, 'errorPopUp').text
    # assert message == GlobalVar.testParams[messageType + '_message']


@step('Validate same "{messageType}" message is displayed upon clicking on alert button')
def validate_error(context, messageType):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'alertErrorButton').click()
    errorMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alertErrorMessage')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, errorMessageXpath)))
    errorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'alertErrorMessage').text
    # assert GlobalVar.testParams[messageType + '_message'] == errorMessage


@step('Expand the row and validate the error message is "{message}"')
def expand_row(context, message):
    currentPage = GlobalVar.currentPage
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'positiveActionButton').click()
    paramBoxXpath = context.baseReader.getElementLocatorValue(context, currentPage, "DataNotAvailable")
    WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, paramBoxXpath), message))


@step('I filter and search the "{searchParam}" parameter')
def step_impl(context, searchParam):
    currentPage = GlobalVar.currentPage
    searchParamXpath = context.baseReader.readElementByPropertyName(currentPage, searchParam).get("value")
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, searchParamXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, searchParam).send_keys(Keys.ARROW_UP)
    context.baseReader.getElementByPropertyName(context, currentPage, searchParam).click()
    context.baseReader.getElementByPropertyName(context, currentPage, searchParam).send_keys(
        GlobalVar.testParams[searchParam])


@step('Wait for the "{searchParam}" search results to appear as expected')
def step_impl(context, searchParam):
    currentPage = GlobalVar.currentPage
    loaderXpath = context.baseReader.getElementLocatorValue(context, currentPage, "LoadingGif")
    try:
        WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, loaderXpath)))
        WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))
        firstResultXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                     "first" + searchParam + "Result")
        WebDriverWait(context.driver, 10).until(
            EC.text_to_be_present_in_element_value((By.XPATH, firstResultXpath), GlobalVar.testParams[searchParam]))
        firstResult = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                     "first" + searchParam + "Result").text
        assert GlobalVar.testParams[searchParam] in searchParam

    except:
        firstResultXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                     "first" + searchParam + "Result")
        WebDriverWait(context.driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, firstResultXpath), GlobalVar.testParams[searchParam]))


@step('Validate that "{resultCount}" row should appear in results')
def step_impl(context, resultCount):
    currentPage = GlobalVar.currentPage
    serviceIdListXpath = context.baseReader.getElementLocatorValue(context, currentPage, "serviceIdList")
    serviceIdList = context.driver.find_elements(By.XPATH, serviceIdListXpath)
    assert len(serviceIdList) == int(resultCount)


@step('Validate that search results should show "{resultCount}" results')
def step_impl(context, resultCount):
    currentPage = GlobalVar.currentPage
    resultCountText = context.baseReader.getElementByPropertyName(context, currentPage, "resultCountText").text
    assert resultCount + ' Result Show' in resultCountText


@step("Validate that only supported port speeds are displayed")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    portSpeedListXpath = context.baseReader.getElementLocatorValue(context, currentPage, "portSpeedList")
    portSpeedList = context.driver.find_elements(By.XPATH, portSpeedListXpath)
    for i in range(0, len(portSpeedList)):
        assert portSpeedList[i].text in GlobalVar.testParams.get("supportedSpeed")


@step('Validate that all results have the expected result for "{searchParam}"')
def step_impl(context, searchParam):
    currentPage = GlobalVar.currentPage
    paramListXpath = context.baseReader.getElementLocatorValue(context, currentPage, searchParam + "List")
    paramList = context.driver.find_elements(By.XPATH, paramListXpath)
    for i in range(0, len(paramList)):
        assert GlobalVar.testParams.get(searchParam) in paramList[i].text


@step('I validate that the "{messageType}" message is as expected')
def step_impl(context, messageType):
    currentPage = GlobalVar.currentPage
    if messageType == 'confirm':
        assert GlobalVar.testParams[messageType + "_message"] == GlobalVar.testParams[messageType + "Message"]
    else:
        assert GlobalVar.testParams[messageType + "_message"] == GlobalVar.testParams[messageType + "Message"]


@step('I "{operation}" update request for selected service id')
def step_impl(context, operation):
    currentPage = GlobalVar.currentPage
    tableDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'tableData')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, tableDataXpath)))
    serviceIdListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'serviceIdList')
    serviceIdList = context.driver.find_elements(By.XPATH, serviceIdListXpath)
    # index variable will store the row number in which the service is appearing
    index = None
    for i in range(0, len(serviceIdList)):
        if serviceIdList[i].text == GlobalVar.testParams['serviceId']:
            index = str(i + 1)
            # print(index)
            break
    else:
        print('Service not displayed in the list')
    # save the request id for the execute request
    requestIdXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'requestId')
    requestIdXpath = requestIdXpath.replace('index', index)
    RequestID['execute'] = context.driver.find_element(By.XPATH, requestIdXpath).text
    requestType = GlobalVar.testParams.get('RequestType')
    GlobalVar.reqId = GlobalVar.request_ID[requestType] = RequestID['execute']

    # read the xpath for the execute Button and replace the row number with the above index
    ButtonXpath = context.baseReader.getElementLocatorValue(context, currentPage, operation + 'Button')
    ButtonXpath = ButtonXpath.replace('index', index)
    context.driver.find_element(By.XPATH, ButtonXpath).click()
    time.sleep(5)


@step('I click on "{button}" button once visible')
def step_impl(context, button):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, button).send_keys(Keys.ARROW_UP)
    context.baseReader.getElementByPropertyName(context, currentPage, button).click()


@step('I navigate History Modal by clicking on "{action}"')
def click_on_action_button(context, action):
    currentPage = GlobalVar.currentPage
    time.sleep(10)
    actionButton = context.baseReader.getElementLocatorValue(context, currentPage, action)
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, actionButton)),
                                            message='Element not visible')
    context.baseReader.getElementByPropertyName(context, currentPage, 'ActionButton').click()
    time.sleep(5)


@step('Validate "{expectedValue}" are present in "{value}"')
def page_title(context, expectedValue, value):
    currentPage = GlobalVar.currentPage
    time.sleep(10)
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, expectedValue).text
    assert expectedValue.lower() == actualValue.lower()


@step('I search the User by the Username')
def page_title(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementLocatorValue(context, currentPage, 'SearchUser')
    time.sleep(5)
    # WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, SearchUser)),
    #                                         message='Element not visible')
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchUser').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchUser').send_keys('x231081')
    time.sleep(5)


@step('I revoke the user "{value}" button')
def click_button(context, value):
    current_page = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, current_page, value).click()
    time.sleep(5)


@step('I validate the user should be enabled')
def page_title(context):
    currentPage = GlobalVar.currentPage

    time.sleep(5)
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'AccountState').is_enabled()
    assert actualValue


@step('I validate Expected config for "{value}" scenario')
def page_title(context, value):
    currentPage = GlobalVar.currentPage
    global ConfigData
    actualMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ExpectedConfigText').text
    ConfigData['ExpectedConfig'] = actualMessage
    if value == 'success':
        assert ConfigData['ExpectedConfig'] == actualMessage
    elif value == 'failure':
        assert ConfigData['ExpectedConfig'] != actualMessage

        # assert 'Too many concurrent requests in flight in TINAA. Please try again after sometime' == actualMessage
    # assert actualMessage in "data"


@step('I validate Current config should different than expected config')
def page_title(context):
    currentPage = GlobalVar.currentPage
    global ConfigData
    Message = context.baseReader.getElementByPropertyName(context, currentPage, 'CurrentConfigData').text
    ConfigData['CurrentConfig'] = Message
    assert ConfigData['ExpectedConfig'] != ConfigData['CurrentConfig']


@step('I wait to page be loaded')
def page_title(context):
    currentPage = GlobalVar.currentPage
    time.sleep(200)


@step('Service should be updated for "{value}" in the BI service dashboard table')
def validate_result_bi_service_dashboard(context, value):
    currentPage = GlobalVar.currentPage
    serviceIdSearchBox = context.baseReader.getElementLocatorValue(context, currentPage, 'serviceIDSearch')
    WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, serviceIdSearchBox))).click()
    serviceId = GlobalVar.testParams['serviceId']
    context.baseReader.getElementByPropertyName(context, currentPage, 'serviceIDSearch').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'serviceIDSearch').send_keys(serviceId)
    dashboardLoadingImageXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                           "dashboardLoadingImage")
    WebDriverWait(context.driver, 20).until(
        EC.invisibility_of_element_located((By.XPATH, dashboardLoadingImageXpath)))
    operationTypeValue = context.baseReader.getElementByPropertyName(context, currentPage, 'operationType').text
    operationResultValue = context.baseReader.getElementByPropertyName(context, currentPage, 'operationResult').text
    assert operationTypeValue == 'modify service'
    assert operationResultValue == value


@step('I wait and for operation to be completed and refresh the page')
def page_title(context):
    currentPage = GlobalVar.currentPage
    time.sleep(300)
    context.driver.refresh()


@step('I wait for expectedConfig valid response')
def page_title(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)


@step("I validate add new user modal should open")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'ModalAddNewUser').text
    assert actualValue == 'Add New User'


@step("I fill telusID and select role of user")
def fill_user_details(context):
    global addUser
    currentPage = GlobalVar.currentPage
    current_time = datetime.datetime.now()
    context.baseReader.getElementByPropertyName(context, currentPage, 'UserTelusID').send_keys(
        GlobalVar.testParams['XID'])
    context.baseReader.getElementByPropertyName(context, currentPage, 'SelectUserRole').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NewUserAdmin').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SelectUserRole').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'AlertSave').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'AlertOK').click()
    LoadingWait = context.baseReader.readElementByPropertyName(currentPage, 'LoadingGif').get("value")
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, LoadingWait)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'UserAddSuccessAlert').click()
    LoadingWait = context.baseReader.readElementByPropertyName(currentPage, 'LoadingGif').get("value")
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, LoadingWait)))


@step("I validate the user should appear in the search result box")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchUser').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchUser').send_keys(
        GlobalVar.testParams['XID'])
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'TelusID').text
    assert actualValue == 'x322195'


@step("I validate successful alert modal should open")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'AlertModal').text
    assert str(actualValue).lower() in 'User successfully added!'.lower()


@step("I validate successful modal should open")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    time.sleep(15)
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'AlertModal').text
    assert GlobalVar.testParams['AlertMessage'] in str(actualValue).lower()
    time.sleep(10)


@step("I validate Delete modal should open")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'DeleteuserModal').text
    assert actualValue == 'Delete User'


@step("I grant the user to read/write access")
def click_button(context):
    currentPage = GlobalVar.currentPage
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'UserRoleAdminCheckBox').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'YesEditUserRole').click()
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'UserRoleChangeSuccessAlert').click()
    time.sleep(10)


@step("I validate the same xid should display in TelusId box")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'TelusIDDelete').text
    assert actualValue == (GlobalVar.testParams['XID'])


@step('I navigate to "{mailIcon}" section')
def step_impl(context, mailIcon):
    currentPage = GlobalVar.currentPage
    mailIconXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'mailIcon')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, mailIconXpath)),
                                            message='Element not visible').click()


@step('I validate that the account state is "{accountState}"')
def step_impl(context, accountState):
    currentPage = GlobalVar.currentPage
    state['Green'] = GlobalVar.testParams.get('rgbGreenAcc')
    state['Grey'] = GlobalVar.testParams.get('rgbGreyAcc')
    AccountStateValue = context.baseReader.getElementByPropertyName(context, currentPage, 'AccStateBtn')
    AccountStateColor = AccountStateValue.value_of_css_property('background-color')
    if accountState == 'active':
        assert AccountStateColor == state['Green']
    elif accountState == 'inactive':
        assert AccountStateColor == state['Grey']


@step('Validate that "{buttonType}" button should "{scenario}" displayed')
def step_impl(context, buttonType, scenario):
    currentPage = GlobalVar.currentPage
    buttonXpath = context.baseReader.getElementLocatorValue(context, currentPage, buttonType)
    if 'not' in scenario:
        WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, buttonXpath)),
                                                message='Element is visible')
    else:
        WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, buttonXpath)),
                                                message='Element is not visible')


@step("Validate the service is available in service queue")
def step_impl(context):
    global index
    currentPage = GlobalVar.currentPage
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noDataFound")
    WebDriverWait(context.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, noDataXpath)))
    serviceIdListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'serviceIdList')
    serviceIdList = context.driver.find_elements(By.XPATH, serviceIdListXpath)
    print("searching for {}".format(GlobalVar.testParams['serviceId']))

    # index variable will store the row number in which the service is appearing
    index = None
    for i in range(0, len(serviceIdList)):
        if serviceIdList[i].text == GlobalVar.testParams['serviceId']:
            index = str(i + 1)
            break
    else:
        print('Service not found..')


@step('Click on "{button}" button in service queue table to open "{expectedParam}"')
def click_button(context, button, expectedParam):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    # read the xpath for the expandButton and replace the row number with the above index
    paramXpath = context.baseReader.getElementLocatorValue(context, currentPage, button)
    paramXpath = paramXpath.replace('index', index)
    time.sleep(5)
    context.driver.find_element(By.XPATH, paramXpath).click()
    expectedItemXpath = context.baseReader.getElementLocatorValue(context, currentPage, expectedParam)
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, expectedItemXpath)),
                                            message='Element is not visible')
    time.sleep(5)


@step("Wait for loader bar to disappear")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    LoadingWait = context.baseReader.getElementLocatorValue(context, currentPage, 'LoadingGif')
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, LoadingWait)))


@step('I validate that the user role "{role}" is "{roleState}"')
def step_impl(context, role, roleState):
    currentPage = GlobalVar.currentPage
    state['Green'] = GlobalVar.testParams.get('rgbGreen')
    state['Grey'] = GlobalVar.testParams.get('rgbGrey')
    roleStateValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, role)
    roleStateValue = WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, roleStateValueXpath)))
    roleStateColor = roleStateValue.value_of_css_property('background-color')

    if roleState == 'enabled':
        assert roleStateColor == state['Green']
    elif roleState == 'disabled':
        assert roleStateColor == state['Grey']


@step('I double click on "{button}" button')
def step_impl(context, button):
    currentPage = GlobalVar.currentPage
    button = context.baseReader.getElementByPropertyName(context, currentPage, button)
    action = ActionChains(context.driver)
    action.double_click(button).perform()


@step('Assert that "{element}" is displayed')
def step_impl(context, element):
    currentPage = GlobalVar.currentPage
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, element)
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))


@step('Assert that "{element}" button is not displayed')
def step_impl(context, element):
    currentPage = GlobalVar.currentPage
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, element)
    element = WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, elementXpath)))
    assert element


@step('Validate that a "{precedence}" "{element}" is generated for "{scenarioType}"')
def step_impl(context, precedence, element, scenarioType):
    currentPage = GlobalVar.currentPage
    xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'updatedRequestId')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    heading = context.baseReader.getElementByPropertyName(context, currentPage, 'updatedRequestId').text
    RequestID[precedence + element] = heading.split(":")[1].strip()
    # assert requestIds[scenario + 'New'] != requestIds[scenario + 'Old']
    GlobalVar.reqId = GlobalVar.requestId = RequestID[precedence + element]


@step('Assert that response for "{configType}" config is "{configMessage}"')
def step_impl(context, configType, configMessage):
    currentPage = GlobalVar.currentPage
    try:
        time.sleep(2)
        ConfigData[configType] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                             '{}ConfigData'.format(configType)).text
        assert ConfigData[configType]
        context.baseReader.getElementByPropertyName(context, currentPage, '{}ConfigButton'.format(configType)).click()

    except:
        context.baseReader.getElementByPropertyName(context, currentPage, '{}ConfigButton'.format(configType)).click()
        time.sleep(2)
        ConfigData[configType] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                             '{}ConfigData'.format(configType)).text
        assert ConfigData[configType]
        context.baseReader.getElementByPropertyName(context, currentPage, '{}ConfigButton'.format(configType)).click()

    finally:
        if 'Progress' in configMessage:
            assert ConfigData[configType] == configMessage
        else:
            assert ConfigData[configType] == GlobalVar.testParams.get('{}ConfigData'.format(configType))


@step('Validate that service request has "{field}" as "{fieldValue}"')
def step_impl(context, field, fieldValue):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    # read the xpath for the expandButton and replace the row number with the above index
    valueXpath = context.baseReader.getElementLocatorValue(context, currentPage, field)
    valueXpath = valueXpath.replace('index', index)
    time.sleep(5)
    actualValue = context.driver.find_element(By.XPATH, valueXpath).text
    assert actualValue == fieldValue


@step('Wait for "{sec}" seconds')
def step_impl(context, sec):
    print("Waiting {} seconds for response".format(sec))
    time.sleep(int(sec))


@step('Validate the service is "{availability}" in service queue')
def step_impl(context, availability):
    global index
    currentPage = GlobalVar.currentPage
    try:
        noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noDataFound")
        WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, noDataXpath)))

    except:
        serviceIdListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'serviceIdList')
        serviceIdList = context.driver.find_elements(By.XPATH, serviceIdListXpath)
        print("searching for {}".format(GlobalVar.testParams['serviceId']))

        # index variable will store the row number in which the service is appearing
        index = None
        for i in range(0, len(serviceIdList)):
            if serviceIdList[i].text == GlobalVar.testParams['serviceId']:
                index = str(i + 1)
                break
        else:
            assert index is None


@step('Validate that "{old}" and "{new}" "{element}" are "{matchType}" for "{scenarioType}"')
def step_impl(context, old, new, element, matchType, scenarioType):
    if 'diff' in matchType:
        assert RequestID[old + element] != RequestID[new + element]
    else:
        assert RequestID[old + element] == RequestID[new + element]


@step('I read the "{precedence}" "{field}" for "{scenarioType}" scenario')
def step_impl(context, precedence, field, scenarioType):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    # read the xpath and replace the row number with the above index
    valueXpath = context.baseReader.getElementLocatorValue(context, currentPage, field)
    valueXpath = valueXpath.replace('index', index)
    RequestID[precedence + 'RequestID'] = context.driver.find_element(By.XPATH, valueXpath).text
    print(RequestID)


@step('"{element}" should not be available in "{column}" column for latest transaction')
def Validate_RollBack_button(context, element, column):
    currentPage = GlobalVar.currentPage
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, element)
    element = WebDriverWait(context.driver, 5).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))
    assert not element


@step('Wait for the "{popupType}" message if appears and click "{button}"')
def step_impl(context, popupType, button):
    currentPage = GlobalVar.currentPage
    try:
        paramBoxXpath = context.baseReader.getElementLocatorValue(context, currentPage, popupType)
        WebDriverWait(context.driver, 5).until(EC.visibility_of_element_located((By.XPATH, paramBoxXpath)))
        actualMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'alertMessage').text
        GlobalVar.testParams['alert_Message'] = actualMessage
        assert GlobalVar.testParams['alert_Message'] == GlobalVar.testParams['alertMessage']

    except Exception as err:
        print(err)


@then('I validate the rolling back Request ID for "{scenario}" scenario')
def step_impl(context, scenario):
    currentPage = GlobalVar.currentPage


@step('I validate the "{precedence}" "{element}" for "{scenarioType}" scenario in history modal')
def Validate_RequestId(context, precedence, element, scenarioType):
    currentPage = GlobalVar.currentPage
    reqID = context.baseReader.getElementByPropertyName(context, currentPage, element + precedence).text
    assert reqID == RequestID[precedence + element]
    RequestID[precedence] = reqID


@step('I search for the "{precedence}" "{element}" for "{scenarioType}" scenario in history modal')
def step_impl(context, precedence, element, scenarioType):
    currentPage = GlobalVar.currentPage
    RequestID[precedence + element] = context.baseReader.getElementByPropertyName(
        context, currentPage, element + precedence).text
    GlobalVar.reqId = RequestID[precedence + element]
    print(RequestID)


@step('Validate that "{configType}" config has response as "{configMessage}"')
def step_impl(context, configType, configMessage):
    currentPage = GlobalVar.currentPage
    time.sleep(10)
    xpath = context.baseReader.getElementLocatorValue(context, currentPage, '{}ConfigData'.format(configType))
    ConfigData[configType] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                         '{}ConfigData'.format(configType)).text
    assert ConfigData[configType].strip() == GlobalVar.testParams.get('{}ConfigData'.format(configType))


@step('Validate the "{messageType}" message is same as returned earlier')
def validate_error(context, messageType):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'alertErrorButton').click()
    errorMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alertErrorMessage')
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, errorMessageXpath)))
    errorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'alertErrorMessage').text
    print(errorMessage)
    assert messageType == GlobalVar.response.json().get('status')
    assert errorMessage == GlobalVar.response.json().get('reason')[0]
    context.baseReader.getElementByPropertyName(context, currentPage, 'alertErrorButtonClose').click()
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, errorMessageXpath)))


@step(u'I change the user role to "{newRole}" from "{oldRole}"')
def change_user_role(context, newRole, oldRole):
    currentPage = GlobalVar.currentPage

    roleStateValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, newRole)
    roleStateValue = WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, roleStateValueXpath)))
    roleStateColor = roleStateValue.value_of_css_property('background-color')

    if roleStateColor == state['Green']:
        roleStateValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, oldRole)
        WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, roleStateValueXpath))).click()

    elif roleStateColor == state['Grey']:
        WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, roleStateValueXpath))).click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'YesEditUserRole').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'UserRoleChangeSuccessAlert').click()
    LoadingWait = context.baseReader.readElementByPropertyName(currentPage, 'LoadingGif').get("value")
    WebDriverWait(context.driver, 20).until(EC.invisibility_of_element_located((By.XPATH, LoadingWait)))


@step('Validate that all results have the expected result for "{searchParam}" for "{matchType}" search')
def step_impl(context, searchParam, matchType):
    currentPage = GlobalVar.currentPage
    paramListXpath = context.baseReader.getElementLocatorValue(context, currentPage, searchParam + "List")
    paramList = context.driver.find_elements(By.XPATH, paramListXpath)
    for i in range(0, len(paramList)):
        if 'exact' in matchType:
            assert paramList[i].text.lower() == GlobalVar.testParams.get(searchParam).lower()
        else:
            assert GlobalVar.testParams.get(searchParam).lower() in paramList[i].text.lower()


@step('Wait for the search results to appear')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    loaderXpath = context.baseReader.getElementLocatorValue(context, currentPage, "LoadingGif")
    try:
        WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, loaderXpath)))
        WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))
    except:
        time.sleep(5)


@step('Validate that no search result is displayed')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noData")
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, noDataXpath)))


@when('Clear the search field "{searchParam}"')
def step_impl(context, searchParam):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, searchParam).send_keys(Keys.CONTROL + "a")
    context.baseReader.getElementByPropertyName(context, currentPage, searchParam).send_keys(Keys.DELETE)


@then('Validate that the "{button}" button is "{displayType}"')
def step_impl(context, button, displayType):
    currentPage = GlobalVar.currentPage
    buttonVisibility = context.baseReader.getElementByPropertyName(context, currentPage, button).is_enabled()
    if displayType == 'enabled':
        assert buttonVisibility
    else:
        assert not buttonVisibility


@step('Validate that "{add}" and "{remove}" button under customer prefixes are not present')
def step_impl(context, add, remove):
    currentPage = GlobalVar.currentPage


@then('Validate that the "{fieldName}" field is "{visiblityType}"')
def step_impl(context, fieldName, visiblityType):
    currentPage = GlobalVar.currentPage
    fieldVisibility = context.baseReader.getElementByPropertyName(context, currentPage, fieldName).is_enabled()
    # print(fieldVisibility)
    if visiblityType == 'enabled':
        assert fieldVisibility
    else:
        assert not fieldVisibility


@when('I clear "{fieldName}" field and click "{button}" button')
def step_impl(context, fieldName, button):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, fieldName).send_keys(Keys.CONTROL + "a")
    context.baseReader.getElementByPropertyName(context, currentPage, fieldName).send_keys(Keys.DELETE)
    context.baseReader.getElementByPropertyName(context, currentPage, button).click()


@then('Validate error message for "{fieldName}" field should be "{expectedErrorMessage}"')
def step_impl(context, fieldName, expectedErrorMessage):
    currentPage = GlobalVar.currentPage
    actualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage, fieldName + 'Error').text
    assert actualErrorMessage == expectedErrorMessage


@step('Validate the expected "{messageType}" message')
def step_impl(context, messageType):
    currentPage = GlobalVar.currentPage
    expectedMessage = GlobalVar.testParams.get(messageType + "Message")
    assert Errormsg['Old'] == expectedMessage