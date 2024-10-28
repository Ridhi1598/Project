import difflib
import json
import random
import string
import time
import os
import sys
import ssl
import zipfile
import getpass
import os

import pysftp
import gzip
import shutil
from os.path import dirname, abspath
import jsonschema as jsonschema
import requests
import datetime

from delayed_assert import expect
from selenium import webdriver
from behave import given, when, then, step
from jsonschema import validate
from requests import HTTPError
from selenium.webdriver import ActionChains
from selenium.webdriver.common import keys
from sqlalchemy.sql.functions import user

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
from features.steps.lcd.lcd_uiFunctional import navigate_to_nextPage
from features.steps.ui_steps_general import page_title_validation, change_currentPage
from selenium.webdriver.support.select import Select
from common.util.payloadGenerator import payloadGenerator
from selenium.webdriver.common.action_chains import ActionChains
from features.steps.globalVar import GlobalVar
from selenium.common.exceptions import TimeoutException
from features.steps.bi.bi_uiFunctional import read_data
from features.steps.lcd.lcd_uiFunctional import navigate_to_nextPage
from common.util.textReadCompare import delete_create_text_file
from common.util.textReadCompare import compare_text_file

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
nodeDetails = {}
nodeNameList = []
lagNameList = []
OLTConfigurationValues = []
BNGIPV4ConfigurationValues = []
BNGIPV6ConfigurationValues = []
BNGCommunityDefinitionsValues = []
OLTMacAddressesValues = []
SEEvpnElementvalues = []
HSIAIESElementValues = []


@step(u'I should land on CS Home page')
def step_impl(context):
    global loginStatus
    currentPage = "LandingPage"
    url = sys.argv[1] + 'URL_' + sys.argv[2]
    context.driver.get(context.config.get(url))
    pageHeadingXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'pageHeading')
    pageHeading = WebDriverWait(context.driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, pageHeadingXpath))).text

    if pageHeading == 'Dashboard':
        pass
    else:
        LoginXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Login')
        WebDriverWait(context.driver, 40).until(
            EC.visibility_of_element_located((By.XPATH, LoginXpath)))
        time.sleep(2)
        context.baseReader.getElementByPropertyName(context, currentPage, 'Login').click()
        currentPage = 'KeycloakLoginPage'
        titleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'PageTitle')
        WebDriverWait(context.driver, 40).until(
            EC.visibility_of_element_located((By.XPATH, titleXpath)))
        # readOnlyStatus = bool(GlobalVar.testParams.get('readOnly'))
        # username = context.envReader.get("TestUserNameReadOnly")
        # password = context.envReader.get('TestUserPassReadOnly')
        username = context.envReader.get("CSPortalTestUserName")
        password = context.envReader.get('CSPortalTestUserPassword')

    usernameXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'UserName')
    WebDriverWait(context.driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, usernameXpath))).send_keys(username)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Password').send_keys(password)
    context.baseReader.getElementByPropertyName(context, currentPage, 'LoginButton').click()
    WebDriverWait(context.driver, 100).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    titleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'title')
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, titleXpath)))


@given("Landing Directly to the dashboard page")
def step_impl(context):
    global loginStatus
    currentPage = "LandingPage"
    url = sys.argv[1] + 'URL_' + sys.argv[2]
    context.driver.get(context.config.get(url))
    pageHeadingXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'pageHeading')
    WebDriverWait(context.driver, 40).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))


@step('I expand the "{value}" sidebar')
def expand_sidebar(context, value):
    currentPage = GlobalVar.currentPage
    # WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, value)))
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()


@step('I navigate view by clicking on "{value}" for CS')
def navigate_to_nextPage(context, value):
    currentPage = GlobalVar.currentPage
    element = context.baseReader.getElementByPropertyName(context, currentPage, value)
    context.driver.execute_script("arguments[0].click();", element)
    time.sleep(2)


@step('I enter the node details and add "{expectedValue}"')
def enter_details(context, expectedValue):
    currentPage = GlobalVar.currentPage
    global nodeDetails
    nodeDetails = {key: value for key, value in GlobalVar.testParams.items() if key.startswith(expectedValue)}
    print("Printing Node Details:")
    print(nodeDetails)
    for key, value in nodeDetails.items():
        print("Key is:" + key + "Value is:" + value)
        WebDriverWait(context.driver, 30).until(EC.invisibility_of_element((By.XPATH, "MainLoader")))
        context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewNode').click()
        time.sleep(1)
        print("Before PlaceHolderClick")
        context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').click()
        time.sleep(1)
        print("After PlaceHolderClick")
        print(value)
        context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').send_keys(value)
        time.sleep(1)
        context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
        time.sleep(2)


@when('I enter "{nodeName}" and add a OLT node')
def add_Nodes(context, nodeName):
    currentPage = GlobalVar.currentPage
    WebDriverWait(context.driver, 2).until(EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewNode').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').send_keys(nodeName)
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()


@then('I validate "{nodeName}" node is {type} successfully')
def step_impl(context, nodeName, type):
    flag = False
    currentPage = GlobalVar.currentPage
    time.sleep(4)
    Node_ListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'NodeList')
    Node_Value = context.driver.find_elements(By.XPATH, Node_ListXpath)

    for i in range(0, len(Node_Value)):
        if (nodeName in Node_Value[i].text):
            flag = True
            break

    if (type in "added"):
        assert True == flag
    if (type in "deleted"):
        assert False == flag


@then('I validate "{Lag}" lag is {type} for "{OLTName}" Node')
def step_impl(context, Lag, OLTName, type):
    flag = False
    currentPage = GlobalVar.currentPage
    time.sleep(3)
    Node_ListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'NodeList')
    Node_Value = context.driver.find_elements(By.XPATH, Node_ListXpath)
    for i in range(0, len(Node_Value)):
        if (OLTName in Node_Value[i].text):
            time.sleep(3)
            Node_Value[i].click()
            Lag_Value = context.driver.find_elements(By.XPATH,
                                                     context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                               'LagList'))
            for j in range(0, len(Lag_Value)):
                if (Lag in Lag_Value[j].text):
                    flag = True
                    break
    if (type in "added"):
        assert True == flag
    if (type in "deleted"):
        assert False == flag


@step('I enter the "{nodeDetails}" and add BNG1, BNG2, SE-Y-1, SE-Y-2')
def enter_details(context, nodeDetails):
    currentPage = GlobalVar.currentPage

    WebDriverWait(context.driver, 300).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').click()
    time.sleep(2)
    BNG1NodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').send_keys(
        GlobalVar.testParams.get('BNG1Name'))
    print(BNG1NodeName)
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
    time.sleep(5)

    WebDriverWait(context.driver, 300).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewNode').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').click()
    time.sleep(2)
    BNG2NodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').send_keys(
        GlobalVar.testParams.get('BNG2Name'))
    print(BNG2NodeName)
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
    time.sleep(5)

    WebDriverWait(context.driver, 300).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewNode').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').click()
    time.sleep(2)
    SE_Y_1NodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').send_keys(
        GlobalVar.testParams.get('SE-Y-1Name'))
    print(SE_Y_1NodeName)
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
    time.sleep(5)

    WebDriverWait(context.driver, 300).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewNode').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').click()
    time.sleep(2)
    SE_Y_2NodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').send_keys(
        GlobalVar.testParams.get('SE-Y-2Name'))
    print(SE_Y_2NodeName)
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
    time.sleep(5)
    WebDriverWait(context.driver, 300).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))


@step('I enter the "{nodeDetails}" and add BNG1 and BNG2')
def enter_details(context, nodeDetails):
    currentPage = GlobalVar.currentPage

    WebDriverWait(context.driver, 300).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').click()
    time.sleep(2)
    BNG1NodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').send_keys(
        GlobalVar.testParams.get('BNG1Name'))
    print(BNG1NodeName)
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
    time.sleep(5)

    WebDriverWait(context.driver, 300).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewNode').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').click()
    time.sleep(2)
    BNG2NodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodePlaceHolder').send_keys(
        GlobalVar.testParams.get('BNG2Name'))
    print(BNG2NodeName)
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
    time.sleep(5)
    WebDriverWait(context.driver, 300).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))


@step('I verify that the node has been added')
def verify_node(context):
    currentPage = GlobalVar.currentPage
    i = 1
    for key, value in nodeDetails.items():
        OLTnodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'Node' + str(i) + 'Box').text
        nodeName = OLTnodeName.split()
        assert value == nodeName[0]
        i += 1


@step('I verify what node has been added')
def verify_node(context):
    currentPage = GlobalVar.currentPage
    i = 1
    for key, value in nodeDetails.items():
        AddednodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'Node' + str(i) + 'Box').text
        nodeName = AddednodeName.split()
        print('Tried to enter node: ' + value)
        AllowedNodeName = (nodeName[0])[0:12]
        print('Node name that should have been allowed: ' + AllowedNodeName)
        # print(value)
        # print(nodeName)
        assert AllowedNodeName == nodeName[0]
        print('Assertion Successful')
        i += 1


@step('I verify that BNG1, BNG2, SE-Y-1, SE-Y-2 have been added')
def verify_node(context):
    currentPage = GlobalVar.currentPage

    BNG1NewNodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'BNG1NewAddedNode').text
    print(BNG1NewNodeName)
    assert "EDTNAB01NG01" in BNG1NewNodeName

    BNG2NewNodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'BNG2NewAddedNode').text
    print(BNG2NewNodeName)
    assert "EDTNAB01NG02" in BNG2NewNodeName

    SE_Y_1NewNodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'SE_Y_1NewAddedNode').text
    print(SE_Y_1NewNodeName)
    assert "EDTNAB03SE01" in SE_Y_1NewNodeName

    SE_Y_2NewNodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'SE_Y_2NewAddedNode').text
    print(SE_Y_2NewNodeName)
    assert "EDTNAB03SE04" in SE_Y_2NewNodeName


@step('I verify that BNG1 and BNG2 have been added')
def verify_node(context):
    currentPage = GlobalVar.currentPage
    time.sleep(10)

    BNG1NewNodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'BNG1NewAddedNode').text

    assert "EDTNAB01NG01" in BNG1NewNodeName

    BNG2NewNodeName = context.baseReader.getElementByPropertyName(context, currentPage, 'BNG2NewAddedNode').text

    assert "EDTNAB01NG02" in BNG2NewNodeName


@step('I search for the OLT for which the node needs to be added')
def search_node(context):
    currentPage = GlobalVar.currentPage
    WebDriverWait(context.driver, 40).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys("EDTNAB01NG01")


@step('I select the OLT from the search results')
def search_result(context):
    currentPage = GlobalVar.currentPage
    firstOLTName = context.baseReader.getElementByPropertyName(context, currentPage, 'OLTNameFirstValue').text
    assert firstOLTName == "EDTNAB01NG01"
    print(firstOLTName)
    context.baseReader.getElementByPropertyName(context, currentPage, 'OLTNameFirstValue').click()
    Node1 = context.baseReader.getElementByPropertyName(context, currentPage, 'Node1Box').text
    assert "EDTNAB01NG00" in Node1


@when("I wait for Spinner to be Invisible")
def step_impl(context):
    WebDriverWait(context.driver, 40).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))


@given('I enter the BNG "{value}" name to be added')
def step_impl(context, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'NewNodeInp').send_keys(value)
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddNodeBtn').click()


@step('I search for the BNG for which the node needs to be added')
def search_node(context):
    currentPage = GlobalVar.currentPage
    WebDriverWait(context.driver, 40).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys("EDTNAB01NG01")


@step('I search for the BNG for which the node needs to be deleted')
def search_nodeForDelete(context):
    currentPage = GlobalVar.currentPage
    WebDriverWait(context.driver, 40).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys("EDTNAB01NG01")


