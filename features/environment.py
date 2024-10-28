import logging
import shutil
import uuid
from datetime import datetime
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from allure_combine import combine_allure
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import subprocess
# from reportportal_client.hooks.behave import get_rp_service, rp_before_feature, rp_before_scenario

import sys
import traceback

from allure_commons.types import LabelType
from allure_commons.model2 import Label


from behave import use_fixture, fixture
from reportportal_client import ReportPortalService


from reportportal_behave.behave_integration_service import BehaveIntegrationService

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from common.util.ymlReader import ReadYMLFile
from common.util.email_temp import send_email, send_message_to_slack
from features.e2e_device_setup import E2EDeviceConfigurator
from common.util.baseReader import BaseReader
from common.util.config import ConfigReader
from common.util.csvRead import ReadCSVFile
from features.steps.globalVar import GlobalVar
from features.steps.lcd.model.rule_tests_framework import RuleTestsFramework
from features.steps.lcd.functional_rule_test_config import FunctionalRuleTestConfig
from features.steps.lcd.tinaa_config import TinaaAuthServiceConfig
from common.util.envDataGenerator import envDataGenerator
failList = {}
failScenarioList = []
currentFailFeature = None
testCasesMessage = None
testTypeValue = None

#
# rp_endpoint = os.getenv('RP_ENDPOINT', 'http://localhost:8080')
# rp_project = os.getenv('RP_PROJECT', 'behave-telus')
# rp_token = os.getenv('RP_TOKEN', 'f818b088-926d-4ccf-9764-4cd9c1f24434')
# rp_launch = os.getenv('RP_LAUNCH', 'default_launch')

# rp_service = ReportPortalService(
#     endpoint=rp_endpoint,
#     project=rp_project,
#     token=rp_token
# )
def before_tag(context, tag):
    if tag == "fixture.load_rule_tests":
        use_fixture(load_rule_tests, context)


@fixture
def load_rule_tests(context, timeout=6000, **kwargs):
    try:
        logging.info("Loading rule tests...")
        framework = RuleTestsFramework(context, FunctionalRuleTestConfig, TinaaAuthServiceConfig)
        framework.load_rule_tests_and_inventory()
        framework.create_test_scenarios()
        framework.initialize_test_runner()
    except:
        traceback.print_exc()
        raise RuntimeError()

    yield context
    framework.destroy_test_runner()


@fixture
def browser_launch(context):
    BROWSER = context.config.get('browser').lower()
    if BROWSER == 'chrome':
        if os.name == 'nt':
            driverExecPath = os.getcwd() + "/resources/driver/chromedriver"
        elif os.name == 'windows':
            driverExecPath = os.getcwd() + "/resources/driver/chromedriver"
        elif os.name == 'OSX':
            driverExecPath = os.getcwd() + "/resources/driver/chromedriver_mac"
        elif os.name == 'posix':
            driverExecPath = os.getcwd() + "/resources/driver/chromedriver_lin"
            os.chmod(driverExecPath, 0o755)

        options = Options()
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--ignore-certificate-errors')
        if os.name == 'posix':
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            # options.add_argument('--remote-debugging-port=9222')
            # options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--disable-dev-shm-usage")
            chrome_prefs = {}
            options.experimental_options["prefs"] = chrome_prefs
            chrome_prefs["profile.default_content_settings"] = {"images": 2}
            options.add_argument("--start-maximized")
            prefs = {"profile.default_content_settings.popups": 0,
                     "download.default_directory":
                         os.getcwd() + "\\",
                     "directory_upgrade": True}
            options.add_experimental_option("prefs", prefs)

            options.add_argument("--start-maximized")
            prefs = {"profile.default_content_settings.popups": 0,
                    "download.default_directory":
                        os.getcwd()+"\\",
                    "directory_upgrade": True}
            options.add_experimental_option("prefs", prefs)
        
        context.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("CHROME BROWSER INITIALISED")
        print(context.driver)

        context.driver.implicitly_wait(30)
        context.driver.maximize_window()
        wait = WebDriverWait(context.driver, 10)

    elif BROWSER == 'firefox':
        context.driver = webdriver.Firefox()
    elif BROWSER == 'safari':
        context.driver = webdriver.Safari()
    elif BROWSER == 'ie':
        context.driver = webdriver.Ie()
    elif BROWSER == 'opera':
        context.driver = webdriver.Opera()
    elif BROWSER == 'phantomjs':
        context.driver = webdriver.PhantomJS()
    else:
        print("Browser you entered:", BROWSER, "is invalid value")
    yield context.driver


