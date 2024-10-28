import time

from behave import *
from random import randint

from selenium.common.exceptions import WebDriverException

from features.steps.bi.bi_uiFunctional import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from features.steps.globalVar import GlobalVar

# declared variables
loginStatus = False
RequestID = {}
testParams = {}
testCase = None
flag = False
qos = {}
prefixes = {}
counter = 1


def generate_random_ip():
    return '.'.join(
        str(randint(0, 255)) for _ in range(4)
    )


@step("I read test data for BI_CLM UI testcase")
def step_impl(context):
    global testCase
    testCase = context.feature.filename.split('_')[3]
    if "ui" in GlobalVar.testComponent[0].lower() or "e2e" in GlobalVar.testComponent[0].lower():
        GlobalVar.testParams = context.csvRead[int(testCase) - 1]
    else:
        GlobalVar.testParams = context.csvReadAPI[int(testCase) - 1]
    GlobalVar.test_case = testCase
    GlobalVar.testParams[GlobalVar.test_case] = {}


@step('I go to "{current}" page')
def change_currentPage(context, current):
    global currentPage
    currentPage = current + 'Page'
    GlobalVar.currentPage = currentPage
    delay(5)


@step('I should land on "{page}" page')
def step_impl(context, page):
    global loginStatus
    currentPage = "LandingPage"
    url = '{}_url_{}'.format(GlobalVar.testComponent[1].lower().split("_")[0], sys.argv[2])
    context.driver.get(context.config.get(url))
    pageHeadingXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'pageHeading')
    pageHeading = WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, pageHeadingXpath))).text

    if pageHeading.lower() != page.lower():
        LoginXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Login')
        WebDriverWait(context.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, LoginXpath)))
        time.sleep(5)
        context.baseReader.getElementByPropertyName(context, currentPage, 'Login').click()
        currentPage = 'KeycloakLoginPage'
        titleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'PageTitle')
        WebDriverWait(context.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, titleXpath)))

        userType = GlobalVar.testParams.get("userType")
        username = context.envReader.get(f'TestUserName{userType}')
        password = context.envReader.get(f'TestUserPass{userType}')
        usernameXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'UserName')
        WebDriverWait(context.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, usernameXpath))).send_keys(username)
        context.baseReader.getElementByPropertyName(context, currentPage, 'Password').send_keys(password)
        context.baseReader.getElementByPropertyName(context, currentPage, 'LoginButton').click()

        titleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'title')
        WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, titleXpath)))


@step('I validate the "{field}" field "{messageType}" message')
def step_impl(context, field, messageType):
    currentPage = GlobalVar.currentPage
    messageXpath = context.baseReader.getElementLocatorValue(context, currentPage, f"{field}{messageType}".strip())

    actualText = WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, messageXpath))).text
    expectedText = GlobalVar.testParams.get(f"{field}_{messageType}")
    # expectedText = f"{field} is required"
    assert actualText.lower() == expectedText.lower()


@step('I wait for the "{page}" to load')
def step_impl(context, page):
    currentPage = GlobalVar.currentPage
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noData")
    context.driver.implicitly_wait(0)
    WebDriverWait(context.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, noDataXpath)))


@step('Wait for the "{popup}" popup to appear')
def wait_for_element(context, popup):
    # delay(3)
    currentPage = GlobalVar.currentPage
    print(popup)
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, popup)
    element = WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))
    return element


@step('I enter the details and click "{action}"')
def step_impl(context, action):
    currentPage = GlobalVar.currentPage
    randomText = "".join([random.choice(string.ascii_lowercase) for i in range(10)])
    context.baseReader.getElementByPropertyName(context, currentPage, "subject").send_keys(randomText)
    context.baseReader.getElementByPropertyName(context, currentPage, "description").send_keys(randomText)
    context.baseReader.getElementByPropertyName(context, currentPage, action).click()


@step('I edit the field value of "{locator}" and set it to "{newValue}"')
def step_impl(context, locator, newValue):
    currentPage = GlobalVar.currentPage
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, locator)
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))

    if newValue == 'NULL':
        delay(5)
        context.baseReader.getElementByPropertyName(context, currentPage, locator).send_keys(Keys.CONTROL, "a",
                                                                                             Keys.DELETE)
    else:
        context.baseReader.getElementByPropertyName(context, currentPage, locator).send_keys(Keys.CONTROL, "a",
                                                                                             Keys.DELETE)
        delay(5)
        context.baseReader.getElementByPropertyName(context, currentPage, locator).send_keys(newValue)

    context.driver.find_element(by=By.ID, value='btnSave').click()
    GlobalVar.toast_msg = ''
    try:
        toast_error = WebDriverWait(context.driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "toast-error")))
        GlobalVar.toast_msg = f'Toast error message: {toast_error.text}'
    except:
        pass


def delay(second):
    time.sleep(second)


@step('I validate that "{popup_type}" popup message appears')
def step_impl(context, popup_type):
    if GlobalVar.toast_msg:
        if popup_type in GlobalVar.toast_msg:
            print(GlobalVar.toast_msg)
        else:
            raise ValueError


@step('I validate the "{alertType}" "{messageType}" alert "{message}"')
def step_impl(context, alertType, messageType, message):
    elementMessage = wait_for_element(context, f"{alertType}{messageType}{message}")
    expectedText = GlobalVar.testParams.get(f"{alertType}{messageType}{message}")
    print(elementMessage.text)
    print(expectedText)

    assert elementMessage.text.lower().strip() == expectedText.lower().strip()


@step('I validate that "{view}" is "{visibility}"')
def step_impl(context, view, visibility):
    currentPage = GlobalVar.currentPage
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, view)
    if "not" in visibility:
        WebDriverWait(context.driver, 20).until(EC.invisibility_of_element_located((By.XPATH, elementXpath)))
    else:
        WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))


@step('I navigate to "{view}" view')
def step_impl(context, view):
    currentPage = GlobalVar.currentPage
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, view)
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, elementXpath))).click()


@step('I enter "{user}" details for "{role}" role')
def step_impl(context, user, role):
    currentPage = GlobalVar.currentPage
    userName = GlobalVar.testParams.get('userName')

    context.baseReader.getElementByPropertyName(context, currentPage, user).send_keys(userName)
    # select the user role
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, f'{role}CheckBox')
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, elementXpath))).click()

    # select status bar to activate the account
    context.baseReader.getElementByPropertyName(context, currentPage, 'statusSlider').click()


@step('I validate that all the fields should be clear')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    checkText = context.baseReader.getElementByPropertyName(context, currentPage, 'userName')
    if checkText != None:
        context.baseReader.getElementByPropertyName(context, currentPage, 'userName').clear()
        context.baseReader.getElementByPropertyName(context, currentPage, 'readCheckBox').click()