@step('I count the number of BNG against Default Service Name')
def count_from_list(context):
    currentPage = GlobalVar.currentPage
    global testParams
    WebDriverWait(context.driver, 40).until(EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBox').send_keys("Default")
    serviceName = context.baseReader.getElementByPropertyName(context, currentPage, 'ServiceFirstValue').text
    assert serviceName == 'Default'
    bngCount = context.baseReader.getElementByPropertyName(context, currentPage, 'BNGCountFirstValue').text
    GlobalVar.testParams['bngCount'] = bngCount


@step('I search for "{value}" BNG Group ID and captured the total OLT count mapped to it')
def step_impl(context, value):
    currentPage = GlobalVar.currentPage
    global testParams
    WebDriverWait(context.driver, 40).until(EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(value)
    serviceName = context.baseReader.getElementByPropertyName(context, currentPage, 'SearchedBNGGroupId').text
    assert serviceName == value
    oltCount = context.baseReader.getElementByPropertyName(context, currentPage, 'OLTCount').text
    GlobalVar.testParams['oltCount'] = oltCount


@step('I verify the value of number of BNG services')
def verify_services(context):
    currentPage = GlobalVar.currentPage
    global testParams
    WebDriverWait(context.driver, 40).until(EC.invisibility_of_element((By.XPATH, "MainLoader")))
    tableRowSize = context.baseReader.getElementLocatorValue(context, currentPage, 'BNGRecords')
    records = context.driver.find_elements(By.XPATH, tableRowSize)
    assert GlobalVar.testParams['bngCount'] == str(len(records))


@step("I verify the value of number of OLT mapped to BNG group Id")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    global testParams
    WebDriverWait(context.driver, 40).until(EC.invisibility_of_element((By.XPATH, "MainLoader")))
    tableRowSize = context.baseReader.getElementLocatorValue(context, currentPage, 'OLTsRecords')
    records = context.driver.find_elements(By.XPATH, tableRowSize)
    assert GlobalVar.testParams['oltCount'] == str(len(records))


@step('I click "{value}" button')
def click_button(context, value):
    currentPage = GlobalVar.currentPage
    WebDriverWait(context.driver, 600).until(EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()
    time.sleep(5)


@step('I add a new "{value}" for the "{expectedValue}"')
def add_lag(context, value, expectedValue):
    currentPage = GlobalVar.currentPage
    print("Adding LAGs for:")
    print(expectedValue)
    global nodeNameList
    global lagNameList
    if expectedValue == "OLTNode":
        lagDetails = {key: value for key, value in GlobalVar.testParams.items() if key.startswith("OLTLag")}
        print("LAGs for OLT Topology:")
        print(lagDetails)
        i = 1
        for (key, value), (key1, value1) in zip(nodeDetails.items(), lagDetails.items()):
            nodeNameList.append(value)
            print(nodeDetails)
            lagNameList.append(value1)
            print(lagDetails)
            print("value-", value, "value1-", value1)
            OLTnodeName = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                      'Node' + str(i) + 'Box').text
            nodeName = OLTnodeName.split()
            assert value == nodeName[0]
            time.sleep(2)
            context.baseReader.getElementByPropertyName(context, currentPage, 'Node' + str(i) + 'Box').click()
            p = context.baseReader.getElementByPropertyName(context, currentPage, 'Node' + str(i) + 'Box').is_selected()
            print("this is the value of select", p)
            time.sleep(2)
            context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewLag').click()
            time.sleep(2)
            context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').click()
            time.sleep(1)
            context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').send_keys(value1)
            context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
            time.sleep(3)
            LagNameDetails = context.baseReader.getElementByPropertyName(context, currentPage, 'Lag1Box').text
            lagName = LagNameDetails.split()
            assert value1 == lagName[0]
            i += 1

    elif expectedValue == "BNGNode":
        # For this to work, the LAG column name should contain the last 4 characters of the corresponding node name in the test data
        lagDetails = {key: value for key, value in GlobalVar.testParams.items() if key.startswith("BNGLag")}
        print("LAGs for BNG Topology:")
        print(lagDetails)
        i = 1

        for (key, value) in nodeDetails.items():
            print("Inside first loop, node column name is: " + key)
            nodeNameList.append(value)
            BNGnodeName = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                      'Node' + str(i) + 'Box').text
            nodeName = BNGnodeName.split()
            assert value == nodeName[0]
            time.sleep(4)
            context.baseReader.getElementByPropertyName(context, currentPage, 'Node' + str(i) + 'Box').click()
            time.sleep(4)

            j = 1

            for (key1, value1) in lagDetails.items():
                if (key[-4:] in key1):
                    print("Inside LAG loop success, node column name is:" + key + " LAG column name is:" + key1)
                    lagNameList.append(value1)

                    context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewLag').click()
                    time.sleep(4)
                    context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').click()
                    time.sleep(4)
                    context.baseReader.getElementByPropertyName(context, currentPage,
                                                                'NewLagPlaceHolder').send_keys(value1)
                    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
                    time.sleep(12)
                    LagNameDetails = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                 'Lag' + str(j) + 'Box').text
                    lagName = LagNameDetails.split()
                    print("Checking if value 1: " + value1 + " = LAGname: " + lagName[0])
                    assert value1 == lagName[0]
                    time.sleep(4)
                    j += 1

            i += 1

    elif expectedValue == "LagTestBNG":
        # For this to work, the LAG column name should contain the last 4 characters of the corresponding node name in the test data
        lagDetails = {key: value for key, value in GlobalVar.testParams.items() if key.startswith("TestLag")}
        print("LAGs for BNG Topology:")
        print(lagDetails)
        i = 1

        for (key, value) in nodeDetails.items():
            print("Inside first loop, node column name is: " + key)
            nodeNameList.append(value)
            BNGnodeName = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                      'Node' + str(i) + 'Box').text
            nodeName = BNGnodeName.split()
            assert value == nodeName[0]
            time.sleep(4)
            context.baseReader.getElementByPropertyName(context, currentPage, 'Node' + str(i) + 'Box').click()
            time.sleep(4)

            j = 1

            for (key1, value1) in lagDetails.items():
                if (key[-4:] in key1):
                    print("Inside LAG loop success, node column name is:" + key + " LAG column name is:" + key1)
                    lagNameList.append(value1)

                    context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewLag').click()
                    time.sleep(4)
                    context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').click()
                    time.sleep(4)
                    context.baseReader.getElementByPropertyName(context, currentPage,
                                                                'NewLagPlaceHolder').send_keys(value1)
                    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
                    time.sleep(2)
                    # time.sleep(12)
                #         LagNameDetails = context.baseReader.getElementByPropertyName(context, currentPage,
                #                                                                      'Lag' + str(j) + 'Box').text
                #         lagName = LagNameDetails.split()
                #         print("Checking if value 1: " + value1 + " = LAGname: " + lagName[0])
                #         assert value1 == lagName[0]
                #         time.sleep(4)
                #         j += 1
                #
                # i += 1

    elif expectedValue == "BNG7PlusLag":
        # For this to work, the LAG column name should contain the last 4 characters of the corresponding node name in the test data
        lagDetails = {key: value for key, value in GlobalVar.testParams.items() if key.startswith("LagBNG7")}
        print("LAGs for BNG Topology:")
        print(lagDetails)
        i = 1

        for (key, value) in nodeDetails.items():
            print("Inside first loop, node column name is: " + key)
            nodeNameList.append(value)
            BNGnodeName = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                      'Node' + str(i) + 'Box').text
            nodeName = BNGnodeName.split()
            assert value == nodeName[0]
            time.sleep(4)
            context.baseReader.getElementByPropertyName(context, currentPage, 'Node' + str(i) + 'Box').click()
            time.sleep(4)

            j = 1

            for (key1, value1) in lagDetails.items():
                if (key[-4:] in key1):
                    print("Inside LAG loop success, node column name is:" + key + " LAG column name is:" + key1)
                    lagNameList.append(value1)

                    context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewLag').click()
                    time.sleep(4)
                    context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').click()
                    time.sleep(4)
                    context.baseReader.getElementByPropertyName(context, currentPage,
                                                                'NewLagPlaceHolder').send_keys(value1)
                    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
                    time.sleep(2)
                    time.sleep(12)
                    LagNameDetails = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                 'Lag' + str(j) + 'Box').text
                    lagName = LagNameDetails.split()
                    allowedLagName = (value1)[0:7]
                    print("Checking if allowedLagName: " + allowedLagName + " = LAGname: " + lagName[0])
                    assert allowedLagName == lagName[0]
                    time.sleep(4)
                    j += 1

            i += 1


    elif expectedValue == "OLT7PlusLag":
        # For this to work, the LAG column name should contain the last 4 characters of the corresponding node name in the test data
        lagDetails = {key: value for key, value in GlobalVar.testParams.items() if key.startswith("LagOLT7")}
        print("LAGs for BNG Topology:")
        print(lagDetails)
        i = 1

        for (key, value) in nodeDetails.items():
            print("Inside first loop, node column name is: " + key)
            nodeNameList.append(value)
            BNGnodeName = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                      'Node' + str(i) + 'Box').text
            nodeName = BNGnodeName.split()
            assert value == nodeName[0]
            time.sleep(4)
            context.baseReader.getElementByPropertyName(context, currentPage, 'Node' + str(i) + 'Box').click()
            time.sleep(4)

            j = 1

            for (key1, value1) in lagDetails.items():
                if (key[-4:] in key1):
                    print("Inside LAG loop success, node column name is:" + key + " LAG column name is:" + key1)
                    lagNameList.append(value1)

                    context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewLag').click()
                    time.sleep(4)
                    context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').click()
                    time.sleep(4)
                    context.baseReader.getElementByPropertyName(context, currentPage,
                                                                'NewLagPlaceHolder').send_keys(value1)
                    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
                    time.sleep(2)
                    time.sleep(12)
                    LagNameDetails = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                 'Lag' + str(j) + 'Box').text
                    lagName = LagNameDetails.split()
                    allowedLagName = (value1)[0:7]
                    print("Checking if allowedLagName: " + allowedLagName + " = LAGname: " + lagName[0])
                    assert allowedLagName == lagName[0]
                    time.sleep(4)
                    j += 1

            i += 1


    elif expectedValue == "LagTestOLT":
        # For this to work, the LAG column name should contain the last 4 characters of the corresponding node name in the test data
        lagDetails = {key: value for key, value in GlobalVar.testParams.items() if key.startswith("TestLag")}
        print("LAGs for BNG Topology:")
        print(lagDetails)
        i = 1

        for (key, value) in nodeDetails.items():
            print("Inside first loop, node column name is: " + key)
            nodeNameList.append(value)
            BNGnodeName = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                      'Node' + str(i) + 'Box').text
            nodeName = BNGnodeName.split()
            assert value == nodeName[0]
            time.sleep(4)
            context.baseReader.getElementByPropertyName(context, currentPage, 'Node' + str(i) + 'Box').click()
            time.sleep(4)

            j = 1

            for (key1, value1) in lagDetails.items():
                if (key[-4:] in key1):
                    print("Inside LAG loop success, node column name is:" + key + " LAG column name is:" + key1)
                    lagNameList.append(value1)

                    context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewLag').click()
                    time.sleep(4)
                    context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').click()
                    time.sleep(4)
                    context.baseReader.getElementByPropertyName(context, currentPage,
                                                                'NewLagPlaceHolder').send_keys(value1)
                    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
                    time.sleep(2)
                    # time.sleep(12)
                #         LagNameDetails = context.baseReader.getElementByPropertyName(context, currentPage,
                #                                                                      'Lag' + str(j) + 'Box').text
                #         lagName = LagNameDetails.split()
                #         print("Checking if value 1: " + value1 + " = LAGname: " + lagName[0])
                #         assert value1 == lagName[0]
                #         time.sleep(4)
                #         j += 1
                #
                # i += 1


    elif expectedValue == "TestNodes":
        # For this to work, the LAG column name should contain the last 4 characters of the corresponding node name in the test data
        lagDetails = {key: value for key, value in GlobalVar.testParams.items() if key.startswith("LagTest")}
        print("LAGs for BNG Topology:")
        print(lagDetails)
        i = 1

        for (key, value) in nodeDetails.items():
            print("Inside first loop, node column name is: " + key)
            nodeNameList.append(value)
            BNGnodeName = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                      'Node' + str(i) + 'Box').text
            nodeName = BNGnodeName.split()
            assert value == nodeName[0]
            time.sleep(4)
            context.baseReader.getElementByPropertyName(context, currentPage, 'Node' + str(i) + 'Box').click()
            time.sleep(4)

            j = 1

            for (key1, value1) in lagDetails.items():
                if (key[-4:] in key1):
                    print("Inside LAG loop success, node column name is:" + key + " LAG column name is:" + key1)
                    lagNameList.append(value1)

                    context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewLag').click()
                    time.sleep(4)
                    context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').click()
                    time.sleep(4)
                    context.baseReader.getElementByPropertyName(context, currentPage,
                                                                'NewLagPlaceHolder').send_keys(value1)
                    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
                    time.sleep(12)
                    LagNameDetails = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                 'Lag' + str(j) + 'Box').text
                    lagName = LagNameDetails.split()
                    print("Checking if value 1: " + value1 + " = LAGname: " + lagName[0])
                    assert value1 == lagName[0]
                    time.sleep(4)
                    j += 1

            i += 1

        ## BELOW CODE TO BE REVIEWED

        # lagDetails = {key: value for key, value in GlobalVar.testParams.items() if key.startswith("BNGLag")}
        # print("LAGs for BNG Topology:")
        # print(lagDetails)
        # i = 1
        # for (key, value), (key1, value1) in zip(nodeDetails.items(), lagDetails.items()):
        #     nodeNameList.append(value)
        #     lagNameList.append(value1)
        #     BNGnodeName = context.baseReader.getElementByPropertyName(context, currentPage,
        #                                                               'Node' + str(i) + 'Box').text
        #     nodeName = BNGnodeName.split()
        #     assert value == nodeName[0]
        #     time.sleep(4)
        #     context.baseReader.getElementByPropertyName(context, currentPage, 'Node' + str(i) + 'Box').click()
        #     time.sleep(4)
        #     context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewLag').click()
        #     time.sleep(4)
        #     context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').click()
        #     time.sleep(4)
        #     context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').send_keys(value1)
        #     context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
        #     time.sleep(12)
        #     LagNameDetails = context.baseReader.getElementByPropertyName(context, currentPage, 'Lag1Box').text
        #     lagName = LagNameDetails.split()
        #     assert value1 == lagName[0]
        #     time.sleep(4)
        #     context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewLag').click()
        #     time.sleep(4)
        #     context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').click()
        #     time.sleep(4)
        #     context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').send_keys(value1)
        #     context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
        #     time.sleep(12)
        #     LagNameDetails = context.baseReader.getElementByPropertyName(context, currentPage, 'Lag2Box').text
        #     lagName = LagNameDetails.split()
        #     assert value1 == lagName[0]
        #     time.sleep(4)
        #
        #     i += 1


@step("I add link between the 2 BNGs")
def add_link_test(context):
    currentPage = GlobalVar.currentPage
    print("Node list is:")
    print(nodeNameList)
    print("Lag list is:")
    print(lagNameList)
    Node1ToAdd = nodeNameList[0]
    print("Going to add Node 1 for Link 1: " + Node1ToAdd)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Node1DropDown').click()
    time.sleep(2)
    Node1Displayed = context.baseReader.getElementByPropertyName(context, currentPage, 'TestLinkNode1')
    print("Selecting node from dropdown: " + Node1Displayed.text)
    Node1InDD = Node1Displayed.text
    assert Node1ToAdd == Node1InDD
    context.baseReader.getElementByPropertyName(context, currentPage, 'TestLinkNode1').click()
    time.sleep(2)

    # Adding link 1 - BNG1 to BNG2 : Adding lag 1
    Lag1ToAdd = lagNameList[0]
    print("Going to add Lag 1 for Link 1: " + Lag1ToAdd)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Lag1DropDown').click()
    time.sleep(2)
    Lag1Displayed = context.baseReader.getElementByPropertyName(context, currentPage, 'TestLinkLag1')
    print("Selecting lag from dropdown: " + Lag1Displayed.text)
    Lag1InDD = Lag1Displayed.text
    assert Lag1ToAdd == Lag1InDD
    context.baseReader.getElementByPropertyName(context, currentPage, 'TestLinkLag1').click()
    time.sleep(2)

    # Adding link 1 - BNG1 to BNG2 : Adding node 2
    Node2ToAdd = nodeNameList[1]
    print("Going to add Node 2 for Link 1: " + Node2ToAdd)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Node2DropDown').click()
    time.sleep(2)
    Node2Displayed = context.baseReader.getElementByPropertyName(context, currentPage, 'TestLinkNode2')
    print("Selecting node from dropdown: " + Node2Displayed.text)
    Node2InDD = Node2Displayed.text
    assert Node2ToAdd == Node2InDD
    context.baseReader.getElementByPropertyName(context, currentPage, 'TestLinkNode2').click()
    time.sleep(2)

    # Adding link 1 - BNG1 to BNG2 : Adding lag 2
    Lag2ToAdd = lagNameList[1]
    print("Going to add Lag 2 for Link 1: " + Lag2ToAdd)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Lag2DropDown').click()
    time.sleep(2)
    Lag2Displayed = context.baseReader.getElementByPropertyName(context, currentPage, 'TestLinkLag2')
    print("Selecting lag from dropdown: " + Lag2Displayed.text)
    Lag2InDD = Lag2Displayed.text
    assert Lag2ToAdd == Lag2InDD
    context.baseReader.getElementByPropertyName(context, currentPage, 'TestLinkLag2').click()
    time.sleep(2)

    # Adding link 1
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
    time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'BypassClick').click()
    time.sleep(2)

    # Verifying the added link
    print("Before assertion of created link")
    Row1Node1 = context.baseReader.getElementByPropertyName(context, currentPage, 'AddedRow1Node1')
    Row1Lag1 = context.baseReader.getElementByPropertyName(context, currentPage, 'AddedRow1Lag1')
    Row1Node2 = context.baseReader.getElementByPropertyName(context, currentPage, 'AddedRow1Node2')
    Row1Lag2 = context.baseReader.getElementByPropertyName(context, currentPage, 'AddedRow1Lag2')

    Node1Added = Row1Node1.text
    Lag1Added = Row1Lag1.text
    Node2Added = Row1Node2.text
    Lag2Added = Row1Lag2.text

    assert Node1InDD == Node1Added
    assert Lag1InDD == Lag1Added
    assert Node2InDD == Node2Added
    assert Lag2InDD == Lag2Added
    print("After assertion of created link")


