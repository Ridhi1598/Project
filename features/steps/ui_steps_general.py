import json
import os
import subprocess
import sys
import stat
# import this
from os.path import dirname

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from behave import given, when, then, step
from features.steps.globalVar import GlobalVar
import time

# declared variables
currentPage = None
ocpCommands = {}
envVarList = {}
envList = []

@step('"{page}" page title should be "{expectedValue}"')
def page_title_validation(context, page, expectedValue):
    global currentPage
    currentPage = page + 'Page'
    PageTitleXpath = context.baseReader.readElementByPropertyName(currentPage, "PageTitle").get("value")
    WebDriverWait(context.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, PageTitleXpath)))

    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, 'PageTitle').text

    if sys.argv[1] == 'lcd':
        loaderXpath = context.baseReader.readElementByPropertyName(currentPage, "loader").get("value")
        WebDriverWait(context.driver, 30).until(EC.invisibility_of_element_located((By.XPATH, loaderXpath)))

    assert expectedValue.lower() == actualValue.lower()
    GlobalVar.currentPage = currentPage
    print("current page:", GlobalVar.currentPage)

@step('I go to "{page}"')
def change_currentPage(context, page):
    global currentPage
    currentPage = page + 'Page'
    GlobalVar.currentPage = currentPage


@step('title of "{page}" should be "{expectedValue}"')
def page_title(context, page, expectedValue):
    global currentPage
    actualValue = context.baseReader.getElementByPropertyName(context, currentPage, page).text
    assert expectedValue.lower() == actualValue.lower()


@then("I verify the Page URL contains {url}")
def step_impl(context, url):
    global currentPage
    currentUrl = context.driver.current_url
    assert url in currentUrl


@step('I validate page and login')
def login(context):
    page_title_validation(context, 'KeycloakLogin', 'Log In')
    username = os.getenv("TestUserName")
    password = os.getenv("TestUserPass")
    currentPage = GlobalVar.currentPage
    context.baseReader.getElementByPropertyName(context, currentPage, 'UserName').send_keys(username)
    context.baseReader.getElementByPropertyName(context, currentPage, 'Password').send_keys(password)
    context.baseReader.getElementByPropertyName(context, currentPage, 'LoginButton').click()


@step('I click on "{value}" button')
def click_button(context, value):
    time.sleep(20)
    currentPage = GlobalVar.currentPage
    print("CurrentPage:", currentPage)
    elementXpath = context.baseReader.getElementLocatorValue(context, currentPage, value)
    print("Element Xpath:", elementXpath)
    print(value)
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, elementXpath)))
    WebDriverWait(context.driver, 30).until(EC.element_to_be_clickable((By.XPATH, elementXpath)))
    context.baseReader.getElementByPropertyName(context, currentPage, value).click()
    time.sleep(7)


@step('Generate command for ocp login')
def ocp_login(context):
    """
    ocp login will be through a service account
    reads the login token for the service account from the config file
    generates ocp login command using the login token
    """
    global ocpCommands
    if 'bi' in sys.argv[1]:
        if "evpn" in GlobalVar.featureFilePath:
            app = "consumer"
        else:
            app = 'bi'
    else:
        app = sys.argv[1]
    if app == 'cs':
        app = 'consumer'

    loginToken = context.config.get(f'ocp_login_{app}_{sys.argv[2]}')
    ocpCommands['ocp_login'] = f'oc login {loginToken}'


@step('Generate command to access current working project')
def ocp_project(context):
    """
    generates the name of the project which needs to be accessed by reading values passed as system arguments
    generates commands to access the current project
    """
    # define environment
    if sys.argv[2] == 'dev':
        env = 'develop'
    else:
        env = sys.argv[2]

    # define app name
    if 'bi' in sys.argv[1]:
        if "evpn" in GlobalVar.featureFilePath:
            app = "consumer"
        else:
            app = 'bi'
    else:
        app = sys.argv[1]

    if app == 'cs':
        app ='consumer'
    # define project name to be accessed
    currentProject = f'bsaf-{env}-{app}'
    ocpCommands['ocp_project'] = f'oc project {currentProject}'
    print(ocpCommands['ocp_project'])