@step('I filter the "{User}" by "{user}" and user "{visibility}" in the results')
def step_impl(context, User, user, visibility):
    currentPage = GlobalVar.currentPage
    if User == "User":
        userName = "x257228"
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%"+"===="+userName)
        delay(5)
        searchBoxXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'searchBox')
        WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, searchBoxXpath))).send_keys(
            userName)
        # context.baseReader.getElementByPropertyName(context, currentPage, 'searchBox').send_keys(
        #     userName)
        if "does'nt" in visibility:
            elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
            WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))

        else:
            elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'userFilterResult')
            WebDriverWait(context.driver, 15).until(
                EC.text_to_be_present_in_element((By.XPATH, elementXpath), userName))

    if User == "Customer":
        customer_name = GlobalVar.testParams.get(user)
        delay(10)
        searchBoxXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'searchBox')
        val = WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, searchBoxXpath)))
        val.send_keys(customer_name)
        # context.baseReader.getElementByPropertyName(context, currentPage, 'searchBox').send_keys(
        #     userName)
        if "does'nt" in visibility:
            elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
            WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))

        else:
            elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'userFilterResult')
            WebDriverWait(context.driver, 30).until(
                EC.text_to_be_present_in_element((By.XPATH, elementXpath), customer_name))

    if User == "Services":
        service_name = GlobalVar.testParams.get("CSID")
        delay(5)
        searchBoxXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'searchBox')
        val = WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, searchBoxXpath)))
        val.send_keys(service_name)
        # context.baseReader.getElementByPropertyName(context, currentPage, 'searchBox').send_keys(
        #     userName)
        if "does'nt" in visibility:
            elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
            WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))

        else:
            elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'userFilterResult')
            WebDriverWait(context.driver, 15).until(
                EC.text_to_be_present_in_element((By.XPATH, elementXpath), service_name))


@step('I clear the "{value}" field')
def step_impl(context, value):
    currentPage = GlobalVar.currentPage
    delay(2)
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, value)
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, elementXpath))).send_keys(
        Keys.CONTROL, "a", Keys.DELETE)
    delay(2)


@step('I validate that the portal user role "{role}" is "{roleState}"')
def step_impl(context, role, roleState):
    currentPage = GlobalVar.currentPage
    time.sleep(5)
    flag = context.baseReader.getElementByPropertyName(context, currentPage, f"{role}RoleCheck").is_selected()
    if roleState == "checked":
        assert flag == True
    elif roleState == "unchecked":
        assert flag == False


@step('I validate that the portal user account "{stateName}" is "{stateValue}"')
def step_impl(context, stateName, stateValue):
    global flag
    currentPage = GlobalVar.currentPage
    userName = GlobalVar.testParams.get("userName")

    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'noData')
    WebDriverWait(context.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, elementXpath)))
    delay(5)

    status = context.baseReader.getElementByPropertyName(context, currentPage, 'stateSelector').is_selected()

    context.driver.implicitly_wait(0)
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'userFilterResult')
    WebDriverWait(context.driver, 25).until(EC.text_to_be_present_in_element((By.XPATH, elementXpath), userName))

    if stateValue == "disabled":
        assert status == False

    elif stateValue == "enabled":
        assert status == True

    # state['disabled'] = GlobalVar.testParams.get('rgbWhite')
    # state['enabled'] = GlobalVar.testParams.get('rgbBlack')

    # element = context.driver.find_element(By.XPATH, elementXpath)
    # stateColor = element.value_of_css_property('background-color')
    # assert stateColor.strip() == state[stateValue].strip()


@step('I search for "{searchParam}" parameter through "{advanceFilter}"')
def step_impl(context, searchParam, advanceFilter):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, advanceFilter).click()
    context.baseReader.getElementByPropertyName(context, currentPage, searchParam).send_keys(
        GlobalVar.testParams[searchParam])
    context.baseReader.getElementByPropertyName(context, currentPage, "SearchResult").click()


@step('Wait for the "{searchParam}" search results to appear')
def step_impl(context, searchParam):
    currentPage = GlobalVar.currentPage
    loaderXpath = context.baseReader.getElementLocatorValue(context, currentPage, "loader")
    try:
        WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, loaderXpath)))
        WebDriverWait(context.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))
        firstResultXpath = context.baseReader.getElementLocatorValue(context, currentPage, f"first{searchParam}Result")
        WebDriverWait(context.driver, 15).until(
            EC.text_to_be_present_in_element_value((By.XPATH, firstResultXpath), GlobalVar.testParams[searchParam]))
        firstResult = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                  f"first{searchParam}Result").text
        assert GlobalVar.testParams[searchParam] in searchParam

    except:
        firstResultXpath = context.baseReader.getElementLocatorValue(context, currentPage, f"first{searchParam}Result")
        WebDriverWait(context.driver, 15).until(
            EC.text_to_be_present_in_element((By.XPATH, firstResultXpath), GlobalVar.testParams[searchParam]))


@step('Validate that the "{precedence}" generated "{element}" is displayed')
def Validate_generated_RequestId(context, precedence, element):
    global RequestID
    currentPage = GlobalVar.currentPage
    xpath = context.baseReader.getElementLocatorValue(context, currentPage, f"first{element}Result")
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, f"first{element}Result").text

    if GlobalVar.requestId is None:
        assert actualValue == RequestID[precedence + element]
    else:
        assert actualValue == GlobalVar.requestId

    RequestID[precedence + element] = actualValue


@step('I click on the "{role}" checkbox')
def step_impl(context, role):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, f"{role}Selector").click()


@step('Validate that "{element}" value should be "{expectedValue}"')
def validate_data(context, element, expectedValue):
    currentPage = GlobalVar.currentPage
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, f"first{element}").text
    if element.lower() == "user":
        assert actualValue == GlobalVar.api_dict["request_params"]["user_id"]
    else:
        assert actualValue.lower().strip() == expectedValue.lower().strip()


@step('I click to "{actionButton}" the "{expectedPopup}"')
def step_impl(context, actionButton, expectedPopup):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, actionButton).click()
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, expectedPopup.replace(" ", ""))
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))


@step('Validate that correct "{field}" value is displayed')
def step_impl(context, field):
    currentPage = GlobalVar.currentPage
    expectedValue = GlobalVar.testParams.get(f"{field}Value")
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, f"{field}ParamValue")
    element = WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))
    assert element.text.lower().strip() == expectedValue.lower().strip()


@step('I click on the "{field}" and read "{popupType}" message')
def step_impl(context, field, popupType):
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, f"first{field}").click()
    delay(2)
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, popupType.replace(" ", ""))
    WebDriverWait(context.driver, 5).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))

    element = context.baseReader.getElementByPropertyName(context, currentPage,
                                                          "{}message".format(popupType.replace(" ", "")))
    # assert element.text.lower().strip()


