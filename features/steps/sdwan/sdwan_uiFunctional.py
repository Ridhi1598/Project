import datetime
import random
import string
import imaplib
import email
import traceback

import sys

from future.backports.datetime import timedelta
# from pip._vendor.toml import tz
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

from common.util.emailReader import validate_last_email
from features.steps.globalVar import GlobalVar
from features.steps.ui_steps_general import *
from features.steps.ui_steps_general import page_title_validation,click_button
# from datetime import datetime


try:
    from behave import given, when, then, step
    from selenium.webdriver.common.by import By
    import time
    import csv
    from selenium.webdriver.support.select import Select
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
except Exception as e:
    print("Some Module are missing : {}".format(e))

#declared Variables
currentPage = GlobalVar.currentPage
vlan = GlobalVar.vlan
vpn = GlobalVar.vpn
device = GlobalVar.device
Device = {}
editLANInterface = {}
afterEditingLANInterface = {}
customers = []
editWANInterface = {}
scenario = None
firstInterfaceVal = None
currentInterface = None
interfaceState = None
vlan_name = None
vlans_list = None
endList = []
myList = []
deviceForEditLan = {}
#End of declared Variables


@step('I should land on SDWAN portal')
def login(context):
    currentPage = "LandingPage"
    url = 'sdwanURL_' + sys.argv[2]
    context.driver.get(context.config.get(url))
    pageHeadingXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'pageHeading')
    WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, pageHeadingXpath)))
    pageHeading = context.driver.find_element_by_xpath(pageHeadingXpath)

    if (pageHeading.text == 'SDWAN Services - Self Serve Portal'):
        page_title_validation(context, 'Landing', 'SDWAN Services - Self Serve Portal')
        currentPage = GlobalVar.currentPage
        context.baseReader.getElementByPropertyName(context, currentPage, 'Login').click()
        page_title_validation(context, 'KeycloakLogin', 'Log In')
        currentPage = GlobalVar.currentPage
        username = os.getenv('TestUserName')
        password = os.getenv('TestUserPass')
        context.baseReader.getElementByPropertyName(context, currentPage, 'UserName').send_keys(username)
        context.baseReader.getElementByPropertyName(context, currentPage, 'Password').send_keys(password)
        context.baseReader.getElementByPropertyName(context, currentPage, 'LoginButton').click()
        WebDriverWait(context.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[text()='SD-WAN Customers ']")))

    elif(pageHeading.text == 'SD-WAN Customers'):
        pass


@step('Validate that all customers on VCO are listed')
def validate_customers(context):
    currentPage = GlobalVar.currentPage
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
    WebDriverWait(context.driver, 20).until(EC.invisibility_of_element_located((By.XPATH, noDataXpath)))
    # time.sleep(2)

    nextPage = context.baseReader.getElementByPropertyName(context, currentPage, 'nextPage')
    while '>' not in nextPage.text:
        customerListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'customerList')
        customerList = context.driver.find_elements(By.XPATH, customerListXpath)
        for i in range(0, len(customerList)):
            customers.append(customerList[i].text)
        nextPage = context.baseReader.getElementByPropertyName(context, currentPage, 'nextPage')
        if '>' in nextPage.text:
            break
        context.baseReader.getElementByPropertyName(context, currentPage, 'nextPage').click()
        # time.sleep(2)

@step('I filter and select a customer')
def filter_customer(context):
    currentPage = GlobalVar.currentPage
    customerName = context.csvRead[0].get('customerName')
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
    WebDriverWait(context.driver, 20).until(EC.invisibility_of_element_located((By.XPATH, noDataXpath)))
    # time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterCustomer').send_keys(customerName)
    networkNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'custValue')
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, networkNameValueXpath), customerName))
    context.baseReader.getElementByPropertyName(context, currentPage, 'custValue').click()

@step('Fill the required network parameters')
def fill_params(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'serviceTypeDropdown').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'l3vpn').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'topologyDropdown').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'anyToAny').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'vendorDropdown').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'velo').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'templateDropdown').click()

    if sys.argv[2] == 'dev':
        context.baseReader.getElementByPropertyName(context, currentPage, 'abEdgeProfile').click()
    if sys.argv[2] == 'preprod':
        context.baseReader.getElementByPropertyName(context, currentPage, 'tinaaDemoProfile').click()

    vpn['networkName'] = 'BHSDWAN_Network_' + str(
        ''.join(random.choices(string.digits, k=2))) + str(
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=3)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'networkName').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'networkName').send_keys(vpn['networkName'])
    vpn['networkDescription'] = 'BHSDWAN_Network_Description' + str(
        ''.join(random.choices(string.digits, k=2))) + str(
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))) + '-Desc'
    context.baseReader.getElementByPropertyName(context, currentPage, 'networkDescription').send_keys(vpn['networkDescription'])

@step('Navigate to sidebar link "{link}"')
def navigate_sidebar(context, link):
    currentPage = GlobalVar.currentPage
    page_title_validation(context, 'Sidebar', 'Monitor')
    currentPage = GlobalVar.currentPage
    WebDriverWait(context.driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[@class='loader-bg']")))
    context.baseReader.getElementByPropertyName(context, currentPage, link).click()

@step('New network should be listed under the list of networks')
def validate_new_network(context):
    currentPage = GlobalVar.currentPage

    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'networks').click()
    page_title_assert(context, 'CustomerNetwork', 'Network View')
    currentPage = GlobalVar.currentPage

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterNetwork').send_keys(vpn['networkName'])
    networkNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'networkVal')
    WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, networkNameValueXpath), vpn['networkName']))
    time.sleep(5)
    networkNameValue = context.baseReader.getElementByPropertyName(context, currentPage, 'networkVal').text
    assert vpn['networkName'] == networkNameValue

@step('Updated network should be listed under the list of networks')
def validate_network(context):
    currentPage = GlobalVar.currentPage

    SaveXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Save')
    WebDriverWait(context.driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, SaveXpath)))

    page_title_assert(context, 'CustomerNetwork', 'Network View')
    currentPage = GlobalVar.currentPage

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterNetwork').send_keys(vpn['networkName'])
    networkNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'networkVal')
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, networkNameValueXpath), vpn['networkName']))

    networkNameValue = context.baseReader.getElementByPropertyName(context, currentPage, 'networkVal').text
    assert vpn['networkName'] == networkNameValue


@step('Added network should be listed under the list of networks')
def validate_added_network(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterNetwork').send_keys(vpn['networkName'])
    networkNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'networkVal')
    WebDriverWait(context.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, networkNameValueXpath), vpn['networkName']))
    networkNameValue = context.baseReader.getElementByPropertyName(context, currentPage, 'networkVal').text
    assert vpn['networkName'] == networkNameValue


@step('"{page}" page title should contain "{expectedValue}"')
def page_title_assert(context, page, expectedValue):
    global currentPage
    isMatched = False
    currentPage = GlobalVar.currentPage
    currentPage = page + 'Page'
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'PageTitle').text
    if expectedValue.lower() in actualValue.lower():
        isMatched = True
    assert isMatched == True

@step('Change the required parameters')
def edit_network(context):
    global vpn
    currentPage = GlobalVar.currentPage

    currentTimeStamp = datetime.datetime.now()
    vpn['networkName'] = 'BHSDWAN_Network_Updated' + str(currentTimeStamp).replace('.', ':')
    nameObj = context.baseReader.getElementByPropertyName(context, currentPage, 'networkName')
    nameObj.clear()
    nameObj.send_keys(vpn['networkName'])

    vpn['networkDescription'] = 'BHSDWAN_Network_Description_Updated' + str(currentTimeStamp).replace('.', ':')
    descObj = context.baseReader.getElementByPropertyName(context, currentPage, 'networkDesc')
    descObj.clear()
    descObj.send_keys(vpn['networkDescription'])

@step('I filter and select a network')
def filter_customer(context):
    currentPage = GlobalVar.currentPage
    global initialNetworkName

    if vpn == {}:
        initialNetworkName = context.csvRead[0].get('initialNetworkName')
    else:
        initialNetworkName = vpn['networkName']

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterNetwork').send_keys(initialNetworkName)
    networkNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'networkVal')
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, networkNameValueXpath), initialNetworkName))
    time.sleep(3)

@step('I filter and select a network for "{scenario}" scenario')
def filter_customer(context, scenario):
    currentPage = GlobalVar.currentPage
    global networkDelete

    if vpn == {}:
        networkDelete = context.csvRead[0].get('networkDelete')
    else:
        networkDelete = vpn['networkName']

    if scenario == 'fail':
        context.baseReader.getElementByPropertyName(context, currentPage, 'filterNetwork').send_keys('Global Segment')
        networkNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'networkVal')
        WebDriverWait(context.driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, networkNameValueXpath), 'Global Segment'))

    if scenario == 'success':
        context.baseReader.getElementByPropertyName(context, currentPage, 'filterNetwork').send_keys(networkDelete)
        networkNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'networkVal')
        WebDriverWait(context.driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, networkNameValueXpath), networkDelete))


@step('Validate VPN changes are correctly displayed on portal')
def validate_changes(context):
    currentPage = GlobalVar.currentPage

    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 50).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'networks').click()
    page_title_assert(context, 'CustomerNetwork', 'Network View')
    currentPage = GlobalVar.currentPage

    # page_title_assert(context, 'CustomerNetwork', 'Network View')
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterNetwork').send_keys(vpn['networkName'])
    networkNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'networkVal')
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, networkNameValueXpath), vpn['networkName']))

    time.sleep(3)
    updatedName = context.baseReader.getElementByPropertyName(context, currentPage, 'nameVal').text
    updatedDescription = context.baseReader.getElementByPropertyName(context, currentPage, 'descVal').text
    assert updatedName == vpn['networkName']
    assert updatedDescription == vpn['networkDescription']

@step('Restore vpn changes to default')
def restore_vpn_default(context):
    currentPage = GlobalVar.currentPage
    click_button(context, 'editButton')
    page_title_assert(context, 'EditNetwork', 'Edit Network')
    currentPage = GlobalVar.currentPage
    nameObj = context.baseReader.getElementByPropertyName(context, currentPage, 'networkName')
    nameObj.clear()
    nameObj.send_keys(initialNetworkName)
    vpn['networkName'] = initialNetworkName
    click_button(context, 'Save')
    currentPage = GlobalVar.currentPage
    validate_network(context)
    click_button(context, 'review')
    currentPage = GlobalVar.currentPage
    page_title_assert(context, 'NetworkReview', 'Network: Review and Commit')
    currentPage = GlobalVar.currentPage
    click_button(context, 'commit')
    currentPage = GlobalVar.currentPage
    validate_changes(context)


@step('I filter and select a Device')
def filter_device(context):
    currentPage = GlobalVar.currentPage
    global deviceAdded
    if Device == {}:
        deviceAdded = context.csvRead[0].get('deviceAdded')
    else:
        deviceAdded = Device.get('Device_Name')

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(
        deviceAdded)
    time.sleep(10)
    deviceNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceVal')
    WebDriverWait(context.driver, 100).until(
        EC.text_to_be_present_in_element((By.XPATH, deviceNameValueXpath), deviceAdded))

@step('I filter and select updated Device')
def filter_updated_device(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(
        deviceAdded)
    deviceNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceVal')
    WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, deviceNameValueXpath), deviceAdded))