@step("I add links between BNG1, BNG2, SE-Y-1 and SE-Y-2")
def add_link(context):
    currentPage = GlobalVar.currentPage
    print("Node list is:", nodeNameList)
    print("Lag list is:", lagNameList)
    for j in range(0, 5):
        ROW_1_ListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Node1Value')
        Row_1_Value = context.driver.find_elements(By.XPATH, ROW_1_ListXpath)
        for i in range(0, len(Row_1_Value)):
            time.sleep(3)
            actions = ActionChains(context.driver)
            actions.move_to_element(Row_1_Value[i]).click().perform()
            time.sleep(3)
            DataListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DataList')
            DataDropDownList = context.driver.find_elements(By.XPATH, DataListXpath)
            for k in range(0, len(DataDropDownList)):
                # Link-1
                if j == 0 and i == 0:
                    NodeName = DataDropDownList[k].text
                    if NodeName == nodeNameList[1]:
                        assert DataDropDownList[k].text == nodeNameList[1]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == nodeNameList[1]
                        break
                elif j == 0 and i == 1:
                    LagName = DataDropDownList[k].text
                    if LagName == lagNameList[1]:
                        assert DataDropDownList[k].text == lagNameList[1]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == lagNameList[1]
                        break
                elif j == 0 and i == 2:
                    NodeName = DataDropDownList[k].text
                    if NodeName == nodeNameList[0]:
                        assert DataDropDownList[k].text == nodeNameList[0]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == nodeNameList[0]
                        break
                elif j == 0 and i == 3:
                    LagName = DataDropDownList[k].text
                    if LagName == lagNameList[1]:
                        assert DataDropDownList[k].text == lagNameList[1]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == lagNameList[1]
                        break

                # Link2
                elif j == 1 and i == 0:
                    NodeName = DataDropDownList[k].text
                    if NodeName == nodeNameList[1]:
                        assert DataDropDownList[k].text == nodeNameList[1]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == nodeNameList[1]
                        break
                elif j == 1 and i == 1:
                    LagName = DataDropDownList[k].text
                    if LagName == lagNameList[0]:
                        assert DataDropDownList[k].text == lagNameList[0]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == lagNameList[0]
                        break
                elif j == 1 and i == 2:
                    NodeName = DataDropDownList[k].text
                    if NodeName == nodeNameList[2]:
                        assert DataDropDownList[k].text == nodeNameList[2]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == nodeNameList[2]
                        break
                elif j == 1 and i == 3:
                    LagName = DataDropDownList[k].text
                    if LagName == lagNameList[5]:
                        assert DataDropDownList[k].text == lagNameList[5]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == lagNameList[5]
                        break

                # Link3
                elif j == 2 and i == 0:
                    NodeName = DataDropDownList[k].text
                    if NodeName == nodeNameList[1]:
                        assert DataDropDownList[k].text == nodeNameList[1]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == nodeNameList[1]
                        break
                elif j == 2 and i == 1:
                    LagName = DataDropDownList[k].text
                    if LagName == lagNameList[0]:
                        assert DataDropDownList[k].text == lagNameList[0]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == lagNameList[0]
                        break
                elif j == 2 and i == 2:
                    NodeName = DataDropDownList[k].text
                    if NodeName == nodeNameList[3]:
                        assert DataDropDownList[k].text == nodeNameList[3]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == nodeNameList[3]
                        break
                elif j == 2 and i == 3:
                    LagName = DataDropDownList[k].text
                    if LagName == lagNameList[5]:
                        assert DataDropDownList[k].text == lagNameList[5]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == lagNameList[5]
                        break
                # Link4
                elif j == 3 and i == 0:
                    NodeName = DataDropDownList[k].text
                    if NodeName == nodeNameList[0]:
                        assert DataDropDownList[k].text == nodeNameList[0]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == nodeNameList[0]
                        break
                elif j == 3 and i == 1:
                    LagName = DataDropDownList[k].text
                    if LagName == lagNameList[0]:
                        assert DataDropDownList[k].text == lagNameList[0]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == lagNameList[0]
                        break
                elif j == 3 and i == 2:
                    NodeName = DataDropDownList[k].text
                    if NodeName == nodeNameList[2]:
                        assert DataDropDownList[k].text == nodeNameList[2]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == nodeNameList[2]
                        break
                elif j == 3 and i == 3:
                    LagName = DataDropDownList[k].text
                    if LagName == lagNameList[4]:
                        assert DataDropDownList[k].text == lagNameList[4]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == lagNameList[4]
                        break
                # Link5
                elif j == 4 and i == 0:
                    NodeName = DataDropDownList[k].text
                    if NodeName == nodeNameList[0]:
                        assert DataDropDownList[k].text == nodeNameList[0]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == nodeNameList[0]
                        break
                elif j == 4 and i == 1:
                    LagName = DataDropDownList[k].text
                    if LagName == lagNameList[0]:
                        assert DataDropDownList[k].text == lagNameList[0]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == lagNameList[0]
                        break
                elif j == 4 and i == 2:
                    NodeName = DataDropDownList[k].text
                    if NodeName == nodeNameList[3]:
                        assert DataDropDownList[k].text == nodeNameList[3]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == nodeNameList[3]
                        break
                elif j == 4 and i == 3:
                    LagName = DataDropDownList[k].text
                    if LagName == lagNameList[4]:
                        assert DataDropDownList[k].text == lagNameList[4]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == lagNameList[4]
                        break
        context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
        time.sleep(5)
    nodeNameList.clear()
    lagNameList.clear()


@step("I add link OLT to the both SE-X-1 and SE-X-2")
def add_link(context):
    currentPage = GlobalVar.currentPage
    print(nodeNameList)
    print(lagNameList)
    for j in range(0, 2):
        ROW_1_ListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Node1Value')
        Row_1_Value = context.driver.find_elements(By.XPATH, ROW_1_ListXpath)
        for i in range(0, len(Row_1_Value)):
            time.sleep(3)
            actions = ActionChains(context.driver)
            actions.move_to_element(Row_1_Value[i]).click().perform()
            time.sleep(3)
            DataListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DataList')
            DataDropDownList = context.driver.find_elements(By.XPATH, DataListXpath)
            for k in range(0, len(DataDropDownList)):
                if i == 0:
                    NodeName = DataDropDownList[k].text
                    if NodeName == nodeNameList[0]:
                        assert DataDropDownList[k].text == nodeNameList[0]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == nodeNameList[0]
                        break
                elif i == 1:
                    LagName = DataDropDownList[k].text
                    if LagName == lagNameList[0]:
                        assert DataDropDownList[k].text == lagNameList[0]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == lagNameList[0]
                        break
                elif j == 0 and i == 2:
                    NodeName = DataDropDownList[k].text
                    if NodeName == nodeNameList[1]:
                        assert DataDropDownList[k].text == nodeNameList[1]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == nodeNameList[1]
                        break
                elif j == 1 and i == 2:
                    NodeName = DataDropDownList[k].text
                    if NodeName == nodeNameList[2]:
                        assert DataDropDownList[k].text == nodeNameList[2]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == nodeNameList[2]
                        break
                elif j == 0 and i == 3:
                    LagName = DataDropDownList[k].text
                    if LagName == lagNameList[1]:
                        assert DataDropDownList[k].text == lagNameList[1]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == lagNameList[1]
                        break
                elif j == 1 and i == 3:
                    LagName = DataDropDownList[k].text
                    if LagName == lagNameList[2]:
                        assert DataDropDownList[k].text == lagNameList[2]
                        DataDropDownList[k].click()
                        time.sleep(5)
                        valueName = (Row_1_Value[i]).get_attribute('value')
                        assert valueName == lagNameList[2]
                        break
                time.sleep(2)

        context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
        time.sleep(5)


@step('I click on Node and delete corresponding lag')
def delete_lag(context):
    currentPage = GlobalVar.currentPage
    Node_ListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'NodeList')
    time.sleep(5)
    Node_Value = context.driver.find_elements(By.XPATH, Node_ListXpath)
    for i in range(0, len(Node_Value)):
        time.sleep(3)
        actions = ActionChains(context.driver)
        actions.move_to_element(Node_Value[i]).click().perform()
        time.sleep(3)
        Lag_ListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LagList')
        Lag_Value = context.driver.find_elements(By.XPATH, Lag_ListXpath)
        for j in range(0, len(Lag_Value)):
            time.sleep(3)
            actions = ActionChains(context.driver)
            actions.move_to_element(Lag_Value[j]).click().perform()
            context.baseReader.getElementByPropertyName(context, currentPage, 'DeleteLagButton').click()
            time.sleep(3)


@step('I delete added node and SE')
def delete_Node(context):
    currentPage = GlobalVar.currentPage
    Node_ListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'NodeList')
    Node_Value = context.driver.find_elements(By.XPATH, Node_ListXpath)
    for i in range(0, len(Node_Value)):
        time.sleep(3)
        actions = ActionChains(context.driver)
        actions.move_to_element(Node_Value[i]).click().perform()
        context.baseReader.getElementByPropertyName(context, currentPage, 'DeleteNodeButton').click()
        time.sleep(30)


@when('I delete "{value}" node')
def delete_Nodes(context, value):
    currentPage = GlobalVar.currentPage
    time.sleep(1)
    Node_ListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'NodeList')
    Node_Value = context.driver.find_elements(By.XPATH, Node_ListXpath)
    for i in range(0, len(Node_Value)):
        if (value in Node_Value[i].text):
            time.sleep(2)
            actions = ActionChains(context.driver)
            actions.move_to_element(Node_Value[i]).click().perform()
            Node_Value[i].find_element(By.XPATH, ".//span").click()
            time.sleep(1)


@step('I delete the added link Between "{value}" and SE')
def delete_link(context, value):
    currentPage = GlobalVar.currentPage
    Link_RowsXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LinkRows')
    Link_Value = context.driver.find_elements(By.XPATH, Link_RowsXpath)
    for i in range(0, len(Link_Value) - 1):
        time.sleep(5)
        # WebDriverWait(context.driver, 20).until(
        #     EC.visibility_of_element_located((By.XPATH, 'DeleteLinkButton')))
        context.baseReader.getElementByPropertyName(context, currentPage, 'DeleteLinkButton').click()
        time.sleep(5)
        # WebDriverWait(context.driver, 30).until(
        #     EC.visibility_of_element_located((By.XPATH, 'linkDeleteSuccessMessage')))
        linkDeleteSuccessMessage = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                               'linkDeleteSuccessMessage').text
        print(GlobalVar.testParams.get('OLTlinkDeleteSuccessMessage'))
        assert linkDeleteSuccessMessage == GlobalVar.testParams.get('OLTlinkDeleteSuccessMessage')
    # context.baseReader.getElementByPropertyName(context, currentPage, 'ArrowBackButton').click()
    time.sleep(15)
    context.baseReader.getElementByPropertyName(context, currentPage, 'OLT').click()
    time.sleep(20)


@step('I verify that the node has been deleted')
def verify_node_deleted(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'OLT').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys('DRRRDC30OT30')
    time.sleep(15)
    ValidationMessage = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                    'NoDataMessage').get_attribute('value')
    assert ValidationMessage == 'No Data'


@step('I verify that the "{expectedValue}" has been deleted')
def verify_node_deleted(context, expectedValue):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
    if expectedValue == "BNG topology":
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(
            GlobalVar.testParams.get('BNGNode_BNG1'))
        time.sleep(10)
    elif expectedValue == "OLT topology":
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(
            GlobalVar.testParams.get('OLTNode_Name'))
        time.sleep(10)
    ValidationMessage = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                    'NoDataMessage').get_attribute('value')
    assert ValidationMessage == 'No Data'


@step('I search for added OLT and click on "{expectedValue}"')
def search_node(context, expectedValue):
    currentPage = GlobalVar.currentPage
    WebDriverWait(context.driver, 40).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys('DRRRDC30OT30')
    time.sleep(5)
    OLTName = context.baseReader.getElementByPropertyName(context, currentPage, 'OLT1Value').text
    print(OLTName)
    assert OLTName == 'DRRRDC30OT30'
    context.baseReader.getElementByPropertyName(context, currentPage, 'OLT1Value').click()
    time.sleep(10)


@step('I search for added topology and click on "{value}" name')
def search_topology(context, value):
    currentPage = GlobalVar.currentPage
    WebDriverWait(context.driver, 40).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
    if value == 'BNG':
        time.sleep(5)
        print(GlobalVar.testParams.get('BNGNode_BNG1'))
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
        time.sleep(2)
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(
            GlobalVar.testParams.get('BNGNode_BNG1'))
        time.sleep(10)
        BNGName = context.baseReader.getElementByPropertyName(context, currentPage, 'OLT1Value').text
        print(BNGName)

    elif value == 'OLT':
        time.sleep(5)
        print(GlobalVar.testParams.get('OLTNode_Name'))
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
        time.sleep(2)
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(
            GlobalVar.testParams.get('OLTNode_Name'))
        time.sleep(5)
        OLTName = context.baseReader.getElementByPropertyName(context, currentPage, 'OLT1Value').text
        print(OLTName)
        assert OLTName == GlobalVar.testParams.get('OLTNode_Name')
    context.baseReader.getElementByPropertyName(context, currentPage, 'OLT1Value').click()
    time.sleep(10)


@step('I select the "{value}" node')
def select_value(context, value):
    currentPage = GlobalVar.currentPage
    time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'l2topologynode1').click()
    time.sleep(3)


@step('I enter the Onboarding "{value}" Configuration Parameters')
def onboarding_details(context, value):
    currentPage = GlobalVar.currentPage
    time.sleep(35)
    if value == 'BNG':
        context.baseReader.getElementByPropertyName(context, currentPage, 'AvailabilityZone').click()
        AvailabiilityZoneXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'ElementList')
        elementDropDownList = context.driver.find_elements(By.XPATH, AvailabiilityZoneXpath)
        for i in range(0, len(elementDropDownList)):
            availableElementName = elementDropDownList[i].text
            time.sleep(3)
            if availableElementName == GlobalVar.testParams.get('BNG Availability Zone'):
                time.sleep(3)
                elementDropDownList[i].click()
                time.sleep(3)
                break
        context.baseReader.getElementByPropertyName(context, currentPage, 'BNGGroupID').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'BNGGroupID').send_keys(
            GlobalVar.testParams.get('BNG Group ID'))
        WebDriverWait(context.driver, 60).until(
            EC.invisibility_of_element((By.XPATH, "MainLoader")))
        context.baseReader.getElementByPropertyName(context, currentPage, 'ValidateButton').click()
        time.sleep(65)
        nextButtonXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Next')
        WebDriverWait(context.driver, 40).until(
            EC.visibility_of_element_located((By.XPATH, nextButtonXpath)), message='Element not visible')



    elif value == 'OLT':
        OLTConfigurationDetails = {key: value for key, value in GlobalVar.testParams.items() if
                                   key.startswith("OLTConfiguration")}
        for key, value in OLTConfigurationDetails.items():
            OLTConfigurationValues.append(value)
            print('values are', OLTConfigurationValues)
        OLTConfigurationParameterListXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                       'AvailabilityZone')
        OLTConfigurationParameterList = context.driver.find_elements(By.XPATH, OLTConfigurationParameterListXpath)
        j = 0
        for i in range(0, len(OLTConfigurationParameterList)):
            print('value of j', j)
            time.sleep(8)
            print('value of i', i)
            OLTConfigurationParameterList[i].click()
            print("after click")
            time.sleep(15)
            if i == 1:
                time.sleep(5)
                print('inside if condition')
                print(GlobalVar.testParams.get('OLT Group ID'))
                context.baseReader.getElementByPropertyName(context, currentPage, 'NoOption').click()
                time.sleep(3)
                context.baseReader.getElementByPropertyName(context, currentPage, 'NoOption').send_keys(
                    GlobalVar.testParams.get('OLT Group ID'))
                time.sleep(10)
                context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
            else:
                print("inside else block")
                elementListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'ElementList')
                elementDropDownList = context.driver.find_elements(By.XPATH, elementListXpath)
                for k in range(0, len(elementDropDownList)):
                    OLTConfigurationParametersOptions = elementDropDownList[k].text
                    if OLTConfigurationParametersOptions == OLTConfigurationValues[j]:
                        assert elementDropDownList[k].text == OLTConfigurationValues[j]
                        elementDropDownList[k].click()
                        time.sleep(10)
                        j += 1
                        break

        time.sleep(5)
        context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceNumber').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceNumber').send_keys(
            GlobalVar.testParams.get('Device Number'))
        time.sleep(5)
        context.baseReader.getElementByPropertyName(context, currentPage, 'Next').click()
        print('Click on Next Button')
        time.sleep(10)


