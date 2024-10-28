import datetime
import os
import random
import string
import sys

from reportportal_behave.reportportal_service import logger
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

from features.steps.globalVar import GlobalVar
from features.steps.ui_steps_general import page_title_validation, change_currentPage

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

# declared Variables
currentPage = None
addBrownfieldJob = None
emailGroupName = None
new_email_val = None
new_group_name = None
cust_grp_name = None
dev_grp_name = None
addCustomer = {}
manageCustomer = None
addDevice = {}
addAuditJob = {}
tags = {}
runRemediateJob = {}
auditReportSummary = None
email_list = []
logging_param_val = None
router_param_val = None
del_group_val = None
schedule_job_name = None
job_runtime = None
customer = {}
deviceName = None
count  = 0
auth_Group = None
device_logging_config = None
parallelJobs = {}
jobEndTime = {}
# End of declared Variables


@step('I should land on Login page')
def step_impl(context):
    url = 'lcdURL_' + sys.argv[2]
    context.driver.get(context.config.get(url))


@step('I should land on Home page')
def step_impl(context):
    url = sys.argv[1] + 'URL_' + sys.argv[2]
    context.driver.get(context.config.get(url))
    currentPage = context.csvRead[0].get('initialCurrentPage')
    time.sleep(5)
    if (context.driver.title == 'Log in to TINAA Platform'):
        username = os.getenv('TestUserName')
        password = os.getenv('TestUserPass')
        context.baseReader.getElementByPropertyName(context, currentPage, 'UserName').send_keys(username)
        context.baseReader.getElementByPropertyName(context, currentPage, 'Password').send_keys(password)
        context.baseReader.getElementByPropertyName(context, currentPage, 'LoginButton').click()
        headingXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'headingTitle')
        WebDriverWait(context.driver, 35).until(
            EC.visibility_of_element_located((By.XPATH, headingXpath)), message='Element not visible')


@step('I navigate view by clicking on "{value}"')
def navigate_to_nextPage(context, value):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    element = context.baseReader.getElementByPropertyName(context, currentPage, value)
    context.driver.execute_script("arguments[0].click();", element)
    time.sleep(3)
    print('Current page')
    print(currentPage)
    print('Current page')

@step('I click on "{item}" button and fill customer details')
def fill_customer_details(context, item):
    global addCustomer
    currentPage = GlobalVar.currentPage
    addCustomerName = context.csvRead[0].get("addCustomerName")
    authCisco = context.csvRead[0].get("authCisco")
    current_time = datetime.datetime.now()
    addCustomer['name'] = addCustomerName + '_' + str(current_time).replace('.', ':')
    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerName').send_keys(addCustomer['name'])

    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerRegion').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerRegionVal').click()

    addCustomer['Customer_Region'] = context.baseReader.getElementByPropertyName(
        context, currentPage, 'CustomerRegionVal').text

    context.baseReader.getElementByPropertyName(context, currentPage, 'TelusWideExpression').click()
    addCustomer['deviceRegularExpression'] = context.baseReader.getElementByPropertyName(
        context, currentPage, 'TelusWideExpression').text

    context.baseReader.getElementByPropertyName(context, currentPage, 'NewAuthgroup').click()
    addCustomer['authGroup'] = addCustomer['name']

    context.baseReader.getElementByPropertyName(context, currentPage, 'AuthgroupUsername').send_keys(authCisco)

    context.baseReader.getElementByPropertyName(context, currentPage, 'AuthgroupPassword').send_keys(authCisco)

    context.baseReader.getElementByPropertyName(context, currentPage, 'AuthgroupSecret').send_keys(authCisco)


@step('Customer name should be displayed in the list of customers with details shown as chosen')
def serach_by_name(context):
    isMatched = False
    currentPage = GlobalVar.currentPage
    addCustomerWait = context.baseReader.readElementByPropertyName(currentPage, 'addingCustomerWait').get("value")
    WebDriverWait(context.driver, 35).until(EC.invisibility_of_element_located((By.XPATH, addCustomerWait)))

    searchObj = context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar')
    searchObj.clear()
    searchObj.send_keys(addCustomer['name'])
    rowsXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'rows')
    rowSize = context.driver.find_elements(By.XPATH, rowsXpath)
    for i in range(0, len(rowSize)):
        cust_name = context.driver.find_element_by_xpath('//table/tbody/tr[' + str(i + 1) + ']//td[1]').text
        if cust_name == addCustomer['name']:
            region = context.baseReader.getElementByPropertyName(context, currentPage, 'region').text
            authGroup = context.baseReader.getElementByPropertyName(context, currentPage, 'authGroup').text
            deviceRegularExpression = context.baseReader.getElementByPropertyName(
                context, currentPage, 'deviceRegularExpression').text                                                         
            device_expression = context.csvRead[0].get("device_expression")
            if ((region == addCustomer['Customer_Region']) and (
                    deviceRegularExpression == device_expression) and (
                    authGroup == addCustomer['authGroup'])):
                isMatched = True
    assert isMatched == True


@step('Search customer by name')
def search_filter(context):
    global manageCustomer
    global count
    global auth_Group
    currentPage = GlobalVar.currentPage
    if addCustomer == {}:
        filterCustomerByName = context.csvRead[0].get("filterCustomerByName")
    else:
        filterCustomerByName = addCustomer['name']

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterData').send_keys(filterCustomerByName)
    cust_name = context.driver.find_element_by_xpath('//table/tbody/tr[1]//td[1]').text
    if count == 0:
       auth_Group = context.driver.find_element_by_xpath('//table/tbody/tr[1]//td[3]').text
       count=+1
    if cust_name != 'No data found':
        searchObj = context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar')
        searchObj.clear()
        manageCustomer = cust_name
        searchObj.send_keys(cust_name)


@step('Open Edit Customer form by clicking on Edit button')
def edit_customer_view(context):
    currentPage = GlobalVar.currentPage
    rowSize = context.driver.find_elements(By.XPATH, '//table/tbody/tr')
    for i in range(0, len(rowSize)):
        cusName = context.driver.find_element_by_xpath('//table/tbody/tr[' + str(i + 1) + ']//td[1]').text
        if cusName == manageCustomer:
            context.driver.find_element_by_xpath('//table/tbody/tr[' + str(i + 1) + ']/td[5]/button[1]').click()
    try:
        editCustomerNameWait = context.baseReader.readElementByPropertyName(currentPage, 'editCustomerName').get(
            "value")
        WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, editCustomerNameWait)))

    except:
        time.sleep(5)
        commitPopup = context.baseReader.getElementLocatorValue(context, currentPage, 'commitPopup')
        WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, commitPopup)))
        context.baseReader.getElementByPropertyName(context, currentPage, 'okCommit').click()

        CustomerNamePath = context.baseReader.getElementLocatorValue(context, currentPage, 'CustomerName')
        WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, CustomerNamePath)))


@step('Update Customer details on Edit Customer form')
def edit_customer_details(context):
    currentPage = GlobalVar.currentPage
    global auth_Group
    editCustomerNameWait = context.baseReader.readElementByPropertyName(currentPage, 'editCustomerName').get("value")
    WebDriverWait(context.driver, 60).until(EC.visibility_of_element_located((By.XPATH, editCustomerNameWait)))

    updatedCustomerName = context.csvRead[0].get("updatedCustomerName")
    editCus = context.baseReader.getElementByPropertyName(context, currentPage, 'editCustomerName')
    editCus.clear()
    current_time = datetime.datetime.now()
    field_value = updatedCustomerName + '_' + str(current_time).replace('.', ':')
    addCustomer['name'] = field_value
    editCus.send_keys(field_value)

    select_fr = Select(context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerRegion'))
    select_fr.select_by_index(1)
    region = context.baseReader.getElementByPropertyName(
        context, currentPage, 'CustomerRegion').get_attribute("value")
    addCustomer['Customer_Region'] = region

    select_fr = Select(context.baseReader.getElementByPropertyName(context, currentPage, 'authgroupDropdown'))
    select_fr.select_by_value(auth_Group)
    authGroup = context.baseReader.getElementByPropertyName(context, currentPage, 'authgroupDropdown').get_attribute("value")
    addCustomer['authGroup'] = authGroup

    context.baseReader.getElementByPropertyName(context, currentPage, "editCustomerSubmitButton").click()

    addCustomerWait = context.baseReader.readElementByPropertyName(currentPage, 'applyingChangesWait').get("value")
    WebDriverWait(context.driver, 60).until(EC.visibility_of_element_located((By.XPATH, addCustomerWait)))


@step('Click on "{value}" button and wait till device is added')
def submit_and_wait_till_device_Added(context, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()
    try:
        addDevicesReportXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'addDevicesReport')
        WebDriverWait(context.driver, 80).until(
            EC.visibility_of_element_located((By.XPATH, addDevicesReportXpath)))
    except:
        commitPopup = context.baseReader.getElementLocatorValue(context, currentPage, 'commitPopup')
        WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, commitPopup)))
        context.baseReader.getElementByPropertyName(context, currentPage, 'okCommit').click()
        addDevicesReportXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'addDevicesReport')
        WebDriverWait(context.driver, 80).until(
            EC.visibility_of_element_located((By.XPATH, addDevicesReportXpath)))


@step('click on "{item}" to open confirmation dialog')
def submit_button(context, item):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, item).click()


@step('Click on Delete button to open "{value}"')
def delete_Customer(context, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()


@step('Enter customer name for verification')
def enter_custname_for_deletion(context):
    currentPage = GlobalVar.currentPage
    deleteCus = context.baseReader.getElementByPropertyName(context, currentPage, 'deleteCustomerName')
    deleteCus.clear()
    deleteCus.send_keys(addCustomer['name'])


@step('Enter customer name to confirm')
def confirm_customer_name(context):
    currentPage = GlobalVar.currentPage
    searchObj = context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar')
    searchObj.clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(addCustomer['name'])
    searchObj.clear()


@step('Customer name should not be displayed in the list of customers')
def customer_visiblity(context):
    currentPage = GlobalVar.currentPage
    rowsXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'rows')
    rowSize = context.driver.find_elements(By.XPATH, rowsXpath)
    isNotMatched = True
    for i in range(1, len(rowSize)):
        cust_name = context.driver.find_element_by_xpath('//table/tbody/tr[' + str(i) + ']//td[1]').text
        if cust_name == addCustomer['name']:
            isNotMatched = False
    assert isNotMatched == True


@step('Commit the delete operation')
def commit_delete(context):
    currentPage = GlobalVar.currentPage
    customerSuccessXPATH = context.baseReader.readElementByPropertyName(currentPage, 'customerDeletedSuccess').get(
        "value")

    WebDriverWait(context.driver, 35).until(
        EC.invisibility_of_element_located((By.XPATH, customerSuccessXPATH)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'commitButton').click()

    confcommitXpath = context.baseReader.readElementByPropertyName(currentPage, 'confirmCommit').get("value")

    WebDriverWait(context.driver, 35).until(
        EC.visibility_of_element_located((By.XPATH, confcommitXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'okCommit').click()

    WebDriverWait(context.driver, 5).until(
        EC.invisibility_of_element_located((By.XPATH, 'commitButtonXPATH')))


@step('Click on Add Device Button and fill device details for "{scenario}" scenario')
def fill_add_device(context, scenario):
    global addDevice
    global deviceName
    currentPage = GlobalVar.currentPage
    addDeviceName = context.csvRead[0].get("addDeviceName")
    Management_IP_Success = context.csvRead[0].get("Management_IP_Success")
    Management_Port_Success = context.csvRead[0].get("Management_Port_Success")
    Management_IP_Fail = context.csvRead[0].get("Management_IP_Fail")
    Management_Port_Fail = context.csvRead[0].get("Management_Port_Fail")
    Management_Protocol = context.csvRead[0].get("Management_Protocol")
    NED_ID = context.csvRead[0].get("NED_ID")
    Device_Type = context.csvRead[0].get("Device_Type")

    if addCustomer == {}:
        Customer = context.csvRead[0].get("Customer")
    else:
        Customer = addCustomer['name']

    N = 7
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

    deviceName = addDeviceName + '_' + str(res)
    addDevice['Device_Name'] = deviceName
    fieldVisibilityXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DeviceName')
    WebDriverWait(context.driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, fieldVisibilityXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceName').send_keys(addDevice['Device_Name'])

    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceDescription').send_keys(
        deviceName + '_Description')

    context.baseReader.getElementByPropertyName(context, currentPage, 'Customer').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerSearch').send_keys(Customer)
    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerSearch').send_keys(Keys.ENTER)
    time.sleep(5)

    if scenario == 'Success':
        context.baseReader.getElementByPropertyName(context, currentPage, 'ManagementIP').send_keys(
            Management_IP_Success)
        context.baseReader.getElementByPropertyName(context, currentPage, 'ManagementPort').send_keys(
            Management_Port_Success)

    elif scenario == 'Failure':
        context.baseReader.getElementByPropertyName(context, currentPage, 'ManagementIP').send_keys(
            Management_IP_Fail)
        context.baseReader.getElementByPropertyName(context, currentPage, 'ManagementPort').send_keys(
            Management_Port_Fail)

    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'ManagementProtocol').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'ManagementProtocolSearch').send_keys(
        Management_Protocol)
    managementProtocolWait = context.baseReader.readElementByPropertyName(currentPage, "ManagementProtocolSearch").get(
        "value")
    WebDriverWait(context.driver, 35).until(
        lambda driver: len(driver.find_element(By.XPATH, managementProtocolWait).get_attribute("value")) != 0)
    context.baseReader.getElementByPropertyName(context, currentPage, 'ManagementProtocolSearch').send_keys(Keys.ENTER)

    context.baseReader.getElementByPropertyName(context, currentPage, 'NEDID').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'NEDIDSearch').send_keys(NED_ID)

    NEDIDwait = context.baseReader.readElementByPropertyName(currentPage, "NEDIDSearch").get("value")
    WebDriverWait(context.driver, 35).until(
        lambda driver: len(driver.find_element(By.XPATH, NEDIDwait).get_attribute("value")) != 0)
    context.baseReader.getElementByPropertyName(context, currentPage, 'NEDIDSearch').send_keys(Keys.ENTER)

    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceType').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceTypeSearch').send_keys(
        Device_Type)
    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceTypeSearch').send_keys(Keys.ENTER)