@step('I filter and select a Device to delete')
def filter_delete_device(context):
    global deviceDelete
    currentPage = GlobalVar.currentPage
    if Device == {}:
        deviceDelete = context.csvRead[0].get('deviceDelete')
    else:
        deviceDelete = Device['Device_Name']

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(
        deviceDelete)
    deviceNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceVal')
    WebDriverWait(context.driver, 40).until(
        EC.text_to_be_present_in_element((By.XPATH, deviceNameValueXpath), deviceDelete))


@step('I navigate to "{action}" button')
def navigate_action(context, action):
    currentPage = GlobalVar.currentPage
    time.sleep(5)

    context.baseReader.getElementByPropertyName(context, currentPage, 'action').click()
    actionMenuXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'actionMenu')
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, actionMenuXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, action).click()

@step('Edit the required device parameters')
def edit_device(context):
    global device
    currentPage = GlobalVar.currentPage
    device['contactName'] = 'U_BHSDWAN_' + str(''.join(random.choices(string.ascii_letters + string.digits, k=4)))
    nameObj = context.baseReader.getElementByPropertyName(context, currentPage, 'contactName')
    nameObj.clear()
    nameObj.send_keys(device['contactName'])

    # tempName = str(''.join(random.choices(string.ascii_uppercase, k=9))) + '-' + str(
    #     ''.join(random.choices(string.digits, k=3))) + '-' + str(
    #     ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))) + '-' + str(
    #     ''.join(random.choices(string.digits, k=3)))

    # deviceNameObj = context.baseReader.getElementByPropertyName(context, currentPage, 'deviceName')
    # device['deviceName'] = tempName
    # deviceNameObj.clear()
    # deviceNameObj.send_keys(device['deviceName'])

    tempAddress = str(''.join(random.choices(string.ascii_lowercase + string.digits, k=9)))
    device['address'] = "U_" + tempAddress
    addressObj = context.baseReader.getElementByPropertyName(context, currentPage, 'address')
    addressObj.clear()
    addressObj.send_keys(device['address'])

    tempCity = str(''.join(random.choices(string.ascii_lowercase, k=5)))
    device['city'] = 'U_' + tempCity
    cityObj = context.baseReader.getElementByPropertyName(context, currentPage, 'city')
    cityObj.clear()
    cityObj.send_keys(device['city'])

    tempZip = str(''.join(random.choices(string.digits, k=6)))
    device['zip'] = "U_" + tempZip
    zipObj = context.baseReader.getElementByPropertyName(context, currentPage, 'zipCode')
    zipObj.clear()
    zipObj.send_keys(device['zip'])

    tempEmail = str(''.join(random.choices(string.ascii_lowercase, k=6))) + '@bhsdwan.com'
    device['email'] = "U" + tempEmail
    emailObj = context.baseReader.getElementByPropertyName(context, currentPage, 'email')
    emailObj.clear()
    emailObj.send_keys(device['email'])

    time.sleep(10)
    # context.baseReader.getElementByPropertyName(context, currentPage, 'initialLicense').click()
    # context.baseReader.getElementByPropertyName(context, currentPage, 'licenseSelect').click()
    # context.baseReader.getElementByPropertyName(context, currentPage, 'updateLicense').click()


    context.baseReader.getElementByPropertyName(context, currentPage, 'countryName').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'countryNameValue').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'countryDropdownClose').click()
    device['country'] = context.baseReader.getElementByPropertyName(context, currentPage, 'countryDropdownClose').text

    context.baseReader.getElementByPropertyName(context, currentPage, 'stateName').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'stateNameValue').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'stateDropdownClose').click()
    device['state'] = context.baseReader.getElementByPropertyName(context, currentPage, 'stateDropdownClose').text
    time.sleep(30)
    context.baseReader.getElementByPropertyName(context, currentPage, "save").click()
    time.sleep(10)

@step('Validate device changes are correctly displayed on portal')
def validate_device_changes(context):
    currentPage = GlobalVar.currentPage
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 80).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))

    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'devices').click()
    page_title_assert(context, 'CustomerDevice', 'Devices')
    currentPage = GlobalVar.currentPage

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(deviceAdded)
    deviceNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceVal')
    response = WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, deviceNameValueXpath), deviceAdded))
    assert response == True
    time.sleep(3)
    context.baseReader.getElementByPropertyName(context, currentPage, 'deviceVal').click()

    overviewObj = context.baseReader.getElementByPropertyName(context, currentPage, 'deviceOverview')
    WebDriverWait(context.driver, 10).until(EC.visibility_of((overviewObj)))

    updatedName = context.baseReader.getElementByPropertyName(context, currentPage, 'contactNameVal').text
    assert updatedName == device['contactName']

    updatedEmail = context.baseReader.getElementByPropertyName(context, currentPage, 'contactEmailVal').text
    assert updatedEmail == device['email']

    # updatedDeviceName = context.baseReader.getElementByPropertyName(context, currentPage, 'deviceNameVal').text
    # assert updatedDeviceName == device['deviceName']

    updatedAddress = context.baseReader.getElementByPropertyName(context, currentPage, 'addressVal').text
    assert updatedAddress == device['address']

    updatedCity = context.baseReader.getElementByPropertyName(context, currentPage, 'cityVal').text
    assert updatedCity == device['city']

    updatedZip = context.baseReader.getElementByPropertyName(context, currentPage, 'zipVal').text
    assert updatedZip == device['zip']

    # updatedCountry = context.baseReader.getElementByPropertyName(context, currentPage, 'countryVal').text
    # if updatedCountry in device['country']:
    #     pass

    # updatedState = context.baseReader.getElementByPropertyName(context, currentPage, 'stateVal').text
    # if updatedState in device['state']:
    #     pass


@step('Restore device changes to default')
def restore_device_changes(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'devices').click()
    page_title_assert(context, 'CustomerDevice', 'Devices')
    currentPage = GlobalVar.currentPage

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(deviceAdded)
    deviceNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceVal')
    response = WebDriverWait(context.driver, 50).until(
        EC.text_to_be_present_in_element((By.XPATH, deviceNameValueXpath), deviceAdded))
    # assert response == True
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'action').click()
    actionMenuXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'actionMenu')
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, actionMenuXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'Edit').click()


    # context.baseReader.getElementByPropertyName(context, currentPage, 'Edit').click()
    page_title_assert(context, 'EditDevice', 'Edit Device')
    currentPage = GlobalVar.currentPage


    # nameObj = context.baseReader.getElementByPropertyName(context, currentPage, 'deviceName')
    # nameObj.clear()
    # nameObj.send_keys(deviceAdded)
    # device['deviceName'] = deviceAdded
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'countryNameRestore').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'countryNameValueRestore').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'countryName').click()
    device['country'] = context.baseReader.getElementByPropertyName(context, currentPage, 'countryName').text

    context.baseReader.getElementByPropertyName(context, currentPage, 'stateNameRestore').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'stateNameValueRestore').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'stateName').click()
    device['state'] = context.baseReader.getElementByPropertyName(context, currentPage, 'stateName').text

    click_button(context, 'save')
    currentPage = GlobalVar.currentPage
    page_title_assert(context, 'CustomerDevice', 'Devices')
    currentPage = GlobalVar.currentPage
    filter_updated_device(context)
    currentPage = GlobalVar.currentPage
    navigate_action(context, 'Commit')
    page_title_assert(context, 'DeviceReview', 'Review and Commit')
    currentPage = GlobalVar.currentPage
    click_button(context, 'Commit')
    currentPage = GlobalVar.currentPage
    validate_device_changes(context)

@step('Validate device is removed on portal')
def validate_delete_device(context):
    currentPage = GlobalVar.currentPage
    deviceDelete = context.csvRead[0].get('deviceDelete')
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 50).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))

    context.driver.refresh()
    time.sleep(10)
    pageTitleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
    WebDriverWait(context.driver, 100).until(
        EC.invisibility_of_element_located((By.XPATH, pageTitleXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(deviceDelete)
    deviceNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceValue')
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, deviceNameValueXpath), 'No data found'))



@step('Validate that device status changes to Activated')
def validate_activation_status(context):
    currentPage = GlobalVar.currentPage
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))
    time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'devices').click()
    page_title_assert(context, 'CustomerDevice', 'Devices')
    currentPage = GlobalVar.currentPage
    time.sleep(3)
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(
        deviceAdded)
    deviceNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceVal')
    WebDriverWait(context.driver, 50).until(
        EC.text_to_be_present_in_element((By.XPATH, deviceNameValueXpath), deviceAdded))
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'action').click()
    actionMenuXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'actionMenu')
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, actionMenuXpath)))
    elementObj = context.baseReader.getElementByPropertyName(context, currentPage, 'ActivateDisable')
    WebDriverWait(context.driver, 10).until(EC.visibility_of((elementObj)))


@step('Navigate to "{deviceView}" view')
def navigate_device_view(context, deviceView):
    currentPage = GlobalVar.currentPage
    # deviceNameValue = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceVal')
    # WebDriverWait(context.driver, 10).until(
    #     EC.text_to_be_present_in_element((By.XPATH, deviceNameValue), deviceAdded))
    time.sleep(3)
    context.baseReader.getElementByPropertyName(context, currentPage, 'deviceVal').click()
    time.sleep(20)
    # deviceViewObj = context.baseReader.getElementByPropertyName(context, currentPage, deviceView)
    # WebDriverWait(context.driver, 10).until(EC.element_selection_state_to_be((deviceViewObj), True))
    context.baseReader.getElementByPropertyName(context, currentPage, deviceView).click()

    # deviceViewObj.click()

    page_title_assert(context, 'DeviceConfig', 'Device Config')
    currentPage = GlobalVar.currentPage
    time.sleep(3)

@step('Validate that device status changes to Deactivated')
def validate_deactivation_status(context):
    currentPage = GlobalVar.currentPage

    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))

    context.driver.refresh()
    time.sleep(10)
    pageTitleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'PageTitle')
    WebDriverWait(context.driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, pageTitleXpath)))

    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(deviceAdded)
    deviceNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceVal')
    WebDriverWait(context.driver, 30).until(
        EC.text_to_be_present_in_element((By.XPATH, deviceNameValueXpath), deviceAdded))
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'action').click()
    actionMenuXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'actionMenu')
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, actionMenuXpath)))
    elementObj = context.baseReader.getElementByPropertyName(context, currentPage, 'DeactivateDisable')
    WebDriverWait(context.driver, 10).until(EC.visibility_of((elementObj)))