@step('I enter the Onboarding BNG Configuration details')
def BNGonboarding_configuration_details(context):
    currentPage = GlobalVar.currentPage
    time.sleep(100)
    # For IPV4 Address Pool Servers:
    BNGIPV4ConfigurationDetails = {key: value for key, value in GlobalVar.testParams.items() if
                                   key.startswith("IPV4")}
    for key, value in BNGIPV4ConfigurationDetails.items():
        BNGIPV4ConfigurationValues.append(value)
    IPV4CongifurationElementXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                              'IPV4AddressPoolServers')
    IPV4CongifurationElementListXpath = context.driver.find_elements(By.XPATH, IPV4CongifurationElementXpath)
    for i in range(0, len(IPV4CongifurationElementListXpath)):
        time.sleep(3)
        IPV4CongifurationElementListXpath[i].click()
        IPV4CongifurationElementListXpath[i].send_keys(BNGIPV4ConfigurationValues[i])
        time.sleep(3)
        if i == 7:
            val = context.baseReader.getElementByPropertyName(context, currentPage, 'Hostname')
            context.driver.execute_script("arguments[0].scrollIntoView();", val)
    time.sleep(5)

    # For IPV6 Address Pool Servers:
    BNGIPV6ConfigurationDetails = {key: value for key, value in GlobalVar.testParams.items() if
                                   key.startswith("IPV6")}
    for key, value in BNGIPV6ConfigurationDetails.items():
        BNGIPV6ConfigurationValues.append(value)
    IPV6CongifurationElementXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                              'IPV6AddressPoolServers')
    IPV6CongifurationElementListXpath = context.driver.find_elements(By.XPATH, IPV6CongifurationElementXpath)
    for j in range(0, len(IPV6CongifurationElementListXpath)):
        time.sleep(3)
        IPV6CongifurationElementListXpath[j].click()
        IPV6CongifurationElementListXpath[j].send_keys(BNGIPV6ConfigurationValues[j])
        time.sleep(5)

    # For Authentication Key:
    context.baseReader.getElementByPropertyName(context, currentPage, 'MultiChassisSync').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'MultiChassisSync').send_keys(
        GlobalVar.testParams.get('Authentication Key'))
    time.sleep(5)

    # For Routing Policies:
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddPrefixButton').click()
    val = context.baseReader.getElementByPropertyName(context, currentPage, 'CommunityDefinitionsText')
    context.driver.execute_script("arguments[0].scrollIntoView();", val)
    context.baseReader.getElementByPropertyName(context, currentPage, 'PrefixEntry1').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'PrefixEntry1').send_keys(
        GlobalVar.testParams.get('Static hosts prefix1'))
    context.baseReader.getElementByPropertyName(context, currentPage, 'PrefixEntry2').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'PrefixEntry2').send_keys(
        GlobalVar.testParams.get('Static hosts prefix2'))
    time.sleep(5)

    # For Community Definitions:
    BNGCommunityDefinitionsDetails = {key: value for key, value in GlobalVar.testParams.items() if
                                      key.startswith("CommunityDefinitions")}
    for key, value in BNGCommunityDefinitionsDetails.items():
        BNGCommunityDefinitionsValues.append(value)
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'CommunityDefinitionAddMemberButton1').click()
    time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'CommunityDefinitionAddMemberButton2').click()
    time.sleep(2)
    val = context.baseReader.getElementByPropertyName(context, currentPage, 'COM2AddMember')
    context.driver.execute_script("arguments[0].scrollIntoView();", val)
    context.baseReader.getElementByPropertyName(context, currentPage, 'COM2AddMember').click()
    time.sleep(5)
    # Member
    val = context.baseReader.getElementByPropertyName(context, currentPage, 'CommunityDefinitionHeadings')
    context.driver.execute_script("arguments[0].scrollIntoView();", val)
    time.sleep(3)
    print("value", GlobalVar.testParams.get('CommunityDefinitions_NG04_Member1'))
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG04Member1').click()
    print("After click")
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG04Member1').send_keys(
        GlobalVar.testParams.get('CommunityDefinitions_NG04_Member1'))
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG04Member2').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG04Member2').send_keys(
        GlobalVar.testParams.get('CommunityDefinitions_NG04_Member2'))
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG03Member1').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG03Member1').send_keys(
        GlobalVar.testParams.get('CommunityDefinitions_NG03_Member1'))
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG03Member2').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG03Member2').send_keys(
        GlobalVar.testParams.get('CommunityDefinitions_NG03_Member2'))

    # COMs
    BNGCOM1Xpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                             'BNGCOMs')
    BNGCOM1ElementListXpath = context.driver.find_elements(By.XPATH, BNGCOM1Xpath)
    k = 4
    print("values are", BNGCommunityDefinitionsValues)
    for i in range(0, len(BNGCOM1ElementListXpath)):
        time.sleep(3)
        print(k)
        BNGCOM1ElementListXpath[i].click()
        print("after click")
        BNGCOM1ElementListXpath[i].send_keys(BNGCommunityDefinitionsValues[k])
        k += 1

    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG03Primary').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG03Primary').send_keys(
        GlobalVar.testParams.get('CommunityDefinitions_COM_NG03_Primary'))
    print(GlobalVar.testParams.get('CommunityDefinitions_COM_NG03_Primary'))
    time.sleep(5)
    # val = context.baseReader.getElementByPropertyName(context, currentPage, 'NG03Secondary')
    # context.driver.execute_script("arguments[0].scrollIntoView();", val)

    time.sleep(10)
    print(GlobalVar.testParams.get('CommunityDefinitions_COM_NG03_Secondary'))
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG04Primary').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG04Primary').send_keys(
        GlobalVar.testParams.get('CommunityDefinitions_COM_NG04_Primary'))
    print(GlobalVar.testParams.get('CommunityDefinitions_COM_NG04_Primary'))
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG03Secondary').click()
    time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG03Secondary').send_keys(
        GlobalVar.testParams.get('CommunityDefinitions_COM_NG03_Secondary'))
    # val = context.baseReader.getElementByPropertyName(context, currentPage, 'NG04Secondary')
    # context.driver.execute_script("arguments[0].scrollIntoView();", val)
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG04Secondary').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NG04Secondary').send_keys(
        GlobalVar.testParams.get('CommunityDefinitions_COM_NG04_Secondary'))
    print(GlobalVar.testParams.get('CommunityDefinitions_COM_NG04_Secondary'))
    time.sleep(5)
    val = context.baseReader.getElementByPropertyName(context, currentPage, 'LastaddMemberButton')
    context.driver.execute_script("arguments[0].scrollIntoView();", val)
    time.sleep(3)

    # For BNG Addresses:
    val = context.baseReader.getElementByPropertyName(context, currentPage, 'LoopBackAddressBNG1')
    context.driver.execute_script("arguments[0].scrollIntoView();", val)
    time.sleep(10)

    LoopBackAddressNG03Xpath = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                           'BNGLoopBackAddressNG03')
    actions = ActionChains(context.driver)
    actions.move_to_element(LoopBackAddressNG03Xpath).click().perform()
    actions.move_to_element(LoopBackAddressNG03Xpath).send_keys(
        GlobalVar.testParams.get('BNGAddresses_loopback_NG03')).perform()

    LoopBackAddressNG04Xapth = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                           'BNGLoopBackAddressNG04')
    actions = ActionChains(context.driver)
    actions.move_to_element(LoopBackAddressNG04Xapth).click().perform()
    actions.move_to_element(LoopBackAddressNG04Xapth).send_keys(
        GlobalVar.testParams.get('BNGAddresses_loopback_NG04')).perform()
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'UserProfileArrowDown').click()


@step('I enter the Onboarding OLT Configuration details')
def OLTonboarding_configuration_details(context):
    currentPage = GlobalVar.currentPage
    time.sleep(250)
    print("wait complete")
    # For Mac-Addresses:
    print('For Mac-Addresses:')
    OLTMacAddressesDetails = {key: value for key, value in GlobalVar.testParams.items() if
                              key.startswith("OLTMac-Addresses")}
    for key, value in OLTMacAddressesDetails.items():
        OLTMacAddressesValues.append(value)
    print('OLT mac value', OLTMacAddressesValues)
    MacAddressesElementXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                         'MacAddresses')
    MacAddressesElementListXpath = context.driver.find_elements(By.XPATH, MacAddressesElementXpath)
    for i in range(0, len(MacAddressesElementListXpath)):
        time.sleep(3)
        MacAddressesElementListXpath[i].click()
        MacAddressesElementListXpath[i].send_keys(OLTMacAddressesValues[i])
        time.sleep(3)

    # For Q/S-tag-range:
    print('For Q/S-tag-range:')
    # context.baseReader.getElementByPropertyName(context, currentPage, 'QSTagStartingValue').click()
    # context.baseReader.getElementByPropertyName(context, currentPage, 'QSTagStartingValue').send_keys(
    #     GlobalVar.testParams.get('QSTagRange_Starting Value'))
    # context.baseReader.getElementByPropertyName(context, currentPage, 'QSTagEndingValue').click()
    # context.baseReader.getElementByPropertyName(context, currentPage, 'QSTagEndingValue').send_keys(
    #     GlobalVar.testParams.get('QSTagRange_Ending Value'))
    # val = context.baseReader.getElementByPropertyName(context, currentPage, 'QSTagEndingValue')
    # context.driver.execute_script("arguments[0].scrollIntoView();", val)

    # For SE EVPNs:
    print(' # For SE EVPNs:')
    # SEEvpnDetails = {key: value for key, value in GlobalVar.testParams.items() if key.startswith("OLTSEEVPNs")}
    # for key, value in SEEvpnDetails.items():
    #     SEEvpnElementvalues.append(value)
    # SEEvpnElementXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SeEvpns')
    # SEEvpnElementListXpath = context.driver.find_elements(By.XPATH, SEEvpnElementXpath)
    # for j in range(0, len(SEEvpnElementListXpath)):
    #     time.sleep(5)
    #     SEEvpnElementListXpath[j].click()
    #     SEEvpnElementListXpath[j].send_keys(SEEvpnElementvalues[j])
    #     time.sleep(3)

    # For SRRP Heartbeat:
    print('# For SRRP Heartbeat:')
    # context.baseReader.getElementByPropertyName(context, currentPage, 'SRRPHeartbeat1').click()
    # context.baseReader.getElementByPropertyName(context, currentPage, 'SRRPHeartbeat1').send_keys(
    #     GlobalVar.testParams.get('SRRP Heartbeat_Dynamic Service VPLS ID'))
    # context.baseReader.getElementByPropertyName(context, currentPage, 'SRRPHeartbeat2').click()
    # context.baseReader.getElementByPropertyName(context, currentPage, 'SRRPHeartbeat2').send_keys(
    #     GlobalVar.testParams.get('SRRP Heartbeat_Static Service VPLS ID'))
    # time.sleep(10)
    # val = context.baseReader.getElementByPropertyName(context, currentPage, 'SRRPHeartbeat2')
    # context.driver.execute_script("arguments[0].scrollIntoView();", val)

    # For Multicast IES:
    print('# For Multicast IES:')
    context.baseReader.getElementByPropertyName(context, currentPage, 'MulticastIES1').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'MulticastIES1').send_keys(
        GlobalVar.testParams.get('Multicast IES_Primary Interface Address'))
    context.baseReader.getElementByPropertyName(context, currentPage, 'MulticastIES2').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'MulticastIES2').send_keys(
        GlobalVar.testParams.get('Multicast IES_Secondary Interface Address'))
    time.sleep(10)

    # For HSIA IES:
    print('For HSIA IES')
    HSIAIESDetails = {key: value for key, value in GlobalVar.testParams.items() if key.startswith('HSIAIES')}
    for key, value in HSIAIESDetails.items():
        HSIAIESElementValues.append(value)
        hSIAIESElementXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'HSIAIES')
        hSIAIESElementListXpath = context.driver.find_elements(By.XPATH, hSIAIESElementXpath)
    for e in range(0, len(hSIAIESElementListXpath)):
        time.sleep(5)
        hSIAIESElementListXpath[e].click()
        hSIAIESElementListXpath[e].send_keys(HSIAIESElementValues[e])
        time.sleep(3)

    # For VOICE IES:
    context.baseReader.getElementByPropertyName(context, currentPage, 'VoiceIES1').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'VoiceIES1').send_keys(
        GlobalVar.testParams.get('VOICE IES_Redundant Interface_Address'))
    context.baseReader.getElementByPropertyName(context, currentPage, 'VoiceIES2').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'VoiceIES2').send_keys(
        GlobalVar.testParams.get('VOICE IES_Redundant Interface_Spoke-sdp-Subset'))
    val = context.baseReader.getElementByPropertyName(context, currentPage, 'DryRun')
    context.driver.execute_script("arguments[0].scrollIntoView();", val)
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'VoiseIESText').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'UserProfileArrowDown').click()
    time.sleep(10)


@step('I search for available "{value}" to "{value1}"')
def search_available_Node(context, value, value1):
    currentPage = GlobalVar.currentPage
    time.sleep(10)
    SearchBoxGenericXpath = context.baseReader.readElementByPropertyName(currentPage, 'SearchBoxGeneric').get(
        "value")
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, SearchBoxGenericXpath)))

    if value == 'BNG':
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
        time.sleep(2)
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(
            GlobalVar.testParams.get('BNGNode_BNG1'))
        time.sleep(10)
    elif value == 'OLT':
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
        time.sleep(2)
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(
            GlobalVar.testParams.get('OLTNode_Name'))
        time.sleep(10)


@step('I validate the "{value}" Status should be "{expectedValue}"')
def validate_data(context, value, expectedValue):
    currentPage = GlobalVar.currentPage
    time.sleep(10)
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'OnboardingStatus').text
    print(actualValue, expectedValue)
    assert actualValue == expectedValue