@step('Device should be connected and displayed in the list of devices')
def search_added_device(context):
    isMatched = False
    currentPage = GlobalVar.currentPage
    searchDevice = context.baseReader.getElementByPropertyName(context, currentPage, 'searchDevice')
    searchDevice.clear()
    searchDevice.send_keys(addDevice.get('Device_Name'))
    rowsXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'rows')
    rowSize = context.driver.find_elements(By.XPATH, rowsXpath)
    for i in range(0, len(rowSize)):
        deviceNameVal = context.driver.find_element_by_xpath('//table/tbody/tr[' + str(i + 1) + ']//td[2]').text
        if deviceNameVal == addDevice.get('Device_Name'):
            isMatched = True
    assert isMatched == True


# @step('Click on "{value}" to upload a csv file')
# def click_to_upload_csv(context, value):
#     currentPage = GlobalVar.currentPage
#     context.baseReader.getElementByPropertyName(context, currentPage, value).send_keys(
#         "F:/LCD-Tinna/lcd/OR/TestData.csv")


@step('Select features to be added in the audit job')
def select_features_audit_job(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'logging').click()


@step('Add Audit Job "{name}" and "{desc}"')
def add_job_name_desc(context, name, desc):
    global addAuditJob
    currentPage = GlobalVar.currentPage
    addAuditJobName = context.csvRead[0].get("addAuditJobName")
    context.baseReader.getElementByPropertyName(context, currentPage, name).clear()
    current_time = datetime.datetime.now()
    tempName = addAuditJobName + '_' + str(current_time).replace('.', ':')
    context.baseReader.getElementByPropertyName(context, currentPage, name).send_keys(tempName)
    addAuditJob['auditJobName'] = tempName

    addAuditJobDesc = context.csvRead[0].get("addAuditJobDesc")
    context.baseReader.getElementByPropertyName(context, currentPage, desc).clear()
    current_time = datetime.datetime.now()
    tempDesc = addAuditJobDesc + '_' + str(current_time).replace('.', ':')
    context.baseReader.getElementByPropertyName(context, currentPage, desc).send_keys(tempDesc)


@step('Add email group/individual email address under "{email}" and "{group}"')
def add_email_group(context, email, group):
    currentPage = GlobalVar.currentPage
    N = 7
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))
    res = res.lower() + '' + '@random.com'
    context.baseReader.getElementByPropertyName(context, currentPage, email).send_keys(res)

    context.baseReader.getElementByPropertyName(context, currentPage, email).send_keys(Keys.ENTER)

    context.baseReader.getElementByPropertyName(context, currentPage, email).send_keys(Keys.ESCAPE)

    M = 6
    ran = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=M))
    ran = ran.lower() + '' + '@abc.com'
    context.baseReader.getElementByPropertyName(context, currentPage, group).send_keys(ran)

    context.baseReader.getElementByPropertyName(context, currentPage, group).send_keys(Keys.ENTER)

    context.baseReader.getElementByPropertyName(context, currentPage, email).send_keys(Keys.ESCAPE)


@step('Filter devices to perform audit by using "{value}"')
def filter_device(context, value):
    currentPage = GlobalVar.currentPage
    if addDevice == {}:
        addAuditJobDevice = context.csvRead[0].get("addAuditJobDevice")
    else:
        addAuditJobDevice = addDevice['Device_Name']

    context.baseReader.getElementByPropertyName(context, currentPage, value).send_keys(addAuditJobDevice)

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDevicesButton').click()
    loading = context.baseReader.readElementByPropertyName(currentPage, "loading").get("value")
    WebDriverWait(context.driver, 35).until(
        EC.invisibility_of_element_located((By.XPATH, loading)))



@step('"{devices}" to Audit and click on "{add}" Button')
def select_devices_audit(context, devices, add):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, devices).click()

    context.baseReader.getElementByPropertyName(context, currentPage, add).click()
    noDataFound = context.baseReader.readElementByPropertyName(currentPage, "noDataFound").get("value")
    WebDriverWait(context.driver, 35).until(
        EC.invisibility_of_element_located((By.XPATH, noDataFound)))


@step('Click on "{proceed}" Button to open the Scheduling view')
def proceed_to_schedule_job(context, proceed):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, proceed).click()

    chooseAuditSchedule = context.baseReader.readElementByPropertyName(currentPage, "headingChooseAuditSchedule").get(
        "value")
    WebDriverWait(context.driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, chooseAuditSchedule)))


@step('Go to the AddAuditJob page')
def go_to_AddAuditJob_view(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, "AddAuditJob").click()
    addAuditJobTitle = context.baseReader.readElementByPropertyName(currentPage, "addAuditJobTitle").get("value")
    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, addAuditJobTitle)))


@step('Filter the audit jobs by "{value}" name')
def filter_Audit_job(context, value):
    global runJobPageURL
    currentPage = GlobalVar.currentPage
    if addDevice == {}:
        runAuditDevice = context.csvRead[0].get("runRemediateDevice")
    else:
        runAuditDevice = addDevice['Device_Name']

    context.baseReader.getElementByPropertyName(context, currentPage, value).send_keys(runAuditDevice)

    context.baseReader.getElementByPropertyName(context, currentPage, "filterJobsButton").click()

    loading = context.baseReader.readElementByPropertyName(currentPage, "loading").get("value")
    WebDriverWait(context.driver, 35).until(EC.invisibility_of_element_located((By.XPATH, loading)))

    runJobPageURL = context.driver.current_url


@step('Search the Audit job for "{scenario}" scenario by name and select the first job')
def search_job_name_in_table(context, scenario):
    currentPage = GlobalVar.currentPage
    reviewAuditJobSuccess = context.csvRead[0].get("runAuditJob")
    reviewAuditJobError = context.csvRead[0].get("reviewAuditJobError")
    reviewAuditJobFailure = context.csvRead[0].get("reviewAuditJobFailure")

    if scenario == 'Success':
        context.baseReader.getElementByPropertyName(context, currentPage, "AuditJobSearch").send_keys(
            reviewAuditJobSuccess)

    elif scenario == 'Error':
        context.baseReader.getElementByPropertyName(context, currentPage, "AuditJobSearch").send_keys(
            reviewAuditJobError)

    elif scenario == 'Failure':
        context.baseReader.getElementByPropertyName(context, currentPage, "AuditJobSearch").send_keys(
            reviewAuditJobFailure)

    context.baseReader.getElementByPropertyName(context, currentPage, "AuditJobSelect").click()

    auditJobTitle = context.baseReader.readElementByPropertyName(currentPage, "auditJobTitle").get("value")
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, auditJobTitle)))


@step('Select the Audit dropdown and click on Audit report')
def go_to_audit_report(context):
    global auditReportSummary
    currentPage = GlobalVar.currentPage
    title_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Title')
    WebDriverWait(context.driver, 60).until(EC.visibility_of_element_located((By.XPATH, title_xpath)))
    auditStatus = context.baseReader.getElementByPropertyName(context, currentPage, 'status').text

    if auditStatus == 'Audit Complete':
        context.baseReader.getElementByPropertyName(context, currentPage, "AuditDropdown").click()
        context.baseReader.getElementByPropertyName(context, currentPage, "viewAuditReport").click()
        alertBox_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'auditReportAlertMsg')
        WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, alertBox_xpath)))
        demo = context.baseReader.getElementByPropertyName(context, currentPage, 'reportCumulative').text
        auditReportSummary = demo.splitlines()

    elif auditStatus == 'Audit Failed':
        context.baseReader.getElementByPropertyName(context, currentPage, "RunAudit").click()
        context.baseReader.getElementByPropertyName(context, currentPage, "useCLI").click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'startAudit').click()
        finishedReportReady = context.baseReader.readElementByPropertyName(currentPage, "finishedReportReady").get(
            "value")
        WebDriverWait(context.driver, 150).until(
            EC.visibility_of_element_located((By.XPATH, finishedReportReady)))
        context.baseReader.getElementByPropertyName(context, currentPage, "ViewAuditReport").click()
        alertBox_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'auditReportAlertMsg')
        WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, alertBox_xpath)))
        demo = context.baseReader.getElementByPropertyName(context, currentPage, 'reportCumulative').text
        auditReportSummary = demo.splitlines()

@step('Validate that the error message is as expected')
def error_expected(context):
    assert auditReportSummary[0] == "1 devices error"


@step('Validate that both Features and Rules return success')
def success(context):
    assert auditReportSummary[1] == "0 devices warning"


@step('Validate that the deviation is as expected')
def failed(context):
    assert auditReportSummary[2] == "1 devices failed"


@step('Validate that the message is as expected')
def failed(context):
    assert auditReportSummary[3] == "1 devices passed"


@step('"{search}" the job and click on selected job to open its "{value}" view')
def select_audit_job(context, search, value):
    global runRemediateJob
    currentPage = GlobalVar.currentPage

    if addAuditJob == {}:
        runRemediateJob['job_name'] = context.csvRead[0].get('reverseRemediateJob')
    else:
        runRemediateJob['job_name'] = addAuditJob.get('auditJobName')

    context.baseReader.getElementByPropertyName(context, currentPage, search).clear()
    context.baseReader.getElementByPropertyName(context, currentPage, search).send_keys(runRemediateJob['job_name'])
    jobValXpath = context.baseReader.getElementLocatorValue(context, currentPage, value)
    WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, jobValXpath), runRemediateJob['job_name']))

    context.baseReader.getElementByPropertyName(context, currentPage, value).click()
    auditJobTitle = context.baseReader.readElementByPropertyName(currentPage, "auditJobTitle").get("value")
    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, auditJobTitle)))


@step('validate "{value}" should be selected')
def validate_do_not_schedule_select(context, value):
    currentPage = GlobalVar.currentPage
    flag = context.baseReader.getElementByPropertyName(context, currentPage, value).is_displayed()

    context.baseReader.getElementByPropertyName(context, currentPage, 'proceedToConfirmAuditJob').click()

    confirmAuditJobTitle = context.baseReader.readElementByPropertyName(currentPage, "confirmAuditJobTitle").get(
        "value")

    assert flag == True

    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, confirmAuditJobTitle)))


@step('click on "{item}" and validate "{value}"')
def validate_click(context, item, value):
    currentPage = GlobalVar.currentPage
    jobName = context.baseReader.getElementByPropertyName(context, currentPage, value).text
    assert addAuditJob['auditJobName'] == jobName

    context.baseReader.getElementByPropertyName(context, currentPage, item).click()


@step('Click on "{value}" button to open Confirm Run Audit dialog')
def run_audit_button(context, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()
    errorStatus = context.baseReader.getElementByPropertyName(context, currentPage, 'message').text

    if errorStatus == 'Number of Audit Runs Exceeded':
        context.baseReader.getElementByPropertyName(context, currentPage, 'Ok').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'auditHistory').click()
        element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'runTitle')
        WebDriverWait(context.driver, 35).until(EC.visibility_of((element_obj)))
        context.baseReader.getElementByPropertyName(context, currentPage, 'selectAll').click()
        deleteButton_xpath = context.baseReader.readElementByPropertyName(currentPage, 'deleteRuns').get('value')
        time.sleep(35)
        WebDriverWait(context.driver, 35).until(EC.element_to_be_clickable((By.XPATH, deleteButton_xpath)))
        context.baseReader.getElementByPropertyName(context, currentPage, 'deleteRuns').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'Ok').click()
        runDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
        WebDriverWait(context.driver, 35).until(
            EC.text_to_be_present_in_element((By.XPATH, runDataXpath), 'No data found'))
        commit_changes(context)
        context.baseReader.getElementByPropertyName(context, currentPage, 'auditJobLink').click()
        element_obj = context.baseReader.getElementByPropertyName(context, currentPage, value)
        WebDriverWait(context.driver, 35).until(EC.visibility_of((element_obj))).click()
        context.baseReader.getElementByPropertyName(context, currentPage, "useCLI").click()

    else:
        context.baseReader.getElementByPropertyName(context, currentPage, "useCLI").click()