@step('Fill the required VLAN parameters')
def add_VLAN_parameters(context):
    global vlan
    currentPage = GlobalVar.currentPage

    N = 5
    vlan['VLANName'] = 'BHSDWANTestVLAN' + str(
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANname').send_keys(vlan['VLANName'])

    N = 2
    vlan['vlanid'] = str(''.join(random.choices(string.digits, k=N)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANid').send_keys(vlan['vlanid'])
    WebDriverWait(context.driver, 20).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[@class='loader-bg']")))

    context.baseReader.getElementByPropertyName(context, currentPage, 'VPNDropdown').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'VPNValue').click()
    # vpnListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'VPNDropdownList')
    # vpnList = context.driver.find_elements(By.XPATH, vpnListXpath)
    # for i in range (0, len(vpnList)):
    #     if vpnList[i].text == initialNetworkName:
    #         vpnList[i].click() VPNValue

    context.baseReader.getElementByPropertyName(context, currentPage, 'LanInterfaceDropdown').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'LanInterfaceValue').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'LanInterfaceDropdown2').click()

    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(3))))
    vlan['network'] = str(ip) + '.0/24'
    context.baseReader.getElementByPropertyName(context, currentPage, 'Network').send_keys(vlan['network'])

    context.baseReader.getElementByPropertyName(context, currentPage, 'LeaseTimeDropdown').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'LeaseTimeValue').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'LeaseTimeDropdown2').click()


    vlan['gateway'] = str(ip) + '.2'
    context.baseReader.getElementByPropertyName(context, currentPage, 'Gateway').send_keys(vlan['gateway'])

    context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPType').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPValue').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPType2').click()

    vlan['DHCPstart'] = str(ip) + '.4'
    vlan['DHCPend'] = str(ip) + '.8'
    context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPstart').send_keys(vlan['DHCPstart'])
    context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPend').send_keys(vlan['DHCPend'])

    context.baseReader.getElementByPropertyName(context, currentPage, 'Save').click()


@step('I filter and select a VLAN')
def filter_customer(context):
    currentPage = GlobalVar.currentPage
    if vlan == {}:
        editVLANname = context.csvRead[0].get('editVLANname')

    else:
        editVLANname = vlan['VLANName']

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterVLAN').send_keys(editVLANname)
    VLANValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'VLANValue')
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, VLANValueXpath), editVLANname))


@step('Edit the required VLAN parameters for DHCP state "{state}"')
def edit_vlan(context, state):
    global vlan
    global vlan_name
    global scenario
    global initialStatus
    global ip
    currentPage = GlobalVar.currentPage

    N = 5
    vlan['VLANName'] = 'BHSDWANTestVLANUpdated' + str(''.join(random.choices(string.ascii_uppercase + string.digits, k=N)))

    nameObj = context.baseReader.getElementByPropertyName(context, currentPage, 'VLANname')
    nameObj.clear()
    nameObj.send_keys(vlan['VLANName'])
    vlan_name= vlan['VLANName']

    vlan['vlanid'] = context.baseReader.getElementByPropertyName(context, currentPage, 'VLANid').get_property('value')

    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(3))))
    vlan['network'] = str(ip) + '.0/24'
    networkObj = context.baseReader.getElementByPropertyName(context, currentPage, 'Network')
    networkObj.clear()
    networkObj.send_keys(vlan['network'])

    # context.baseReader.getElementByPropertyName(context, currentPage, 'LeaseTimeDeselect').click()
    # context.baseReader.getElementByPropertyName(context, currentPage, 'LeaseTimeDropdown').click()
    # context.baseReader.getElementByPropertyName(context, currentPage, 'LeaseTimeValue').click()

    vlan['gateway'] = str(ip) + '.1'
    gatewayObj = context.baseReader.getElementByPropertyName(context, currentPage, 'Gateway')
    gatewayObj.clear()
    gatewayObj.send_keys(vlan['gateway'])

    stateValue = context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPState').text

    if 'Enabled' in stateValue:
        initialStatus = 'Enabled'
        if state == 'Initial':
            scenario = state
            vlan['DHCPstart'] = str(ip) + '.2'
            context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPstart').clear()
            context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPstart').send_keys(vlan['DHCPstart'])

            vlan['DHCPend'] = str(ip) + '.3'
            context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPend').clear()
            context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPend').send_keys(vlan['DHCPend'])

        elif state == 'Enabled':
            scenario = state
            time.sleep(5)
            context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPTypeEn').click()
            context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPValueDs').click()

    elif 'Disabled' in stateValue:
        initialStatus = 'Disabled'
        context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPTypeDs').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPValueRl').click()

        vlan['DHCPrelay'] =str(ip) + '.4'
        context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPrelay').clear()
        context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPrelay').send_keys(vlan['DHCPrelay'])

    elif 'Relay' in stateValue:
        initialStatus = 'Relay'
        context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPTypeRl').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPValueEn').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPTypeEn').click()

        vlan['DHCPstart'] = str(ip) + '.5'
        startObj = context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPstart')
        startObj.clear()
        startObj.send_keys(vlan['DHCPstart'])

        vlan['DHCPend'] = str(ip) + '.6'
        stopObj = context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPend')
        stopObj.clear()
        stopObj.send_keys(vlan['DHCPend'])

@step('I save and commit the changes')
def save_commit(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Save').click()

    SaveXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Save')
    WebDriverWait(context.driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, SaveXpath)))

    page_title_assert(context, 'DeviceConfig', 'Device Config')
    currentPage = GlobalVar.currentPage

    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANs').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterVLAN').send_keys(vlan['VLANName'])

    filterValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'VLANValue')
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, filterValueXpath), vlan['VLANName']))

    context.baseReader.getElementByPropertyName(context, currentPage, 'Review').click()

@step('Validate VLAN updates are shown on VLAN table on portal')
def validate_vlan_changes(context):
    currentPage = GlobalVar.currentPage
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 180).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))
    time.sleep(2)
    page_title_assert(context, 'DeviceConfig', 'Device Config')
    currentPage = GlobalVar.currentPage

    WebDriverWait(context.driver, 5).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[@class='loader-bg']")))

    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANs').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterVLAN').send_keys(vlan['VLANName'])

    filterValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'VLANValue')
    resVal = WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, filterValueXpath), vlan['VLANName']))

    assert resVal == True

    vlanid = context.baseReader.getElementByPropertyName(context, currentPage, 'VLANidVal').text
    assert vlan['vlanid'] == vlanid

    vlanNetwork = context.baseReader.getElementByPropertyName(context, currentPage, 'NetworkValue').text
    assert vlan['network'] == vlanNetwork

    vlanGateway = context.baseReader.getElementByPropertyName(context, currentPage, 'GatewayValue').text
    assert vlan['gateway'] == vlanGateway

    if initialStatus == 'Enabled':
        if scenario == 'Initial':
            vlanDHCPstart = context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPstartValue').text
            assert vlan['DHCPstart'] == vlanDHCPstart

            vlanDHCPend = context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPendValue').text
            assert vlan['DHCPend'] == vlanDHCPend

        else:
            vlanDHCPstart = context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPstartValue').text
            assert vlanDHCPstart == str(ip) + '.13'

            vlanDHCPend = context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPendValue').text
            assert vlanDHCPend == str(ip) + '.255'

    elif initialStatus == 'Disabled':
        vlanDHCPstart = context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPstartValue').text
        assert vlanDHCPstart == str(ip) + '.13'

        vlanDHCPend = context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPendValue').text
        assert vlanDHCPend == str(ip) + '.255'

    elif initialStatus == 'Relay':
        vlanDHCPstart = context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPstartValue').text
        assert vlan['DHCPstart'] == vlanDHCPstart

        vlanDHCPend = context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPendValue').text
        assert vlan['DHCPend'] == vlanDHCPend


@step('Restore VLAN changes to default')
def restore_vlan_changes(context):
    currentPage = GlobalVar.currentPage
    click_button(context, 'Edit')
    currentPage = GlobalVar.currentPage
    page_title_assert(context, 'EditVLAN', 'Edit VLAN')
    currentPage = GlobalVar.currentPage

    vlan['VLANName'] = context.csvRead[0].get('editVLANname')
    nameObj = context.baseReader.getElementByPropertyName(context, currentPage, 'VLANname')
    nameObj.clear()
    nameObj.send_keys(vlan['VLANName'])

    save_commit(context)
    page_title_assert(context, 'VLANReview', 'Review and Commit')
    currentPage = GlobalVar.currentPage
    click_button(context, 'Commit')
    currentPage = GlobalVar.currentPage
    validate_vlan_changes(context)

@step('I click on Yes button')
def proceed_to_delete(context):
    currentPage = GlobalVar.currentPage
    confirmDialogXpath = "//div[@class='modal-content']"
    yesXpath = "//button[text()='Yes']"
    WebDriverWait(context.driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, confirmDialogXpath)))
        # context.baseReader.getElementLocatorValue(context, currentPage, 'Yes')
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, yesXpath)))
    # context.baseReader.getElementByPropertyName(context, currentPage, 'Yes').click()
    context.driver.find_element_by_xpath(yesXpath).click()


@step('Navigate to commit view')
def navigate_to_commit(context):
    currentPage = GlobalVar.currentPage

    SaveXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Save')
    WebDriverWait(context.driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, SaveXpath)))

    page_title_assert(context, 'DeviceConfig', 'Device Config')
    currentPage = GlobalVar.currentPage

    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[@class='loader-bg']")))

    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANs').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterVLAN').send_keys(vlan['VLANName'])

    filterValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'VLANValue')
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, filterValueXpath), vlan['VLANName']))

    context.baseReader.getElementByPropertyName(context, currentPage, 'Review').click()

@step('Validate VLAN is added to VLAN table on portal')
def validate_add_VLAN(context):
    currentPage = GlobalVar.currentPage
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 100).until(EC.visibility_of_element_located((By.XPATH, alertXpath)))

    page_title_assert(context, 'DeviceConfig', 'Device Config')
    currentPage = GlobalVar.currentPage

    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[@class='loader-bg']")))

    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANs').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterVLAN').send_keys(vlan['VLANName'])

    filterValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'VLANValue')
    response = WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, filterValueXpath), vlan['VLANName']))
    assert response == True


@step('Validate deleting VPN with active site configurations should fail')
def validate_delete_error(context):
    currentPage = GlobalVar.currentPage
    errorMessage = context.csvRead[0].get('errorMessage')
    messageXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'message')
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, messageXpath)))
    message = context.baseReader.getElementByPropertyName(context, currentPage, 'message').text
    isMatched = False
    if errorMessage in message:
        isMatched = True
    assert isMatched == True


@step('I click on addNetwork button')
def click_add_network(context):
    currentPage = GlobalVar.currentPage
    buttonXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'addNetwork')
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, buttonXpath)))
    # WebDriverWait(context.driver, 10).until(
    #     EC.visibility_of_element_located((By.XPATH, "//*[@class='loader-bg']")))
    # WebDriverWait(context.driver, 10).until(
    #     EC.invisibility_of_element_located((By.XPATH, "//*[@class='loader-bg']")))
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'addNetwork').click()


@step('wait till the Customer HomePage is loaded')
def customer_Homepage(context):
    currentPage = GlobalVar.currentPage
    customerHomePageTitle = context.baseReader.getElementLocatorValue(context, currentPage, 'customerHomePageTitle')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, customerHomePageTitle)))