@step('Generate command to "{mode}" the "{variable}" variables of the "{component}"')
def ocp_component(context, mode, variable, component):
    """
    :param mode: update or restore; defined as per the scenario
    :param component: the microservice for which the environment variables are being changed

    reads the environment variables from a json file which needs to be changed
    generates commands which needs to be written in the batch file to overwrite the environment variables
    """
    global envVarList, envList
    if "clm" in sys.argv[1]:
        if "evpn" in component:
            app = "cs"
        else:
            app = "clm"
    else:
        app = sys.argv[1]

    # define the service
    if "evpn" in component or app.lower() == 'cs' or 'l2vpn' in component.lower():
        service = component
    elif "bng" in component:
        service = component
    else:
        service = f'{app}-{component}'
    # Read env variables from json
    fileName = f'envVars_{component}_{mode}{variable}.json'
    filePath = os.getcwd() + '/resources/payload/' + sys.argv[1] + '/' + GlobalVar.testComponent[0].lower() \
               + '/' + fileName
    envVarList = json.load(open(filePath, 'rb'))
    ocpCommands['var_list'] = ''
    envList = []
    # generate update commands for all the values and store in a string format
    for envVar in envVarList:
        envList.append(envVar)
        ocpCommands['update_' + envVar] = 'oc set env dc/' + service + ' --overwrite ' + \
                                          envVar + '=' + envVarList.get(envVar)
        ocpCommands['var_list'] += ocpCommands['update_' + envVar] + '\n'


@step('Create batch file and execute the commands for "{component}"')
def execute_batch_file(context, component):
    """
    :param component: the microservice for which the environment variables are being changed

    creates a batch file at the defined location
    write commands to be executed in the batch file
    run the batch file
    """
    # create folder for batch file
    batchFileLocation = os.getcwd() + '/resources/batch'
    if not os.path.exists(batchFileLocation):
        os.mkdir(batchFileLocation)

    if os.name == 'nt':
        # define batch file path
        batchFilePath = batchFileLocation + '/' + sys.argv[1] + '_envVar_' + component + '.bat'

        # write commands in batch file
        with open(batchFilePath, "w") as batchFile:
            batchFile.write('@echo off \n' + ocpCommands['ocp_login'] + '\n' + ocpCommands['ocp_project'] + '\n' +
                            ocpCommands['show_initial_variables'] + '\n' + ocpCommands['var_list'] +
                            ocpCommands['show_changed_variables'])

        # calling the batch file to execute the above commands
        subprocess.call(batchFilePath)

    elif os.name == 'posix':
        # define shell file path
        shellFilePath = batchFileLocation + '/' + sys.argv[1] + '_envVar_' + component + '.sh'
        with open(shellFilePath, "w") as shellFile:

            shellFile.write('#!/bin/sh \n' + ocpCommands['ocp_login'] + '\n' + ocpCommands['ocp_project'] + '\n' +
                            ocpCommands['show_initial_variables'] + '\n' + ocpCommands['var_list'] +
                            ocpCommands['show_changed_variables'])

            # making the file executable
            st = os.stat(shellFilePath)
            os.chmod(shellFilePath, st.st_mode | stat.S_IEXEC)

        # calling the shell file to execute the above commands
        subprocess.call(shellFilePath)


@step('Generate command to show all the "{state}" variables of the "{component}"')
def ocp_show_variables(context, state, component):
    """
    :param state: initial or changed depending on the scenario
    :param component: the microservice for which the environment variables are being changed

    reads the environment variables for the component and stores in a text file
    """
    global envListFilePath
    if "clm" in sys.argv[1]:
        app = "clm"
    else:
        app = sys.argv[1]

    # define the service
    if "evpn" in component or app.lower() == 'cs':
        service = component
    else:
        service = f'{app}-{component}'

    envListFileName = sys.argv[1] + '_' + 'envVarsList_' + component + '_' + state + '.txt'
    envListFilePath = os.getcwd() + '/resources/batch/' + envListFileName
    ocpCommands['show_' + state + '_variables'] = 'oc set env dc/' + service + ' --all --list > ' + envListFilePath


@step('Validate that environment variables are successfully changed')
def validate_environment_variables(context):
    """
    reads the env list file and creates a new dictionary 'data' from the parameters changed in the previous steps
    validates that the changed values are same as the ones passed in the json
    """
    # Wait for new instance to get created
    print("waiting till new pods instances are up..")
    time.sleep(100)

    # create new dictionary with changed parameters
    data = {}
    with open(envListFilePath) as envFile:
        for line in envFile:
            for env in envList:
                if env in line:
                    key, value = line.strip().split('=', 1)
                    data[key] = value.strip()

    # validate that the changed parameters are same as passed
    for envVar in data:
        assert envVarList[envVar] == data[envVar]


def custom_click_and_wait(context, page, clickElement, expectedElement):
    clickElementXpath = context.baseReader.getElementLocatorValue(context, page, clickElement)
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, clickElementXpath)))

    expectedElementXpath = context.baseReader.getElementLocatorValue(context, page, expectedElement)
    WebDriverWait(context.driver, 30).until(EC.visibility_of_element_located((By.XPATH, expectedElementXpath)))