@step('Click on "{value}" to open the Audit Status view')
def startAudit(context, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()

    finishedReportReady = context.baseReader.readElementByPropertyName(currentPage, "finishedReportReady").get("value")

    WebDriverWait(context.driver, 150).until(
        EC.visibility_of_element_located((By.XPATH, finishedReportReady)))


@step('Click on "{Customers}" and filter the customer by "{filterData}"')
def click_on_customer_and_filter(context, Customers, filterData):
    currentPage = GlobalVar.currentPage
    if addCustomer == {}:
        customerForAddTag = context.csvRead[0].get("customerForAddTag")
    else:
        customerForAddTag = addCustomer['name']

    # context.baseReader.getElementByPropertyName(context, currentPage, Customers).click()
    #
    # loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    # WebDriverWait(context.driver, 35).until(
    #     EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, filterData).send_keys(customerForAddTag)

    firstRowCellXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'firstRowCell')
    WebDriverWait(context.driver, 35).until(
        EC.text_to_be_present_in_element((By.XPATH, firstRowCellXpath), customerForAddTag))

    tags['customer_name'] = context.baseReader.getElementByPropertyName(context, currentPage, 'firstCustomerName').text

    context.baseReader.getElementByPropertyName(context, currentPage, 'firstRowCell').click()

    loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    WebDriverWait(context.driver, 35).until(
        EC.invisibility_of_element_located((By.XPATH, loaderXpath)))


@step('Add corresponding tags to selected customer and click submit')
def add_tag(context):
    global tags
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'addTagButton').click()
    N = 7
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))
    tags['Customer_tag'] = res
    context.baseReader.getElementByPropertyName(context, currentPage, 'inputTag').send_keys(res)

    context.baseReader.getElementByPropertyName(context, currentPage, 'addTagButton').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'inputTag').send_keys(Keys.ESCAPE)


@step('go to device level by "{devicesButton}"')
def go_to_device_level(context, devicesButton):
    global tags
    currentPage = GlobalVar.currentPage
    if addDevice == {}:
        deviceForAddTag = context.csvRead[0].get('deviceForAddTag')
    else:
        deviceForAddTag = addDevice['Device_Name']
    context.baseReader.getElementByPropertyName(context, currentPage, devicesButton).click()

    loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    WebDriverWait(context.driver, 35).until(
        EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDeviceName').send_keys(deviceForAddTag)

    testDeviceFirstResultXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'testDeviceFirstResult')
    WebDriverWait(context.driver, 35).until(
        EC.text_to_be_present_in_element((By.XPATH, testDeviceFirstResultXpath), deviceForAddTag))

    tags['device_name'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                      'testDeviceFirstResult').text

    context.baseReader.getElementByPropertyName(context, currentPage, 'testDeviceFirstResult').click()

    loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    WebDriverWait(context.driver, 50).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

@step('Add corresponding tags to selected device')
def add_tag_to_selected(context):
    currentPage = GlobalVar.currentPage
    N = 7
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))
    tags['device_tag'] = res

    deviceModelFamily_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceModelFamily')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, deviceModelFamily_xpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterDataDeviceTag').send_keys('DEVICE GROUP')

    Tags_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Tags')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, Tags_xpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'addTagButton').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'inputTag').send_keys(res)

    context.baseReader.getElementByPropertyName(context, currentPage, 'addTagButton').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'inputTag').send_keys(Keys.ESCAPE)


@step('Navigate to "{item}" and click on "{value}"')
def go_to_deviceOnboard_then_add_Job(context, item, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, item).click()

    valueXpath = context.baseReader.getElementLocatorValue(context, currentPage, value)
    WebDriverWait(context.driver, 35).until(
        EC.text_to_be_present_in_element((By.XPATH, valueXpath), 'Add Brownfield Job'))

    context.baseReader.getElementByPropertyName(context, currentPage, value).click()

    loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    WebDriverWait(context.driver, 50).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))


@step('validate the correct device is filterd by using Customer Tag')
def filter_device_by_tag(context):
    currentPage = GlobalVar.currentPage
    customerTag = tags.get('Customer_tag')

    context.baseReader.getElementByPropertyName(context, currentPage, "addJobCustomerTag").click()
    context.baseReader.getElementByPropertyName(context, currentPage, "addJobCustomerTag").send_keys(customerTag)

    searchedTagXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'searchedTag')
    tagList = context.driver.find_elements(By.XPATH, searchedTagXpath)
    for i in range(0, len(tagList)):
        if tagList[i].text == customerTag:
            tagList[i].click()

    # searchedTagXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'searchedTag')
    # WebDriverWait(context.driver, 35).until(
    #     EC.text_to_be_present_in_element((By.XPATH, searchedTagXpath), customerTag))
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, "filterDeviceButton").click()
    time.sleep(5)

    firstRowCustomerNameXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'firstRowCustomerName')
    WebDriverWait(context.driver, 35).until(
        EC.text_to_be_present_in_element((By.XPATH, firstRowCustomerNameXpath), tags.get("customer_name")))

    firstValue = context.baseReader.getElementByPropertyName(context, currentPage, "firstRowCustomerName").text
    assert tags.get("customer_name") == firstValue


@step('validate that the result is as expected based on device tag')
def validate_result_by_device_tag(context):
    currentPage = GlobalVar.currentPage
    deviceTag = tags.get("device_tag")
    context.baseReader.getElementByPropertyName(context, currentPage, "addJobDeviceTag").send_keys(deviceTag)

    deviceTagListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceTagList')
    tagList = context.driver.find_elements(By.XPATH, deviceTagListXpath)
    for i in range(0, len(tagList)):
        if tagList[i].text == deviceTag:
            tagList[i].click()

    # context.baseReader.getElementByPropertyName(context, currentPage, "addJobDeviceTag").send_keys(Keys.ENTER)

    context.baseReader.getElementByPropertyName(context, currentPage, "buttonFilterDevice").click()

    firstCellDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'firstCellData')
    WebDriverWait(context.driver, 35).until(
        EC.text_to_be_present_in_element((By.XPATH, firstCellDataXpath), tags.get("device_name")))

    firstValue = context.baseReader.getElementByPropertyName(context, currentPage, "firstCellData").text
    assert tags.get("device_name") == firstValue


@step('Select option "{value}" to add audit job')
def select_run_audit_immediately(context, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()


@step('Select Audit Option and format')
def select_Audit_option(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'useCLI').click()


@step('Click on "{value}" button to open Confirm Audit Job page')
def confirm_Audit_by_run_immediately(context, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()

    titleConfirmAuditJob = context.baseReader.readElementByPropertyName(currentPage, "titleConfirmAuditJob").get(
        "value")

    WebDriverWait(context.driver, 35).until(
        EC.visibility_of_element_located((By.XPATH, titleConfirmAuditJob)))

    context.baseReader.getElementByPropertyName(context, currentPage, "confirmAuditButton").click()


@step('Click on "{value}" button')
def click_confirm_audit_button(context, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()


@step('Audit status displays "{value}"')
def validate_finish_report_ready(context, value):
    currentPage = GlobalVar.currentPage
    title = context.baseReader.getElementByPropertyName(context, currentPage, 'finishedReportReady').text
    assert title == "Finished - Report Ready"


def wait_for_page_load(context, self, timeout=35):
    self.log.debug("Waiting for page to load at {}.".format(context.driver.current_url))
    old_page = context.driver.find_element_by_tag_name('html')
    yield
    WebDriverWait(self, timeout).until(staleness_of(old_page))


@step('Filter device(s) to onboard')
def filter_devices(context):
    currentPage = GlobalVar.currentPage
    global addOnboardingDevice
    if addDevice == {}:
        addOnboardingDevice = context.csvRead[0].get("addOnboardingDevice")
    else:
        addOnboardingDevice = addDevice['Device_Name']

    context.baseReader.getElementByPropertyName(context, currentPage, 'FilterDeviceName').send_keys(addOnboardingDevice)
    context.baseReader.getElementByPropertyName(context, currentPage, 'FilterDevices').click()


@step('Select device(s) to onboard')
def select_devices(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable').send_keys(addOnboardingDevice)
    selectedDevice_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'selectedDevice')
    checkClick = context.driver.find_elements(By.XPATH, selectedDevice_xpath)
    for i in checkClick:
        i.click()


@step('Enter Onboarding Job Name and Description')
def enter_job_name(context):
    global addBrownfieldJob
    currentPage = GlobalVar.currentPage
    nameObj = context.baseReader.getElementByPropertyName(context, currentPage, 'OnboardingJobName')
    nameObj_text = nameObj.get_property('value')
    nameObj_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'OnboardingJobName')
    if len(nameObj_text) != 0:
        nameObj.clear()
    else:
        WebDriverWait(context.driver, 35).until(
            EC.text_to_be_present_in_element_value((By.XPATH, nameObj_xpath), 'brown'))
        nameObj.clear()

    current_time = datetime.datetime.now()
    addBrownfieldJob = 'BHLCD_BrownfieldJob_' + addOnboardingDevice
    nameObj.send_keys(addBrownfieldJob)
    context.baseReader.getElementByPropertyName(context, currentPage, 'OnboardingJobDescription').send_keys(
        'BHLCD_BrownfieldJobDescription_' + addOnboardingDevice)


@step('Validate that the job is added and listed')
def validate_job(context):
    currentPage = GlobalVar.currentPage
    alertBox_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alertBox')
    WebDriverWait(context.driver, 35).until(EC.invisibility_of_element_located((By.XPATH, alertBox_xpath)))
    jobName_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'JobName')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, jobName_xpath)))
    jobName_Val = context.baseReader.getElementByPropertyName(context, currentPage, 'JobName').text
    assert jobName_Val == addBrownfieldJob


@step('Filter and select the onboarding jobs for "{scenario}"')
def select_jobs(context, scenario):
    currentPage = GlobalVar.currentPage
    global runBrownfieldDevice
    global runBrownfieldJob
    if addDevice == {}:
        runBrownfieldDevice = context.csvRead[0].get("runBrownfieldDevice")
    else:
        runBrownfieldDevice = addDevice['Device_Name']

    if addBrownfieldJob == None:
        runBrownfieldJob = context.csvRead[0].get("runBrownfieldJob")
    else:
        runBrownfieldJob = addBrownfieldJob

    runBrownfieldDeviceFail = context.csvRead[0].get("runBrownfieldDeviceFail")
    runBrownfieldJobFail = context.csvRead[0].get("runBrownfieldJobFail")

    if (scenario == 'Success'):
        context.baseReader.getElementByPropertyName(context, currentPage, 'FilterDeviceName').send_keys(
            runBrownfieldDevice)
        context.baseReader.getElementByPropertyName(context, currentPage, 'FilterJobs').click()
        val1 = context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable')
        val1.send_keys(runBrownfieldJob)
        jobValue_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'JobValue')
        WebDriverWait(context.driver, 35).until(
            EC.text_to_be_present_in_element((By.XPATH, jobValue_xpath), runBrownfieldJob))
        context.baseReader.getElementByPropertyName(context, currentPage, 'JobValue').click()

    elif (scenario == 'Fail'):
        context.baseReader.getElementByPropertyName(context, currentPage, 'FilterDeviceName').send_keys(
            runBrownfieldDeviceFail)
        context.baseReader.getElementByPropertyName(context, currentPage, 'FilterJobs').click()
        val1 = context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable')
        val1.send_keys(runBrownfieldJobFail)
        jobValue_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'JobValue')
        WebDriverWait(context.driver, 35).until(
            EC.text_to_be_present_in_element((By.XPATH, jobValue_xpath), runBrownfieldJobFail))
        context.baseReader.getElementByPropertyName(context, currentPage, 'JobValue').click()


@step('"{item}" stage status value should be "{value}"')
def check_status(context, item, value):
    currentPage = GlobalVar.currentPage
    val_obj = context.baseReader.getElementByPropertyName(context, currentPage, item).text
    assert val_obj == value


@step('"{item}" stage status should be "{value}" and "{reachability}"')
def check_status(context, item, value, reachability):
    currentPage = GlobalVar.currentPage
    val_obj = context.baseReader.getElementByPropertyName(context, currentPage, item).text
    if (val_obj != value):
        context.baseReader.getElementByPropertyName(context, currentPage, 'ResetOnboardingJob').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'ConfirmReset').click()
        jobStatus_xpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                    'OnboardBrownfieldDevicesStatus')
        WebDriverWait(context.driver, 35).until(
            EC.text_to_be_present_in_element((By.XPATH, jobStatus_xpath), value))
        if reachability == 'Connected':
            deviceReachability_xpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                 'deviceReachability')
            WebDriverWait(context.driver, 40).until(
                EC.text_to_be_present_in_element((By.XPATH, deviceReachability_xpath), 'Reachable - Connected'))
        elif reachability == 'Not Connected':
            deviceReachability_xpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                 'deviceReachability')
            WebDriverWait(context.driver, 40).until(
                EC.text_to_be_present_in_element((By.XPATH, deviceReachability_xpath), 'Not Reachable Recheck'))
    else:
        if reachability == 'Connected':
            assert val_obj == value
            deviceReachability_xpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                 'deviceReachability')
            WebDriverWait(context.driver, 40).until(
                EC.text_to_be_present_in_element((By.XPATH, deviceReachability_xpath), 'Reachable - Connected'))
        elif reachability == 'Not Connected':
            assert val_obj == value
            deviceReachability_xpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                 'deviceReachability')
            WebDriverWait(context.driver, 40).until(
                EC.text_to_be_present_in_element((By.XPATH, deviceReachability_xpath), 'Not Reachable Recheck'))

    context.baseReader.getElementByPropertyName(context, currentPage, 'FetchParametersfromDevices').click()
    ConfirmButtonXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'ConfirmButton')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, ConfirmButtonXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'ConfirmButton').click()