@step('Click on "{value}" and wait for the devices page')
def devices_page(context, value):
    currentPage = GlobalVar.currentPage
    loaderAfterSelectingCustomerXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'loaderAfterSelectingCustomer')
    WebDriverWait(context.driver, 20).until(EC.invisibility_of_element_located((By.XPATH, loaderAfterSelectingCustomerXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, value).click()
    deviceLoaderXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceLoader')
    WebDriverWait(context.driver, 20).until(EC.invisibility_of_element_located((By.XPATH, deviceLoaderXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'addDeviceButton').click()
    deviceLoaderXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceLoader')
    WebDriverWait(context.driver, 20).until(EC.invisibility_of_element_located((By.XPATH, deviceLoaderXpath)))


@step('Fill the required parameter to add a new device for "{value}"')
def add_new_device(context,value):
    global Device
    global deviceForEditLan
    loaderXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'loader')
    WebDriverWait(context.driver, 20).until(
        EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'vendorDropdown').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'velo').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'countryDropdown').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'canadaVal').click()

    letters = string.ascii_uppercase
    ranDevice = 'BHSDWANTD' + '-' + str(
        ''.join(random.choices(string.digits, k=3))) + '-' + str(
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))) + '-' + str(
        ''.join(random.choices(string.digits, k=3)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'deviceName').send_keys(ranDevice)

    context.baseReader.getElementByPropertyName(context, currentPage, 'modelDropdown').click()
    if value == "modelE3800Val":
        Device['Device_Name'] = ranDevice
        context.baseReader.getElementByPropertyName(context, currentPage, 'modelE3800Val').click()

    if value == "modelE610Val":
        deviceForEditLan['Device_Name'] = ranDevice
        context.baseReader.getElementByPropertyName(context, currentPage, 'modelE610Val').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'stateDropdown').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'ABAlberta').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'deviceTemplateDropdown').click()
    # context.baseReader.getElementByPropertyName(context, currentPage, 'quickStartProfile').click()

    if sys.argv[2] == "dev":
        context.baseReader.getElementByPropertyName(context, currentPage, 'abEdgeProfile').click()
    if sys.argv[2] == "preprod":
        context.baseReader.getElementByPropertyName(context, currentPage, 'TinnaDemoProfile').click()

    ranAdd = 'sdwan ' + str(''.join(random.choices(string.ascii_letters + string.digits, k=7)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'address1').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'address1').send_keys(ranAdd)
    Device['Address'] = ranAdd

    ranCity = 'sdwan ' + str(''.join(random.choices(string.ascii_letters + string.digits, k=4)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'city').send_keys(ranCity)
    Device['City'] = ranCity

    ranName = ''.join(random.choice(letters) for i in range(4))
    ranName = 'sdwan'+ranName
    context.baseReader.getElementByPropertyName(context, currentPage, 'contactName').send_keys(ranName)
    Device['ContactName'] = ranName

    ranEmail = ranName + '@mail.com'
    context.baseReader.getElementByPropertyName(context, currentPage, 'contactEmail').send_keys(ranEmail)
    Device['Email'] = ranEmail

    ranIN = ''.join(random.choice(letters) for i in range(3))
    ranZip = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=3)))
    ranZip = ranIN+' '+ranZip
    context.baseReader.getElementByPropertyName(context, currentPage, 'zipCode').send_keys(ranZip)
    Device['zipCode'] = ranZip

    context.baseReader.getElementByPropertyName(context, currentPage, 'selectLicense').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'firstLicenseVal').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'save').send_keys((Keys.ARROW_UP))

    Device['Vendor'] = context.baseReader.getElementByPropertyName(context, currentPage, 'vendorSelectedVal').text
    Device['Country'] = context.baseReader.getElementByPropertyName(context, currentPage, 'countrySelectedVal').text
    Device['Model'] = context.baseReader.getElementByPropertyName(context, currentPage, 'modelSelectedVal').text
    Device['State'] = context.baseReader.getElementByPropertyName(context, currentPage, 'stateSelectedVal').text
    Device['Device_Template'] = context.baseReader.getElementByPropertyName(context, currentPage, 'deviceTemplateSelectedVal').text
    Device['License'] = context.baseReader.getElementByPropertyName(context, currentPage, 'licenseSelectedVal').text

    # saveXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'save')
    # WebDriverWait(context.driver, 20).until(EC.element_to_be_clickable((By.XPATH, saveXpath)))
    time.sleep(30)
    WebDriverWait(context.driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, '//*[@src="static/assets/img/user.png"')))

    context.baseReader.getElementByPropertyName(context, currentPage, 'save').click()
    loaderXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'loader')
    WebDriverWait(context.driver, 20).until(
        EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

    devicePageTitle = context.baseReader.getElementLocatorValue(context, currentPage, 'devicePageTitle')
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, devicePageTitle)))


@step('I perform Commit operation to add a new Device for "{value}"')
def commit_add_device(context, value):
    global Device
    currentPage = GlobalVar.currentPage
    if value == "modelE3800Val":
        device_name = Device.get("Device_Name")
    elif value == "modelE610Val":
        device_name = deviceForEditLan.get("Device_Name")
    time.sleep(10)
    searchBoxXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'searchByDeviceName')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, searchBoxXpath)))

    time.sleep(10)
    click_on_the_element(context, "searchByDeviceName")
    time.sleep(10)

    # context.driver.execute_script('document.evaluate("//input[@placeholder="Device Name"]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value=device_name;')
    context.baseReader.getElementByPropertyName(context, currentPage, 'searchByDeviceName').send_keys(device_name)
    time.sleep(10)
    deviceValXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'firstDevice')
    if value == "modelE3800Val":
        WebDriverWait(context.driver, 120).until(
            EC.text_to_be_present_in_element((By.XPATH, deviceValXpath), Device.get('Device_Name')))
    elif value == "modelE610Val":
        WebDriverWait(context.driver, 120).until(
            EC.text_to_be_present_in_element((By.XPATH, deviceValXpath), deviceForEditLan.get('Device_Name')))
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'actionButton').click()
    time.sleep(10)
    actionCommitXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'actionCommit')
    WebDriverWait(context.driver, 40).until(EC.element_to_be_clickable((By.XPATH, actionCommitXpath)))
    time.sleep(20)
    context.baseReader.getElementByPropertyName(context, currentPage, 'actionCommit').click()


@step('Validate that the added device for "{value}" is shown on portal')
def validate_added_device(context, value):
    global Device
    isMatched = False
    currentPage = GlobalVar.currentPage
    time.sleep(5)

    finalCommitXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'finalCommit')
    WebDriverWait(context.driver, 20).until(EC.element_to_be_clickable((By.XPATH, finalCommitXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'finalCommit').click()

    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 80).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))
    time.sleep(5)
    click_button(context, 'siderDeviceUrl')

    if value == "modelE3800Val":
        context.baseReader.getElementByPropertyName(context, currentPage, 'searchByDeviceName').send_keys(Device.get('Device_Name'))
    elif value == "modelE610Val":
        context.baseReader.getElementByPropertyName(context, currentPage, 'searchByDeviceName').send_keys(deviceForEditLan.get('Device_Name'))

    noDataFoundXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noDataFound')
    WebDriverWait(context.driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, noDataFoundXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'firstDeviceLink').click()
    time.sleep(5)

    #change the current context to CustomerDevicePage from AddNewDevicePage
    change_currentPage(context,'CustomerDevice')
    currentPage = GlobalVar.currentPage

    deviceNameVal = context.baseReader.getElementByPropertyName(context, currentPage, 'deviceNameVal').text
    vendorValue = context.baseReader.getElementByPropertyName(context, currentPage, 'vendorValue').text
    modelValue = context.baseReader.getElementByPropertyName(context, currentPage, 'modelValue').text
    deviceTemplateValue = context.baseReader.getElementByPropertyName(context, currentPage, 'deviceTemplateValue').text
    contactNameValue = context.baseReader.getElementByPropertyName(context, currentPage, 'contactNameValue').text
    ContactEmailValue = context.baseReader.getElementByPropertyName(context, currentPage, 'ContactEmailValue').text
    addressValue = context.baseReader.getElementByPropertyName(context, currentPage, 'addressVal').text
    cityValue = context.baseReader.getElementByPropertyName(context, currentPage, 'cityVal').text
    zipValue = context.baseReader.getElementByPropertyName(context, currentPage, 'zipVal').text

    if value == "modelE3800Val":
        if (deviceNameVal == Device.get('Device_Name')) and (vendorValue in Device.get('Vendor')) and (
                modelValue in Device.get('Model')) and (deviceTemplateValue in Device.get('Device_Template')) and (
                contactNameValue == Device.get('ContactName')) and (ContactEmailValue == Device.get('Email')) and (
                addressValue == Device.get('Address')) and (cityValue == Device.get('City')) and (
                str(zipValue) == str(Device.get('zipCode'))):
            isMatched = True
        assert isMatched == True
    if value == "modelE610Val":
        pass
    time.sleep(5)

# ADD DEVICE STEPS END

@step('I Navigate to the Devices Link and filter a device by name')
def navigate_deviceLink_filter_device(context):
    currentPage = GlobalVar.currentPage
    global deviceAdded
    if Device == {}:
        deviceAdded = context.csvRead[0].get('deviceAdded')
    else:
        deviceAdded = Device.get('Device_Name')
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'devicesURL').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(deviceAdded)
    time.sleep(5)

@step('Select a Device and Navigate to the DeviceConfigPage')
def filter_and_select_device(context):
    currentPage = GlobalVar.currentPage
    time.sleep(15)
    # deviceNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceVal')
    # WebDriverWait(context.driver, 30).until(
    #     EC.text_to_be_present_in_element((By.XPATH, deviceNameValueXpath), deleteDevice))
    context.baseReader.getElementByPropertyName(context, currentPage, 'deviceVal').click()
    # context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(deviceAdded)
    # time.sleep(10)
    # deviceNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'firstCustomerDevice')
    # WebDriverWait(context.driver, 30).until(
    #     EC.text_to_be_present_in_element((By.XPATH, deviceNameValueXpath), deviceAdded))
    # context.baseReader.getElementByPropertyName(context, currentPage, 'firstCustomerDevice').click()
    # time.sleep(20)

    deviceConfig = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceConfigURL')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, deviceConfig)))
    time.sleep(10)
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[@class='loader-bg']")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'deviceConfigURL').click()
    # LANURL = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceURL')
    # WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, LANURL)))
    time.sleep(10)

@step('Click on the LAN Interfaces to open EDIT/VIEW LAN Interfaces')
def click_on_LAN_Interfaces(context):
    global editLANInterface
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'LANInterfaceLink').click()
    time.sleep(15)
    editXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'edit')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, editXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'edit').click()
    time.sleep(5)
    editLANInterface['Mode'] = context.baseReader.getElementByPropertyName(context, currentPage, 'modeVal').text
    editLANInterface['VLANs'] = context.baseReader.getElementByPropertyName(context, currentPage, 'VLANsVal').text
    editLANInterface['MTU'] = context.baseReader.getElementByPropertyName(context, currentPage, 'mtuVal').get_attribute('value')

@step('Edit the required parameters for LAN Interface')
def edit_required_field_for_LAN(context):
    global editLANInterface
    global afterEditingLANInterface
    mode = editLANInterface.get('Mode')
    # lan = editLANInterface.get('VLANs')
    modeList = mode.split(' ')
    # lanList = lan.split(' ')
    currentPage = GlobalVar.currentPage

    elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enableState')
    flag = elementState.is_selected()
    if flag == False:
        context.baseReader.getElementByPropertyName(context, currentPage, 'enabledState').click()
    time.sleep(5)

    if modeList[0] == 'trunk':
        context.baseReader.getElementByPropertyName(context, currentPage, 'modeDropdown').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'accessMode').click()
        afterEditingLANInterface['Mode'] = 'access'

    if modeList[0] == 'access':
        context.baseReader.getElementByPropertyName(context, currentPage, 'modeDropdown').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'trunkVal').click()
        afterEditingLANInterface['Mode'] = 'trunk'

    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANsDropdown').click()
    vlanListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'VLANsList')
    vlanList = context.driver.find_elements(By.XPATH, vlanListXpath)
    for i in range(0, len(vlanList)):
        if vlanList[i].text == context.csvRead[0].get('initialNetworkName'):
            vlanList[i].click()

    randomMTU = '1400'
    context.baseReader.getElementByPropertyName(context, currentPage, 'mtuVal').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'mtuVal').send_keys(randomMTU)
    afterEditingLANInterface['MTU'] = randomMTU

    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    LANInterfaceXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceLink')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, LANInterfaceXpath)))