@step('I fetch the information of first record from "{page}"')
def step_impl(context, page):
    currentPage = GlobalVar.currentPage
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noData")
    WebDriverWait(context.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, noDataXpath)))
    delay(5)
    if page == "Service Details page":
        GlobalVar.customer['csid'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                 "firstCSIDResultService").text
        GlobalVar.customer['customer'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                     "firstCustomerResultService").text
        GlobalVar.customer['name'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                 "firstNameResultService").text

    elif page == "WorkOrders Details page":
        GlobalVar.transactions['request_id'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                           "request_id_transactions").text
        GlobalVar.transactions['csid'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                     "csid_transactions").text
        GlobalVar.transactions['customer_name'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                              "customer_name_transactions").text
        GlobalVar.transactions['operation_type'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                               "operation_type_transactions").text
        GlobalVar.transactions['network_type'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                             "network_type_transactions").text
        GlobalVar.transactions['status'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                       "statusTransactions").text
        print("##########################1234##########################")
    print(currentPage)


@step('I search the Service by using "{param}" value from advance filter')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    if param != "non_existing_CSID":
        if param == "CSID":
            csid = GlobalVar.customer.get("csid")
            elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, "advanceFilterCSID")
            WebDriverWait(context.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, elementXpath)))
            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCSID').send_keys(
                Keys.CONTROL, "a", Keys.DELETE)
            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCSID').send_keys(csid)

        elif param == "Customer":
            csid = GlobalVar.customer.get("customer")
            elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, "advanceFilterCustomer")
            WebDriverWait(context.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, elementXpath)))

            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCustomer').send_keys(
                Keys.CONTROL, "a", Keys.DELETE)
            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCustomer').send_keys(csid)

        elif param == "CSID_Customer_Name":
            customer = GlobalVar.customer.get("customer")
            csid = GlobalVar.customer.get("csid")
            name = GlobalVar.customer.get("name")

            elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, "advanceFilterCustomer")
            WebDriverWait(context.driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, elementXpath)))

            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCustomer').send_keys(
                Keys.CONTROL, "a", Keys.DELETE)
            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCSID').send_keys(
                Keys.CONTROL, "a", Keys.DELETE)
            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterName').send_keys(
                Keys.CONTROL, "a", Keys.DELETE)

            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCustomer').send_keys(
                customer)
            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCSID').send_keys(csid)
            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterName').send_keys(name)

        context.baseReader.getElementByPropertyName(context, currentPage, 'searchResultButton').click()
        noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noData")
        WebDriverWait(context.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, noDataXpath)))

    elif param == "non_existing_CSID":
        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCSID').send_keys("Dummy_CSID")
        context.baseReader.getElementByPropertyName(context, currentPage, 'searchResultButton').click()
        noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noData")
        WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, noDataXpath)))


@step('I validate that the searched result should appear for "{param}" value in Service details table')
def step_imp(context, param):
    currentPage = GlobalVar.currentPage
    global flag
    if param == "CSID":
        csids = context.baseReader.getElementLocatorValue(context, currentPage, "allCSID")
        rows = context.driver.find_elements(By.XPATH, csids)
        for i in range(1, len(rows) + 1):
            id = context.driver.find_element(By.XPATH, "//tbody/tr[" + str(i) + "]/td[1]").text
            if (GlobalVar.customer.get("csid")).strip() == id.strip():
                flag = True
                break
            else:
                raise Exception("CSID doesn't exist!!")

    elif param == "CSID_Customer_Name":
        csids = context.baseReader.getElementLocatorValue(context, currentPage, "allCSID")
        rows = context.driver.find_elements(By.XPATH, csids)
        for i in range(1, len(rows) + 1):
            id = context.driver.find_element(By.XPATH, "//tbody/tr[" + str(i) + "]/td[1]").text
            customer = context.driver.find_element(By.XPATH, "//tbody/tr[" + str(i) + "]/td[2]").text
            name = context.driver.find_element(By.XPATH, "//tbody/tr[" + str(i) + "]/td[3]").text

            if id.strip() == (GlobalVar.customer.get("csid")).strip() and customer.strip() == (
            GlobalVar.customer.get("customer")).strip() and \
                    name.strip() == (GlobalVar.customer.get("name")).strip():
                flag = True
                break
            else:
                raise Exception("CSID & Customer name doesn't exist")

    elif param == "Customer":
        csids = context.baseReader.getElementLocatorValue(context, currentPage, "allCSID")
        rows = context.driver.find_elements(By.XPATH, csids)
        for i in range(1, len(rows) + 1):
            customer = context.driver.find_element(By.XPATH, "//tbody/tr[" + str(i) + "]/td[2]").text
            if customer.strip() == (GlobalVar.customer.get("customer")).strip():
                flag = True
                break
            else:
                raise Exception("Customer doesn't exist")

    elif param == "non_existing_CSID":
        noDataText = context.baseReader.getElementByPropertyName(context, currentPage, "noDataFound").text
        if noDataText != None:
            flag = True
        else:
            raise Exception("Data exist")

    assert flag == True


@step('I navigate to the "{param}" page')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noData")
    WebDriverWait(context.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, noDataXpath)))
    if param == "transaction":
        tr = context.baseReader.getElementByPropertyName(context, currentPage, 'transactionSidebar')
        tr.click()

    elif param == "User management":
        context.baseReader.getElementByPropertyName(context, currentPage, 'UserManagementSidebar').click()
    elif param == "Service Update":
        context.baseReader.getElementByPropertyName(context, currentPage, 'serviceUpdateSidebar').click()
    time.sleep(5)


