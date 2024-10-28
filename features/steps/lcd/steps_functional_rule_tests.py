import sys
import yaml
from behave   import given, when, then
from hamcrest import assert_that, equal_to
import requests
from features.steps.lcd.functional_rule_test_config import FunctionalRuleTestConfig
from features.steps.lcd.model.rule_test_case_parser import RuleTestCaseParser
from features.steps.lcd.model.rule_test_case import RuleTestCase


@given(u'Feature under test is "{testdir}"')
def step_load_rule_test_file(context, testdir):
    # Parsing then dumping will set the filename in RuleTestCase
    context.testdir = testdir

@given(u'I load test in "{filename}"')
def step_load_rule_test_file(context, filename):
    filepath = context.testdir + '/' + filename
    test_case: RuleTestCase = RuleTestCaseParser.parse(filepath)
    # Parsing then dumping will set the filename in RuleTestCase
    context.test_file_content = yaml.dump(test_case)

@given(u'@"{description}"')
@when (u'@"{description}"')
def step_describe(context, description):
    pass

@then (u'@"{description}"')
def step_test_passes(context, description):
    display = None
    if 'failure' in context.test_result:
        display = context.test_result['failure']
    elif 'error' in context.test_result:
        display = context.test_result['error']

    if display:
        if isinstance(display, list):
            for item in display:
                print(item, file=sys.stderr)
        else:
            print(display, file=sys.stderr)

    assert_that(context.test_result['was-successful'], equal_to('true'))

@given(u'I set device_type to "{device_type}"')
def step_set_device_type(context, device_type):
    context.device_type = device_type
    with open(f"{FunctionalRuleTestConfig.FUNCTIONAL_TESTING_DEVICE_INVENTORY}") as f:
        context.device_inventory = f.read()


@when(u'I run the test')
def step_i_run_rule_test(context):
    context.test_process_id = context.runner.prepare_test(context.device_inventory, context.device_type, context.test_file_content)


@when(u'I receive test results')
def step_i_receive_test_results(context):
    context.test_result = context.runner.poll_test_status(context.test_process_id)


@when(u'I stop and delete test process id "{uuid}"')
def step_delete_test_pid(context, uuid):
    context.runner.stop_and_delete_test(uuid)
    output = context.poll_test_status(context.test_process_id)
    
    print("output = ", output)
    raise NotImplementedError("Not fully implemented/Tested")


@when(u'I stop all processes and delete the session')
def step_delete_all_pids(context, uuid):
    context.runner.stop_and_delete_test(uuid)
    output = context.poll_test_status(context.test_process_id)
    
    print("output = ", output)
    raise NotImplementedError("Not fully implemented/Tested")


