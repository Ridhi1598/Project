import logging
import os
import sys
from shutil import rmtree
from exitstatus import ExitStatus
from behave import __main__ as runner_with_options

# read feature file path from console
from common.util.envDataGenerator import envDataGenerator
from features.steps.globalVar import GlobalVar

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    appName = ''
    appEnv = ''
    featureFilePath = ''
    tagOptions = ''
    reportPortalFlag = ''
    try:
        appName = sys.argv[1]
        appEnv = ' ' + sys.argv[2] + ' '
        featureFilePath = ' ' + sys.argv[3] + ' '
        tagOptions = ' ' + sys.argv[4] + ' '
        reportPortalFlag = ' ' + sys.argv[5] + ' '
    except IndexError:
        logger.error(
            'appName[1] or appEnv[2] or featurefilePath[3]/sequencefeaturefilePath[3]  or tagOptions[4] 0r reportPortalFlag[5]  was not provided')

    sys.stdout.flush()
    GlobalVar.featureFilePath = featureFilePath.strip()
    testTypeValue = envDataGenerator.defineTestType(None, GlobalVar.featureFilePath)
    reporting_folder_name = './reports/' + sys.argv[1].upper() + '_' + testTypeValue[1] + '_SummaryReport/'

    # remove if any reporting folder exists
    if os.path.exists(reporting_folder_name):
        rmtree(reporting_folder_name)
    os.makedirs(reporting_folder_name)

    # reporting related command line arguments
    # reportingRelated = ' -f html -o ' + reporting_folder_name + 'Automation_Summary_Report.html'

    reportingRelated = ' -f allure_behave.formatter:AllureFormatter -o allure-reports/json '

    # command line argument to capture console output
    if not reportPortalFlag:
        commonRunnerOptions = ' -f pretty --logging-level=INFO --no-skipped '
    else:
        commonRunnerOptions = ' -f pretty --logging-level=INFO --no-skipped -D rp_enable=True'

    # full list of command line options
    fullRunnerOptions = tagOptions + featureFilePath + reportingRelated + commonRunnerOptions
    # Set Exit code to validate the failure of Behave command
    runStatus = runner_with_options.main(fullRunnerOptions)
    if runStatus != 0:
        sys.exit(ExitStatus.failure)