@step('I search WorkOrders details by using "{param}" value from advance filter')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    print(param)
    if param != "non_existing_values":
        if param == "CSID":
            csid = GlobalVar.transactions.get("csid")
            context.baseReader.getElementByPropertyName(context, currentPage,
                                                        'advanceCustomerServiceIdTransactions').send_keys(csid)

        elif param == "Operation_Type_and_Status":
            delay(10)
            print(currentPage)
            status = GlobalVar.testParams.get("status")
            print("*******************")
            print(status)
            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceStatus').send_keys(status)
            operation = GlobalVar.testParams.get("OperationType")
            print(operation)
            print("*******************")
            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceOperationType').send_keys(
                operation)
            delay(3)

        elif param == "OperationType_Status_NetworkType":
            operationType = GlobalVar.transactions.get('operation_type')
            networkType = GlobalVar.transactions.get('network_type')
            status = GlobalVar.transactions.get('status')
            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceOperationType').send_keys(
                operationType)
            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceNetworkType').send_keys(
                networkType)
            context.baseReader.getElementByPropertyName(context, currentPage, 'advanceStatus').send_keys(status)

        context.baseReader.getElementByPropertyName(context, currentPage, 'searchResultButton').click()
        noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noData")
        WebDriverWait(context.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, noDataXpath)))

    elif param == "OperationType_Status":
        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceOperationType').send_keys("DummyOT")
        delay(3)
        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceNetworkType').send_keys("DummyNT")
        delay(3)
        context.baseReader.getElementByPropertyName(context, currentPage, 'searchResultButton').click()




    elif param == "Status":
        status = GlobalVar.testParams.get("status")
        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceStatus').send_keys(status)
        delay(3)


    elif param == "non_existing_values":
        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceOperationType').send_keys("DummyOT")
        time.sleep(3)
        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceNetworkType').send_keys("DummyNT")
        time.sleep(3)
        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceStatus').send_keys("DummyStatus")
        time.sleep(3)

        context.baseReader.getElementByPropertyName(context, currentPage, 'searchResultButton').click()
        noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noData")
        WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, noDataXpath)))


@step('I validate that the searched result should appear for "{param}" value in WorkOrders details table')
def step_imp(context, param):
    currentPage = GlobalVar.currentPage
    global flag
    if param == "CSID":
        csids = context.baseReader.getElementLocatorValue(context, currentPage, "allCSID")
        rows = context.driver.find_elements(By.XPATH, csids)
        for i in range(1, len(rows) + 1):
            id = context.driver.find_element(By.XPATH, "//tbody/tr[" + str(i) + "]/td[2]").text
            if GlobalVar.transactions.get("csid") == id:
                flag = True
                context.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                break
            else:
                raise Exception("Result not matched")

    elif param == "OperationType_Status_NetworkType":
        csids = context.baseReader.getElementLocatorValue(context, currentPage, "allCSID")
        rows = context.driver.find_elements(By.XPATH, csids)

        for i in range(1, len(rows) + 1):
            operationType = context.driver.find_element(By.XPATH, "//tbody/tr[" + str(i) + "]/td[6]").text
            networkType = context.driver.find_element(By.XPATH, "//tbody/tr[" + str(i) + "]/td[9]").text
            status = context.driver.find_element(By.XPATH, "//tbody/tr[" + str(i) + "]/td[11]").text

            if operationType.strip() == (
            GlobalVar.transactions.get("operation_type")).strip() and networkType.strip() == (
            GlobalVar.transactions.get("network_type")).strip() and status.strip() == (
            GlobalVar.transactions.get("status")).strip():
                flag = True
                break
            else:
                raise Exception("Result not matched")

    elif param == "non_existing_values":
        noDataText = context.baseReader.getElementByPropertyName(context, currentPage, "noDataFound").text
        if noDataText != None:
            flag = True
        else:
            raise Exception("Data exist")

    assert flag == True


@step('I search the service-id to validate the Update parameters')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    csid = GlobalVar.testParams['serviceId']
    customer = GlobalVar.testParams['Customer']
    serviceName = GlobalVar.testParams['ServiceName']

    context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCustomer').send_keys(customer)
    context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCSID').send_keys(csid)
    context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterName').send_keys(serviceName)

    context.baseReader.getElementByPropertyName(context, currentPage, 'searchResultButton').click()
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noData")
    WebDriverWait(context.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, noDataXpath)))


@step('I search and validate for a non existing service-id {csid}')
def step_impl(context, csid):
    not_found_flag = False
    currentPage = GlobalVar.currentPage
    # csid = GlobalVar.testParams['serviceId']
    context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCSID').send_keys(csid)
    context.baseReader.getElementByPropertyName(context, currentPage, 'searchResultButton').click()
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noData")
    try:
        # Wait for the element to appear for up to 10 seconds
        element = WebDriverWait(context.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, noDataXpath))
        )
        # Check if the element contains "no data found"
        start_time = time.time()
        while "no data found" in element.text.lower():
            # If it contains "no data found", wait for a second and check again
            time.sleep(1)
            elapsed_time = time.time() - start_time
            if elapsed_time > 10:
                print(f'service {csid} not found')
                break
    except:
        # If the element doesn't appear within 10 seconds, return True
        return True


@step('Validate that the "{value}" field should be enable')
def step_impl(context, value):
    currentPage = GlobalVar.currentPage
    global qos, prefixes
    if value == "QoS":
        qos['ingressOverrideRate'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                 "qosIngressOverrideRate").is_enabled()
        qos['egressOverrideRate'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                "qosEgressOverrideRate").is_enabled()
        assert qos.get('ingressOverrideRate') == True
        assert qos.get('ingressOverrideRate') == True
    elif value == "Prefixes":
        prefixes['ipv4ProviderPrefixes_0'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                         "ipv4ProviderPrefixes_0").is_enabled()
        prefixes['ipv4ProviderPrefixes_1'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                         "ipv4ProviderPrefixes_1").is_enabled()
        prefixes['ipv4CustomerPrefixes_0'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                         "ipv4CustomerPrefixes_0").is_enabled()
        prefixes['ipv4CustomerPrefixes_1'] = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                                         "ipv4CustomerPrefixes_1").is_enabled()
        assert prefixes.get('ipv4ProviderPrefixes_0') == True
        assert prefixes.get('ipv4ProviderPrefixes_1') == True
        assert prefixes.get('ipv4CustomerPrefixes_0') == True
        assert prefixes.get('ipv4CustomerPrefixes_1') == True


@step('I search the service by "{value}" only')
def step_impl(context, value):
    currentPage = GlobalVar.currentPage
    if value == "CSID":
        csid = GlobalVar.testParams['serviceId']
        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCSID').send_keys(csid)
    elif value == "Customer":
        customer = GlobalVar.testParams['Customer']
        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterCustomer').send_keys(customer)
    elif value == "ServiceName":
        serviceName = GlobalVar.testParams['ServiceName']
        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceFilterName').send_keys(serviceName)

    context.baseReader.getElementByPropertyName(context, currentPage, 'searchResultButton').click()
    noDataXpath = context.baseReader.getElementLocatorValue(context, currentPage, "noData")
    WebDriverWait(context.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, noDataXpath)))