@step('"{item}" stage status should be displayed "{value}"')
def check_status(context, item, value):
    currentPage = GlobalVar.currentPage
    val_obj = context.baseReader.getElementByPropertyName(context, currentPage, item).text
    if (val_obj != value):
        context.baseReader.getElementByPropertyName(context, currentPage, 'ResetOnboardingJob').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'ConfirmReset').click()
        onboardingStatusText_xpath = context.baseReader.getElementLocatorValue(
            context, currentPage, 'OnboardBrownfieldDevicesStatus')
        WebDriverWait(context.driver, 35).until(
            EC.text_to_be_present_in_element((By.XPATH, onboardingStatusText_xpath), value))
        deviceReachability_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceReachability')
        WebDriverWait(context.driver, 80).until(
            EC.text_to_be_present_in_element((By.XPATH, deviceReachability_xpath), 'Reachable - Connected'))
        context.baseReader.getElementByPropertyName(context, currentPage, 'FetchParametersfromDevices').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'ConfirmButton').click()
        saveParametersStatusText_xpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                   'SaveParameterstoDatastoreStatus')
        WebDriverWait(context.driver, 350).until(
            EC.text_to_be_present_in_element((By.XPATH, saveParametersStatusText_xpath), value))

    else:
        assert val_obj == value

    button_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SaveParameterstoDatastore')
    time.sleep(35)
    WebDriverWait(context.driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, button_xpath)))


@step('"{item}" stage status should change to "{value}"')
def wait_for_fetch_parameters(context, item, value):
    currentPage = GlobalVar.currentPage
    item_xpath = context.baseReader.getElementLocatorValue(context, currentPage, item)
    WebDriverWait(context.driver, 350).until(
        EC.text_to_be_present_in_element((By.XPATH, item_xpath), value))
    val_obj = context.baseReader.getElementByPropertyName(context, currentPage, item).text
    assert val_obj == value


@step('"{item}" stage status should become "{value}"')
def wait_for_save_parameters(context, item, value):
    currentPage = GlobalVar.currentPage
    item_xpath = context.baseReader.getElementLocatorValue(context, currentPage, item)
    WebDriverWait(context.driver, 60).until(
        EC.text_to_be_present_in_element((By.XPATH, item_xpath), value))
    val_obj = context.baseReader.getElementByPropertyName(context, currentPage, item).text
    assert val_obj == value


@step('"{item}" value should be "{value_1}" or "{value_2}" but not "{value_3}"')
def wait_for_result(context, item, value_1, value_2, value_3):
    currentPage = GlobalVar.currentPage
    value_4 = 'Not Available Yet'
    val_obj = context.baseReader.getElementByPropertyName(context, currentPage, item).text

    if (val_obj == value_4):
        deviceReachability_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceReachability')
        WebDriverWait(context.driver, 40).until(
            EC.text_to_be_present_in_element((By.XPATH, deviceReachability_xpath), 'Reachable - Connected'))
        context.baseReader.getElementByPropertyName(context, currentPage, 'FetchParametersfromDevices').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'ConfirmButton').click()
        saveParametersStatusText_xpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                   'SaveParameterstoDatastoreStatus')
        WebDriverWait(context.driver, 350).until(
            EC.text_to_be_present_in_element((By.XPATH, saveParametersStatusText_xpath), value_3))


    elif (val_obj == value_1) or (val_obj == value_2):
        pass

    else:
        context.baseReader.getElementByPropertyName(context, currentPage, 'ResetOnboardingJob').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'ConfirmReset').click()
        onboardingStatusText_xpath = context.baseReader.getElementLocatorValue(
            context, currentPage, 'OnboardBrownfieldDevicesStatus')
        WebDriverWait(context.driver, 35).until(
            EC.text_to_be_present_in_element((By.XPATH, onboardingStatusText_xpath), value_3))
        deviceReachability_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceReachability')
        WebDriverWait(context.driver, 40).until(
            EC.text_to_be_present_in_element((By.XPATH, deviceReachability_xpath), 'Reachable - Connected'))
        context.baseReader.getElementByPropertyName(context, currentPage, 'FetchParametersfromDevices').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'ConfirmButton').click()
        viewResultStatusText_xpath = context.baseReader.getElementLocatorValue(
            context, currentPage, 'ViewBrownfieldOnboardingResultStatus')
        WebDriverWait(context.driver, 350).until(
            EC.text_to_be_present_in_element((By.XPATH, viewResultStatusText_xpath), value_1))

    button_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'ViewBrownfieldOnboardingResult')
    time.sleep(35)
    WebDriverWait(context.driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, button_xpath)))


@step('Wait for OnboardingResult page to load')
def wait_for_page_to_load(context):
    currentPage = GlobalVar.currentPage
    title_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Title')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, title_xpath)))


@step('Results should be displayed in rows with columns for "{header_1}", "{header_2}", "{header_3}"  and "{header_4}"')
def verify_result(context, header_1, header_2, header_3, header_4):
    currentPage = GlobalVar.currentPage
    header_1_Val = context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceName').text
    assert header_1_Val.lower() == header_1.lower()
    header_2_Val = context.baseReader.getElementByPropertyName(context, currentPage, 'RuleID').text
    assert header_2_Val.lower() == header_2.lower()
    header_3_Val = context.baseReader.getElementByPropertyName(context, currentPage, 'Error').text
    assert header_3_Val.lower() == header_3.lower()
    header_4_Val = context.baseReader.getElementByPropertyName(context, currentPage, 'Message').text
    assert header_4_Val.lower() == header_4.lower()


@step('Enter group name at "{nameField}" and email addresses to the "{emailField}"')
def enter_emails(context, nameField, emailField):
    global emailGroupName
    global email_list
    x = 5
    randomvalue = ''.join(random.choices(string.ascii_uppercase + string.digits, k=x))
    emailGroupName = 'BHLCD_Group_' + str(randomvalue)
    context.baseReader.getElementByPropertyName(context, currentPage, nameField).send_keys(emailGroupName)

    for i in range(1, 5):
        email_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=x))
        email_text = email_text.lower() + '' + '@bhlcd.com'

        context.baseReader.getElementByPropertyName(context, currentPage, emailField).send_keys(email_text)
        context.baseReader.getElementByPropertyName(context, currentPage, emailField).send_keys(Keys.ENTER)
        i = i + 1

    context.baseReader.getElementByPropertyName(context, currentPage, emailField).send_keys(Keys.ESCAPE)


@step('Verify that the email group is added and displayed')
def verify_add_emails(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable').send_keys(emailGroupName)
    value = context.baseReader.getElementByPropertyName(context, currentPage, 'GroupNameValue').text
    assert value == emailGroupName


@step('clicking on "{addAuditJob}"')
def click_addAuditJob(context, addAuditJob):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, addAuditJob).click()

    titleAddAuditJob = context.baseReader.readElementByPropertyName(currentPage, 'titleAddAuditJob').get("value")

    loadingWait = context.baseReader.readElementByPropertyName(currentPage, 'loadingWait').get("value")

    WebDriverWait(context.driver, 50).until(
        EC.visibility_of_element_located((By.XPATH, titleAddAuditJob)))

    WebDriverWait(context.driver, 35).until(
        EC.invisibility_of_element_located((By.XPATH, loadingWait)))


@step('I perform Commit action')
def commit_changes(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'commitButton').click()
    confcommitXpath = context.baseReader.readElementByPropertyName(currentPage, 'confirmCommit').get("value")
    WebDriverWait(context.driver, 35).until(
        EC.visibility_of_element_located((By.XPATH, confcommitXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'okCommit').click()
    WebDriverWait(context.driver, 5).until(
        EC.element_selection_state_to_be((context.baseReader.getElementByPropertyName(
            context, currentPage, 'commitButton')), False))

@step('Select an email group and click "{actionButton}"')
def select_email_group(context, actionButton):
    currentPage = GlobalVar.currentPage
    global del_group_val
    updateEmailGroup = context.csvRead[0].get("updateEmailGroup")
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable').send_keys(updateEmailGroup)
    del_group_val = context.baseReader.getElementByPropertyName(context, currentPage, 'GroupNameValue').text
    context.baseReader.getElementByPropertyName(context, currentPage, actionButton).click()


@step('Edit Email Group name and email addresses')
def edit_email_group(context):
    currentPage = GlobalVar.currentPage
    global new_email_val
    global new_group_name
    x = 5
    randomvalue = ''.join(random.choices(string.ascii_uppercase + string.digits, k=x))
    new_group_name = 'BHLCD_Group_' + str(randomvalue) + '_Updated'

    name_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'EmailGroupName')
    name_obj.clear()
    name_obj.send_keys(new_group_name)

    context.baseReader.getElementByPropertyName(context, currentPage, 'DeleteIcon').click()

    x = 6
    new_email_val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=x))
    new_email_val = new_email_val.lower() + '' + '@xyz.com'

    context.baseReader.getElementByPropertyName(context, currentPage, 'EmailField').send_keys(new_email_val)
    context.baseReader.getElementByPropertyName(context, currentPage, 'EmailField').send_keys(Keys.ENTER)
    context.baseReader.getElementByPropertyName(context, currentPage, 'SaveButton').click()


@step('Validate that the changes are displayed in the list of email groups')
def validate_edit_email_group(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable').send_keys(new_group_name)
    email_group_val = context.baseReader.getElementByPropertyName(context, currentPage, 'EmailValue').text
    assert email_group_val == new_group_name

    email_list_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'emailList')
    email_list = context.driver.find_elements(By.XPATH, email_list_xpath)

    matched = False
    for i in range(0, len(email_list)):
        email = email_list[i]
        if (new_email_val == email.text):
            matched = True
    assert matched == True


@step('Validate that the deleted email group is not displayed in the list')
def validate_delete_email_group(context):
    currentPage = GlobalVar.currentPage
    alert_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DeleteAlert')
    WebDriverWait(context.driver, 35).until(EC.invisibility_of_element_located((By.XPATH, alert_xpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable').send_keys(del_group_val)
    group_list_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'groupList')
    group_list = context.driver.find_elements(By.XPATH, group_list_xpath)

    matched = True
    for i in range(0, len(group_list)):
        value = group_list[i]
        if (del_group_val == value.text):
            matched = False
    assert matched == True


@step('"{searchintable}" the parameter "{param}" for review and select "{action}"')
def perform_deviation(context, searchintable, param, action):
    currentPage = GlobalVar.currentPage

    search_xpath = context.baseReader.getElementLocatorValue(context, currentPage, searchintable)
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, search_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, searchintable).send_keys(param)
    context.baseReader.getElementByPropertyName(context, currentPage, action).click()
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'UpdateGroupStandard').click()
    try:
        time.sleep(2)
        commitPopup = context.baseReader.getElementLocatorValue(context, currentPage, 'commitPopup')
        WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, commitPopup)))
        context.baseReader.getElementByPropertyName(context, currentPage, 'okCommit').click()
        popupXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'popupBox')
        WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, popupXpath)))
        popupXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'popupBox')
        WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, popupXpath)))
    except:
        popupXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'popupBox')
        WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, popupXpath)))

@step('I assert that the changed parameter is as it appears')
def validate_accept_deviation(context):
    pass


@step('Assert that device level parameter is clear')
def validate_reject_deviation(context):
    pass


@step('Navigate to manage audit configs')
def validate_update_standard(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'Audit&Remediation').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'ManageAuditConfigs').click()