@step('Review and commit the edited parameters for Edit LAN Interface')
def review_commit_LAN_Interface(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'LANInterfaceLink').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'Review_Commit').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'commitButton').click()
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))

@step('Validate LAN interface updates are shown on portal')
def validate_updated_lan_interface(context):
    global afterEditingLANInterface
    currentPage = GlobalVar.currentPage
    isMatched = False

    change_currentPage(context, 'CustomerDevice')
    navigate_deviceLink_filter_device(context)
    filter_and_select_device(context)
    change_currentPage(context, 'LANInterfaces')
    click_on_LAN_Interfaces(context)
    u_modeVal = context.baseReader.getElementByPropertyName(context, currentPage, 'modeVal').text
    # u_VLANsVal = context.baseReader.getElementByPropertyName(context, currentPage, 'VLANsVal').text
    u_mtuVal = context.baseReader.getElementByPropertyName(context, currentPage, 'mtuVal').get_attribute('value')

    if (afterEditingLANInterface.get('Mode') in u_modeVal) and (str(afterEditingLANInterface.get('MTU')) == str(u_mtuVal)):
       isMatched = True
    # and (afterEditingLANInterface.get('VLANs') == u_VLANsVal)
    assert isMatched == True
    time.sleep(20)


@step('Verify that selected network has no active sites')
def verify_active_sites(context):
    currentPage = GlobalVar.currentPage
    activeSites = context.baseReader.getElementByPropertyName(context, currentPage, 'activeSites').text
    assert activeSites == '0 devices'

@step('Validate network is removed on portal')
def validate_delete_network(context):
    currentPage = GlobalVar.currentPage
    networkDelete = context.csvRead[0].get('networkDelete')
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))

    context.driver.refresh()
    time.sleep(10)
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
    WebDriverWait(context.driver, 120).until(
        EC.invisibility_of_element_located((By.XPATH, noDataXpath)))
    time.sleep(5)
    filterNetworkObj = context.baseReader.getElementByPropertyName(context, currentPage, 'filterNetwork')
    WebDriverWait(context.driver, 20).until(EC.visibility_of((filterNetworkObj)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterNetwork').send_keys(networkDelete)
    deviceNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'networkVal')
    WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, deviceNameValueXpath), 'No data found'))


@step('I select "{option}" option and confirm')
def proceed_to_deactivate(context, option):
    currentPage = GlobalVar.currentPage
    time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, option).click()
    confirmDialogXpath = "//div[@class='modal-content']"
    yesXpath = "//button[text()='Yes']"
    WebDriverWait(context.driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, confirmDialogXpath)))
    # context.baseReader.getElementLocatorValue(context, currentPage, 'Yes')
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, yesXpath)))
    # context.baseReader.getElementByPropertyName(context, currentPage, 'Yes').click()
    context.driver.find_element_by_xpath(yesXpath).click()
    time.sleep(5)


@step('Click on the WAN Interfaces to open EDIT/VIEW WAN Interfaces')
def click_on_edit_WANInterface(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'wanInterfaceLink').click()
    time.sleep(5)

@step('Edit the WAN Interface by addressing type dhcp')
def edit_WANInterface_by_dhcp(context):
    global editWANInterface
    global firstInterfaceVal
    currentPage = GlobalVar.currentPage

    context.baseReader.getElementByPropertyName(context, currentPage, 'editInterface').send_keys(firstInterfaceVal)
    time.sleep(5)
    editXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'editWAN')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, editXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'editWAN').click()
    time.sleep(5)

    elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enabledState')
    flag = elementState.is_selected()
    if flag == False:
        context.baseReader.getElementByPropertyName(context, currentPage, 'enabledState').click()
    time.sleep(5)
    addType = context.baseReader.getElementByPropertyName(context, currentPage, 'addressingType').text
    if addType != 'Select addressType':
        addTypeVal = context.baseReader.getElementByPropertyName(context, currentPage, 'addressingTypeValue').text

        if 'dhcp' not in addTypeVal:
            time.sleep(10)
            context.baseReader.getElementByPropertyName(context, currentPage, 'addressingType').click()
            context.baseReader.getElementByPropertyName(context, currentPage, 'dhcpAddress').click()
        randomMTU = '1400'
        context.baseReader.getElementByPropertyName(context, currentPage, 'mtuWAN').clear()
        context.baseReader.getElementByPropertyName(context, currentPage, 'mtuWAN').send_keys(randomMTU)
        time.sleep(10)
        editWANInterface['Address_Type'] = 'dhcp'
        editWANInterface['MTU'] = randomMTU
    time.sleep(10)

    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'wanInterfaceLink').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'editInterface').send_keys(firstInterfaceVal)
    time.sleep(10)

@step('Review and commit the edited parameters for Edit WAN Interface by addressing type "{val}"')
def rc_edit_WAN(context, val):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'commitTab').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'commitButton').click()
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))
    time.sleep(5)

@step('Validate the updated parameter should be reflected on the portal for dhcp')
def validate_dhcp_updated_fields(context):
    global editWANInterface
    isMatched = False
    currentPage = GlobalVar.currentPage
    change_currentPage(context, 'CustomerDevice')
    navigate_deviceLink_filter_device(context)
    filter_and_select_device(context)
    change_currentPage(context, 'WANInterfaces')

    context.baseReader.getElementByPropertyName(context, currentPage, 'wanInterfaceLink').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'editInterface').send_keys(firstInterfaceVal)
    time.sleep(5)
    editXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'editWAN')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, editXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'editWAN').click()
    time.sleep(5)

    rc_addType = context.baseReader.getElementByPropertyName(context, currentPage, 'rc_addressingType').text
    rc_mtu = context.baseReader.getElementByPropertyName(context, currentPage, 'rc_MTU').get_attribute("value")


    if editWANInterface.get('Address_Type') in rc_addType and str(editWANInterface.get('MTU')) in str(rc_mtu):
        isMatched = True
    assert True == isMatched

@step('Edit the WAN Interface by addressing type static address')
def editWAN_by_staticAddress(context):
    global editWANInterface
    global firstInterfaceVal
    currentPage = GlobalVar.currentPage

    firstInterfaceVal = context.baseReader.getElementByPropertyName(context, currentPage, 'firstInterface').text
    context.baseReader.getElementByPropertyName(context, currentPage, 'editInterface').send_keys(firstInterfaceVal)
    time.sleep(5)
    editXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'editWAN')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, editXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'editWAN').click()
    time.sleep(5)

    elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enabledState')
    flag = elementState.is_selected()
    if flag == False:
        context.baseReader.getElementByPropertyName(context, currentPage, 'enabledState').click()
    time.sleep(5)
    addType = context.baseReader.getElementByPropertyName(context, currentPage, 'addressingType').text
    if addType != 'Select addressType':
        addTypeVal = context.baseReader.getElementByPropertyName(context, currentPage, 'addressingTypeValue').text
        time.sleep(10)
        if 'static-address' not in addTypeVal:
            context.baseReader.getElementByPropertyName(context, currentPage, 'addressingType').click()
            context.baseReader.getElementByPropertyName(context, currentPage, 'staticAddress').click()

        randomMTU = '1400' #random.randint(1000, 2500)
        context.baseReader.getElementByPropertyName(context, currentPage, 'mtuWAN').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'mtuWAN').clear()
        context.baseReader.getElementByPropertyName(context, currentPage, 'mtuWAN').send_keys(randomMTU)
        time.sleep(10)
        editWANInterface['MTU'] = randomMTU

        ip = ".".join(map(str, (random.randint(0, 150)
                                for _ in range(3))))
        ipslash = '.0' + '/' + '24'
        ip_address = str(ip) + str(ipslash)
        context.baseReader.getElementByPropertyName(context, currentPage, 'ipAddress').clear()
        context.baseReader.getElementByPropertyName(context, currentPage, 'ipAddress').send_keys(ip_address)
        editWANInterface['IP'] = ip_address

        gw = ".".join(map(str, (random.randint(0, 150)
                                for _ in range(1))))
        gateway = ip +'.'+ gw
        context.baseReader.getElementByPropertyName(context, currentPage, 'gateway').clear()
        context.baseReader.getElementByPropertyName(context, currentPage, 'gateway').send_keys(gateway)
        editWANInterface['Gateway'] = gateway

    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'wanInterfaceLink').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'editInterface').send_keys(firstInterfaceVal)
    time.sleep(10)

@step('Validate the updated parameter should be reflected on the portal for static Address')
def validate_updatedVal_pppoe(context):
    global editWANInterface
    isMatched = False
    currentPage = GlobalVar.currentPage
    # change_currentPage(context, 'CustomerDevice')
    # navigate_deviceLink_filter_device(context)
    # filter_and_select_device(context)
    # change_currentPage(context, 'WANInterfaces')

    context.baseReader.getElementByPropertyName(context, currentPage, 'wanInterfaceLink').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'editInterface').send_keys(firstInterfaceVal)
    time.sleep(10)
    editXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'editWAN')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, editXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'editWAN').click()

    rc_mtu = context.baseReader.getElementByPropertyName(context, currentPage, 'rc_MTU').get_attribute("value")
    rc_Gateway = context.baseReader.getElementByPropertyName(context, currentPage, 'rc_Gateway').get_attribute("value")
    rc_ipAddress = context.baseReader.getElementByPropertyName(context, currentPage, 'rc_ipAddress').get_attribute("value")

    if editWANInterface.get('Gateway') in rc_Gateway and str(editWANInterface.get('MTU')) in str(rc_mtu) and editWANInterface.get('IP') in rc_ipAddress:
        isMatched = True
    assert True == isMatched