@step('I update the Qos and prefix values of the selected service')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    # ingress = context.baseReader.getElementByPropertyName(context, currentPage, 'qosIngressOverrideRate').get_attribute("value")
    context.baseReader.getElementByPropertyName(context, currentPage, 'qosIngressOverrideRate').send_keys(Keys.CONTROL,
                                                                                                          "a",
                                                                                                          Keys.DELETE)
    context.baseReader.getElementByPropertyName(context, currentPage, 'qosIngressOverrideRate').send_keys(
        randint(100000, 500000))

    # egress = context.baseReader.getElementByPropertyName(context, currentPage, 'qosEgressOverrideRate').get_attribute("value")
    context.baseReader.getElementByPropertyName(context, currentPage, 'qosEgressOverrideRate').send_keys(Keys.CONTROL,
                                                                                                         "a",
                                                                                                         Keys.DELETE)
    context.baseReader.getElementByPropertyName(context, currentPage, 'qosEgressOverrideRate').send_keys(
        randint(100000, 500000))

    # ipv4ProviderPrefixes = context.baseReader.getElementByPropertyName(context, currentPage, 'ipv4ProviderPrefixes_1').get_attribute("value")
    context.baseReader.getElementByPropertyName(context, currentPage, 'ipv4ProviderPrefixes_1').send_keys(Keys.CONTROL,
                                                                                                          "a",
                                                                                                          Keys.DELETE)
    context.baseReader.getElementByPropertyName(context, currentPage, 'ipv4ProviderPrefixes_1').send_keys(
        generate_random_ip() + "/" + str(randint(10, 99)))

    # ipv4CustomerPrefixes = context.baseReader.getElementByPropertyName(context, currentPage, 'ipv4CustomerPrefixes_1').get_attribute("value")
    context.baseReader.getElementByPropertyName(context, currentPage, 'ipv4CustomerPrefixes_1').send_keys(Keys.CONTROL,
                                                                                                          "a",
                                                                                                          Keys.DELETE)
    context.baseReader.getElementByPropertyName(context, currentPage, 'ipv4CustomerPrefixes_1').send_keys(
        generate_random_ip() + "/" + str(randint(10, 99)))


@step('I validate that the alert message should appear for "{page}"')
def step_impl(context, page):
    global counter
    currentPage = GlobalVar.currentPage
    message = context.baseReader.getElementByPropertyName(context, currentPage, 'popupMessage').text
    print("Alert Message:", message)

    popupMessage = context.baseReader.getElementLocatorValue(context, currentPage, 'popupMessage')
    WebDriverWait(context.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, popupMessage)))

    context.baseReader.getElementByPropertyName(context, currentPage, 'yesConfirmationRequest').click()


@step('Fetch the request-id from the Total Requests table of Service Update Page')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    firstRequestServiceUpdateQueueXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                    'firstRequestServiceUpdateQueue')
    WebDriverWait(context.driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, firstRequestServiceUpdateQueueXpath)))
    delay(10)
    actions = ActionChains(context.driver)
    elementToHover = context.driver.find_element_by_xpath(firstRequestServiceUpdateQueueXpath)
    actions.move_to_element(elementToHover).perform()
    delay(5)
    requestId = context.baseReader.getElementByPropertyName(context, currentPage, 'requestIdToolTip').text
    GlobalVar.requestId = requestId


@step('Validate the popup message should appears for "{errorType}"')
def step_impl(context, errorType):
    currentPage = GlobalVar.currentPage
    toast_error = context.baseReader.getElementByPropertyName(context, currentPage, 'errorMessage').text
    assert GlobalVar.testParams.get("errorMessage") == toast_error


@step('I validate that the edit button should be disable for read-only user')
def step_impl(context):
    rows = context.driver.find_elements_by_xpath("//tbody/tr")

    for i in range(1, len(rows) + 1):
        my_element = context.driver.find_element_by_xpath("//tbody/tr[" + str(i) + "]/td[8]//div[@id='divEditService']")
        flag = my_element.get_attribute("class")
        assert flag == "btnPencilDisabled"
    print("Edit field is disabled for Read-only user")
    # btnPencilDisabled class is used when the editable field is disabled
    # editIcon is used when the editable field is enabled


@step('I validate that the "{value}" button should be clickable')
def step_impl(context, value):
    currentPage = GlobalVar.currentPage
    valueXpath = context.baseReader.getElementLocatorValue(context, currentPage, value)
    WebDriverWait(context.driver, 15).until(EC.element_to_be_clickable((By.XPATH, valueXpath)))
    time.sleep(5)


@step('Validate that the request-id should be similar to the request-id of created service')
def step_impl(context):
    currentPage = GlobalVar.currentPage

    cancelAlertRequestIdXpath = context.baseReader.getElementLocatorValue(context, currentPage, "cancelAlertRequestId")
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, cancelAlertRequestIdXpath)))

    expectedRequestsId = GlobalVar.requestId
    actualRequestId = context.baseReader.getElementByPropertyName(context, currentPage, "cancelAlertRequestId").text
    assert expectedRequestsId == actualRequestId


@step('I validate the pop-up message for "{param}"')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    popupMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage, "popupMessage")
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, popupMessageXpath)))

    expectedMessage = GlobalVar.testParams.get("errorMessage")
    actualMessage = context.baseReader.getElementByPropertyName(context, currentPage, "popupMessage").text

    assert expectedMessage == actualMessage


@step('I validate that the "{value}" button should not appear in the Display config box')
def step_impl(context, value):
    global flag
    currentPage = GlobalVar.currentPage
    valueXpath = context.baseReader.getElementLocatorValue(context, currentPage, value)
    WebDriverWait(context.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, valueXpath)))
    try:
        context.baseReader.getElementByPropertyName(context, currentPage, valueXpath).click()
    except:
        flag = True

    assert flag == True


@step('I fill the required parameter for Expected config box')
def step_impl(context):
    currentPage = GlobalVar.currentPage

    workOrderNumberXpath = context.baseReader.getElementLocatorValue(context, currentPage, "workOrderNumber")
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, workOrderNumberXpath)))

    context.baseReader.getElementByPropertyName(context, currentPage, "workOrderNumber").send_keys(
        generate_random_ip() + "/" + str(randint(10, 99)))

    letters = string.ascii_uppercase
    context.baseReader.getElementByPropertyName(context, currentPage, "description").send_keys(
        "TEST_" + ''.join(random.choice(letters) for i in range(5)))


@step('I validate that the created transaction should be in "{state}" state')
def step_impl(context, state):
    currentPage = GlobalVar.currentPage
    statusTransactionsXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'statusTransactions')
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, statusTransactionsXpath)))

    actualState = context.baseReader.getElementByPropertyName(context, currentPage, "statusTransactions").text
    assert actualState == state