@step('Navigate to the device view and search for "{param}" to assert')
def check_updated_param(context, param):
    currentPage = GlobalVar.currentPage
    if addCustomer == {}:
        customerReviewDeviation2 = context.csvRead[0].get("runRemediateCustomer")
    else:
        customerReviewDeviation2 = addCustomer['name']

    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBar')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(customerReviewDeviation2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerVal').click()
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'CustomerGroup')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceTab').click()

    if addDevice == {}:
        deviceReviewDeviation2 = context.csvRead[0].get("runRemediateDevice")
    else:
        deviceReviewDeviation2 = addDevice['Device_Name']

    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(deviceReviewDeviation2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceVal').click()
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DeviceModel')

    WebDriverWait(context.driver, 50).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(param)
    logging_param_val = context.baseReader.getElementByPropertyName(context, currentPage, 'loggingListAfterUpdate').text
    assert len(logging_param_val) == 0


@step('I click on "{value}" tab')
def click_tab(context, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBar')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))


@step('I click on "{value}" button and add customer group')
def add_customer_group(context, value):
    currentPage = GlobalVar.currentPage
    global cust_grp_name
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()
    x = 4
    randomVal = ''.join(random.choices(string.ascii_lowercase + string.digits, k=x))
    cust_grp_name = 'BHLCD_CG_' + randomVal
    context.baseReader.getElementByPropertyName(context, currentPage, 'GropuInputField').send_keys(cust_grp_name)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Save').click()


@step('Validate that customer group is displayed in the list')
def validate_customer_group(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(cust_grp_name)
    cust_grp_val = context.baseReader.getElementByPropertyName(context, currentPage, 'GrpupVal').text
    assert cust_grp_val == cust_grp_name


@step('Select a customer and click on "{tabValue}"')
def navigate_device_tab(context, tabValue):
    currentPage = GlobalVar.currentPage
    customerForAddGroup = context.csvRead[0].get("customerForAddGroup")
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBar')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(customerForAddGroup)
    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerVal').click()
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'CustomerGroup')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, tabValue).click()


@step('I click on "{value}" button and add device group')
def add_device_group(context, value):
    global dev_grp_name
    currentPage = GlobalVar.currentPage
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBar')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()
    x = 4
    randomVal = ''.join(random.choices(string.ascii_lowercase + string.digits, k=x))
    dev_grp_name = 'BHLCD_DG_' + randomVal
    context.baseReader.getElementByPropertyName(context, currentPage, 'GropuInputField').send_keys(dev_grp_name)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Save').click()


@step('Validate that device group is displayed in the list')
def validate_customer_group(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(dev_grp_name)
    dev_grp_val = context.baseReader.getElementByPropertyName(context, currentPage, 'GrpupVal').text
    assert dev_grp_val == dev_grp_name


@step('I click on commit Ok button for add audit job only')
def audit_commit_ok(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'commitOk').click()
    alertSuccess = context.baseReader.readElementByPropertyName(currentPage, 'auditJobAddedMsg').get("value")
    WebDriverWait(context.driver, 35).until(
        EC.visibility_of_element_located((By.XPATH, alertSuccess)))


@step('Click on Ok button to commit add audit job by run remediation')
def audit_commit_ok_by_remediation(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'commitOk').click()

    status = context.baseReader.readElementByPropertyName(currentPage, 'auditStatus').get("value")
    WebDriverWait(context.driver, 350).until(
        EC.visibility_of_element_located((By.XPATH, status)))


@step('Add email group/individual at all stages')
def add_email_at_all_stages(context):
    currentPage = GlobalVar.currentPage
    emailGroup1 = context.csvRead[0].get("emailGroup1")
    context.baseReader.getElementByPropertyName(context, currentPage, 'atAllStages').send_keys(emailGroup1)

    context.baseReader.getElementByPropertyName(context, currentPage, 'firstGroup').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'atAllStages').send_keys(Keys.ESCAPE)


@step('Add email group/individual only at remediation')
def add_email_only_at_remediation(context):
    currentPage = GlobalVar.currentPage
    emailGroup2 = context.csvRead[0].get("emailGroup2")
    context.baseReader.getElementByPropertyName(context, currentPage, 'onlyAtRemediation').send_keys(emailGroup2)

    context.baseReader.getElementByPropertyName(context, currentPage, 'firstGroup').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'onlyAtRemediation').send_keys(Keys.ESCAPE)


@step('click on "{value}" and refresh current page')
def voilation_checkbo(context, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()
    context.driver.refresh()
    time.sleep(35)
    noVoilationFound = context.baseReader.readElementByPropertyName(currentPage, 'noVoilationFound').get("value")
    WebDriverWait(context.driver, 35).until(EC.invisibility_of_element_located((By.XPATH, noVoilationFound)))
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()


@step('select the "{checkbox}" value and click on "{button}"')
def select_firstCheckbox_value(context, checkbox, button):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, checkbox).click()

    context.baseReader.getElementByPropertyName(context, currentPage, button).click()

    confirmRemediationAlert = context.baseReader.readElementByPropertyName(currentPage, 'confirmRemediationAlert').get(
        "value")
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, confirmRemediationAlert)))


@step('click on "{ok}" and check "{status}" to be ready')
def validate_status(context, ok, status):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, ok).click()
    remediationStatus = context.baseReader.readElementByPropertyName(currentPage, status).get("value")
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, remediationStatus)))
    assert (context.baseReader.getElementByPropertyName(context, currentPage, status).text) == "Finished - Report Ready"


@step('Filter and select a device')
def select_device(context):
    currentPage = GlobalVar.currentPage
    if addDevice == {}:
        paramReviewDevice = context.csvRead[0].get("paramReviewDevice")
    else:
        paramReviewDevice = addDevice['Device_Name']

    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(paramReviewDevice)
    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceVal').click()


@step('Validate that the parameters appear as expected after onboarding')
def validate_parameters(context):
    currentPage = GlobalVar.currentPage
    global device_logging_config
    global device_router_config
    device_logging_config = context.csvRead[0].get("loggingServer")
    device_router_config = context.csvRead[0].get("customerRouterIP")
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DeviceModel')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys('Logging Server')
    param_val_logging = context.baseReader.getElementByPropertyName(context, currentPage, 'loggingParamList').text
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys('Customer Router IP')
    param_val_router = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                   'routerParamList').get_property('value')
    assert param_val_logging == device_logging_config
    assert param_val_router == device_router_config


@step('Set parameters for "{param2}"')
def set_parameters(context, param2):
    global router_param_val
    global resVal
    currentPage = GlobalVar.currentPage
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DeviceModel')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    router_param_val = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                   'routerParamList').get_property('value')

    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(param2)
    global ip
    ip = ".".join(map(str, (random.randint(0, 255)
                            for _ in range(4))))
    context.baseReader.getElementByPropertyName(context, currentPage, 'routerParamList').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'routerParamList').send_keys(ip)


@step('I refresh the page')
def refresh_page(context):
    currentPage = GlobalVar.currentPage
    context.driver.refresh()
    time.sleep(35)
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DeviceModel')
    WebDriverWait(context.driver, 60).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))


@step('Validate that the modified values for "{param2}" are displayed')
def validate_parameter_value(context, param2):
    currentPage = GlobalVar.currentPage
    searchXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBar')
    WebDriverWait(context.driver, 60).until(EC.visibility_of_element_located((By.XPATH, searchXpath)))
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').click()
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').clear()
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(param2)
    time.sleep(10)

    router_param_val_updated = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                           'routerParamList').get_property('value')

    assert router_param_val != router_param_val_updated
    assert router_param_val_updated == ip


@step('Select Audit options and format')
def select_audit_options(context):
    global schedule_job_name
    currentPage = GlobalVar.currentPage
    nameObj = context.baseReader.getElementByPropertyName(context, currentPage, 'ScheduledJobName')
    nameObj.send_keys('_Audit')
    schedule_job_name = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                    'ScheduledJobName').get_property('value')

    context.baseReader.getElementByPropertyName(context, currentPage, 'ScheduledJobDescription').send_keys('Audit')
    context.baseReader.getElementByPropertyName(context, currentPage, 'UseCLI').click()


@step('Enter Audit Schedule details')
def create_schedule(context):
    global schedule_job_name
    currentPage = GlobalVar.currentPage
    current_time = datetime.datetime.now()
    schedule_job_name = 'BHLCD_ScheduleAuditJob_' + str(current_time).replace('.', ':')
    context.baseReader.getElementByPropertyName(context, currentPage, 'ScheduledJobName').send_keys(schedule_job_name)
    context.baseReader.getElementByPropertyName(context, currentPage, 'ScheduledJobDescription').send_keys('Audit')
    context.baseReader.getElementByPropertyName(context, currentPage, 'UseCLI').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'AuditDateTime').click()

    currentTime = datetime.datetime.now()

    scheduleTime = currentTime + datetime.timedelta(minutes=15)

    scheduleTime = scheduleTime.strftime('%m/%d/%Y, %I:%M %p')

    context.baseReader.getElementByPropertyName(context, currentPage, 'AuditDateTime').send_keys(scheduleTime)

    time.sleep(35)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Cancel').click()
    time.sleep(30)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Save').click()


@step('Wait for job to be added and displayed')
def job_view(context):
    currentPage = GlobalVar.currentPage
    alert_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'ScheduleAlert')
    WebDriverWait(context.driver, 80).until(EC.invisibility_of_element_located((By.XPATH, alert_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'OK').click()


@step('Validate that the scheduled job is added successfully')
def validate_job_run(context):
    currentPage = GlobalVar.currentPage
    auditJobScheduling = context.csvRead[0].get("auditJobScheduling")
    context.baseReader.getElementByPropertyName(context, currentPage, 'toggle').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'searchfield').send_keys(auditJobScheduling)
    context.baseReader.getElementByPropertyName(context, currentPage, 'searchfield').send_keys(Keys.ENTER)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Searchintable').send_keys(schedule_job_name)
    job_val_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'jobval')
    WebDriverWait(context.driver, 35).until(
        EC.text_to_be_present_in_element((By.XPATH, job_val_xpath), schedule_job_name))


@step('Select Audit Recurrence and fill details')
def select_recurrence(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'OnceA').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'AuditDateTime').click()

    currentTime = datetime.datetime.now()

    scheduleTime = currentTime + datetime.timedelta(minutes=15)

    scheduleTime = scheduleTime.strftime('%m/%d/%Y, %I:%M %p')

    context.baseReader.getElementByPropertyName(context, currentPage, 'AuditDateTime').send_keys(scheduleTime)

    time.sleep(35)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Cancel').click()
    time.sleep(30)
    # proceedtoConfirmXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'ProceedtoConfirm')
    # WebDriverWait(context.driver, 80).until(EC.element_to_be_clickable((By.XPATH, proceedtoConfirmXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'ProceedtoConfirm').click()


@step('Select Audit Recurrence and fill details for audit and remediation')
def select_recurrence(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'RecurringAR').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'RecurringFrequency').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SelectOccurenceOption').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'selHour').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'RecHrs').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'selMin').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'RecMin').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'Percentagetext').send_keys('80')


@step('Wait for page to load')
def confirm_job(context):
    currentPage = GlobalVar.currentPage
    alert_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alert')
    WebDriverWait(context.driver, 350).until(
        EC.invisibility_of_element_located((By.XPATH, alert_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'OK').click()


@step('Validate that Audit job is created and displayed')
def validate_job_created(context):
    currentPage = GlobalVar.currentPage
    element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'Title')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((element_obj)))

    job_name = context.baseReader.getElementByPropertyName(context, currentPage, 'AuditJobName').text
    assert job_name == addAuditJob['auditJobName']

    context.baseReader.getElementByPropertyName(context, currentPage, 'ViewScheduledJob').click()


@step('Validate that the scheduled job is displayed under list of scheduled jobs')
def validate_job_scheduled(context):
    currentPage = GlobalVar.currentPage
    element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'scheduleJobName')
    WebDriverWait(context.driver, 30).until(EC.visibility_of((element_obj)))

    scheduled_job_val_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'scheduleJobVal')
    WebDriverWait(context.driver, 60).until(
        EC.text_to_be_present_in_element((By.XPATH, scheduled_job_val_xpath), schedule_job_name))


@step('Validate that the scheduled job is run at the specified time')
def validate_job_run(context):
    global job_runtime
    currentPage = GlobalVar.currentPage
    auditJobSchedulingCreated = context.csvRead[0].get("auditJobSchedulingCreated")
    search_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Searchintable')
    WebDriverWait(context.driver, 35).until(
        EC.visibility_of_element_located((By.XPATH, search_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'Searchintable').send_keys(
        auditJobSchedulingCreated)
    job_val_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'jobval')
    WebDriverWait(context.driver, 35).until(
        EC.text_to_be_present_in_element((By.XPATH, job_val_xpath), auditJobSchedulingCreated))
    job_runtime = context.baseReader.getElementByPropertyName(context, currentPage, 'RunningAt').text
    context.baseReader.getElementByPropertyName(context, currentPage, 'Audit&Remediation').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'Run&Remediate').click()


@step('Assert that job ran at the specified time')
def job_run(context):
    currentPage = GlobalVar.currentPage
    element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'Title')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((element_obj)))
    start_time = datetime.datetime.strptime(job_runtime, '%b %d, %Y, %H:%M:%S %p')
    search_time = start_time.strftime('%H:%M')
    checkStartTime = start_time.strftime('%b-%d-%Y, %H:%M %p')
    context.baseReader.getElementByPropertyName(context, currentPage, 'auditHistory').click()
    element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'runTitle')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((element_obj)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'search').send_keys(search_time)
    date_ran = context.baseReader.getElementByPropertyName(context, currentPage, 'DateRan').text
    actual_RunTime = datetime.datetime.strptime(date_ran, '%d-%m-%y - %H:%M %p')
    checkRunTime = actual_RunTime.strftime('%b-%d-%Y, %H:%M %p')
    assert checkStartTime == checkRunTime