@step('Edit the WAN Interface by addressing type pppoe')
def edit_WAN_pppoe(context):
    global editWANInterface
    currentPage = GlobalVar.currentPage

    context.baseReader.getElementByPropertyName(context, currentPage, 'editInterface').send_keys(firstInterfaceVal)
    time.sleep(5)
    editXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'editWAN')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, editXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'editWAN').click()
    time.sleep(5)

    elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enabledState')
    flag = elementState.is_selected()
    if flag == False:
        context.baseReader.getElementByPropertyName(context, currentPage, 'enabledState').click()
    time.sleep(5)
    addType = context.baseReader.getElementByPropertyName(context, currentPage, 'addressingType').text
    if addType != 'Select addressType':
        addTypeVal = context.baseReader.getElementByPropertyName(context, currentPage, 'addressingTypeValue').text
        time.sleep(10)
        if 'pppoe' not in addTypeVal:
            context.baseReader.getElementByPropertyName(context, currentPage, 'addressingType').click()
            context.baseReader.getElementByPropertyName(context, currentPage, 'pppoeAddress').click()

        randomMTU = '1400' #random.randint(1000, 2500)
        context.baseReader.getElementByPropertyName(context, currentPage, 'mtuWAN').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'mtuWAN').clear()
        context.baseReader.getElementByPropertyName(context, currentPage, 'mtuWAN').send_keys(randomMTU)
        time.sleep(10)
        editWANInterface['MTU'] = randomMTU

    letters = string.ascii_uppercase
    ranUser = ''.join(random.choice(letters) for i in range(5))
    u_ranUser = 'SDWAN-'+ranUser
    context.baseReader.getElementByPropertyName(context, currentPage, 'username').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'username').send_keys(u_ranUser)
    editWANInterface['Username'] = u_ranUser
    time.sleep(5)

    letters = string.ascii_uppercase
    ranPswd = ''.join(random.choice(letters) for i in range(4))
    u_ranPswd = 'SDWAN-' + ranPswd
    context.baseReader.getElementByPropertyName(context, currentPage, 'password').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'password').send_keys(u_ranPswd)
    editWANInterface['Password'] = u_ranPswd

    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'wanInterfaceLink').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'editInterface').send_keys(firstInterfaceVal)
    time.sleep(10)

@step('Validate the updated parameter should be reflected on the portal for pppoe')
def validate_updated_PPPOE(context):
    global editWANInterface
    isMatched = False
    global firstInterfaceVal
    currentPage = GlobalVar.currentPage
    # change_currentPage(context, 'CustomerDevice')
    # navigate_deviceLink_filter_device(context)
    # filter_and_select_device(context)
    # change_currentPage(context, 'WANInterfaces')
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'wanInterfaceLink').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'editInterface').send_keys(firstInterfaceVal)
    time.sleep(10)
    editXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'editWAN')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, editXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'editWAN').click()

    rc_mtu = context.baseReader.getElementByPropertyName(context, currentPage, 'rc_MTU').get_attribute("value")
    rc_Username = context.baseReader.getElementByPropertyName(context, currentPage, 'rc_Username').get_attribute("value")
    rc_Password = context.baseReader.getElementByPropertyName(context, currentPage, 'rc_Password').get_attribute("value")

    if editWANInterface.get('Username') in rc_Username and str(editWANInterface.get('MTU')) in str(rc_mtu) and editWANInterface.get(
            'Password') in rc_Password:
        isMatched = True

    assert True == isMatched


@step('I confirm "{action}" action')
def confirm_activate(context, action):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    page_title_assert(context, 'ActivateDevice', 'Activate Device')
    currentPage = GlobalVar.currentPage

    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, action).click()

@step('I navigate to the provided interface for "{value}" scenario')
def navigate_provided_interface(context, value):
    global currentInterface
    currentPage = GlobalVar.currentPage
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'LANInterfaceLink').click()
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'interfaceSearchField').click()
    time.sleep(10)
    if value == "access" or value == "DE_access" or value == "switch_AT":
        currentInterface = context.csvRead[0].get("GE1InterfaceValue")
    elif value == "DE_trunk" or value == "delete_vlan_GE2" or value == "switch_TA":
        currentInterface = context.csvRead[0].get("GE2InterfaceValue")
    elif value == "disable" or value == "switch_AD":
        currentInterface = context.csvRead[0].get("GE3InterfaceValue")
    elif value == "ED_access":
        currentInterface = context.csvRead[0].get("GE5InterfaceValue")
    elif value == "ED_trunk":
        currentInterface = context.csvRead[0].get("GE6InterfaceValue")

    context.baseReader.getElementByPropertyName(context, currentPage, 'interfaceSearchField').send_keys(currentInterface)
    time.sleep(5)
    editXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'edit')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, editXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'edit').click()
    time.sleep(5)

@step('Disable the selected Interface')
def disable_GE3_Interface(context):
    currentPage = GlobalVar.currentPage
    elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enableState')
    flag = elementState.is_selected()
    if flag == True:
        context.baseReader.getElementByPropertyName(context, currentPage, 'enableState').click()
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    LANInterfaceXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceLink')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, LANInterfaceXpath)))

@step('Review and commit the "{value}" interface')
def review_commit_disabled_interface(context, value):
    currentPage = GlobalVar.currentPage
    global currentInterface
    context.baseReader.getElementByPropertyName(context, currentPage, 'LANInterfaceLink').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'interfaceSearchField').click()
    time.sleep(10)

    if value == "disable":
        currentInterface = context.csvRead[0].get("GE3InterfaceValue")
    if value == "access":
        currentInterface = context.csvRead[0].get("GE1InterfaceValue")

    context.baseReader.getElementByPropertyName(context, currentPage, 'interfaceSearchField').send_keys(currentInterface)
    time.sleep(5)

    context.baseReader.getElementByPropertyName(context, currentPage, 'Review_Commit').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'commitButton').click()
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))
    time.sleep(10)

@step('Fill the required parameter to add a VLAN under "{value}" Interface')
def required_paramters_for_any_Interface(context, value):
    global vlan
    global vlan_name
    currentPage = GlobalVar.currentPage

    N = 5
    vlan['VLANName'] = 'BH-SDWAN_GE-' + str(
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANname').send_keys(vlan['VLANName'])
    vlan_name = vlan['VLANName']

    N = 3
    newVlanId = str(''.join(random.choices(string.digits, k=N)))
    # print(vlan['vlanid'])
    # if newVlanId != vlan['vlanid']:
    vlan['vlanid'] = newVlanId

    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANid').send_keys(vlan['vlanid'])
    WebDriverWait(context.driver, 20).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[@class='loader-bg']")))

    context.baseReader.getElementByPropertyName(context, currentPage, 'VPNDropdown').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'VPNValue').click()
    # vpnListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'VPNDropdownList')
    # vpnList = context.driver.find_elements(By.XPATH, vpnListXpath)
    # for i in range (0, len(vpnList)):
    #     if vpnList[i].text == context.csvRead[0].get('initialNetworkName'):
    #         vpnList[i].click() VPNValue

    context.baseReader.getElementByPropertyName(context, currentPage, 'LanInterfaceDropdown').click()
    if value == "GE1":
        context.baseReader.getElementByPropertyName(context, currentPage, 'LanInterfaceValue').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'LanInterfaceDropdown2').click()
    if value == "GE2":
        context.baseReader.getElementByPropertyName(context, currentPage, 'GE2LanInterface').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'LanInterfaceGE2').click()
    if value == "GE3":
        context.baseReader.getElementByPropertyName(context, currentPage, 'GE3LanInterface').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'LanInterfaceGE3').click()
    if value == "GE6":
        context.baseReader.getElementByPropertyName(context, currentPage, 'GE6LanInterface').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'LanInterfaceGE6').click()
    # ip = ".".join(map(str, (random.randint(0, 255)
    #                         for _ in range(3))))
    # ip = '128.4.5'
    # ipslash = '/' + str(''.join(random.choices(string.digits, k=N)))
    # vlan['network'] = str(ip) + '.1/24' #str(ipslash)

    ip = ".".join(map(str, (random.randint(0, 150)
                            for _ in range(3))))
    ipslash = '.0' + '/' + '24'
    ip_address = str(ip) + str(ipslash)
    vlan['network'] = ip_address

    gw = ".".join(map(str, (random.randint(0, 150)
                            for _ in range(1))))
    gateway = ip + '.' + gw

    context.baseReader.getElementByPropertyName(context, currentPage, 'Network').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'Network').send_keys(vlan['network'])

    context.baseReader.getElementByPropertyName(context, currentPage, 'LeaseTimeDropdown').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'LeaseTimeValue').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'LeaseTimeDropdown2').click()

    # gateway = ".".join(map(str, (random.randint(0, 255)
    #                              for _ in range(4))))
    # vlan['gateway'] = str(ip) + '.2'

    gw = ".".join(map(str, (random.randint(0, 150)
                            for _ in range(1))))
    gateway = ip + '.' + gw
    vlan['gateway'] = gateway

    context.baseReader.getElementByPropertyName(context, currentPage, 'Gateway').send_keys(vlan['gateway'])
    context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPType').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPValue').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPType2').click()

    vlan['DHCPstart'] = str(ip) + '.2'
    vlan['DHCPend'] = str(ip) + '.4'

    context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPstart').send_keys(vlan['DHCPstart'])
    context.baseReader.getElementByPropertyName(context, currentPage, 'DHCPend').send_keys(vlan['DHCPend'])
    context.baseReader.getElementByPropertyName(context, currentPage, 'Save').click()

@step('Validate the state of selected Interface')
def validate_state_Selected_Interface(context):
    currentPage = GlobalVar.currentPage
    elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enableState')
    flag = elementState.is_selected()
    if flag == False:
        context.baseReader.getElementByPropertyName(context, currentPage, 'enableState').click()
    time.sleep(10)
    mode = context.baseReader.getElementByPropertyName(context, currentPage, 'modeVal').text
    modeUpdated = mode.split(' ')
    if 'trunk' in modeUpdated:
        time.sleep(10)
        context.baseReader.getElementByPropertyName(context, currentPage, 'modeDropdown').click()
        time.sleep(5)
        context.baseReader.getElementByPropertyName(context, currentPage, 'accessMode').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    LANInterfaceXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceLink')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, LANInterfaceXpath)))

@step('Navigate to the Devices Link and filter a device of "{value}" model')
def filter_E610_model_device(context, value):
    currentPage = GlobalVar.currentPage
    global deviceAdded
    deviceAdded = context.csvRead[0].get('E610Device')
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'devicesURL').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(deviceAdded)
    time.sleep(5)

@step('Enable an disabled interface and map it to a access mode')
def enable_an_disabled_interface_for_editLAN_access(context):
    currentPage = GlobalVar.currentPage
    global interfaceState
    elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enableState')
    flag = elementState.is_selected()
    if flag == False:
        context.baseReader.getElementByPropertyName(context, currentPage, 'enableState').click()
        interfaceState = "enable"
    modeValue = context.baseReader.getElementByPropertyName(context, currentPage, 'modeVal').text
    modeUpdated = modeValue.split(' ')
    if 'access' not in modeUpdated:
        context.baseReader.getElementByPropertyName(context, currentPage, 'modeDropdown').click()
        time.sleep(5)
        context.baseReader.getElementByPropertyName(context, currentPage, 'accessMode').click()
        time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    LANInterfaceXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceLink')
    WebDriverWait(context.driver, 60).until(EC.visibility_of_element_located((By.XPATH, LANInterfaceXpath)))
    time.sleep(5)

@step('Review and commit for "{value}" interface')
def review_edit_Interface(context, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'LANInterfaceLink').click()
    time.sleep(5)
    if value == "DE_access" or value == "switch_AT":
        currentInterface = context.csvRead[0].get("GE1InterfaceValue")
    elif value == "switch_TA" or value == "delete_vlan_GE2" or value == "DE_trunk":
        currentInterface = context.csvRead[0].get("GE2InterfaceValue")
    elif value == "ED_access":
        currentInterface = context.csvRead[0].get("GE5InterfaceValue")
    elif value == "ED_trunk":
        currentInterface = context.csvRead[0].get("GE6InterfaceValue")
    elif value == "switch_AD":
        currentInterface = context.csvRead[0].get("GE3InterfaceValue")
    context.baseReader.getElementByPropertyName(context, currentPage, 'interfaceSearchField').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'interfaceSearchField').send_keys(currentInterface)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Review_Commit').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'commitButton').click()
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))