@step('I wait for the transaction state to be changed to "{param}"')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    statusSubmittedXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'statusSubmitted')
    WebDriverWait(context.driver, 140).until(EC.invisibility_of_element_located((By.XPATH, statusSubmittedXpath)))

    #     if actualState == "Submitted":
    #         state_change(context)

    actualState = context.baseReader.getElementByPropertyName(context, currentPage, "statusTransactions").text
    print("Actual State", actualState)
    if param == "Failed":
        print("Status is changed to : Failed")
        assert actualState == "Failed"
    elif param == "Timeout":
        print("Status is changed to : Timeout")
        assert actualState == "Timeout"
    elif param == "Completed":
        print("Status is changed to : Completed")
        assert actualState == "Completed"


@step('I wait for the loader to be disabled')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    loaderXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'loader')
    WebDriverWait(context.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))


@step('I wait for the "{element}" to load and click on it')
def step_impl(context, element):
    currentPage = GlobalVar.currentPage
    delay(10)
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, element)

    button = context.driver.find_element_by_xpath(elementXpath)
    context.driver.execute_script("arguments[0].click();", button)


@step('I click on RollbackButton and "{expectedValue}" Modal should open')
def step_impl(context, expectedValue):
    currentPage = GlobalVar.currentPage
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'RollbackButton').click()
    expectedValueXpath = context.baseReader.getElementLocatorValue(context, currentPage, expectedValue)
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, expectedValueXpath)))
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, expectedValue).text

    assert expectedValue.lower() in (actualValue.replace(" ", "")).lower()


@step('I click on ServiceVersion and select Version option')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    actions = ActionChains(context.driver)
    ServiceDropDown = context.baseReader.getElementByPropertyName(context, currentPage, 'ServiceDropDown')
    actions.move_to_element(ServiceDropDown).click().perform()
    ServiceDropDownElement = context.baseReader.getElementByPropertyName(context, currentPage, 'ServiceDropDownElement')
    actions.move_to_element(ServiceDropDownElement).click().perform()


@step('I search the request by using "{param}" from Service Update Queue page')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    csid = GlobalVar.testParams.get("serviceId")
    simpleSearchXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'simpleSearch')
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, simpleSearchXpath)))

    if param == "CSID":
        context.baseReader.getElementByPropertyName(context, currentPage, "simpleSearch").send_keys(csid)
        delay(5)


@step('I validate that the loader should appear after clicking on "{param}" button')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    loaderXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'loader')
    WebDriverWait(context.driver, 15).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))


@step('I wait for the loader to be invisible')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    displayConfigLoaderXpath = context.baseReader.getElementLocatorValue(context, currentPage, "displayConfigLoader")
    WebDriverWait(context.driver, 150).until(EC.invisibility_of_element_located((By.XPATH, displayConfigLoaderXpath)))


@step('I validate that the CurrentConfig and ExpectedConfig status should change to "{param}"')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    currentConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'currentConfigs').text
    expectedConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'expectedConfig').text


@step('I wait for the "{param}" element to be visible')
def step_impl(context, param):
    time.sleep(5)
    currentPage = GlobalVar.currentPage
    paramXpath = context.baseReader.getElementLocatorValue(context, currentPage, param)
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, paramXpath)))


@step('I select the version from the dropdown to rollback the service')
def select_rollback_version(context):
    count = GlobalVar.counter
    currentPage = GlobalVar.currentPage
    currentVersion = context.baseReader.getElementByPropertyName(context, currentPage, "currentVersion").text
    context.baseReader.getElementByPropertyName(context, currentPage, "versionDropdown").click()
    delay(2)
    versionsList = context.baseReader.getElementLocatorValue(context, currentPage, 'versionsList')
    rows = context.driver.find_elements_by_xpath(versionsList)
    GlobalVar.versions = len(rows)
    for i in range(count, len(rows)):
        existingVersions = context.driver.find_element_by_xpath(
            '//div[@class="dropdown-list"]/ul[2]/li[' + str(i) + ']').text
        print("SelectedVersion:-", existingVersions)
        if currentVersion != existingVersions:
            print("Current version and selected versions are different")
            context.driver.find_element_by_xpath('//div[@class="dropdown-list"]/ul[2]/li[' + str(i) + ']').click()
            delay(5)
            break
        else:
            continue
    print("Total list of versions:", GlobalVar.versions)

    rollbackParameterInformationXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                  'rollbackParameterInformation')
    WebDriverWait(context.driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, rollbackParameterInformationXpath)))
    WebDriverWait(context.driver, 15).until(EC.element_to_be_clickable((By.XPATH, rollbackParameterInformationXpath)))
    delay(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'rollbackParameterInformation').click()

    rollbackConfirmationMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                                 'rollbackConfirmationMessage')
    WebDriverWait(context.driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, rollbackConfirmationMessageXpath)))
    WebDriverWait(context.driver, 15).until(EC.element_to_be_clickable((By.XPATH, rollbackConfirmationMessageXpath)))

    rollbackConfirmXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'rollbackConfirm')
    WebDriverWait(context.driver, 15).until(EC.element_to_be_clickable((By.XPATH, rollbackConfirmXpath)))
    delay(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'rollbackConfirm').click()

    popupMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'popupMessage')
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, popupMessageXpath)))

    alertMessage = context.baseReader.getElementByPropertyName(context, currentPage, 'popupMessage').text
    print("Alert Message:-", alertMessage)
    WebDriverWait(context.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, popupMessageXpath)))

    if alertMessage == "Rollback won't affect service parameters":
        GlobalVar.counter = GlobalVar.counter + 1
        select_rollback_version(context)
    time.sleep(5)


@step('I validate that the "{param}" should be disable')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    paramXpath = context.baseReader.getElementLocatorValue(context, currentPage, param)
    element = context.driver.find_element_by_xpath(paramXpath)
    status = element.get_attribute("class")
    assert status == "btnDisabled"


@step('I validate that the "{param}" button should not be visible for read-only user')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    try:
        paramXpath = context.baseReader.getElementLocatorValue(context, currentPage, param)
        WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, paramXpath)))
    except:
        print("Button does'nt exist for read only user!!!")


@step('I Validate that the Service state should be "{serviceState}"')
def step_impl(context, serviceState):
    currentPage = GlobalVar.currentPage
    currentState = context.baseReader.getElementByPropertyName(context, currentPage, "state").text
    assert currentState == serviceState


@step('Validate that the new Service version should be added under the list of versions')
def step_impl(context):
    currentPage = GlobalVar.currentPage

    context.baseReader.getElementByPropertyName(context, currentPage, "versionDropdown").click()

    versionsList = context.baseReader.getElementLocatorValue(context, currentPage, 'versionsList')
    rows = context.driver.find_elements_by_xpath(versionsList)

    assert len(rows) == int(GlobalVar.versions) + 1