@step('Filter a device and select a job to open its audit view for "{scenario}"')
def select_job(context, scenario):
    currentPage = GlobalVar.currentPage
    reviewRemediateDevice = context.csvRead[0].get("reviewRemediateDevice")
    reviewRemediateAuditJobError = context.csvRead[0].get("reviewRemediateAuditJobError")
    reviewRemediateAuditJobFailure = context.csvRead[0].get("reviewRemediateAuditJobFailure")
    reviewRemediateAuditJobSuccess = context.csvRead[0].get("reviewRemediateAuditJobSuccess")

    context.baseReader.getElementByPropertyName(context, currentPage, 'FilterDeviceName').send_keys(
        reviewRemediateDevice)
    context.baseReader.getElementByPropertyName(context, currentPage, 'FilterJobs').click()

    if scenario == 'Error':
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable').send_keys(
            reviewRemediateAuditJobError)
        jobValue_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'JobVal')
        WebDriverWait(context.driver, 35).until(
            EC.text_to_be_present_in_element((By.XPATH, jobValue_xpath), reviewRemediateAuditJobError))
        context.baseReader.getElementByPropertyName(context, currentPage, 'JobVal').click()

    elif scenario == 'Failure':
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable').send_keys(
            reviewRemediateAuditJobFailure)
        jobValue_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'JobVal')
        WebDriverWait(context.driver, 35).until(
            EC.text_to_be_present_in_element((By.XPATH, jobValue_xpath), reviewRemediateAuditJobFailure))
        context.baseReader.getElementByPropertyName(context, currentPage, 'JobVal').click()

    elif scenario == 'Success':
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable').send_keys(
            reviewRemediateAuditJobSuccess)
        jobValue_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'JobVal')
        WebDriverWait(context.driver, 35).until(
            EC.text_to_be_present_in_element((By.XPATH, jobValue_xpath), reviewRemediateAuditJobSuccess))
        context.baseReader.getElementByPropertyName(context, currentPage, 'JobVal').click()


@step('Navigate to "{action}" from "{status}" dropdown')
def navigate_auditreport(context, action, status):
    currentPage = GlobalVar.currentPage
    element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'Title')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((element_obj)))
    context.baseReader.getElementByPropertyName(context, currentPage, status).click()
    context.baseReader.getElementByPropertyName(context, currentPage, action).click()


@step('Navigate to "{action}" button')
def navigate_auditreport(context, action):
    currentPage = GlobalVar.currentPage
    element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'Title')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((element_obj)))
    context.baseReader.getElementByPropertyName(context, currentPage, action).click()


@step('Select the audit feature from Pre-Feature Summary to open its Violations for remediation')
def select_features(context):
    currentPage = GlobalVar.currentPage
    element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'Feature')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((element_obj)))
    element_obj.click()
    context.driver.refresh()
    time.sleep(35)
    noVoilation_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noVoilation')
    WebDriverWait(context.driver, 35).until(EC.invisibility_of_element_located((By.XPATH, noVoilation_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'Feature').click()

    ruleboxObj = context.baseReader.getElementByPropertyName(context, currentPage, 'RuleBox')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((ruleboxObj)))
    ruleboxObj.click()


@step('Select the audit feature from Pre-Feature Summary to open its Violations for reverse remediation')
def select_feature_for_remediate(context):
    currentPage = GlobalVar.currentPage
    element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'Services')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((element_obj)))
    element_obj.click()
    context.driver.refresh()
    time.sleep(35)
    noVoilation_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noVoilation')
    WebDriverWait(context.driver, 35).until(EC.invisibility_of_element_located((By.XPATH, noVoilation_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'Services').click()


@step('Click "{action}" button on selected rule(s)')
def click_button(context, action):
    currentPage = GlobalVar.currentPage
    tableObj = context.baseReader.getElementByPropertyName(context, currentPage, 'tableheader')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((tableObj)))
    context.baseReader.getElementByPropertyName(context, currentPage, action).click()
    alert_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'AlertBox')
    WebDriverWait(context.driver, 80).until(EC.invisibility_of_element((By.XPATH, alert_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'OK').click()


@step('Remediation status should be "{expectedtext}"')
def assert_remediation_status(context, expectedtext):
    currentPage = GlobalVar.currentPage
    reportstatus_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'RemediationReportStatus')
    WebDriverWait(context.driver, 50).until(
        EC.text_to_be_present_in_element((By.XPATH, reportstatus_xpath), expectedtext))
    reportStatusObj = context.baseReader.getElementByPropertyName(context, currentPage, 'RemediationReportStatus')

    assert expectedtext == reportStatusObj.text

    statusText = context.baseReader.getElementByPropertyName(context, currentPage, 'RemediationStatus').text
    assert statusText == 'Remediation Complete'


@step('Report should have a Blue type with success message "{expectedtext}"')
def assert_remediation(context, expectedtext):
    currentPage = GlobalVar.currentPage
    summaryObj = context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceSummary')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((summaryObj)))
    summary = summaryObj.text
    auditResult = summary.splitlines()
    assert auditResult[4] == expectedtext


@step('Click on "{button}" and navigate to report page')
def run_audit(context, button):
    currentPage = GlobalVar.currentPage
    status_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Title')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, status_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, button).click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'useCLI').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'startAudit').click()


@step('Navigate to "{tab}" at device level')
def access_review_deviation(context, tab):
    currentPage = GlobalVar.currentPage
    global router_param_val
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBar')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))

    if addCustomer == {}:
        customerReviewDeviation = context.csvRead[0].get("runRemediateCustomer")
    else:
        customerReviewDeviation = addCustomer['name']

    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(customerReviewDeviation)
    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerVal').click()

    loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    WebDriverWait(context.driver, 50).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'CustomerGroup')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceTab').click()

    loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    WebDriverWait(context.driver, 50).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

    if addDevice == {}:
        deviceReviewDeviation = context.csvRead[0].get("runRemediateDevice")
    else:
        deviceReviewDeviation = addDevice['Device_Name']

    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(deviceReviewDeviation)
    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceVal').click()

    loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    WebDriverWait(context.driver, 50).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DeviceModel')
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))

    time.sleep(5)
    searchXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBar')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, searchXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys('customer-router-ip')

    router_param_val = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                   'routerParamList').get_property('value')

    context.baseReader.getElementByPropertyName(context, currentPage, tab).click()

    loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    WebDriverWait(context.driver, 50).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBar')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))


@step('Search the parameter "{param}" and accept deviation')
def update_standard(context, param):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(param)
    context.baseReader.getElementByPropertyName(context, currentPage, 'acceptDeviation').click()
    try:
        time.sleep(2)
        commitPopup = context.baseReader.getElementLocatorValue(context, currentPage, 'commitPopup')
        WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, commitPopup)))
        context.baseReader.getElementByPropertyName(context, currentPage, 'okCommit').click()
        popupXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'popupBox')
        WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, popupXpath)))
        popupXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'popupBox')
        WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, popupXpath)))
    except:
        popupXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'popupBox')
        WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, popupXpath)))


@step('Filter and select the onboarding job for Update Standards')
def filter_job(context):
    currentPage = GlobalVar.currentPage
    if addDevice == {}:
        deviceReviewDeviation2 = context.csvRead[0].get("runRemediateDevice")
    else:
        deviceReviewDeviation2 = addDevice['Device_Name']

    if addBrownfieldJob == None:
        jobReviewDeviation2 = context.csvRead[0].get("runRemediateOnboarding")
    else:
        jobReviewDeviation2 = addBrownfieldJob

    context.baseReader.getElementByPropertyName(context, currentPage, 'FilterDeviceName').send_keys(
        deviceReviewDeviation2)
    context.baseReader.getElementByPropertyName(context, currentPage, 'FilterJobs').click()
    val1 = context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable')
    val1.send_keys(jobReviewDeviation2)
    jobValue_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'JobValue')
    WebDriverWait(context.driver, 35).until(
        EC.text_to_be_present_in_element((By.XPATH, jobValue_xpath), jobReviewDeviation2))
    context.baseReader.getElementByPropertyName(context, currentPage, 'JobValue').click()


@step('Navigate to device level and assert that parameters "{param}" are accepted')
def assert_params(context, param):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'GeneralDeviceParameters').click()
    context.driver.refresh()
    loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    WebDriverWait(context.driver, 50).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

    time.sleep(10)

    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DeviceModel')
    WebDriverWait(context.driver, 60).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    time.sleep(10)

    searchXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBar')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, searchXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').click()
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').clear()
    time.sleep(10)
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(param)
    time.sleep(10)
    router_updated_val = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                     'routerParamList').get_property('value')
    assert router_updated_val == router_param_val


@step('Validate that the audit returned "{expectedText}" for "{scenario}"')
def validate_error(context, expectedText, scenario):
    currentPage = GlobalVar.currentPage
    summaryObj = context.baseReader.getElementByPropertyName(context, currentPage, 'deviceSummary')
    WebDriverWait(context.driver, 50).until(EC.visibility_of((summaryObj)))
    summary = summaryObj.text
    auditResult = summary.splitlines()
    if scenario == 'Error':
        assert auditResult[0] == expectedText
    elif scenario == 'Failure':
        assert auditResult[2] == expectedText
    elif scenario == 'Success':
        assert auditResult[3] == expectedText


@step('Select the audit feature from Pre-Feature Summary to open its Violations')
def select_features(context):
    currentPage = GlobalVar.currentPage
    element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'Feature')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((element_obj)))
    element_obj.click()
    context.driver.refresh()
    time.sleep(35)


@step('Validate that no violations are found')
def no_violations_found(context):
    currentPage = GlobalVar.currentPage
    element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'Feature')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((element_obj)))
    element_obj.click()
    textObj = context.baseReader.getElementByPropertyName(context, currentPage, 'noVoilation')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((textObj)))
    assert textObj.text == 'No violations found'


@step('"{run}" job and click on "{report}"')
def run_auditJob(context, run, report):
    currentPage = GlobalVar.currentPage
    element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'Title')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((element_obj)))
    context.baseReader.getElementByPropertyName(context, currentPage, run).click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'useCLI').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'startAudit').click()

    reportStatus_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'auditStatus')
    WebDriverWait(context.driver, 50).until(
        EC.text_to_be_present_in_element((By.XPATH, reportStatus_xpath), 'Finished - Report Ready'))
    context.baseReader.getElementByPropertyName(context, currentPage, report).click()


@step('Navigate to the device onboarding job')
def navigate_onboarding_job(context):
    currentPage = GlobalVar.currentPage
    paramReviewOnboardingJob = context.csvRead[0].get("paramReviewOnboardingJob")
    context.baseReader.getElementByPropertyName(context, currentPage, 'deviceOnboarding').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'RunManageJobs').click()
    element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'searchBox')
    WebDriverWait(context.driver, 35).until(EC.visibility_of((element_obj)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'searchBox').send_keys(paramReviewOnboardingJob)
    jobValue_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'JobValue')
    WebDriverWait(context.driver, 35).until(
        EC.text_to_be_present_in_element((By.XPATH, jobValue_xpath), paramReviewOnboardingJob))
    context.baseReader.getElementByPropertyName(context, currentPage, 'JobValue').click()


@step('Reset and run onboarding on same device')
def reset_onboarding(context):
    currentPage = GlobalVar.currentPage
    deviceReachability_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceReachability')
    WebDriverWait(context.driver, 80).until(
        EC.text_to_be_present_in_element((By.XPATH, deviceReachability_xpath), 'No need to check'))
    context.baseReader.getElementByPropertyName(context, currentPage, 'ResetOnboardingJob').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'ConfirmReset').click()
    onboardingStatusText_xpath = context.baseReader.getElementLocatorValue(
        context, currentPage, 'OnboardBrownfieldDevicesStatus')
    WebDriverWait(context.driver, 35).until(
        EC.text_to_be_present_in_element((By.XPATH, onboardingStatusText_xpath), 'Ready'))
    deviceReachability_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'deviceReachability')
    WebDriverWait(context.driver, 80).until(
        EC.text_to_be_present_in_element((By.XPATH, deviceReachability_xpath), 'Reachable - Connected'))
    context.baseReader.getElementByPropertyName(context, currentPage, 'FetchParametersfromDevices').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'ConfirmButton').click()
    saveParametersStatusText_xpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                               'SaveParameterstoDatastoreStatus')
    WebDriverWait(context.driver, 350).until(
        EC.text_to_be_present_in_element((By.XPATH, saveParametersStatusText_xpath), 'Ready'))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SaveParameterstoDatastore').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'YesButton').click()
    button_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'ReviewDeviationsBtn')
    time.sleep(35)
    WebDriverWait(context.driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, button_xpath)))


@step('Assert that "{param1}" and "{param2}" are not displayed in Review deviations report')
def validate_nodeviation(context, param1, param2):
    currentPage = GlobalVar.currentPage
    search_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'searchintable')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, search_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'searchintable').send_keys(param1)
    noData_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, noData_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'searchintable').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'searchintable').send_keys(param2)
    noData_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, noData_xpath)))


@step('Select a customer and navigate to "{tabValue}"')
def navigate_to_device(context, tabValue):
    currentPage = GlobalVar.currentPage
    if addCustomer == {}:
        paramReviewCustomer = context.csvRead[0].get("paramReviewCustomer")
    else:
        paramReviewCustomer = addCustomer['name']

    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBar')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(paramReviewCustomer)
    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerVal').click()
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'CustomerGroup')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, tabValue).click()