@step('I validate the generated configurations for "{value}"')
def config_validation(context, value):
    currentPage = GlobalVar.currentPage
    time.sleep(30)
    if value == "bng":
        for i in range(1, 3):
            olt_config_data = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                          'BNGConfig' + str(i)).text
            delete_create_text_file(value, 'new_bng' + str(i), olt_config_data)
            bng_compareResult = compare_text_file(value, 'new_bng' + str(i), 'new_bng' + str(i))
            print('bng' + str(i) + '_compareResult', bng_compareResult)
            assert bng_compareResult

    elif value == "olt":
        for i in range(1, 9):
            olt_config_data = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                          'OLTConfig' + str(i)).text
            delete_create_text_file(value, 'new_olt' + str(i), olt_config_data)
            olt_compareResult = compare_text_file(value, 'new_olt' + str(i), 'new_olt' + str(i))
            print('olt' + str(i) + '_compareResult', olt_compareResult)
            assert olt_compareResult
    time.sleep(5)
    val = context.baseReader.getElementByPropertyName(context, currentPage, 'Commit')
    context.driver.execute_script("arguments[0].scrollIntoView();", val)
    time.sleep(5)


@step('Wait for the BNG DryRun status response and validate the status for "success" scenario')
def validate_bng_status(context):
    currentPage = GlobalVar.currentPage
    WebDriverWait(context.driver, 60).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    # MainLoaderXpath = context.baseReader.readElementByPropertyName(context, currentPage, 'MainLoader').get('value')
    # WebDriverWait(context.driver, 200).until(
    #     EC.invisibility_of_element_located((By.XPATH, MainLoaderXpath)))
    # context.baseReader.getElementByPropertyName(context, currentPage, 'OnboardingBNG').click()
    time.sleep(500)
    # context.driver.refresh()
    # time.sleep(15)
    # context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
    # time.sleep(2)
    # context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(
    #     GlobalVar.testParams.get('BNGNode_BNG1'))
    # time.sleep(5)
    # actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'OnboardingStatus').text
    # assert actualValue == 'DryRun-Completed'


@step('Wait for the OLT DryRun status response and validate the status for "success" scenario')
def validate_olt_status(context):
    currentPage = GlobalVar.currentPage
    WebDriverWait(context.driver, 70).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    # MainLoaderXpath = context.baseReader.readElementByPropertyName(context, currentPage, 'MainLoader').get('value')
    # WebDriverWait(context.driver, 200).until(
    #     EC.invisibility_of_element_located((By.XPATH, MainLoaderXpath)))
    # context.baseReader.getElementByPropertyName(context, currentPage, 'OnboardingOLT').click()
    time.sleep(500)
    # context.driver.refresh()
    # time.sleep(15)
    # context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
    # time.sleep(2)
    # context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(
    #     GlobalVar.testParams.get('OLTNode_Name'))
    # time.sleep(5)
    # actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'OnboardingStatus').text
    # assert actualValue == 'DryRun-Completed'


@step('I verify the error message for short node name')
def enter_details(context):
    currentPage = GlobalVar.currentPage
    ActualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ErrorMessage')
    ErrorMessageText = ActualErrorMessage.text
    print(ErrorMessageText)
    assert ErrorMessageText == 'Node name should contain 12 letters'
    print('Error message verified')


# @step('I verify the error message for empty OLT node name')
# def enter_details(context):
#     currentPage = GlobalVar.currentPage
#     ActualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ErrorMessage')
#     ErrorMessageText = ActualErrorMessage.text
#     print(ErrorMessageText)
#     assert ErrorMessageText == 'Please enter node name'
#     print('Error message verified')

@step('I verify the error message for empty lag name')
def enter_details(context):
    currentPage = GlobalVar.currentPage
    ActualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ErrorMessage')
    ErrorMessageText = ActualErrorMessage.text
    print(ErrorMessageText)
    assert ErrorMessageText == 'Please enter lag name'
    print('Error message verified')


@step('I verify the error message for numeric lag name')
def enter_details(context):
    currentPage = GlobalVar.currentPage
    ActualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ErrorMessage')
    ErrorMessageText = ActualErrorMessage.text
    print(ErrorMessageText)
    assert ErrorMessageText == 'Lag should be lowercase.'
    print('Error message verified')


@step('I verify the error message for allcaps lag name')
def enter_details(context):
    currentPage = GlobalVar.currentPage
    ActualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ErrorMessage')
    ErrorMessageText = ActualErrorMessage.text
    print(ErrorMessageText)
    assert ErrorMessageText == 'Lag should be lowercase.'
    print('Error message verified')


@step('I verify the error message for double hyphen lag name')
def enter_details(context):
    currentPage = GlobalVar.currentPage
    # ActualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ErrorMessage')
    # # ErrorMessageText = ActualErrorMessage.text
    # # print(ErrorMessageText)
    # # assert ErrorMessageText == 'Lag should be lowercase.'
    # # print('Error message verified')


@step('I verify the error message for empty OLT node name')
def enter_details(context):
    currentPage = GlobalVar.currentPage
    ActualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ErrorMessage')
    ErrorMessageText = ActualErrorMessage.text
    print(ErrorMessageText)
    assert ErrorMessageText == 'Please enter node name'
    print('Error message verified')


@step('I verify the error message for short OLT node name')
def enter_details(context):
    currentPage = GlobalVar.currentPage
    ActualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ErrorMessage')
    ErrorMessageText = ActualErrorMessage.text
    print(ErrorMessageText)
    assert ErrorMessageText == 'Node name should contain 12 letters'
    print('Error message verified')


@step('I verify the error message for empty OLT lag name')
def enter_details(context):
    currentPage = GlobalVar.currentPage
    ActualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ErrorMessage')
    ErrorMessageText = ActualErrorMessage.text
    print(ErrorMessageText)
    assert ErrorMessageText == 'Please enter lag name'
    print('Error message verified')


@step('I verify the error message for numeric OLT lag name')
def enter_details(context):
    currentPage = GlobalVar.currentPage
    ActualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ErrorMessage')
    ErrorMessageText = ActualErrorMessage.text
    print(ErrorMessageText)
    assert ErrorMessageText == 'Lag should be lowercase.'
    print('Error message verified')


@step('I verify the error message for allcaps OLT lag name')
def enter_details(context):
    currentPage = GlobalVar.currentPage
    ActualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ErrorMessage')
    ErrorMessageText = ActualErrorMessage.text
    print(ErrorMessageText)
    assert ErrorMessageText == 'Lag should be lowercase.'
    print('Error message verified')


@step('I verify the error message for double hyphen OLT lag name')
def enter_details(context):
    currentPage = GlobalVar.currentPage
    # ActualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'ErrorMessage')
    # # ErrorMessageText = ActualErrorMessage.text
    # # print(ErrorMessageText)
    # # assert ErrorMessageText == 'Lag should be lowercase.'
    # # print('Error message verified')


@when('I add "{Lag1}" Lag for "{OLTName}" Node')
def step_impl(context, Lag1, OLTName):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    Node_ListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'NodeList')
    Node_Value = context.driver.find_elements(By.XPATH, Node_ListXpath)
    for i in range(0, len(Node_Value)):
        if (OLTName in Node_Value[i].text):
            time.sleep(7)
            Node_Value[i].click()
            time.sleep(1)
            context.baseReader.getElementByPropertyName(context, currentPage, 'AddNewLag').click()
            context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').click()
            context.baseReader.getElementByPropertyName(context, currentPage, 'NewLagPlaceHolder').send_keys(Lag1)
            context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
            time.sleep(3)
            break


@then('I delete "{LagName}" lag for "{OLTName}" Node')
def delete_log(context, LagName, OLTName):
    currentPage = GlobalVar.currentPage
    time.sleep(3)
    Node_ListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'NodeList')
    Node_Value = context.driver.find_elements(By.XPATH, Node_ListXpath)
    for i in range(0, len(Node_Value)):
        if (OLTName in Node_Value[i].text):
            time.sleep(3)
            Node_Value[i].click()
            Lag_Value = context.driver.find_elements(By.XPATH,
                                                     context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                               'LagList'))
            for j in range(0, len(Lag_Value)):
                time.sleep(3)
                actions = ActionChains(context.driver)
                actions.move_to_element(Lag_Value[j]).click().perform()
                Lag_Value[j].find_element(By.XPATH, ".//span").click()
                time.sleep(3)
            break


@then("I click on Add Link CTA")
def click_on_add_cta(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddButton').click()
    time.sleep(10)


@when("I delete the link for {Node1Value} Node1")
def step_impl(context, Node1Value):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    records_rows = context.baseReader.getElementLocatorValue(context, currentPage, 'OLTLinksRows')
    records = context.driver.find_elements(By.XPATH, records_rows)
    print(str(len(records)))
    for row in range(0, len(records)):
        node1Text = records[row].find_element(By.XPATH, ".//div[@data-row-colmn-name='Node1']//div").text
        if (node1Text == Node1Value):
            records[row].find_element(By.XPATH, ".//span[text()='delete']").click()
            break

    time.sleep(3)


@step("I click on {dropdowntoBeSelect} dropdown and select {NodeValue}")
def selectNodes(context, dropdowntoBeSelect, NodeValue):
    currentPage = GlobalVar.currentPage
    time.sleep(2)
    dropDown_ListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'selectLinkValueDropdown')
    dropdown = context.driver.find_elements(By.XPATH, dropDown_ListXpath)
    for i in range(0, len(dropdown)):
        time.sleep(3)
        attributeName = dropdown[i].get_attribute("data-row-colmn-name")
        if (attributeName in dropdowntoBeSelect):
            time.sleep(2)
            dropdown[i].click()
            time.sleep(1)
            DataListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DataList')
            DataDropDownList = context.driver.find_elements(By.XPATH, DataListXpath)

            for k in range(0, len(DataDropDownList)):
                dropdownText = DataDropDownList[k].text.strip()
                if (dropdownText == NodeValue):
                    DataDropDownList[k].click()
                    time.sleep(2)
                    assert NodeValue == dropdownText
                    break

            break
        time.sleep(3)


@step("I validate the link is added for {Node1}, {Lag1}, {Node2}, {Lag2}")
def validate_link_is_added(context, Node1, Lag1, Node2, Lag2):
    currentPage = GlobalVar.currentPage
    expectedValues = [Node1, Lag1, Node2, Lag2]
    actualValues = []
    time.sleep(5)
    records_rows = context.baseReader.getElementLocatorValue(context, currentPage, 'OLTLinksRows')
    records = context.driver.find_elements(By.XPATH, records_rows)
    for row in range(0, len(records)):
        node1Text = records[row].find_element(By.XPATH, ".//div[@data-row-colmn-name='Node1']//div").text
        if (node1Text == Node1):
            for j in range(0, 5):
                rowValue = records[row].find_elements(By.XPATH, ".//div[@style='font-size: inherit;']")
                actualValues.append(rowValue[j].text)
            break
    check = all(item in actualValues for item in expectedValues)
    assert check == True


@then("I validate {Node1} link is deleted")
def step_impl(context, Node1):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    flag = True
    records_rows = context.baseReader.getElementLocatorValue(context, currentPage, 'OLTLinksRows')
    records = context.driver.find_elements(By.XPATH, records_rows)
    for row in range(0, len(records)):
        node1Text = records[row].find_element(By.XPATH, ".//div[@data-row-colmn-name='Node1']//div").text
        if (node1Text == Node1):
            flag = False
            break

    assert flag == True


@step('I add {BNGDropDownType} as {Value}')
def step_impl(context, BNGDropDownType, Value):
    currentPage = GlobalVar.currentPage
    if (BNGDropDownType in "BNG1"):
        context.baseReader.getElementByPropertyName(context, currentPage, 'BNG1DropDown').click()
    if (BNGDropDownType in "BNG2"):
        context.baseReader.getElementByPropertyName(context, currentPage, 'BNG2DropDown').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'BNGInputBoxToAddBNG').send_keys(Value)
    time.sleep(15)
    context.baseReader.getElementByPropertyName(context, currentPage, 'AddBNGCTA').click()
    time.sleep(15)
    context.baseReader.getElementByPropertyName(context, currentPage, 'BNG1DropDown').click()


@then("I select {BNGValue} as {DropDown}")
def step_impl(context, BNGValue, DropDown):
    flag = False
    currentPage = GlobalVar.currentPage
    time.sleep(3)
    if (DropDown in "BNG1"):
        context.baseReader.getElementByPropertyName(context, currentPage, 'BNG1DropDown').click()
    if (DropDown in "BNG2"):
        context.baseReader.getElementByPropertyName(context, currentPage, 'BNG2DropDown').click()
    BNGValues = context.baseReader.getElementLocatorValue(context, currentPage, 'BNGList')
    bngValue = context.driver.find_elements(By.XPATH, BNGValues)
    time.sleep(1)
    for row in range(0, len(bngValue)):
        if (bngValue[row].text == BNGValue):
            bngValue[row].click()
            flag = True
            break
    time.sleep(2)
    assert flag == True


@step("user click on Discard CTA")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'discardCTA').click()
    time.sleep(25)


@step("I click on Next CTA")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Next').click()
    time.sleep(120)


@step("I validate that Validate text is displayed")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    time.sleep(10)
    valiadteText = context.baseReader.getElementByPropertyName(context, currentPage, 'validatedText').text
    statusOfMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'validatedText').is_displayed()
    assert valiadteText == "Validated!"
    assert statusOfMessage == True


@step("I enter below data for DNS server {DNSServerType} Input fields")
def step_impl(context, DNSServerType):
    currentPage = GlobalVar.currentPage
    if (DNSServerType in "IPV4"):
        inputLabels = context.baseReader.getElementLocatorValue(context, currentPage, 'DNSServersIPV4Labels')
    if (DNSServerType in "IPV6"):
        inputLabels = context.baseReader.getElementLocatorValue(context, currentPage, 'DNSServersIPV6Labels')
    records = context.driver.find_elements(By.XPATH, inputLabels)
    for i in range(len(records)):
        for row in context.table:
            testData = context.baseReader.fill_field(row['LabelName'], row['InputValue'])
            if (testData[0] in records[i].text):
                records[i].find_element(By.XPATH, ".//parent::app-input//input").send_keys(testData[1])
                break


@step("I enter below data for IPV4 Address Pool Servers {ServerType} Input fields")
def add_IPV_address_Pool_Servers_data(context, ServerType):
    currentPage = GlobalVar.currentPage
    if (ServerType in "ODD"):
        inputLabels = context.baseReader.getElementLocatorValue(context, currentPage, 'IPV4localDhcpServerODD')
    if (ServerType in "EVEN"):
        inputLabels = context.baseReader.getElementLocatorValue(context, currentPage, 'IPV4localDhcpServerEven')
    if (ServerType in "DV"):
        inputLabels = context.baseReader.getElementLocatorValue(context, currentPage, 'IPV4localDhcpServerDV')

    records = context.driver.find_elements(By.XPATH, inputLabels)
    for i in range(len(records)):
        for row in context.table:
            testData = context.baseReader.fill_field(row['LabelName'], row['InputValue'])
            if (testData[0] in records[i].text):
                records[i].find_element(By.XPATH, ".//parent::app-input//input").send_keys(testData[1])
                break


@step("I enter below data for IPV6 Address Pool Servers {serverName} Input fields")
def add_Address_Pool_Servers_Data(context, serverName):
    currentPage = GlobalVar.currentPage
    if (serverName in "V6-ODD"):
        inputLabels = context.baseReader.getElementLocatorValue(context, currentPage, 'IPV6V6ODD')
    if (serverName in "V6-EVEN"):
        inputLabels = context.baseReader.getElementLocatorValue(context, currentPage, 'IPV6V6Even')

    records = context.driver.find_elements(By.XPATH, inputLabels)
    for i in range(len(records)):
        for row in context.table:
            testData = context.baseReader.fill_field(row['LabelName'], row['InputValue'])
            if (testData[0] in records[i].text):
                records[i].find_element(By.XPATH, ".//parent::app-input//input").send_keys(testData[1])
                break