@step('Interface should go back to its previous state for "{value}"')
def cleanup_for_ED_LANInterface(context, value):
    currentPage = GlobalVar.currentPage
    navigate_provided_interface(context, value)
    time.sleep(5)
    if value == "switch_AT" or value == "DE_access" or value == "DE_trunk":
        elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enableState')
        flag = elementState.is_selected()
        if flag == False:
            context.baseReader.getElementByPropertyName(context, currentPage, 'enableState').click()
            modeValue = context.baseReader.getElementByPropertyName(context, currentPage, 'modeVal').text
            modeUpdated = modeValue.split(' ')
            if 'access' not in modeUpdated:
                context.baseReader.getElementByPropertyName(context, currentPage, 'modeDropdown').click()
                time.sleep(5)
                context.baseReader.getElementByPropertyName(context, currentPage, 'accessMode').click()
                time.sleep(10)
    elif value == "ED_access" or value == "ED_trunk":
        elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enableState')
        flag = elementState.is_selected()
        if flag != False:
            context.baseReader.getElementByPropertyName(context, currentPage, 'enableState').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(40)
    # review_edit_Interface(context, value)

@step('Add a VLAN under "{value}" Interface')
def add_vlan_under_any_GE_Interface(context, value):
    change_currentPage(context, "DeviceConfig")
    click_button(context, "VLANs")
    click_button(context, "addVLAN")
    page_title_assert(context, "AddVLAN", "Add VLAN")
    required_paramters_for_any_Interface(context, value)
    navigate_to_commit(context)
    page_title_assert(context, "VLANReview", "Review and Commit")
    click_button(context, "Commit")
    validate_add_VLAN(context)

@step('Validate the mode and added VLAN under this GE6 Interface')
def validate_Added_Vlan_under_GE6_Interface(context):
    currentPage= GlobalVar.currentPage
    global interfaceState
    change_currentPage(context, "LANInterfaces")
    navigate_provided_interface(context, "ED_trunk")
    currentPage = GlobalVar.currentPage
    elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enableState')
    flag = elementState.is_selected()
    if flag == False:
        context.baseReader.getElementByPropertyName(context, currentPage, 'enableState').click()
        modeValue = context.baseReader.getElementByPropertyName(context, currentPage, 'modeVal').text
        interfaceState = "enable"
        modeUpdated = modeValue.split(' ')
        if 'trunk' not in modeUpdated:
            context.baseReader.getElementByPropertyName(context, currentPage, 'modeDropdown').click()
            context.baseReader.getElementByPropertyName(context, currentPage, 'trunkVal').click()
            time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    LANInterfaceXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceLink')
    WebDriverWait(context.driver, 60).until(EC.visibility_of_element_located((By.XPATH, LANInterfaceXpath)))
    time.sleep(5)
    review_edit_Interface(context, "ED_trunk")

@step('Disable an enable interface and map it to a access mode')
def disable_an_enable_interface_for_editLAN_access(context):
    currentPage = GlobalVar.currentPage
    global interfaceState
    elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enableState')
    flag = elementState.is_selected()
    if flag == True:
        # context.baseReader.getElementByPropertyName(context, currentPage, 'VLANsDropdown').click()
        # time.sleep(5)
        # context.baseReader.getElementByPropertyName(context, currentPage, 'corporateDropdownVal').click()
        # time.sleep(5)
        modeValue = context.baseReader.getElementByPropertyName(context, currentPage, 'modeVal').text
        interfaceState = "enable"
        modeUpdated = modeValue.split(' ')
        if 'access' not in modeUpdated:
            context.baseReader.getElementByPropertyName(context, currentPage, 'modeDropdown').click()
            time.sleep(5)
            context.baseReader.getElementByPropertyName(context, currentPage, 'accessMode').click()
            time.sleep(10)
        context.baseReader.getElementByPropertyName(context, currentPage, 'enableState').click()
        modeValue = context.baseReader.getElementByPropertyName(context, currentPage, 'modeVal').text
        interfaceState = "enable"
        modeUpdated = modeValue.split(' ')
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    LANInterfaceXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceLink')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, LANInterfaceXpath)))
    time.sleep(5)

@step('Disable an enable interface and map it to a trunk mode')
def disable_an_enable_interface_for_editLAN_trunk(context):
    currentPage = GlobalVar.currentPage
    global interfaceState
    elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enableState')
    flag = elementState.is_selected()
    if flag == True:
        modeValue = context.baseReader.getElementByPropertyName(context, currentPage, 'modeVal').text
        interfaceState = "enable"
        modeUpdated = modeValue.split(' ')
        if 'trunk' not in modeUpdated:
            context.baseReader.getElementByPropertyName(context, currentPage, 'modeDropdown').click()
            time.sleep(5)
            context.baseReader.getElementByPropertyName(context, currentPage, 'trunkVal').click()
            time.sleep(10)
        context.baseReader.getElementByPropertyName(context, currentPage, 'enableState').click()
        modeValue = context.baseReader.getElementByPropertyName(context, currentPage, 'modeVal').text
        interfaceState = "enable"
        modeUpdated = modeValue.split(' ')
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    LANInterfaceXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceLink')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, LANInterfaceXpath)))
    time.sleep(5)

@step('Validate the selected Interface for switching the mode from access to trunk')
def validate_interface_for_switching_access_to_trunk(context):
    currentPage = GlobalVar.currentPage
    global interfaceState
    elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enableState')
    flag = elementState.is_selected()
    if flag == False:
        context.baseReader.getElementByPropertyName(context, currentPage, 'enableState').click()
        interfaceState = "enable"
    modeValue = context.baseReader.getElementByPropertyName(context, currentPage, 'modeVal').text
    modeUpdated = modeValue.split(' ')
    if 'access' not in modeUpdated:
        context.baseReader.getElementByPropertyName(context, currentPage, 'modeDropdown').click()
        time.sleep(10)
        context.baseReader.getElementByPropertyName(context, currentPage, 'accessMode').click()
        time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    LANInterfaceXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceLink')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, LANInterfaceXpath)))
    time.sleep(5)

@step('Validate the mode and added VLAN under this GE1 Interface')
def validate_added_Vlan_under_selected_interface(context):
    currentPage = GlobalVar.currentPage
    global interfaceState
    change_currentPage(context, "LANInterfaces")
    navigate_provided_interface(context, "switch_AT")
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    LANInterfaceXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceLink')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, LANInterfaceXpath)))
    time.sleep(5)
    review_edit_Interface(context, "switch_AT")

@step('Validate the selected Interface for switching the mode from trunk to access')
def validate_Selected_Interface_trunk_access(context):
    currentPage = GlobalVar.currentPage
    global interfaceState
    elementState = context.baseReader.getElementByPropertyName(context, currentPage, 'enableState')
    flag = elementState.is_selected()
    if flag == False:
        context.baseReader.getElementByPropertyName(context, currentPage, 'enableState').click()
        interfaceState = "enable"
    modeValue = context.baseReader.getElementByPropertyName(context, currentPage, 'modeVal').text
    modeUpdated = modeValue.split(' ')
    if 'access' not in modeUpdated:
        context.baseReader.getElementByPropertyName(context, currentPage, 'modeDropdown').click()
        time.sleep(5)
        context.baseReader.getElementByPropertyName(context, currentPage, 'accessMode').click()
        time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    LANInterfaceXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceLink')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, LANInterfaceXpath)))
    time.sleep(5)

@step('Validate the mode and added VLAN under this GE2 Interface')
def validate_added_vlan_under_GE2_Interface(context):
    currentPage = GlobalVar.currentPage
    global interfaceState
    change_currentPage(context, "LANInterfaces")
    navigate_provided_interface(context, "switch_TA")
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    LANInterfaceXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceLink')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, LANInterfaceXpath)))
    time.sleep(5)
    review_edit_Interface(context, "switch_TA")


@step('I Navigate to the Devices Link and filter a device for Delete VLAN Scenerio')
def delete_Device_for_VLAN(context):
    currentPage = GlobalVar.currentPage
    global deleteDevice
    if Device == {}:
        deleteDevice = context.csvRead[0].get('DEL_VLAN_Device')
    else:
        deleteDevice = Device.get('Device_Name')

    time.sleep(30)
    context.baseReader.getElementByPropertyName(context, currentPage, 'devicesURL').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(deleteDevice)
    time.sleep(5)

@step('Validate the delete VLAN mapped to multiple interface')
def delete_vlan_mapped_to_one_interface(context):
    currentPage = GlobalVar.currentPage
    global interfaceState
    modeValue = context.baseReader.getElementByPropertyName(context, currentPage, 'modeVal').text
    modeUpdated = modeValue.split(' ')
    if 'access' in modeUpdated:
        context.baseReader.getElementByPropertyName(context, currentPage, 'modeDropdown').click()
        time.sleep(5)
        context.baseReader.getElementByPropertyName(context, currentPage, 'trunkVal').click()
        time.sleep(5)
    all_vlans = context.baseReader.getElementByPropertyName(context, currentPage, 'allVlans').text
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'allVlans').click()
    time.sleep(5)
    allDropdownValXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'allDropdownVal')
    vlanList = context.driver.find_elements(By.XPATH, allDropdownValXpath)
    for i in range(0, len(vlanList)):
        if vlanList[i].text == vlan_name:
            # print(vlanList[i])
            vlanList[i].click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    LANInterfaceXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceLink')
    WebDriverWait(context.driver, 60).until(EC.visibility_of_element_located((By.XPATH, LANInterfaceXpath)))
    time.sleep(5)

@step('Delete the VLAN mapped to multiple Interface')
def delete_vlan_to_multiple_Interface(context):
    currentPage = GlobalVar.currentPage
    global vlans_list
    global endList
    global vlan_name
    global myList
    allVlansFromLANInterface = []
    change_currentPage(context, "LANInterfaces")
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'LANInterfaceLink').click()
    time.sleep(5)
    allVLANsFromTableXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'allVLANsFromTable')
    vlanList = context.driver.find_elements(By.XPATH, allVLANsFromTableXpath)
    time.sleep(5)
    for i in range(0, len(vlanList)):
        allVlansFromLANInterface.append(vlanList[i].text)
    for i in range(0, len(allVlansFromLANInterface)):
        currentVal = allVlansFromLANInterface[i]
        if 'Corporate' != currentVal:
            myList = currentVal.split('\n')
            for j in range(0, len(myList)):
                endList.append(myList[j])
    endList.sort()
    for i in range(0, len(endList)):
        if endList[i] == endList[i+1]:
            vlan_name = endList[i]
            break
    time.sleep(5)
    change_currentPage(context, "DeviceConfig")
    currentPage = GlobalVar.currentPage
    click_button(context, "VLANs")
    time.sleep(5)
    change_currentPage(context, "DeviceConfig")
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'vlanNameSearch').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'vlanNameSearch').send_keys(vlan_name)
    firstvlanName_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'firstvlanName')
    WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, firstvlanName_xpath), vlan_name))
    context.baseReader.getElementByPropertyName(context, currentPage, 'deleteVlanIcon').click()
    deleteVlanYes_Xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deleteVlanYes')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, deleteVlanYes_Xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'deleteVlanYes').click()
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))