@step('Filter a device and select a job to open its audit view')
def select_auditJob(context):
    currentPage = GlobalVar.currentPage
    if addAuditJob == {}:
        auditJobScheduling = context.csvRead[0].get("auditJobScheduling")
    else:
        auditJobScheduling = addAuditJob['auditJobName']

    if addDevice == {}:
        auditDeviceScheduling = context.csvRead[0].get("auditDeviceScheduling")
    else:
        auditDeviceScheduling = addDevice['Device_Name']

    context.baseReader.getElementByPropertyName(context, currentPage, 'FilterDeviceName').send_keys(
        auditDeviceScheduling)
    context.baseReader.getElementByPropertyName(context, currentPage, 'FilterJobs').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable').send_keys(
        auditJobScheduling)
    jobValue_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'JobVal')
    WebDriverWait(context.driver, 35).until(
        EC.text_to_be_present_in_element((By.XPATH, jobValue_xpath), auditJobScheduling))
    context.baseReader.getElementByPropertyName(context, currentPage, 'JobVal').click()


@step('filter the Customer group by name and select first result')
def validate_customer_group(context):
    currentPage = GlobalVar.currentPage

    context.baseReader.getElementByPropertyName(context, currentPage, 'firstCustomerGroup').click()


@step('validate the Logging Server and get the value')
def validate_loggingServer(context):
    currentPage = GlobalVar.currentPage
    val = context.baseReader.getElementByPropertyName(context, currentPage, 'loggingParamListConfrm').text
    assert len(val) == 0


@step('filter the Customer by name and select first result')
def filter_customer_name(context):
    currentPage = GlobalVar.currentPage
    if addCustomer == {}:
        customerGroup = context.csvRead[0].get("runRemediateCustomer")
    else:
        customerGroup = addCustomer['name']

    context.baseReader.getElementByPropertyName(context, currentPage, 'filterCustomer').send_keys(customerGroup)
    context.baseReader.getElementByPropertyName(context, currentPage, 'firstCustomerGroup').click()


@step('I go to the Devices and select the first value')
def go_to_devices(context):
    currentPage = GlobalVar.currentPage
    devicesAlertMsg = context.baseReader.readElementByPropertyName(currentPage, 'HeadingCustomerGroup').get("value")
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, devicesAlertMsg)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceTab').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceVal').click()


@step('search the "{value}" and get the logging server value')
def get_logging_server_value(context, value):
    global logging_param_val
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerSearch').send_keys(value)
    logging_param_val = context.baseReader.getElementByPropertyName(context, currentPage, 'loggingServerValue').text


@step('go to the "{link}" and applying filter for "{value}"')
def go_to_deviation_review(context, link, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'deviationReviewLink').click()
    searchAlertMsg = context.baseReader.readElementByPropertyName(currentPage, 'CustomerSearch').get("value")
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, searchAlertMsg)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerSearch').send_keys(value)


@step('navigate to the update standard button and select update Customer Group Standard')
def select_updateCustomerGroupStandard(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'updateStandardButton').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'updateCustomerGroupStandard').click()
    time.sleep(5)


@step('go to the "{value}" and select the Customer Group')
def go_to_customer_group(context, value):
    currentPage = GlobalVar.currentPage
    if cust_grp_name == None:
        groupCustomer = context.csvRead[0].get('custGroup')
    else:
        groupCustomer = cust_grp_name

    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()
    loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    WebDriverWait(context.driver, 50).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerSearch').send_keys(groupCustomer)
    context.baseReader.getElementByPropertyName(context, currentPage, 'firstCustomerGroup').click()

    loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    WebDriverWait(context.driver, 50).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

@step('I validate the logging server value')
def logging_server_validations(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    val = context.baseReader.getElementByPropertyName(context, currentPage, 'loggingParamListConfrm').text
    assert val == context.csvRead[0].get("loggingServer")


@step('Validate that device is not onboarded already')
def check_onboarded_device(context):
    currentPage = GlobalVar.currentPage
    deviceStatus = context.baseReader.getElementByPropertyName(context, currentPage, 'deviceStatus').text
    if (deviceStatus == 'Not Onboarded Yet'):
        pass

    elif (deviceStatus == 'Already In An Onboarding Job'):
        context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceOnoarding').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'RunManageJobs').click()

        page_title_validation(context, 'Run&ManageOnboardingJobs', 'RUN & MANAGE ONBOARDING JOBS')
        currentPage = GlobalVar.currentPage
        if addDevice == {}:
            BrownfieldDevice = context.csvRead[0].get("addOnboardingDevice")
        else:
            BrownfieldDevice = addDevice['Device_Name']

        context.baseReader.getElementByPropertyName(context, currentPage, 'FilterDeviceName').send_keys(
            BrownfieldDevice)
        context.baseReader.getElementByPropertyName(context, currentPage, 'FilterJobs').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable').send_keys(BrownfieldDevice)

        jobValue_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'JobValue')
        WebDriverWait(context.driver, 35).until(
            EC.text_to_be_present_in_element((By.XPATH, jobValue_xpath), 'BHLCD_BrownfieldJob_' + BrownfieldDevice))
        context.baseReader.getElementByPropertyName(context, currentPage, 'JobValue').click()

        page_title_validation(context, 'BrownfieldOnboardingJob', 'BROWNFIELD ONBOARDING JOB')
        currentPage = GlobalVar.currentPage
        deleteButton_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DeleteOnboardingJob')
        time.sleep(35)
        WebDriverWait(context.driver, 35).until(
            EC.element_to_be_clickable((By.XPATH, deleteButton_xpath))).click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'ConfirmDelete').click()
        element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'onboardJobs')
        WebDriverWait(context.driver, 35).until(
            EC.text_to_be_present_in_element((By.XPATH, element_xpath), 'Onboarding Jobs'))
        commit_changes(context)
        context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceOnoarding').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'AddBrownfieldJob').click()

        page_title_validation(context, 'AddBrownfieldJob', 'ADD BROWNFIELD ONBOARDING JOB')
        currentPage = GlobalVar.currentPage
        addOnboardingDevice = context.csvRead[0].get("addOnboardingDevice")
        context.baseReader.getElementByPropertyName(context, currentPage, 'FilterDeviceName').send_keys(
            addOnboardingDevice)
        context.baseReader.getElementByPropertyName(context, currentPage, 'FilterDevices').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable').send_keys(
            addOnboardingDevice)
        selectedDevice_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'selectedDevice')
        checkClick = context.driver.find_elements(By.XPATH, selectedDevice_xpath)
        for i in checkClick:
            i.click()


@step('Wait for the onboarding job to be added')
def wait_for_job(context):
    currentPage = GlobalVar.currentPage
    alertBox_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'alertBox')
    WebDriverWait(context.driver, 50).until(EC.invisibility_of_element_located((By.XPATH, alertBox_xpath)))


@step('Validate that error message is "{expectedText}"')
def validate_error_message(context, expectedText):
    currentPage = GlobalVar.currentPage
    errorMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'errorMessage').text
    assert errorMessage.lower() == expectedText.lower()


@step('Navigate to Manage Audit Configs page')
def navigate_to_configs(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'AuditRemediation').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'ManageAuditConfigs').click()
    page_title_validation(context, 'ManageAuditConfigs', 'MANAGE AUDIT CONFIGURATIONS')
    currentPage = GlobalVar.currentPage


@step('Assert that device parameters are available')
def assert_parameters(context):
    global device_logging_config
    currentPage = GlobalVar.currentPage
    if addCustomer == {}:
        customer = context.csvRead[0].get("onboardingCustomer")
    else:
        customer = addCustomer['name']

    if addDevice == {}:
        device = context.csvRead[0].get("runBrownfieldDevice")
    else:
        device = addDevice['Device_Name']

    customerRouterIP = context.csvRead[0].get("customerRouterIP")
    device_logging_config = context.csvRead[0].get("loggingServer")
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBar')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(customer)
    context.baseReader.getElementByPropertyName(context, currentPage, 'CustomerVal').click()

    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'CustomerGroup')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceTab').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(device)
    context.baseReader.getElementByPropertyName(context, currentPage, 'DeviceVal').click()
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DeviceModel')

    WebDriverWait(context.driver, 50).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys('Customer Router')
    router_param_val = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                   'routerParamList').get_property('value')

    assert len(router_param_val) != 0
    assert router_param_val == customerRouterIP


@step('Verify that alert message appears with a success message')
def verify_alert(context):
    currentPage = GlobalVar.currentPage
    alert_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'successAlert')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, alert_xpath)))


@step('Validate that "{rule}" message is "{expectedText}"')
def remediation_not_available(context, rule, expectedText):
    currentPage = GlobalVar.currentPage
    noVoilation_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noVoilation')
    WebDriverWait(context.driver, 40).until(EC.invisibility_of_element_located((By.XPATH, noVoilation_xpath)))
    element_obj = context.baseReader.getElementByPropertyName(context, currentPage, 'Feature')
    WebDriverWait(context.driver, 40).until(EC.visibility_of((element_obj)))
    element_obj.click()
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, rule)
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    tacacs_error = context.baseReader.getElementByPropertyName(context, currentPage, rule).text
    if expectedText in tacacs_error:
        pass


@step('Updated details should be reflected in the list of Customers')
def serach_by_name(context):
    currentPage = GlobalVar.currentPage
    global auth_Group
    isMatched = False
    addCustomerWait = context.baseReader.readElementByPropertyName(currentPage, 'applyingChangesWait').get("value")
    WebDriverWait(context.driver, 60).until(EC.invisibility_of_element_located((By.XPATH, addCustomerWait)))

    searchObj = context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar')
    searchObj.clear()
    searchObj.send_keys(addCustomer.get('name'))

    searchedDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'searchedData')
    WebDriverWait(context.driver, 35).until(
        EC.text_to_be_present_in_element((By.XPATH, searchedDataXpath), addCustomer.get('name')))

    rowsXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'rows')
    rowSize = context.driver.find_elements(By.XPATH, rowsXpath)
    for i in range(0, len(rowSize)):
        cust_name = context.driver.find_element_by_xpath('//table/tbody/tr[' + str(i + 1) + ']//td[1]').text
        if cust_name == addCustomer.get('name'):
            if ((addCustomer.get("Customer_Region") == "alberta") and (
                    addCustomer.get("authGroup") == auth_Group)):
                isMatched = True
    assert isMatched == True


@step('Add tag for a device')
def device_tag(context):
    currentPage = GlobalVar.currentPage
    N = 7
    res = 'BHLCD_Tag_' + ''.join(random.choices(string.ascii_uppercase +
                                                string.digits, k=N))
    context.baseReader.getElementByPropertyName(context, currentPage, 'deviceTag').send_keys(res)


@step('Validate the status of device for success')
def validate_device_status_success(context):
    currentPage = GlobalVar.currentPage
    status = context.baseReader.getElementByPropertyName(context, currentPage, 'deviceStatus').text
    assert status == "Connected"


@step('Validate that device status is not connected')
def validate_device_status_failure(context):
    currentPage = GlobalVar.currentPage
    status = context.baseReader.getElementByPropertyName(context, currentPage, 'deviceStatus').text
    assert status == "Not Connected Retry.."


@step('Select "{value}" feature to Audit Job')
def select_AAA_to_audit(context, value):
    time.sleep(5)
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'allFeature').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'allFeature').click()
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()


@step('I click on Ok button to add audit job')
def click_on_Button_to_Add_Audit_job(context):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'commitOk').click()
    AuditJobTitle = context.baseReader.readElementByPropertyName(currentPage, "AuditJobTitle").get("value")
    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, AuditJobTitle)))


@step('Filter the jobs by audit job name')
def filter_audit_job_name(context):
    currentPage = GlobalVar.currentPage

    loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    WebDriverWait(context.driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

    AuditJobSearchXpath = context.baseReader.readElementByPropertyName(currentPage, "AuditJobSearch").get("value")
    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, AuditJobSearchXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'AuditJobSearch').send_keys(addAuditJob.get('auditJobName'))
    firstRow = context.baseReader.getElementByPropertyName(context, currentPage, 'AuditJobSelect').text
    assert firstRow == addAuditJob.get('auditJobName')


@step('navigate to the view by clicking "{value}"')
def navigate_To_runRemediate_via_link(context, value):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()
    linkTitleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'linkTitle')
    WebDriverWait(context.driver, 35).until(
        EC.visibility_of_element_located((By.XPATH, linkTitleXpath)))
    page_title_validation(context, 'RunRemediateAuditJobs', 'RUN & REMEDIATE AUDIT JOBS')
    currentPage = GlobalVar.currentPage


@step('Validate the Run Audit button & Job Name')
def validate_run_Audit_button(context):
    currentPage = GlobalVar.currentPage
    button = context.baseReader.getElementByPropertyName(context, currentPage, 'RunAuditButton').is_displayed()
    jobName = context.baseReader.getElementByPropertyName(context, currentPage, 'JobName').text
    if button == True:
        assert jobName == addAuditJob.get('auditJobName')


@step('Validate the audit status')
def validate_audit_status(context):
    currentPage = GlobalVar.currentPage
    status = context.baseReader.getElementByPropertyName(context, currentPage, 'auditStatus').text
    assert status == "Finished - Report Ready"