def before_all(context):
    global testTypeValue
    # Dir to output test artifacts
    context.artifacts_dir = 'artifacts'
    # scenario_labels = [Label(name=LabelType.SUITE, value=context.suite_name)]
    # test_case.labels.append(Label(name=LabelType.SUITE, value=scenario.feature.name))
    tags = ', '.join([tag for tags in context.config.tags.ands for tag in tags])
    attributes = {
        # Used to label launches in Report Portal
        "environment": context.config.userdata.get('environment', sys.argv[2]),
        "version": context.config.userdata.get('version', "unknown"),
    }

    testTypeValue = envDataGenerator.defineTestType(context, GlobalVar.featureFilePath)
    context.requested_browser = context.config.userdata.get('browser', "chrome")

    context.config = ConfigReader().configFileReader(sys.argv[1] + "_appConfig.json")

    if sys.argv[1].lower() == 'lcd':
        if context.config.get("runDeviceSetupScript").lower() != "off":
            print("Setting up devices before running Test Scripts.....")
            E2EDeviceConfigurator().setup_device_e2e_test()
            print("Setting up devices completed....")

    context.baseReader = BaseReader(sys.argv[1] + "_PagesElements.yml")
    context.envReader = ReadYMLFile.readEnvVar(context)
    GlobalVar.testComponent = envDataGenerator.defineTestType(context, GlobalVar.featureFilePath)
    if 'UI' in GlobalVar.featureFilePath:
        context.csvRead = ReadCSVFile().read_csv_file(sys.argv[1] + "_UITestData_" + sys.argv[2] + ".csv")
    if 'E2E' in GlobalVar.featureFilePath or 'NED' in GlobalVar.featureFilePath:
        context.csvRead = ReadCSVFile().read_csv_file(sys.argv[1] + "_TestData_" + sys.argv[2] + ".csv")
    if not (
            'UI' in GlobalVar.featureFilePath or 'E2E' in GlobalVar.featureFilePath or 'NED' in GlobalVar.featureFilePath):
        print(sys.argv[1] + "_APITestData_" + GlobalVar.testComponent[0] + "_" + sys.argv[
                                                                 2].lower() + ".csv")
        if sys.argv[1] == "cs":
            context.csvReadAPI = ReadCSVFile().read_csv_file(sys.argv[1] + "_APITestData_" +
                                                             GlobalVar.testComponent[0] + "_" + sys.argv[
                                                                 2].lower() + ".csv")
        else:
            context.csvReadAPI = ReadCSVFile().read_csv_file(sys.argv[1] + "_APITestData_" +
                                                         GlobalVar.testComponent[0] + ".csv")


    if 'feature_UIFunctional' in GlobalVar.featureFilePath or '@resources/sequence/csE2E_sequence.txt' in GlobalVar.featureFilePath or 'features/feature_E2E/cs_Portal_Phase2_Positive' in GlobalVar.featureFilePath or '@resources/sequence/csUI_UM_sequence.txt':
        use_fixture(browser_launch, context)

    if '@' in GlobalVar.featureFilePath:
        GlobalVar.featureCount = envDataGenerator.features_counter(context, GlobalVar.featureFilePath)

    GlobalVar.allure_json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "allure-reports", "json")
    GlobalVar.allure_html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "allure-reports", "html")
    try:
        os.makedirs(GlobalVar.allure_json_path, exist_ok=True)
        print(f"Created directory: {GlobalVar.allure_json_path}")
        os.makedirs(GlobalVar.allure_html_path, exist_ok=True)
        print(f"Created directory: {GlobalVar.allure_html_path}")
    except Exception as e:
        print(f"Error creating directory:allure-json or allure-html")
        print(e)