@step('"{param}" response should be appear in the Display config results for the created request')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage

    if param == "In-progress":
        currentConfigsXpath = context.baseReader.getElementLocatorValue(context, currentPage, "currentConfigs")
        WebDriverWait(context.driver, 20).until(
            EC.text_to_be_present_in_element((By.XPATH, currentConfigsXpath), "In-Progress"))

        currentConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'currentConfigs').text
        expectedConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'expectedConfig').text
        print("Current Config:", currentConfig)
        print("Expected Config:", expectedConfig)

    else:
        displayConfigLoaderXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                             "displayConfigLoader")
        WebDriverWait(context.driver, 140).until(
            EC.invisibility_of_element_located((By.XPATH, displayConfigLoaderXpath)))

        currentConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'currentConfigs').text
        expectedConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'expectedConfig').text

        if param == "Timeout":
            currentConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'currentConfigs').text
            expectedConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'expectedConfig').text

        elif param == "Success":
            currentConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'currentConfigs').text
            expectedConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'expectedConfig').text
        elif param == "Failed":
            currentConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'currentConfigs').text
            expectedConfig = context.baseReader.getElementByPropertyName(context, currentPage, 'expectedConfig').text
        delay(5)


@step('I validate the alert Message for "{type}" Service')
def step_impl(context, type):
    currentPage = GlobalVar.currentPage
    popupMessageXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'popupMessage')
    WebDriverWait(context.driver, 5).until(EC.visibility_of_element_located((By.XPATH, popupMessageXpath)))
    message = context.baseReader.getElementByPropertyName(context, currentPage, 'popupMessage').text
    expected_message = GlobalVar.testParams.get("errorMessage")
    print(len(message))
    print(message)
    print(message.strip())
    print(len(expected_message))
    print(expected_message)
    print(expected_message.strip())
    assert message.strip() == expected_message.strip()


@step('I login into the application')
def re_login(context):
    global loginStatus
    currentPage = "LandingPage"
    LoginXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'Login')
    WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, LoginXpath)))
    time.sleep(5)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Login').click()
    currentPage = 'KeycloakLoginPage'
    titleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'PageTitle')
    WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, titleXpath)))

    userType = GlobalVar.testParams.get("userType")
    username = context.envReader.get(f'TestUserName{userType}')
    password = context.envReader.get(f'TestUserPass{userType}')
    usernameXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'UserName')
    WebDriverWait(context.driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, usernameXpath))).send_keys(username)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Password').send_keys(password)
    context.baseReader.getElementByPropertyName(context, currentPage, 'LoginButton').click()

    titleXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'title')
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, titleXpath)))


@step('Validate the service type should be "{type}"')
def step_impl(context, type):
    currentPage = GlobalVar.currentPage
    actualServiceType = context.baseReader.getElementByPropertyName(context, currentPage, "serviceType").text
    print("ActualServiceType:", actualServiceType)
    assert type == actualServiceType


@step('I validate that the MWR details should be "{param}"')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    mwrServiceDetailsXpath = context.baseReader.getElementLocatorValue(context, currentPage, 'mwrServiceDetails')
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, mwrServiceDetailsXpath)))

    element = context.driver.find_element_by_xpath(mwrServiceDetailsXpath)
    status = element.get_attribute("class")
    print("Status:", status)
    if param == "enabled":
        assert status == "panel"
    elif param == "disabled":
        assert status == "panel disableAccordion"


@step('I validate that the MWR should be enabled on Parameter Information page')
def step_impl(context):
    pass


@step("Select the version from the dropdown to rollback the service for read-only user")
def select_service_version(context):
    currentPage = GlobalVar.currentPage
    GlobalVar.counter = 1
    currentVersion = context.baseReader.getElementByPropertyName(context, currentPage, "currentVersion").text
    print("Current Version:-", currentVersion)
    context.baseReader.getElementByPropertyName(context, currentPage, "versionDropdown").click()
    delay(2)
    versionsList = context.baseReader.getElementLocatorValue(context, currentPage, 'versionsList')
    rows = context.driver.find_elements_by_xpath(versionsList)
    GlobalVar.versions = len(rows)
    for i in range(GlobalVar.counter, len(rows)):
        existingVersions = context.driver.find_element_by_xpath(
            '//div[@class="dropdown-list"]/ul[2]/li[' + str(i) + ']').text
        if currentVersion != existingVersions:
            print("Current version and selected versions are different")
            context.driver.find_element_by_xpath('//div[@class="dropdown-list"]/ul[2]/li[' + str(i) + ']').click()
            delay(5)
            break
        else:
            continue


@step('I search the WorkOrders by using "{param}"')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    if param == "CSID":
        csid = GlobalVar.testParams.get("serviceId")
        context.baseReader.getElementByPropertyName(context, currentPage,
                                                    'advanceCustomerServiceIdTransactions').send_keys(Keys.CONTROL,
                                                                                                      "a",
                                                                                                      Keys.DELETE)
        context.baseReader.getElementByPropertyName(context, currentPage,
                                                    'advanceCustomerServiceIdTransactions').send_keys(csid)
    if param == "OperationType":
        operation = GlobalVar.testParams.get("OperationType")

        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceOperationType').send_keys(
            Keys.CONTROL,
            "a",
            Keys.DELETE)
        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceOperationType').send_keys(operation)
    if param == "CSID_OperationType":
        csid = GlobalVar.testParams.get("serviceId")

        context.baseReader.getElementByPropertyName(context, currentPage,
                                                    'advanceCustomerServiceIdTransactions').send_keys(Keys.CONTROL,
                                                                                                      "a",
                                                                                                      Keys.DELETE)
        context.baseReader.getElementByPropertyName(context, currentPage,
                                                    'advanceCustomerServiceIdTransactions').send_keys(csid)
        operation = GlobalVar.testParams.get("OperationType")

        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceOperationType').send_keys(
            Keys.CONTROL,
            "a",
            Keys.DELETE)
        context.baseReader.getElementByPropertyName(context, currentPage, 'advanceOperationType').send_keys(operation)


@step('I validate that the operation type should contain MWR in it')
def step_impl(context):
    currentPage = GlobalVar.currentPage
    actualOperationType = context.baseReader.getElementByPropertyName(context, currentPage,
                                                                      "operation_type_transactions").text
    assert actualOperationType == "ADD_MWR"


@step('I validate that the rollback button should be "{param}"')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    if param == "enabled":
        enabledRollbackXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                         'enabledRollback')
        WebDriverWait(context.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, enabledRollbackXpath)))
        element = context.driver.find_element_by_xpath(enabledRollbackXpath)
        status = element.get_attribute("class")
        assert status == "btnEnabled"

    elif param == "disabled":
        disabledRollbackXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                          'disabledRollback')
        WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, disabledRollbackXpath)))
        element = context.driver.find_element_by_xpath(disabledRollbackXpath)
        status = element.get_attribute("class")
        assert status == "btnDisabled"