@step('I assign a customer group to the selected customer')
def assign_group(context):
    currentPage = GlobalVar.currentPage

    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'customerGroup')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys('Customer Group')

    context.baseReader.getElementByPropertyName(context, currentPage, 'groupDropdown').click()

    groupListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'groupDropdownList')
    groupList = context.driver.find_elements(By.XPATH, groupListXpath)
    for i in range(0, len(groupList)):
        if groupList[i].text == cust_grp_name:
            groupList[i].click()


@step('Filter a device and select a job to open its audit view for checking runtime')
def select_auditJob(context):
    currentPage = GlobalVar.currentPage
    auditJobScheduling = context.csvRead[0].get("auditJobScheduling")
    auditDeviceScheduling = context.csvRead[0].get("auditDeviceScheduling")

    context.baseReader.getElementByPropertyName(context, currentPage, 'FilterDeviceName').send_keys(
        auditDeviceScheduling)
    context.baseReader.getElementByPropertyName(context, currentPage, 'FilterJobs').click()

    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchinTable').send_keys(
        auditJobScheduling)
    jobValue_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'JobVal')
    WebDriverWait(context.driver, 35).until(
        EC.text_to_be_present_in_element((By.XPATH, jobValue_xpath), auditJobScheduling))
    context.baseReader.getElementByPropertyName(context, currentPage, 'JobVal').click()


@step('Select features to be added in the audit job for scheduling')
def select_features_audit_schedule(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'services').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'logging').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'ipBase').click()


@step('Navigate to device level and read value for "{param}"')
def read_param_val(context, param):
    currentPage = GlobalVar.currentPage
    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'DeviceModel')
    WebDriverWait(context.driver, 60).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    time.sleep(5)
    searchXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'SearchBar')
    WebDriverWait(context.driver, 35).until(EC.visibility_of_element_located((By.XPATH, searchXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(param)


@step('Validate the Add Device Homepage Title')
def add_device_homepage_load(context):
    global currentPage
    expectedValue = 'CPE AUDIT/REMEDIATION USE CASE'
    currentPage = 'Home' + 'Page'
    PageTitleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'PageTitle')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, PageTitleXpath)))
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'PageTitle').text
    assert expectedValue.lower() == actualValue.lower()
    Audit_Remediation_Homepage_Xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Audit_Remediation_Homepage')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, Audit_Remediation_Homepage_Xpath)))
    GlobalVar.currentPage = currentPage

@step('I should land on Home page for Unauthorized access')
def step_impl(context):
    url = 'lcdURL_' + sys.argv[2]
    context.driver.get(context.config.get(url))
    currentPage = 'UnAuthorizedAccessPage'
    time.sleep(5)
    unAuthUserId = context.csvRead[0].get("unAuth_user")
    unAuthPassword = context.csvRead[0].get("UnAuth_pass")
    if context.driver.title == 'Log in to TINAA Platform':
        context.baseReader.getElementByPropertyName(context, currentPage, 'UserName').send_keys(unAuthUserId)
        context.baseReader.getElementByPropertyName(context, currentPage, 'Password').send_keys(unAuthPassword)
        context.baseReader.getElementByPropertyName(context, currentPage, 'LoginButton').click()

@step('wait till the Login page is loaded')
def wait_till_login_is_loaded(context):
    currentPage = GlobalVar.currentPage
    loginTitleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'loginTitle')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, loginTitleXpath)))


@step('Select all features to be added in the audit job')
def select_allFeatures_audit_job(context):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'allFeature').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'allBase').click()


@step('Add Audit Job "{name}" and "{desc}" for all features')
def add_job_details(context, name, desc):
    global addAuditJob
    currentPage = GlobalVar.currentPage
    addAuditJobName = context.csvRead[0].get("addAuditJobName")
    context.baseReader.getElementByPropertyName(context, currentPage, name).clear()
    current_time = datetime.datetime.now()
    tempName = addAuditJobName + '_' + str(current_time).replace('.', ':')
    context.baseReader.getElementByPropertyName(context, currentPage, name).send_keys(tempName)
    addAuditJob['auditJobAllFeature'] = tempName

    addAuditJobDesc = context.csvRead[0].get("addAuditJobDesc")
    context.baseReader.getElementByPropertyName(context, currentPage, desc).clear()
    current_time = datetime.datetime.now()
    tempDesc = addAuditJobDesc + '_' + str(current_time).replace('.', ':')
    context.baseReader.getElementByPropertyName(context, currentPage, desc).send_keys(tempDesc)


@step('click on "{item}" and validate "{value}" for all features')
def validate_click(context, item, value):
    currentPage = GlobalVar.currentPage
    jobName = context.baseReader.getElementByPropertyName(context, currentPage, value).text
    assert addAuditJob['auditJobAllFeature'] == jobName
    context.baseReader.getElementByPropertyName(context, currentPage, item).click()


@step('Validate the Run Audit button & Job Name for all features')
def validate_run_Audit_button(context):
    currentPage = GlobalVar.currentPage
    button = context.baseReader.getElementByPropertyName(context, currentPage, 'RunAuditButton').is_displayed()
    jobName = context.baseReader.getElementByPropertyName(context, currentPage, 'JobName').text
    if button == True:
        assert jobName == addAuditJob.get('auditJobAllFeature')


@step('Filter the jobs by audit job name for all features')
def filter_audit_job_name(context):
    currentPage = GlobalVar.currentPage

    loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
    WebDriverWait(context.driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

    AuditJobSearchXpath = context.baseReader.readElementByPropertyName(currentPage, "AuditJobSearch").get("value")
    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, AuditJobSearchXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'AuditJobSearch').send_keys(
        addAuditJob.get('auditJobAllFeature'))
    firstRow = context.baseReader.getElementByPropertyName(context, currentPage, 'AuditJobSelect').text
    assert firstRow == addAuditJob.get('auditJobAllFeature')


@step('Search the "{job}" job and open its Audit Job view')
def filter_job(context, job):
    global parallelJobs
    currentPage = GlobalVar.currentPage

    if addAuditJob == {}:
        parallelJobs[job] = context.csvRead[0].get('auditJob' + job)
    else:
        parallelJobs['first'] = addAuditJob.get('auditJobName')
        parallelJobs['second'] = addAuditJob.get('auditJobAllFeature')

    context.baseReader.getElementByPropertyName(context, currentPage, 'AuditJobSearch').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'AuditJobSearch').send_keys(parallelJobs[job])
    jobValXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'AuditJobSelect')
    WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, jobValXpath), parallelJobs[job]))
    context.baseReader.getElementByPropertyName(context, currentPage, 'AuditJobSelect').click()
    auditJobTitle = context.baseReader.readElementByPropertyName(currentPage, "auditJobTitle").get("value")
    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, auditJobTitle)))


@step('Open a new tab and navigate to "{page}" page')
def open_new_tab(context, page):
    currentPage = GlobalVar.currentPage
    context.driver.execute_script("window.open('');")
    context.driver.switch_to.window(context.driver.window_handles[1])
    context.driver.get(runJobPageURL)
    time.sleep(5)


@step('Run the "{job}" job for parallel execution')
def run_parallel_jobs(context, job):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'RunAudit').click()
    context.baseReader.getElementByPropertyName(context, currentPage, "useCLI").click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'startAudit').click()


@step('Wait till audit status for "{job}" job displays "{status}"')
def wait_for_status(context, job, status):
    global jobEndTime
    currentPage = GlobalVar.currentPage
    finishedReportReady = context.baseReader.readElementByPropertyName(currentPage, "finishedReportReady").get("value")
    WebDriverWait(context.driver, 360).until(
        EC.visibility_of_element_located((By.XPATH, finishedReportReady)))
    title = context.baseReader.getElementByPropertyName(context, currentPage, 'finishedReportReady').text
    assert title == "Finished - Report Ready"
    jobEndTime[job] = datetime.datetime.now()


@step('Switch to "{index}" tab')
def switch_tab(context, index):
    currentPage = GlobalVar.currentPage
    if index == 'first':
        context.driver.switch_to.window(context.driver.window_handles[0])
    elif index == 'second':
        context.driver.switch_to.window(context.driver.window_handles[1])
    time.sleep(2)


@step('Close "{index}" tab')
def close_tab(context, index):
    currentPage = GlobalVar.currentPage
    context.driver.close()
    context.driver.switch_to.window(context.driver.window_handles[0])


@step('Validate that "{job1}" job finished before "{job2}" job')
def validate_audit_job_status(context, job1, job2):
    currentPage = GlobalVar.currentPage
    assert jobEndTime.get(job1) < jobEndTime.get(job2)


@step('I define "{param}" value under the selected customer')
def define_logging_server(context, param):
    global loggingServerVal
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'SearchBar').send_keys(param)

    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'loggingHeading')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))

    logging_val = context.baseReader.getElementByPropertyName(context, currentPage, 'loggingParamList').text
    loggingServerVal = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

    if len(logging_val) == 0:
        context.baseReader.getElementByPropertyName(context, currentPage, 'plusButton').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'inputBox').send_keys(loggingServerVal)
        context.baseReader.getElementByPropertyName(context, currentPage, 'plusButton').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'inputBox').send_keys(Keys.ESCAPE)
    else:
        context.baseReader.getElementByPropertyName(context, currentPage, 'plusButton').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'inputBox').send_keys(loggingServerVal)
        context.baseReader.getElementByPropertyName(context, currentPage, 'plusButton').click()
        context.baseReader.getElementByPropertyName(context, currentPage, 'inputBox').send_keys(Keys.ESCAPE)
        loggingServerVal = context.baseReader.getElementByPropertyName(context, currentPage, 'loggingParamList').text


@step('Filter the audit job to open its Audit Job view')
def filter_job(context):
    global reverseRemediateJob
    currentPage = GlobalVar.currentPage
    if addDevice == {}:
        runRemediateDevice = context.csvRead[0].get("runRemediateDevice")
    else:
        runRemediateDevice = addDevice['Device_Name']

    context.baseReader.getElementByPropertyName(context, currentPage, 'FilterDeviceName').send_keys(runRemediateDevice)
    context.baseReader.getElementByPropertyName(context, currentPage, "filterJobsButton").click()
    loading = context.baseReader.readElementByPropertyName(currentPage, "loading").get("value")
    WebDriverWait(context.driver, 35).until(EC.invisibility_of_element_located((By.XPATH, loading)))

    if addAuditJob == {}:
        reverseRemediateJob = context.csvRead[0].get('reverseRemediateJob')
    else:
        reverseRemediateJob = addAuditJob.get('auditJobName')

    context.baseReader.getElementByPropertyName(context, currentPage, 'AuditJobSearch').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'AuditJobSearch').send_keys(reverseRemediateJob)
    jobValXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'AuditJobSelect')
    WebDriverWait(context.driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, jobValXpath), reverseRemediateJob))
    context.baseReader.getElementByPropertyName(context, currentPage, 'AuditJobSelect').click()
    auditJobTitle = context.baseReader.readElementByPropertyName(currentPage, "auditJobTitle").get("value")
    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, auditJobTitle)))


@step('Click on "{feature}" feature to open its Violations table')
def violations_table(context, feature):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'remFeature').click()
    violationsTitle = context.baseReader.readElementByPropertyName(currentPage, "violations").get("value")
    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, violationsTitle)))


@step('Assert that "{remBtn}" is available on "{feature}" rule')
def assert_rev_remediation(context, remBtn, feature):
    currentPage = GlobalVar.currentPage
    ruleAudit = context.csvRead[0].get('ruleAudit')
    ruleListXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'ruleList')
    ruleList = context.driver.find_elements(By.XPATH, ruleListXpath)
    for i in range(0, len(ruleList)-1):
        if ruleAudit in ruleList[i].text:
            assert remBtn in ruleList[i].text


@step('Click on "{button}" button to open reverse remediation results table')
def open_reverse_remediation_result(context, button):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, button).click()

    element_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'confirmButton')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, 'confirmButton').click()

    alert_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'reverseRemAlert')
    WebDriverWait(context.driver, 60).until(EC.invisibility_of_element_located((By.XPATH, alert_xpath)))

    title_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'resultTableTitle')
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, title_xpath)))

    searchBar_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'searchBar')
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, searchBar_xpath)))


@step('Filter "{param}" and assert that "{deviationOption}" is available')
def validate_remediation_result(context, param, deviationOption):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'searchBar').click()
    context.baseReader.getElementByPropertyName(context, currentPage, 'searchBar').clear()
    context.baseReader.getElementByPropertyName(context, currentPage, 'searchBar').send_keys(param)
    cellValue = context.baseReader.getElementLocatorValue(context, currentPage, 'paramCellValue')
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, cellValue), param))
    deviationXpath = context.baseReader.getElementLocatorValue(context, currentPage, deviationOption)
    WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, deviationXpath)))


@step('Wait for popup and click on "{button}" button')
def wait_for_popup(context, button):
    currentPage = GlobalVar.currentPage
    popupXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'popupBox')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, popupXpath)))
    buttonXpath = context.baseReader.getElementLocatorValue(context, currentPage, button)
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, buttonXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, button).click()
    noData_xpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
    WebDriverWait(context.driver, 40).until(EC.visibility_of_element_located((By.XPATH, noData_xpath)))