@step("I enter below data for Routing Policies Input fields")
def add_Routing_Policies(context):
    currentPage = GlobalVar.currentPage
    time.sleep(2)
    inputLabels = context.baseReader.getElementLocatorValue(context, currentPage, 'PrefixEntryInp')
    records = context.driver.find_elements(By.XPATH, inputLabels)
    for i in range(len(records)):
        for row in context.table:
            testData = context.baseReader.fill_field(row['LabelName'], row['InputValue'])
            if (testData[0] in records[i].text):
                records[i].find_element(By.XPATH, ".//parent::app-input//input").send_keys(testData[1])
                break


@step("I enter below data for BNG Addresses Input fields")
def add_BNG_Addresses_Data(context):
    currentPage = GlobalVar.currentPage
    inputLabels = context.baseReader.getElementLocatorValue(context, currentPage, 'BNGAddressesInps')
    records = context.driver.find_elements(By.XPATH, inputLabels)
    for i in range(len(records)):
        for row in context.table:
            testData = context.baseReader.fill_field(row['LabelName'], row['InputValue'])
            if (testData[0] in records[i].text):
                records[i].find_element(By.XPATH, ".//parent::app-input//input").send_keys(testData[1])
                break


@step("I enter below data for HSIA IES {SubscriberType} Input fields")
def add_HSIA_IES_Data(context, SubscriberType):
    currentPage = GlobalVar.currentPage
    if (SubscriberType in "Odd Subscriber"):
        inputLabels = context.baseReader.getElementLocatorValue(context, currentPage, 'HSIAIESODDSubscriberInterface')
    if (SubscriberType in "EVEN Subscriber"):
        inputLabels = context.baseReader.getElementLocatorValue(context, currentPage, 'HSIAIESEvenSubscriberInterface')

    records = context.driver.find_elements(By.XPATH, inputLabels)
    for i in range(len(records)):
        for row in context.table:
            testData = context.baseReader.fill_field(row['LabelName'], row['InputValue'])
            if (testData[0] in records[i].text):
                records[i].find_element(By.XPATH, ".//parent::app-input//input").send_keys(testData[1])
                break


@step('I enter HSIA IES Address as {HSIAAddressValue}')
def add_HSIA_Address_Value(context, HSIAAddressValue):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'HSIAIESAddress').send_keys(HSIAAddressValue)


@step("I enter VOICE IES Address as {VOICEIESAddress}")
def add_VOICE_IES_Address(context, VOICEIESAddress):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'VOICEIESAddressInps').send_keys(VOICEIESAddress)


@then("I enter Routing Policies as {RoutingPolicies}")
def step_impl(context, RoutingPolicies):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'PrefixEntryInp').send_keys(RoutingPolicies)


@step('I search for {OLTName} OLT to onboard')
def search_OLT(context, OLTName):
    currentPage = GlobalVar.currentPage
    SearchBoxGenericXpath = context.baseReader.readElementByPropertyName(currentPage, 'SearchBoxGeneric').get("value")
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, SearchBoxGenericXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').click()
    time.sleep(1)
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(OLTName)
    time.sleep(2)


@then('I Select the BNG Group CLLI ID {OLTID} OLT drop down value')
def select_OLT_Value(context, OLTID):
    currentPage = GlobalVar.currentPage
    time.sleep(3)
    context.baseReader.getElementByPropertyName(context, currentPage, 'BNGGroupCLLIIDDropDown').click()
    time.sleep(2)
    oltList = context.baseReader.getElementLocatorValue(context, currentPage, 'BNGGroupCLLIIDValues')
    olts = context.driver.find_elements(By.XPATH, oltList)
    print(len(olts))
    for row in range(0, len(olts)):
        print(olts[row].text.strip())
        if (olts[row].text.strip() == OLTID):
            olts[row].click()
            break
    time.sleep(2)


@then("Wait and verify for OLT DryRun to be completed for {DeviceName}")
def step_impl(context, DeviceName):
    currentPage = GlobalVar.currentPage
    WebDriverWait(context.driver, 600).until(EC.invisibility_of_element((By.XPATH, "MainLoader")))
    time.sleep(200)
    headerText = context.baseReader.getElementByPropertyName(context, currentPage,
                                                             'SuccessOLTDryRunSuccessMessage').text

    assert headerText.strip() == "Dry Run Configuration - " + DeviceName


@then("wait and verify the BNG dry run is completed for {DeviceName}")
def step_impl(context, DeviceName):
    currentPage = GlobalVar.currentPage
    time.sleep(200)
    WebDriverWait(context.driver, 600).until(EC.invisibility_of_element((By.XPATH, "MainLoader")))
    headerText = context.baseReader.getElementByPropertyName(context, currentPage,
                                                             'SuccessBNGGROUPCONFIGONBNGDEVICESMessage').text

    if (headerText.strip() != "BNG GROUP CONFIG ON BNG DEVICES- " + DeviceName):
        print("Terminating the execution as the expected result didn't matched")
        assert headerText.strip() != "BNG GROUP CONFIG ON BNG DEVICES- " + DeviceName
        exit(1)

    assert headerText.strip() == "BNG GROUP CONFIG ON BNG DEVICES- " + DeviceName


@then("I click on OLT {CTAName} button")
def step_impl(context, CTAName):
    currentPage = GlobalVar.currentPage
    if CTAName in "Commit":
        context.baseReader.getElementByPropertyName(context, currentPage, 'CommitCTA').click()
    if CTAName in "Reject":
        context.baseReader.getElementByPropertyName(context, currentPage, 'RejectCTA').click()
    if CTAName in "Download Config":
        context.baseReader.getElementByPropertyName(context, currentPage, 'DownloadConfigCTA').click()
    time.sleep(5)


@then("I click on {CTAName} CTA on reject confirmation overlay")
def step_impl(context, CTAName):
    currentPage = GlobalVar.currentPage
    if CTAName in "Yes Reject":
        context.baseReader.getElementByPropertyName(context, currentPage, 'YesRejectCTAOnRejectOverlay').click()
    if CTAName in "Cancel Reject":
        context.baseReader.getElementByPropertyName(context, currentPage, 'CancelCTAOnOverlay').click()


@then("I click on {CTAName} CTA on commit confirmation overlay")
def step_impl(context, CTAName):
    currentPage = GlobalVar.currentPage
    if CTAName in "commit":
        context.baseReader.getElementByPropertyName(context, currentPage, 'CommitCTAOnOverlay').click()
    if CTAName in "Cancel":
        context.baseReader.getElementByPropertyName(context, currentPage, 'CancelCTAOnOverlay').click()


@then("I validate the Commit request {messageType} message is display and close the overlay")
def step_impl(context, messageType):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    if messageType == "success":
        successMessageTxt = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                        'CommitOverlaySuccessMessageText').text
        assert successMessageTxt == "Commit Request has been submitted Successfully and is now in progress.This may take few minutes to complete..."

    if messageType == "reject":
        rejectMessageTxt = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                       'CommitOverlaySuccessMessageText').text
        print(rejectMessageTxt)
        assert rejectMessageTxt == "Reject Request has been submitted Successfully and is now in progress."

    context.baseReader.getElementByPropertyName(context, currentPage, 'CommitOverlayCloseCTA').click()
    time.sleep(4)


@then(
    'I unzip {fileName} folder and move in Framework directory and Delete the actual downloaded zip folder from download folders')
def step_impl(context, fileName):
    username = getpass.getuser()
    print(os.path.exists(os.getcwd() + "\onboarding-bng-config.zip"))
    # if "bng" in fileName:
    #     assert os.path.exists(os.getcwd() + "\onboarding-bng-config.zip") == True
    #
    # if "olt" in fileName:
    #     assert os.path.exists(os.getcwd() + "\\onboarding-olt-config.zip") == True

    print(os.listdir("\\"))

    if (os.path.exists(os.path.expanduser(os.getcwd() + "\\onboarding-bng-config"))):
        path1 = os.path.expanduser(os.getcwd() + "\\onboarding-bng-config")
        shutil.rmtree(path1)
    if (os.path.exists(os.path.expanduser(os.getcwd() + "\\onboarding-olt-config"))):
        path2 = os.path.expanduser(os.getcwd() + "\\onboarding-olt-config")
        shutil.rmtree(path2)

    filePath = ""

    for root, dirs, files in os.walk(r"C:\Users\\" + username + "\\Downloads"):
        for name in files:
            if name == fileName:
                filePath = os.path.abspath(os.path.join(root, name))
    filePath = filePath.replace('\\', '/')

    with zipfile.ZipFile(filePath, 'r') as zip:
        filePath = filePath.replace('.zip', '')
        zip.extractall(filePath + "/all")

    path1 = os.path.expanduser(filePath)
    path2 = os.path.expanduser(os.getcwd())
    shutil.move(path1, path2)
    os.remove(filePath + ".zip")


@then('I validate {BNGValue} BNG status as {expectedStatus}')
def step_impl(context, BNGValue, expectedStatus):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(BNGValue)
    time.sleep(2)
    status = context.baseReader.getElementByPropertyName(context, currentPage, 'BNGStatus').text
    if (status != expectedStatus):
        print("Terminating the execution as the expected result didn't matched")
        assert status == expectedStatus
        exit(1)
    assert status == expectedStatus
    time.sleep(2)


@then("I validate {OLTName} OLT status as {expectedStatus}")
def step_impl(context, OLTName, expectedStatus):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(OLTName)
    time.sleep(2)
    status = context.baseReader.getElementByPropertyName(context, currentPage, 'OLTStatus').text

    if (status != expectedStatus):
        print("Terminating the execution as the expected result didn't matched")
        assert status == expectedStatus
        exit(1)

    assert status == expectedStatus
    time.sleep(2)


@then("I Search {BngName} BNG and click on Onboard CTA")
def step_impl(context, BngName):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(BngName)
    time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'BNGRowOnboardCTA').click()
    time.sleep(2)


@then("I Search {OLTName} OLT and click on Onboard CTA")
def step_impl(context, OLTName):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(OLTName)
    time.sleep(2)
    print(context.baseReader.getElementByPropertyName(context, currentPage, 'OLTRowOnboardCTA'))
    context.baseReader.getElementByPropertyName(context, currentPage, 'OLTRowOnboardCTA').click()
    time.sleep(2)


@then("I Search {BNGName} BNG on dashboard default listing and verify the count of OLT is {OLTCount}")
def step_impl(context, BNGName, OLTCount):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(BNGName)
    time.sleep(2)
    print(context.baseReader.getElementByPropertyName(context, currentPage, 'OLTCountForBNG').text)
    if (context.baseReader.getElementByPropertyName(context, currentPage, 'OLTCountForBNG').text != OLTCount):
        print("Terminating the execution as the expected result didn't matched")
        assert context.baseReader.getElementByPropertyName(context, currentPage, 'OLTCountForBNG').text == OLTCount
        exit(1)

    assert OLTCount == context.baseReader.getElementByPropertyName(context, currentPage, 'OLTCountForBNG').text
    time.sleep(2)


@then("I click on reload input fields toggle icon to reload all the input values")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'reloadIpputFieldsToggle').click()
    time.sleep(1)


@then("I wait until {BNGName} BNG dry run is completed and disappear from the BNG list")
def step_impl(context, BNGName):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(BNGName)
    totalBNGRecords = context.baseReader.getElementLocatorValue(context, currentPage, 'BNGNameFirstRow')
    Node_Value = len(context.driver.find_elements(By.XPATH, totalBNGRecords))
    while (Node_Value > 0):
        time.sleep(5)
        context.driver.refresh()
        time.sleep(2)
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(BNGName)
        time.sleep(1)
        Node_Value = len(context.driver.find_elements(By.XPATH, totalBNGRecords))


@then("I wait until {OLTName} OLT dry run is completed and disappear from the OLT list")
def step_impl(context, OLTName):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(OLTName)
    totalBNGRecords = context.baseReader.getElementLocatorValue(context, currentPage, 'OLTFirstRow')
    Node_Value = len(context.driver.find_elements(By.XPATH, totalBNGRecords))
    while Node_Value > 0:
        time.sleep(5)
        context.driver.refresh()
        time.sleep(2)
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(OLTName)
        time.sleep(1)
        Node_Value = len(context.driver.find_elements(By.XPATH, totalBNGRecords))


@given("Delete the downloaded config files")
def step_impl(context):
    if (os.path.exists(os.path.expanduser(os.getcwd() + "\\onboarding-bng-config"))):
        path1 = os.path.expanduser(os.getcwd() + "\\onboarding-bng-config")
        shutil.rmtree(path1)
    if (os.path.exists(os.path.expanduser(os.getcwd() + "\\onboarding-olt-config"))):
        path2 = os.path.expanduser(os.getcwd() + "\\onboarding-olt-config")
        shutil.rmtree(path2)


@then("I enter OLT mac-address as {OLTMacAddress}")
def step_impl(context, OLTMacAddress):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'OLTMacAddressInp').send_keys(OLTMacAddress)


@then("I enter SE-x1 Interface Address as {SEX1InterfaceAddress}")
def step_impl(context, SEX1InterfaceAddress):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SEX1InterfaceAddress').send_keys(
        SEX1InterfaceAddress)


@then("I enter SE-x2 Interface Address as {SEX2InterfaceAddress}")
def step_impl(context, SEX2InterfaceAddress):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SEX2InterfaceAddress').send_keys(
        SEX2InterfaceAddress)


@then("I enter below data for Routing Policies {policyType} Input fields")
def step_impl(context, policyType):
    currentPage = GlobalVar.currentPage
    if (policyType in "CONSUMER-STATIC"):
        context.baseReader.getElementByPropertyName(context, currentPage, 'CONSUMERSTATICPrefixEntryInp1').send_keys(
            "10.160.63.64/27")
        context.baseReader.getElementByPropertyName(context, currentPage, 'CONSUMERSTATICPrefixEntryInp2').send_keys(
            "10.160.63.96/27")
    if (policyType in "CONSUMER-BVOICE"):
        context.baseReader.getElementByPropertyName(context, currentPage, 'CONSUMERBVOICEPrefixEntryInp1').send_keys(
            "10.160.64.128/27")
        context.baseReader.getElementByPropertyName(context, currentPage, 'CONSUMERBVOICEPrefixEntryInp2').send_keys(
            "10.160.64.160/27")
    if (policyType in "CONSUMER-STB"):
        context.baseReader.getElementByPropertyName(context, currentPage, 'CONSUMERSTBPrefixEntryInp1').send_keys(
            "10.160.65.192/27")
        context.baseReader.getElementByPropertyName(context, currentPage, 'CONSUMERSTBPrefixEntryInp2').send_keys(
            "10.160.65.224/27")