#def before_feature(context, feature):
#    if '@resources/sequence/csUI_sequence' in GlobalVar.featureFilePath or 'features/feature_E2E/cs_Portal' in GlobalVar.featureFilePath or '@resources/sequence/csE2E_sequence' in GlobalVar.featureFilePath:
#        use_fixture(browser_launch, context)
    # feature_item_name = feature.filename
    # feature_item_start_time = str(int(time.time() * 1000))
    # context.rp_feature_item = rp_service.start_test_item(
    #     name=feature_item_name,
    #     start_time=feature_item_start_time,
    #     item_type="SUITE",
    #     launch_id=context.launch_id,
    #     attributes=attributes
    # )
#     context.feature_id = context.behave_integration_service.before_feature(feature)


def before_scenario(context, scenario):
    pass
    # context.scenario_id = context.behave_integration_service.before_scenario(scenario,
#                                                                              feature_id=context.feature_id)
    # Log scenario start event to ReportPortal
    # Log scenario start event to ReportPortal
    # tags = ', '.join([tag for tags in context.config.tags.ands for tag in tags])
    # attributes = {
    #     # Used to label launches in Report Portal
    #     "environment": context.config.userdata.get('environment', sys.argv[2]),
    #     "version": context.config.userdata.get('version', "unknown"),
    # }

    # attributes = {
    #    # Used to label launches in Report Portal
    #    "environment": "context.config.userdata.get('environment', sys.argv[2])",
    #    "version": "unknown"
    # }
    # test_item_name = scenario.name
    # test_item_start_time = str(int(time.time() * 1000))
    # context.rp_test_item = rp_service.start_test_item(
    #     name=test_item_name,
    #     start_time=test_item_start_time,
    #     item_type="SCENARIO",
    #     launch_id=context.launch_id,
    #     attributes=attributes
    # )

def before_step(context, step):
    context.current_step = step.name
    GlobalVar.currentStep = context.current_step


# def before_step(context, step):
#     context.step_id = context.behave_integration_service.before_step(step, scenario_id=context.scenario_id)


# def after_step(context, step):
#     context.behave_integration_service.after_step(step, context.step_id)
    # Log step event to ReportPortal
    # print('RP LOG',rp_service.log(
    #     time=str(int(time.time() * 1000)),
    #     message=step.exception,
    #     level=step.status.name,
    #     item_id=context.rp_test_item
    # ))

def after_scenario(context, scenario):
    global status, failScenarioList, currentFailFeature
    status = 'Passed'
    currentScenario = scenario.name
    currentFeature = scenario.feature.name
    if scenario.status == "failed":
        status = 'Failed'
        GlobalVar.failCounter += 1
        if currentFailFeature == currentFeature:
            failScenarioList.append(currentScenario)
        else:
            failScenarioList = []
            failScenarioList.append(currentScenario)
            currentFailFeature = currentFeature

        testTypeValue = envDataGenerator.defineTestType(context, GlobalVar.featureFilePath)
        scenario_error_dir = './reports/' + sys.argv[1].upper() + '_' + testTypeValue[1] + '_SummaryReport'
        make_dir(scenario_error_dir)
        if 'ui' in testTypeValue[1].lower() or sys.argv[1] == 'cs':
            scenario_file_path = os.path.join(scenario_error_dir, scenario.feature.name.replace(' ', '_')
                                              + '_' + time.strftime("%H%M%S_%d_%m_%Y") + '.png')
            context.driver.save_screenshot(scenario_file_path)
    # context.behave_integration_service.after_scenario(scenario, context.scenario_id)
        # Log scenario end event to ReportPortal
    # print('-----------',scenario.status.name.lower())
    # rp_service.finish_test_item(
    #     end_time=str(int(time.time() * 1000)),
    #     status=scenario.status.name.upper(),
    #     item_id=context.rp_test_item
    # )


def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def after_feature(context, feature):
    global currentFailFeature, testCasesMessage
    # context.behave_integration_service.after_feature(feature, context.feature_id)
    testCasesMessage = 'All Test Scenarios Passed in this run.'
    if feature.status == 'failed':
        currentFailFeature = feature.name
        failList[currentFailFeature] = failScenarioList
    GlobalVar.featureCount -= 1