@step('Delete the VLAN mapped to one Interface')
def Delete_vlan_mapped_one_interface(context):
    global vlans_list
    global endList
    global vlan_name
    global myList
    allVlansFromLANInterface = []
    change_currentPage(context, "LANInterfaces")
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'LANInterfaceLink').click()
    time.sleep(5)
    allVLANsFromTableXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'allVLANsFromTable')
    vlanList = context.driver.find_elements(By.XPATH, allVLANsFromTableXpath)
    time.sleep(5)
    for i in range(0, len(vlanList)):
        allVlansFromLANInterface.append(vlanList[i].text)
    for i in range(0, len(allVlansFromLANInterface)):
        currentVal = allVlansFromLANInterface[i]
        if 'Corporate' != currentVal:
            myList = currentVal.split('\n')
            for j in range(0, len(myList)):
                endList.append(myList[j])
    endList.sort()
    endList = set(endList)
    for val in endList:
        if val != "Corporate":
            vlan_name = val
    time.sleep(5)
    change_currentPage(context, "DeviceConfig")
    currentPage = GlobalVar.currentPage
    click_button(context, "VLANs")
    time.sleep(5)
    change_currentPage(context, "DeviceConfig")
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'vlanNameSearch').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'vlanNameSearch').send_keys(vlan_name)
    firstvlanName_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'firstvlanName')
    WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, firstvlanName_xpath), vlan_name))
    context.baseReader.getElementByPropertyName(context, currentPage, 'deleteVlanIcon').click()
    deleteVlanYes_Xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deleteVlanYes')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, deleteVlanYes_Xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'deleteVlanYes').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'vlanNameSearch').clear()
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))

@step('Edit attributes of Vlan mapped to only "{value}" interface')
def edit_attribute_vlan_mapped_one_interface(context, value):
    global vlans_list
    global endList
    global vlan_name
    global myList
    allVlansFromLANInterface = []
    change_currentPage(context, "LANInterfaces")
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'LANInterfaceLink').click()
    time.sleep(5)
    allVLANsFromTableXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'allVLANsFromTable')
    vlanList = context.driver.find_elements(By.XPATH, allVLANsFromTableXpath)
    time.sleep(5)
    for i in range(0, len(vlanList)):
        allVlansFromLANInterface.append(vlanList[i].text)
    for i in range(0, len(allVlansFromLANInterface)):
        if 'Corporate' != allVlansFromLANInterface[i]:
            interfaceList = allVlansFromLANInterface[i].split('\n')
            myList = myList + interfaceList

    if value == "one":
        endList = set(myList)
        for val in endList:
            if val != "Corporate":
                vlan_name = val


    if value == "multiple":
        for i in range(0, len(myList)):
            for j in range(i+1, len(myList)):
                if myList[i] == myList[j]:
                    if myList[i] != "Corporate":
                        vlan_name = myList[i]
                        break
    time.sleep(5)
    change_currentPage(context, "DeviceConfig")

    currentPage = GlobalVar.currentPage
    click_button(context, "VLANs")

    time.sleep(5)
    change_currentPage(context, "DeviceConfig")
    currentPage = GlobalVar.currentPage
    time.sleep(5)

    context.baseReader.getElementByPropertyName(context, currentPage, 'vlanNameSearch').click()
    context.baseReader.getElementByPropertyName(context,currentPage, 'vlanNameSearch').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'vlanNameSearch').send_keys(vlan_name)

    firstvlanName_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'firstvlanName')
    WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, firstvlanName_xpath), vlan_name))
    context.baseReader.getElementByPropertyName(context, currentPage, 'editFirstVLAN').click()
    change_currentPage(context, "EditVLAN")

    currentPage = GlobalVar.currentPage
    edit_vlan_parameter_for_one_interface(context)

    page_title_assert(context, 'VLANReview', 'Review and Commit')
    currentPage = GlobalVar.currentPage

    click_button(context, 'Commit')
    currentPage = GlobalVar.currentPage

    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))


@step('Edit some VLAN parameters for one/multiple interface')
def edit_vlan_parameter_for_one_interface(context):
    global vlan_name
    global vlan
    currentPage = GlobalVar.currentPage

    N = 5
    vlan['VLANName'] = 'BHSDWAN-VLAN-U' + str(
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=N)))

    nameObj = context.baseReader.getElementByPropertyName(context, currentPage, 'VLANname')
    nameObj.clear()
    nameObj.send_keys(vlan['VLANName'])
    vlan_name = vlan['VLANName']

    time.sleep(15)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Save').click()

    loadingAfterSaveXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'loadingAfterSave')
    WebDriverWait(context.driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, loadingAfterSaveXpath)))

    VLANsURLxpath = context.baseReader.getElementLocatorValue(context, currentPage, 'VLANsURL')
    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, VLANsURLxpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANsURL').click()
    time.sleep(5)

    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANsSearchField').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANsSearchField').send_keys(vlan_name)

    Review_commit_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Review_commit')
    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, Review_commit_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'Review_commit').click()


@step('Validate updated values for Vlan that mapped to only one/multiple interface')
def validate_the_updated_Vlan_mapped_one_interface(context):

    change_currentPage(context, "EditVLAN")
    currentPage = GlobalVar.currentPage

    loadingAfterSaveXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'loadingAfterSave')
    WebDriverWait(context.driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, loadingAfterSaveXpath)))

    VLANsURLxpath = context.baseReader.getElementLocatorValue(context, currentPage, 'VLANsURL')
    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, VLANsURLxpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANsURL').click()
    time.sleep(5)

    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANsSearchField').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'VLANsSearchField').send_keys(vlan_name)
    time.sleep(20)

@step('Switch an access mode interface to a different VLAN for access mode')
def switch_access_mode_to_different_VLAN_for_access(context):
    currentPage = GlobalVar.currentPage
    navigate_provided_interface(context, "switch_AD")
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'modeDropdown').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'accessMode').click()
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'allVlans').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'corporateDropdownVal').click()
    time.sleep(5)
    allDropdownValXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'allDropdownVal')
    vlanList = context.driver.find_elements(By.XPATH, allDropdownValXpath)
    for i in range(0, len(vlanList)):
        if vlanList[i].text == vlan_name:
            print(vlanList[i].text)
            vlanList[i].click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'saveButton').click()
    time.sleep(10)
    LANInterfaceXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'LANInterfaceLink')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, LANInterfaceXpath)))
    time.sleep(5)
    review_edit_Interface(context, "switch_AD")


@step('Validate that activation email is sent to the user')
def validate_activation(context):
    currentPage = GlobalVar.currentPage
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))
    time.sleep(2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'devices').click()
    page_title_assert(context, 'CustomerDevice', 'Devices')
    currentPage = GlobalVar.currentPage
    time.sleep(3)
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(
        deviceAdded)
    deviceNameValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceVal')
    WebDriverWait(context.driver, 50).until(
        EC.text_to_be_present_in_element((By.XPATH, deviceNameValueXpath), deviceAdded))
    time.sleep(5)
    adminState = context.baseReader.getElementByPropertyName(context, currentPage, 'adminState').text
    assert adminState == 'pending'

@step('Validate that device status should be "{status1}" or "{status2}"')
def validate_device_status(context, status1, status2):
    currentPage = GlobalVar.currentPage
    time.sleep(2)
    adminState = context.baseReader.getElementByPropertyName(context, currentPage, 'adminState').text
    assert adminState == status1 or status2

@step('Delete an added VLAN for Edit VLAN Scenerio')
def delete_VLAN_for_Edit_VLAN(context):
    change_currentPage(context, "DeviceConfig")
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'deleteVlanIcon').click()
    deleteVlanYes_Xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deleteVlanYes')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, deleteVlanYes_Xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'deleteVlanYes').click()
    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))
    time.sleep(10)

@step('I Navigate to the Devices Link and filter a device for edit LAN Interface')
def filter_device_for_edit_LAN(context):
    global deviceAdded
    global deviceForEditLan
    currentPage = GlobalVar.currentPage

    if deviceForEditLan == {}:
        deviceAdded = context.csvRead[0].get('deviceForEditLan')
    else:
        deviceAdded = deviceForEditLan.get('Device_Name')
    time.sleep(10)
    WebDriverWait(context.driver, 20).until(
        EC.invisibility_of_element_located((By.XPATH, "//*[@class='loader-bg']")))
    context.baseReader.getElementByPropertyName(context, currentPage, 'devicesURL').click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevice').send_keys(deviceAdded)
    time.sleep(5)

@step('filter and delete the last added VLAN for edit LAN Interface')
def filter_and_delete_vlan_for_edit_lan(context):
    global vlan
    change_currentPage(context, "DeviceConfig")
    currentPage = GlobalVar.currentPage
    vlanName = vlan.get("VLANName")
    click_button(context, "VLANs")
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'filterVLAN').send_keys(vlanName)
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'deleteVlanIcon').click()

    deleteVlanYes_Xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deleteVlanYes')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, deleteVlanYes_Xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'deleteVlanYes').click()

    alertXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, alertXpath)))
    time.sleep(10)


@step('Fill the required parameters for Device activation')
def fill_required_paramters_device_Activation(context):
    global new_final_time

    currentPage = GlobalVar.currentPage

    context.baseReader.getElementByPropertyName(context, currentPage, 'siteContactName').clear()
    name = 'BHSDWAN ' + str(''.join(random.choices(string.ascii_letters + string.digits, k=4)))
    email = context.csvRead[0].get('FROM_EMAIL')+'@gmail.com'


    context.baseReader.getElementByPropertyName(context, currentPage, 'siteContactName').send_keys(name)
    # siteContactNameXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'siteContactName')
    # WebDriverWait(context.driver, 10).until(
    #     EC.text_to_be_present_in_element((By.XPATH, siteContactNameXpath), name))

    context.baseReader.getElementByPropertyName(context, currentPage, 'siteContactEmail').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'siteContactEmail').send_keys(email)
    # siteContactEmailXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'siteContactEmail')
    # WebDriverWait(context.driver, 10).until(
    #     EC.text_to_be_present_in_element((By.XPATH, siteContactEmailXpath), email))
    confirm_activate(context, "Activate")
    time.sleep(15)

@step('Validate that activation email is sent to the test account')
def read_email_from_gmail(context):
    from_email = context.csvRead[0].get('FROM_EMAIL')
    password = context.csvRead[0].get('FROM_PWD')
    sender_email = context.csvRead[0].get('sender')
    mail_subject = context.csvRead[0].get('subject')
    status = validate_last_email(context, from_email, password, sender_email, mail_subject)
    assert status == "success"


@step('Navigate view by clicking on "{value}"')
def click_on_the_element(context, value):
    currentPage = GlobalVar.currentPage
    element = context.baseReader.getElementByPropertyName(context, currentPage, value)
    context.driver.execute_script("arguments[0].click();", element)
    time.sleep(5)


@step('I filter and select corporate VLAN for initial setup')
def filter_customer(context):
    currentPage = GlobalVar.currentPage
    if vlan == {}:
        editVLANname = 'Corporate'

    else:
        editVLANname = vlan['VLANName']

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterVLAN').send_keys(editVLANname)
    VLANValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'VLANValue')
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, VLANValueXpath), editVLANname))