@step('I validate the error message for "{type}" test')
def step_impl(context, type):
    currentPage = GlobalVar.currentPage
    expectedErrorMessage = GlobalVar.testParams['errorMessage']
    actual_error_message = None
    if type == "emptyOLT":
        emptyNodeErrorMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                               'emptyNodeErrorMessage')
        actual_error_message = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, emptyNodeErrorMessageXpath)),

            message='Element not visible').text
        WebDriverWait(context.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, emptyNodeErrorMessageXpath)), message='Element not visible')

    elif type == "minimum_length_olt":
        minimumLengthNodeErrorMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                       'minimumLengthNodeErrorMessage')
        actual_error_message = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, minimumLengthNodeErrorMessageXpath)),
            message='Element not visible').text

    elif type == "minimum_length_bng" or type == "maximum_length_bng":
        minimumLengthErrorMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                   'minimumLengthErrorMessage')
        actual_error_message = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, minimumLengthErrorMessageXpath)),
            message='Element not visible').text

    elif type == "emptyLag":
        emptyLagErrorMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                              'emptyLagErrorMessage')
        actual_error_message = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, emptyLagErrorMessageXpath)),

            message='Element not visible').text
        WebDriverWait(context.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, emptyLagErrorMessageXpath)), message='Element not visible')

    elif type == "lagLowerCase":
        lagLowerCaseErrorMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                  'lagLowerCaseErrorMessage')
        actual_error_message = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, lagLowerCaseErrorMessageXpath)),

            message='Element not visible').text
        WebDriverWait(context.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, lagLowerCaseErrorMessageXpath)),
            message='Element not visible')

    elif type == "duplicateLag":
        duplicateLagErrorMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                  'duplicateLagErrorMessage')
        actual_error_message = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, duplicateLagErrorMessageXpath)),

            message='Element not visible').text
        WebDriverWait(context.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, duplicateLagErrorMessageXpath)),
            message='Element not visible')

    elif type == "duplicateLinks":
        errorMessageDuplicateLinkXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                   'errorMessageDuplicateLink')
        print(errorMessageDuplicateLinkXpath)
        print(currentPage)
        actual_error_message = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, errorMessageDuplicateLinkXpath)),

            message='Element not visible').text
        WebDriverWait(context.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, errorMessageDuplicateLinkXpath)),
            message='Element not visible')

    elif type == "deleteLagWithActiveLink":
        errorMessageDuplicateLinkXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                   'errorMessageDuplicateLink')
        print(errorMessageDuplicateLinkXpath)
        print(currentPage)
        actual_error_message = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, errorMessageDuplicateLinkXpath)),

            message='Element not visible').text
        WebDriverWait(context.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, errorMessageDuplicateLinkXpath)),
            message='Element not visible')

    elif type == "emptyBNG":
        Xpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                          'xpath')

        actual_error_message = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, Xpath)),

            message='Element not visible').text
        WebDriverWait(context.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, Xpath)),
            message='Element not visible')
    print("Expected Error Message Below ====================================================================")
    print(expectedErrorMessage)
    print("Actual Error Message Below ======================================================================")
    print(actual_error_message)
    assert str(expectedErrorMessage).strip() == str(actual_error_message).strip()


@step('I fill the required parameter for "{test_type}" of BNG name')
def step_impl(context, test_type):
    currentPage = GlobalVar.currentPage
    firstBNGNameXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'firstBNGName')
    WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, firstBNGNameXpath))).send_keys(GlobalVar.testParams.get('BNG1Name'))


@step('I fill the required parameter for "{test_type}" of OLT name')
def step_impl(context, test_type):
    currentPage = GlobalVar.currentPage
    if test_type == "minimum_length":
        newNodeXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'newNode')
        WebDriverWait(context.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, newNodeXpath))).send_keys(
            GlobalVar.testParams.get('OLTNode_Name'))

    elif test_type == "maximum_length":
        newNodeXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'newNode')
        WebDriverWait(context.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, newNodeXpath))).send_keys(
            GlobalVar.testParams.get('OLTNode_Name'))


@step('I validate that the olt name should contain only 12 characters')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    newNodeXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'newNode')

    olt_name = WebDriverWait(context.driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, newNodeXpath))).text
    assert olt_name < GlobalVar.testParams.get('OLTNode_Name')
    assert olt_name in GlobalVar.testParams.get('OLTNode_Name')


@step('I fetch the first OLT info from the table and select it')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    firstOLTNameXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'firstOLTName')
    oltName = WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, firstOLTNameXpath))).text

    context.baseReader.getElementByPropertyName(context, currentPage, 'OLTSearchBar').send_keys(oltName)
    context.baseReader.getElementByPropertyName(context, currentPage, 'firstOLTName').click()


@step('Wait for the loader to disappear')
def loader_wait(context):
    currentPage = GlobalVar.currentPage
    loaderXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'loader')
    WebDriverWait(context.driver, 20).until(
        EC.invisibility_of_element_located((By.XPATH, loaderXpath)))


@step('I enter a "{param}" value for adding the new OLT lag')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    lagName = GlobalVar.testParams['OLTLag_Node']
    newLagInputFieldXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'newLagInputField')
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, newLagInputFieldXpath))).send_keys(
        lagName)


@step('I validate the error message for deleting the Lag with active Link')
@step('Validate the error message for deleting the node that has an existing lag in it')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    expectedErrorMessage = GlobalVar.testParams['errorMessage']
    deleteNodeErrorMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                            'deleteNodeErrorMessage')
    actual_error_message = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, deleteNodeErrorMessageXpath)),

        message='Element not visible').text
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, deleteNodeErrorMessageXpath)), message='Element not visible')
    print("Expected error message below:")
    print(str(expectedErrorMessage).strip())
    print("Actual error message below:")
    print(str(actual_error_message).strip())
    assert str(expectedErrorMessage).strip() in str(actual_error_message).strip()


@step('I fill the required details to add a "{param}" new node')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    if param == "first":
        oltNodeName = GlobalVar.testParams['OLTNode_Name']
        newNodeFieldXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'newNodeField')
        WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, newNodeFieldXpath))).send_keys(
            oltNodeName)
    elif param == "second":
        oltNodeName = GlobalVar.testParams['OLTNode_SE-X1']
        newNodeFieldXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'newNodeField')
        WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, newNodeFieldXpath))).send_keys(
            oltNodeName)

    elif param == "third":
        oltNodeName = GlobalVar.testParams['OLTNode_SE-X2']
        newNodeFieldXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'newNodeField')
        WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, newNodeFieldXpath))).send_keys(
            oltNodeName)


@step('I validate that the created node should exist in the nodes table at "{param}" place')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage

    if param == "first":
        expectedNode = GlobalVar.testParams['OLTNode_Name']
        firstNodeNameXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                       'firstNodeName')
        actualNode = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, firstNodeNameXpath)),

            message='Element not visible').text
        assert expectedNode in actualNode

        context.baseReader.getElementByPropertyName(context, currentPage, 'firstNodeName').click()
    if param == "second":
        expectedNode = GlobalVar.testParams['OLTNode_SE-X1']
        secondNodeNameXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                        'secondNodeName')
        actualNode = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, secondNodeNameXpath)),

            message='Element not visible').text

        assert expectedNode in actualNode
        context.baseReader.getElementByPropertyName(context, currentPage, 'secondNodeName').click()

    if param == "third":
        expectedNode = GlobalVar.testParams['OLTNode_SE-X2']
        thirdNodeNameXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                       'thirdNodeName')
        actualNode = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, thirdNodeNameXpath)),

            message='Element not visible').text

        assert expectedNode in actualNode
        context.baseReader.getElementByPropertyName(context, currentPage, 'thirdNodeName').click()


@step('I fill the required details to add a "{param}" lag')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage

    if param == "first":
        oltLagName = GlobalVar.testParams['OLTLag_Node']
        NewLagPlaceHolderXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'NewLagPlaceHolder')
        WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, NewLagPlaceHolderXpath))).send_keys(
            oltLagName)
    elif param == "second" or param == "third":
        oltLagName = GlobalVar.testParams['OLTLag_SE-X-1']
        NewLagPlaceHolderXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'NewLagPlaceHolder')
        WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, NewLagPlaceHolderXpath))).send_keys(
            oltLagName)


@step('I validate that none of the dropdowns should have any values selected')
def step_impl(context):
    currentPage = GlobalVar.currentPage

    node1Xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'node1')
    lag1Xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'lag1')
    node2Xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'node2')
    lag2Xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'lag2')

    element = context.driver.find_element(By.XPATH, node1Xpath)
    node1_placeholder_value = element.get_attribute("placeholder")
    assert node1_placeholder_value == "Select"

    element = context.driver.find_element(By.XPATH, lag1Xpath)
    lag1_placeholder_value = element.get_attribute("placeholder")
    assert lag1_placeholder_value == "Select"

    element = context.driver.find_element(By.XPATH, node2Xpath)
    node2_placeholder_value = element.get_attribute("placeholder")
    assert node2_placeholder_value == "Select"

    element = context.driver.find_element(By.XPATH, lag2Xpath)
    lag2_placeholder_value = element.get_attribute("placeholder")
    assert lag2_placeholder_value == "Select"

    try:
        # Wait for up to 10 seconds for the button to be clickable
        addXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'add')
        button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, addXpath))
        )

        # If the button is clickable, you can interact with it here
        button.click()
        assert False, "Button is not clickable"
    except Exception as e:
        print("Button is not clickable:", str(e))


@step('I choose the dropdown options to add a duplicate node')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'node1').click()
    time.sleep(2)
    dropdownListLen = context.baseReader.getElementLocatorValue(context, currentPage, 'dropdownList')
    node1Elements = context.driver.find_elements(By.XPATH, dropdownListLen)

    for i in range(1, len(node1Elements) + 1):
        node1_temp = context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']')
        node1 = node1_temp.text
        if node1 == GlobalVar.testParams['OLTNode_Name']:
            context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']').click()
            break

    context.baseReader.getElementByPropertyName(context, currentPage, 'lag1').click()
    time.sleep(2)
    dropdownListLen = context.baseReader.getElementLocatorValue(context, currentPage, 'dropdownList')
    lag1Elements = context.driver.find_elements(By.XPATH, dropdownListLen)
    for i in range(1, len(lag1Elements) + 1):
        lag1_temp = context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']')
        lag1 = lag1_temp.text
        if lag1 == GlobalVar.testParams['OLTLag_Node']:
            context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']').click()
            break

    context.baseReader.getElementByPropertyName(context, currentPage, 'node2').click()
    time.sleep(2)
    dropdownListLen = context.baseReader.getElementLocatorValue(context, currentPage, 'dropdownList')
    node2Elements = context.driver.find_elements(By.XPATH, dropdownListLen)
    for i in range(1, len(node2Elements) + 1):
        node2_temp = context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']')
        node2 = node2_temp.text
        if node2 == GlobalVar.testParams['OLTNode_SE-X1']:
            context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']').click()
            break

    context.baseReader.getElementByPropertyName(context, currentPage, 'lag2').click()
    time.sleep(2)
    dropdownListLen = context.baseReader.getElementLocatorValue(context, currentPage, 'dropdownList')
    lag2Elements = context.driver.find_elements(By.XPATH, dropdownListLen)
    for i in range(1, len(lag2Elements) + 1):
        lag2_temp = context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']')
        lag2 = lag2_temp.text
        if lag2 == GlobalVar.testParams['OLTLag_SE-X-1']:
            context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']').click()
            break
    time.sleep(5)


@step('I validate that the BNG parameters should be disable')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    ipv4DNS1ServerLabel1Xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'ipv4DNS1ServerLabel1')

    element = context.driver.find_element(By.XPATH, ipv4DNS1ServerLabel1Xpath)
    node1_placeholder_value = element.get_attribute("class")
    assert node1_placeholder_value == "disabled"


@step('I provided the necessary information to create a BNG dry run using incorrect values')
def step_impl(context):
    currentPage = GlobalVar.currentPage

    firstBNGXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'firstBNG')

    WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, firstBNGXpath))).click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'firstBNGName').send_keys(
        GlobalVar.testParams['OLTNode_Name'])

    context.baseReader.getElementByPropertyName(context, currentPage, 'bng1AddButton').click()
    time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'bng1ListVal').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'secondBNG').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'secondBNGName').send_keys(
        GlobalVar.testParams['OLTNode_SE-X1'])
    context.baseReader.getElementByPropertyName(context, currentPage, 'bng2AddButton').click()
    time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'bng2ListVal').click()


@step('I fill the required information from the dropdown to add "{param1}" & "{param2}" node')
def step_impl(context, param1, param2):
    currentPage = GlobalVar.currentPage
    print(">>>>>>>>>")
    print(currentPage)
    node1Xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'node1')
    print(node1Xpath)

    context.baseReader.getElementByPropertyName(context, currentPage, 'node1').click()
    time.sleep(2)
    dropdownListLen = context.baseReader.getElementLocatorValue(context, currentPage, 'dropdownList')
    node1Elements = context.driver.find_elements(By.XPATH, dropdownListLen)

    for i in range(1, len(node1Elements) + 1):
        node1_temp = context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']')
        node1 = node1_temp.text
        if node1 == GlobalVar.testParams['OLTNode_Name']:
            context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']').click()
            break

    context.baseReader.getElementByPropertyName(context, currentPage, 'lag1').click()
    time.sleep(2)
    dropdownListLen = context.baseReader.getElementLocatorValue(context, currentPage, 'dropdownList')
    lag1Elements = context.driver.find_elements(By.XPATH, dropdownListLen)
    for i in range(1, len(lag1Elements) + 1):
        lag1_temp = context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']')
        lag1 = lag1_temp.text
        if lag1 == GlobalVar.testParams['OLTLag_Node']:
            context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']').click()
            break

    context.baseReader.getElementByPropertyName(context, currentPage, 'node2').click()
    time.sleep(2)
    dropdownListLen = context.baseReader.getElementLocatorValue(context, currentPage, 'dropdownList')
    node2Elements = context.driver.find_elements(By.XPATH, dropdownListLen)
    for i in range(1, len(node2Elements) + 1):
        node2_temp = context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']')
        node2 = node2_temp.text
        if node2 == GlobalVar.testParams['OLTNode_SE-X2']:
            context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']').click()
            break

    context.baseReader.getElementByPropertyName(context, currentPage, 'lag2').click()
    time.sleep(2)
    dropdownListLen = context.baseReader.getElementLocatorValue(context, currentPage, 'dropdownList')
    lag2Elements = context.driver.find_elements(By.XPATH, dropdownListLen)
    for i in range(1, len(lag2Elements) + 1):
        lag2_temp = context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']')
        lag2 = lag2_temp.text
        if lag2 == GlobalVar.testParams['OLTLag_SE-X-1']:
            context.driver.find_element(By.XPATH, '//app-select/div/div[3]/ul/li[' + str(i) + ']').click()
            break


@step('I validate the error message while onboarding the OLT without selecting a value from the dropdown')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    expectedErrorMessage = GlobalVar.testParams['errorMessage']
    indexOutOfRangeErrorXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                          'indexOutOfRangeError')
    actual_error_message = WebDriverWait(context.driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, indexOutOfRangeErrorXpath)),

        message='Element not visible').text
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, indexOutOfRangeErrorXpath)),
        message='Element not visible')

    assert str(expectedErrorMessage).strip() in str(actual_error_message).strip()


@step('I validate that the fields are disabled for dry-run values')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    dryRunButtonXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DryRunButton')

    element = context.driver.find_element(By.XPATH, dryRunButtonXpath)
    button_status = element.get_attribute("class")
    assert button_status == "disabled"