@step('validate the access type should be "{param}" on Parameter Information page')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    accessTypeParameterInfoXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                             'accessTypeParameterInfo')
    accessType = WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, accessTypeParameterInfoXpath))).text
    assert accessType == param


@step('MWR "{param}" value should be visible on Parameter Information page')
def step_impl(context, param):
    currentPage = GlobalVar.currentPage
    tunnelValueXpath = context.baseReader.getElementLocatorValue(context, currentPage,
                                                                 'tunnelValue')
    expectedValue = WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, tunnelValueXpath))).text
    assert param == expectedValue


@step('I navigate to "{param}" page')
def step_impl(context, param):
    url = param + "_url"
    context.driver.get(context.config.get(url))


@step(u'I enter "{param1}" and "{param2}"')
def step_impl(context, param1, param2):
    currentpage = GlobalVar.currentPage
    if param1 == "CustomerID" and param2 == "CustomerName":
        CustomerID = GlobalVar.testParams.get("CustomerID")
        element = context.baseReader.getElementByPropertyName(context, currentpage, "customer_id")
        element.send_keys(CustomerID)
        CustomerName = GlobalVar.testParams.get("Customer_name")
        val = context.baseReader.getElementByPropertyName(context, currentpage, "customer_name")
        val.send_keys(CustomerName)


@step(u'I enter "{param}"')
def step_impl(context, param):
    currentpage = GlobalVar.currentPage
    if param == "Email":
        Email = GlobalVar.testParams.get("Email")
        element = context.baseReader.getElementByPropertyName(context, currentpage, "email")
        element.send_keys(Email)
    if param == "CustomerName":
        customername = GlobalVar.testParams.get("CustomerName")
        element = context.baseReader.getElementByPropertyName(context, currentpage, "customer_name")
        element.send_keys(customername)
    if param == "CustomerID":
        customerid = GlobalVar.testParams.get("CustomerID")
        element = context.baseReader.getElementByPropertyName(context, currentpage, "customer_id")
        element.send_keys(customerid)
    if param == "editcustomerName":
        customerid = GlobalVar.testParams.get("editcustomerName")
        element = context.baseReader.getElementByPropertyName(context, currentpage, "editcustomerName")
        element.send_keys(customerid)
    if param == "editEmail":
        customerid = GlobalVar.testParams.get("editEmail")
        element = context.baseReader.getElementByPropertyName(context, currentpage, "editEmail")
        element.send_keys(customerid)
    if param == "Status":
        Status = GlobalVar.testParams.get("status")
        print("######################")
        print(Status)
        print("######################")
        element = context.baseReader.getElementByPropertyName(context, currentpage, "advanceStatus")
        print(element)
        element.send_keys(Status)
    time.sleep(5)


@when(u'I enter the prexisting "customer id" and "CustomerName"')
def step_impl(context):
    currentpage = GlobalVar.currentPage
    customerid = GlobalVar.testParams.get("CustomerID")
    element = context.baseReader.getElementByPropertyName(context, currentpage, "customer_id")
    element.send_keys(12345)
    customername = GlobalVar.testParams.get("CustomerName")
    element = context.baseReader.getElementByPropertyName(context, currentpage, "customer_name")
    element.send_keys("blahblah")


@step(u'I check "{val}" button is enabled')
def step_impl(context, val):
    if val == "save":
        Save = GlobalVar.testParams.get("save")
        assert Save == None


@step(u'I left "{param}" blank')
def step_impl(context, param):
    currentpage = GlobalVar.currentPage
    if param == "CustomerID":
        element = context.baseReader.getElementByPropertyName(context, currentpage, "customer_id")
        element.send_keys("")
    if param == "CustomerName":
        element = context.baseReader.getElementByPropertyName(context, currentpage, "customer_name")
        element.send_keys("")


@step(u'I clear all fields of "{page}"')
def step_impl(context, page):
    currentpage = GlobalVar.currentPage
    if page == "Customer":
        element = context.baseReader.getElementByPropertyName(context, currentpage, "customer_id")
        element.clear()
        element = context.baseReader.getElementByPropertyName(context, currentpage, "customer_name")
        element.clear()
        element = context.baseReader.getElementByPropertyName(context, currentpage, "customer_name")
        element.clear()
    if page == "edit":
        element = context.baseReader.getElementByPropertyName(context, currentpage, "editcustomerName")
        element.clear()
        element = context.baseReader.getElementByPropertyName(context, currentpage, "editEmail")
        element.clear()


@step(u'I click on "{val}" icon')
def step_impl(context, val):
    currentPage = GlobalVar.currentPage
    # if val == "delete":
    time.sleep(10)
    elementxpath = context.baseReader.getElementLocatorValue(context, currentPage, 'selectfirst')
    element = context.driver.find_element(By.XPATH, elementxpath)
    actions = ActionChains(context.driver)
    value = actions.move_to_element(element).perform()
    time.sleep(10)
    elementxpath = context.baseReader.getElementLocatorValue(context, currentPage, val)
    WebDriverWait(context.driver, 15).until(EC.visibility_of_element_located((By.XPATH, elementxpath))).click()


@step(u'Count "{val}"')
def step_impl(context, val):
    currentPage = GlobalVar.currentPage
    time.sleep(10)
    elementxpath = context.baseReader.getElementLocatorValue(context, currentPage, "ServicesRelated")
    print("***************" + elementxpath)
    element = context.driver.find_elements(By.XPATH, elementxpath)
    row = len(element)
    print(row)
    type(element)
    for x in element:
        print(x.text)

    if val == "no_data":
        assert row == 1


@step(u'I find the "{state}" of "{column_name}" column')
def step_impl(context, state, column_name):
    delay(15)
    currentPage = GlobalVar.currentPage
    if state == "presence":  # Checking the presence of column in work orders table
        elementxpath = context.baseReader.getElementLocatorValue(context, currentPage, column_name)
        print(elementxpath)
        column_value = WebDriverWait(context.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, elementxpath))).text

        column = GlobalVar.testParams['ColumnName']
        assert column_value == column

    else:
        table = context.baseReader.getElementLocatorValue(context, currentPage, "WorkOrdersTableRow")
        table_list = context.driver.find_elements(By.XPATH, table)
        for x in table_list:
            assert x.text != column_name  # validating that column is not present in table


@then(u'I find the "{value}" is present')
def step_impl(context, value):
    delay(10)
    currentPage = GlobalVar.currentPage
    elementxpath = context.baseReader.getElementLocatorValue(context, currentPage, value)
    print(value)
    print(elementxpath)
    column_value = context.driver.find_element(By.XPATH, elementxpath)
    assert column_value != None