def after_all(context):
    global testCasesMessage, testTypeValue
    testTypeValue = envDataGenerator.defineTestType(context, GlobalVar.featureFilePath)

    # close the browser in case of UI tests
    if 'feature_UIFunctional' in GlobalVar.featureFilePath or '@resources/sequence/lcdUI' in GlobalVar.featureFilePath \
            or '@resources/sequence/sdwanUI' in GlobalVar.featureFilePath or '@resources/sequence/biUI' in GlobalVar.featureFilePath or '@resources/sequence/bi_clmUI' in GlobalVar.featureFilePath:
        context.driver.quit()

    ##
    ##
    mailTitlePrefix = context.config.get("appName") + '_' + testTypeValue[1]
    try:
        # check if java is installed
        try:
            subprocess.check_output(["java", "-version"],stderr=subprocess.STDOUT)
        except Exception as e:
            logging.error(e)

        #check if allure is in path
        try:
            subprocess.check_output(["allure", "--version"], stderr=subprocess.STDOUT)
        except Exception as e:
            logging.error(e)

        # generate allure html report
        # Specify the paths to the Allure results directory and the custom report directory
        # 'allure generate --clean allure-reports/json -o allure-reports/html '
        cmd = f"allure generate {GlobalVar.allure_json_path} -o {GlobalVar.allure_html_path}"
        # Run the command in a subprocess
        try:
            # Get the root directory of the project by going up two levels from the current directory
            project_dir = os.path.dirname(os.path.dirname(__file__))
            subprocess.run(cmd, shell=True, cwd=project_dir)
            shutil.rmtree(GlobalVar.allure_json_path)

            report_folder_path = f"{project_dir}/allure-reports/one_page_report"
            report_file_name = mailTitlePrefix + '_Automation_report_summary.html'
            report_file_path = f'{report_folder_path}/{report_file_name}'
            if os.path.exists(report_file_path):
                os.remove(report_file_path)

            # Convert allure report into one page report_dir
            combine_allure(GlobalVar.allure_html_path, dest_folder=report_folder_path, remove_temp_files=True,
                           auto_create_folders=True)

            os.rename(f'{report_folder_path}/complete.html', report_file_path)
            # above line will create a single page html report which will contain all dependencies inside it,
            # like css, js, json, configs, image screenshots etc

            shutil.rmtree(GlobalVar.allure_html_path)
            # if os.path.exists(f'{results_dir}/history'):
            #     shutil.rmtree(f'{results_dir}/history')
            # shutil.copytree(f'{report_dir}/history', f'{results_dir}/history')
            # delete entire folder if no of json is == 10
            # Get the list of files in the directory
            # files = os.listdir(GlobalVar.allure_json_path)
            # json_files = [f for f in files if os.path.splitext(f)[1] == '.json']
            # os.remove(f'{GlobalVar.allure_json_path}/{json_files[0]}')

        except Exception as e:
            logging.error(f'Error generating Allure report: {e}')
    except subprocess.CalledProcessError as e:
        print(f"Error generating Allure report: {e}")
        logging.error(e)
    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.error(e)

    ##
    ##
    runStatus = 'Passed'
    if GlobalVar.failCounter > 0:
        runStatus = 'Failed'
        testCasesMessage = envDataGenerator.dictToStr(context, failList)
    mailTitle = f'{mailTitlePrefix} Automation Run Result on {(sys.argv[2]).title()}:{runStatus}'

    plainPrintableText = f'\nHi Team,\n\nHere is the AUTOMATION RUN results below for the latest run:\n\n' \
                         f'{mailTitle}\n\n{("=" * 80)}\n\n{testCasesMessage}\n\n{("=" * 80)}\n' \
                         f'Thanks,\nTest Automation Team !!\n'
    # msg = MIMEMultipart('alternative')
    # plain = msg.attach(MIMEText(plainPrintableText, 'plain'))
    # html = msg.attach(MIMEText(mailMessageRawHtmlBody, 'html'))

    if "commit" not in GlobalVar.featureFilePath:
        if context.config.get("sendSlackNotification").lower() != "off":
            send_message_to_slack(plainPrintableText)
        if context.config.get("senEmail").lower() != "off":
            recipient_List = context.config.get("recipient_List")
            recipient_List = [email.strip() for email in recipient_List.split(",")]
            emailStatus = send_email(mailTitle,plainPrintableText, recipient_List, [report_file_path], 'exporter.pltf-develop-pubsub.svc', '8888')
            print("Email Sent Status: {}".format(emailStatus))