@step('Fill the required information to add a new user with "{param}" access rights')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    # userName = GlobalVar.testParams["user"]
    xid = GlobalVar.testParams["xid"]
    # email = GlobalVar.testParams["email"]

    # print(userName)
    # print(xid)
    # print(email)
    context.baseReader.getElementByPropertyName(context, currentPage, "telusId").send_keys(xid)
    # context.baseReader.getElementByPropertyName(context, currentPage, "userName").send_keys(userName)
    # context.baseReader.getElementByPropertyName(context, currentPage, "emailID").send_keys(email)

    # select the user role
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, "readRole")
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, "readRole").click()

    # select status bar to activate the account
    context.baseReader.getElementByPropertyName(context, currentPage, 'statusSlider').click()


@step('I filter the user by "{searchBy}" and the searched user "{visibility}" be present in the results')
def step_impl(context, searchBy, visibility):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    searchedKey = GlobalVar.testParams[f'{searchBy}']
    print("Searched key:")
    print(searchedKey)

    searchBoxXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'searchBox')
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, searchBoxXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'searchBox').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'searchBox').send_keys(
        searchedKey)

    if "should not" == visibility:
        elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
        WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))
        noData = context.baseReader.getElementByPropertyName(context, currentPage, 'noData').text
        assert searchedKey != noData

    elif searchBy == "user":
        firstNameResultXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'firstNameResult')
        WebDriverWait(context.driver, 15).until(
            EC.text_to_be_present_in_element((By.XPATH, firstNameResultXpath), searchedKey))

        firstUser = context.baseReader.getElementByPropertyName(context, currentPage, 'firstNameResult').text
        assert searchedKey == firstUser

    elif searchBy == "email":
        firstEmailResultXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'firstEmailResult')
        WebDriverWait(context.driver, 15).until(
            EC.text_to_be_present_in_element((By.XPATH, firstEmailResultXpath), searchedKey))

        firstEmail = context.baseReader.getElementByPropertyName(context, currentPage, 'firstEmailResult').text
        assert searchedKey == firstEmail


@step('I validate the "{param}" message for deleting the user')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    expectedMessage = GlobalVar.testParams['errorMessage']
    if param == "success":
        pass

    deleteSuccessMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                          'deleteSuccessMessage')
    actual_error_message = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, deleteSuccessMessageXpath)),

        message='Element not visible').text
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, deleteSuccessMessageXpath)),
        message='Element not visible')

    assert str(expectedMessage).strip() in str(actual_error_message).strip()


@step('I change the user role from "{current_role}" to "{expected_role}"')
def step_impl(context, current_role, expected_role):
    currentPage = GlobalVar.currentPage
    writeRoleMainXpath = context.baseReader.getElementLocatorValue(context, currentPage, "writeRoleMain")
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, writeRoleMainXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, "writeRoleMain").click()


@step('I validate that the "{role}" role should be selected for the user')
def step_impl(context, role):
    currentPage = GlobalVar.currentPage
    writeRoleMainXpath = context.baseReader.getElementLocatorValue(context, currentPage, "writeRoleMain")
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, writeRoleMainXpath)))

    # adminRoleStatus = context.baseReader.getElementByPropertyName(context, currentPage, "adminRoleMain").is_selected()

    readRoleStatus = context.baseReader.getElementByPropertyName(context, currentPage, "readRoleMain").is_selected()
    writeRoleStatus = context.baseReader.getElementByPropertyName(context, currentPage, "writeRoleMain").is_selected()

    assert readRoleStatus == True and writeRoleStatus == True


@step('I change the account state from "{currentState}" to "{expectedState}"')
def step_impl(context, currentState, expectedState):
    currentPage = GlobalVar.currentPage
    if expectedState == "active":
        try:
            inactiveAccountStateXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                  "inactiveAccountState")
            WebDriverWait(context.driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, inactiveAccountStateXpath)))
            context.baseReader.getElementByPropertyName(context, currentPage, "inactiveAccountState").click()
        except:
            print(f"Account is already in {expectedState} State")
    elif expectedState == "inactive":
        try:
            inactiveAccountStateXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                  "activeAccountState")
            WebDriverWait(context.driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, inactiveAccountStateXpath)))
            context.baseReader.getElementByPropertyName(context, currentPage, "activeAccountState").click()
        except:
            print(f"Account is already in {expectedState} State")


@step('I validate that the selected user should be in "{state}" state')
def step_impl(context, state):
    currentPage = GlobalVar.currentPage
    if state == "active":
        activeAccountStateXpath = context.baseReader.getElementLocatorValue(context, currentPage, "activeAccountState")
        WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, activeAccountStateXpath)))
    else:
        inactiveAccountStateXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                              "inactiveAccountState")
        WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, inactiveAccountStateXpath)))


@step('I validate the error message while adding the new user with empty values')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    expectedErrorMessage = GlobalVar.testParams['errorMessage']
    newUserErrorMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                         'newUserErrorMessage')
    actual_error_message = WebDriverWait(context.driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, newUserErrorMessageXpath)),

        message='Element not visible').text
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, newUserErrorMessageXpath)),
        message='Element not visible')

    assert str(expectedErrorMessage).strip() in str(actual_error_message).strip()


@step('I validate the input field validation for "{field}" is "{errorMessage}"')
def step_impl(context, field, errorMessage):
    actualErrorMessage = ""
    currentPage = GlobalVar.currentPage
    if field == "telus-id":
        actualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                         "userIDValidation").text
    elif field == "user-name":
        actualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                         "userNameValidation").text
    elif field == "email-id":
        actualErrorMessage = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                         "emailIDValidation").text
    assert str(errorMessage).strip() == str(actualErrorMessage).strip()


@then("I navigate to consumer Home page")
def step_impl(context):
    time.sleep(3)
    url = context.driver.current_url.split("ca/")
    urlParam = url[0] + "ca/dashboard/dashboard-item"
    context.driver.get(urlParam)
    time.sleep(5)


@step('I clear the "{param}" from User management screen')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    paramXpath = context.baseReader.getElementLocatorValue(context, currentPage, f'{param}')
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, paramXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, f'{param}').send_keys(Keys.CONTROL + 'a')
    context.baseReader.getElementByPropertyName(context, currentPage, f'{param}').send_keys(Keys.DELETE)


@step('I validate that the read-only user should be selected')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, "readRoleMain").click()
    # writeRoleStatus = context.baseReader.getElementByPropertyName(context, currentPage, "writeRoleMain").is_selected()
    # assert readRoleStatus == True and writeRoleStatus == True


@step('I login into the application with read-only user')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    LoginXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Login')
    WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, LoginXpath)))
    time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Login').click()
    currentPage = 'KeycloakLoginPage'
    titleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'PageTitle')
    WebDriverWait(context.driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, titleXpath)))
    # readOnlyStatus = bool(GlobalVar.testParams.get('readOnly'))
    username = context.envReader.get("TestUserNameReadOnly")
    password = context.envReader.get('TestUserPassReadOnly')

    usernameXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'UserName')
    WebDriverWait(context.driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, usernameXpath))).send_keys(username)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Password').send_keys(password)
    context.baseReader.getElementByPropertyName(context, currentPage, 'LoginButton').click()
    WebDriverWait(context.driver, 100).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    titleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'title')
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, titleXpath)))


@step('I login into the application with admin user')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    LoginXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Login')
    WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, LoginXpath)))
    time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Login').click()
    currentPage = 'KeycloakLoginPage'
    titleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'PageTitle')
    WebDriverWait(context.driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, titleXpath)))
    # readOnlyStatus = bool(GlobalVar.testParams.get('readOnly'))
    username = context.envReader.get("CSPortalTestUserName")
    password = context.envReader.get('CSPortalTestUserName')

    usernameXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'UserName')
    WebDriverWait(context.driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, usernameXpath))).send_keys(username)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Password').send_keys(password)
    context.baseReader.getElementByPropertyName(context, currentPage, 'LoginButton').click()
    WebDriverWait(context.driver, 100).until(
        EC.invisibility_of_element((By.XPATH, "MainLoader")))
    titleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'title')
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, titleXpath)))


@step('I confirm that the read-only box should remain checked')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    flag = context.baseReader.getElementByPropertyName(context, currentPage, 'firstUserRead').is_selected()

    if flag == True:
        context.baseReader.getElementByPropertyName(context, currentPage, 'firstUserRead').click()
        expectedStatus = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                     'firstUserRead').is_selected()
        assert expectedStatus == True


@step('I validate that the "{param}" option should not be visible for read-only user')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    try:
        UserManagementXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'UserManagement')
        WebDriverWait(context.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, UserManagementXpath)))
    except Exception as e:
        print("User Management is not visible for Read-only user")


@step('I confirm that the selected OLT is as expected')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    oltName = context.baseReader.getElementByPropertyName(context, currentPage, 'oltHeading').text
    print(str(oltName))
    print(str(GlobalVar.testParams.get('OLTNode_Name')))

    print(len(str(oltName)))
    print(len(str(GlobalVar.testParams.get('OLTNode_Name'))))
    assert str(oltName).strip() == str(GlobalVar.testParams.get('OLTNode_Name')).strip()


@step('I validate the expected OLT should exist in the Node table')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    flag = False
    nodesXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'nodes')
    nodeValues = context.driver.find_elements(By.XPATH, nodesXpath)

    for i in range(1, len(nodeValues)):
        node_name = context.driver.find_element(By.XPATH, "//app-new-olt-pair/div[2]/div[1]/div/ul/li[" + str(
            i + 1) + "]/div").text
        if node_name == GlobalVar.testParams.get('OLTNode_Name'):
            time.sleep(2)
            context.driver.find_element(By.XPATH, "//app-new-olt-pair/div[2]/div[1]/div/ul/li[" + str(
                i + 1) + "]/div").click()
            flag = True
            break
    assert flag == True


@step('I validate that the expected lag should exist in the Termination points')
def step_impl(context):
    flag = False
    currentPage = GlobalVar.currentPage
    terminationPointsXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'terminationPoints')
    lagValues = context.driver.find_elements(By.XPATH, terminationPointsXpath)

    for i in range(1, len(lagValues) + 1):
        actual_lag = context.driver.find_element(By.XPATH,
                                                 "//app-dashboard-outlet/div/app-new-olt-pair/div[2]/div[2]/div[2]/ul/li[" + str(
                                                     i + 1) + "]/div").text
        print(actual_lag)
        print(GlobalVar.testParams['OLTLag_Node'])
        print(">>><<<<")
        if str(actual_lag).strip() == str(GlobalVar.testParams['OLTLag_Node']).strip():
            flag = True
            break
    assert flag == True


@step('I validate that the link should be added in the selected lag')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    allLinksXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'allLinks')
    linkValues = context.driver.find_elements(By.XPATH, allLinksXpath)

    for i in range(1, len(linkValues)):
        actual_link = context.driver.find_element(By.XPATH,
                                                  "//app-grid/div/div/div[2]/div[" + str(i + 1) + "]/div/div[1]").text
        assert actual_link.strip() == str(GlobalVar.testParams['OLTNode_Name']).strip()


@step('Verify that "{button}" button is disable')
def step_impl(context, button):
    currentPage = GlobalVar.currentPage
    print(currentPage)
    buttonXpath = context.baseReader.getElementLocatorValue(context, currentPage, button)
    print(buttonXpath)
    element = context.driver.find_element(By.XPATH, buttonXpath)
    result = element.get_attribute("disabled")
    print(result)
    assert result == "true", f"Button was disabled at that moment"


@step('I am searching for the first BNG on the BNG Onboarding BNG page')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    SearchBoxGenericXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBoxGeneric')
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, SearchBoxGenericXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(
        GlobalVar.testParams['BNG1Name'])


@step('I am searching for the first OLT on the BNG Onboarding OLT page')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    SearchBoxGenericXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBoxGeneric')
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, SearchBoxGenericXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(
        GlobalVar.testParams['OLTNode_Name'])


@step('I validate that the delete icon is not visible for the "{param}"')
def step(context, param):
    currentPage = GlobalVar.currentPage
    if param == "lag":
        try:
            deleteLagIconXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deleteLagIcon')
            WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, deleteLagIconXpath)))
            context.baseReader.getElementByPropertyName(context, currentPage, 'deleteLagIcon').click()
        except Exception as e:
            print("In Exception block- Delete icons are not visble for read-only user")

    else:
        try:
            deletIconXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deleteIcon')
            WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, deletIconXpath)))
            context.baseReader.getElementByPropertyName(context, currentPage, 'deletIconXpath').click()

        except Exception as e:
            print("In Exception block- Delete icons are not visble for read-only user")


@then("I click on Birth Certificate Action Icon")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'BNGBirthCertificateAction').click()
    time.sleep(5)


@then("I Search {BNGName} BNG on birth certificate page and validate BNG is displayed")
def step_impl(context, BNGName):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBoxGeneric').send_keys(BNGName)
    time.sleep(2)
    tableRowSize = context.baseReader.getElementLocatorValue(context, currentPage, 'BngRowRecords')
    records = context.driver.find_elements(By.XPATH, tableRowSize)
    assert "1" == str(len(records))


@then("I click on {NodeName} regenerate birth certificate icon and validate regenrate birth certificate message is display")
def step_impl(context, NodeName):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'regenerateBirthCertificate').click()
    time.sleep(3)
    regenerateHeading = context.baseReader.getElementByPropertyName(context, currentPage, 'regenerateBirthCertificateHeadline').text
    if(NodeName in "BNG"):
        assert regenerateHeading == "Regenerate BNG Birth-certificate"
    else:
        assert regenerateHeading == "Regenerate OLT Birth-certificate"

    assert "Successfully submitted the request" == context.baseReader.getElementByPropertyName(context, currentPage, 'regenerateBirthCertificateDesc').text


@when("I select {birthCertficateRow}")
def step_impl(context, birthCertficateRow):
    currentPage = GlobalVar.currentPage
    rows = context.baseReader.getElementLocatorValue(context, currentPage, 'containerRows')
    row = context.driver.find_elements(By.XPATH, rows)

    for i in range(0, len(row)):
        if (birthCertficateRow in row[i].text):
            row[i].click()
            break



@then("I validate {tab1}, {tab2}, {tab3} tabs is displayed")
def step_impl(context, tab1, tab2, tab3):
    currentPage = GlobalVar.currentPage
    expectedTabs = [tab1, tab2, tab3]
    actualTabs = []
    rows = context.baseReader.getElementLocatorValue(context, currentPage, 'containerTabs')
    row = context.driver.find_elements(By.XPATH, rows)

    for i in range(0, len(row)):
        actualTabs.append(row[i].text)

    assert actualTabs == expectedTabs


@then("I select {tabName} tab and validate the content is available")
def step_impl(context, tabName):
    currentPage = GlobalVar.currentPage
    rows = context.baseReader.getElementLocatorValue(context, currentPage, 'containerRows')
    row = context.driver.find_elements(By.XPATH, rows)
    containerText= ""

    for i in range(1, len(row)):
        if (tabName in row[i].text):
            row[i].click()
            containerText = context.baseReader.getElementByPropertyName(context, currentPage, 'containertexts').text
            break

    assert len(containerText) >= 0
    time.sleep(2)


@then("I click on BNG row to open mapped OLT")
def step_impl(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'oltCount').click()


@then('I validate that the "{actual_diff}" is successfully matched with "{expected_diff}" for "{type}" for "{action}" cs service')
def step_impl(context, actual_diff, expected_diff, type, action):
    assert FileCompare.compare_config_diff(context, GlobalVar.testParams[GlobalVar.test_case][f'configDiff_{type}'],
                                           GlobalVar.test_case, type, action)

