import os
import fnmatch
import yaml
import traceback

from behave import fixture
from behave import use_fixture
from behave.model import Table, Examples
from hamcrest import assert_that, equal_to, greater_than

from features.steps.lcd.model.device_inventory import DeviceInventory
from features.steps.lcd.model.rule_test_case import RuleTestCase
from features.steps.lcd.model.rule_test_case_parser import RuleTestCaseParser

from features.steps.lcd.model.mediation_layer_nso_context import MediationLayerNSOContext
from features.steps.lcd.model.rule_test_case_runner import FunctionalRuleTestRunner
from features.steps.lcd.model.mock_tinaa_auth_service import MockTinaaAuthService
from features.steps.lcd.model.tinaa_auth_service import TinaaAuthService

from features.steps.lcd.functional_rule_test_config import FunctionalRuleTestConfig
from features.steps.lcd.tinaa_config import TinaaAuthServiceConfig

class RuleTestsFramework:
    def __init__(self, context, framework_config: FunctionalRuleTestConfig, tinaa_config: TinaaAuthServiceConfig):
        self.context = context
        self.framework_config = framework_config
        self.tinaa_config = tinaa_config

    def load_rule_tests_and_inventory(self):
        self.context.testfiles = self._get_valid_files_in_dir(self.framework_config.FUNCTIONAL_RULE_TEST_DIR,"test-*.yml")
        assert_that(len(self.context.testfiles), greater_than(0), "Rule test files not loaded")
        with open(f"{self.framework_config.FUNCTIONAL_TESTING_DEVICE_INVENTORY}") as f:
            self.context.device_inventory_content = f.read()

        self.context.device_inventory = DeviceInventory.parse_str(self.context.device_inventory_content)

    def create_test_scenarios(self):
        table = self._create_table_from_files(self.context.testfiles, self.context.device_inventory)
        examples = Examples("dynamic_loading", 1, "Examples", "RuleTests", table=table)

        scenarios = self.context.feature.scenarios[0]
        if not scenarios.examples:
            scenarios.examples = [examples]
        else:
            scenarios.examples.append(examples)

    def initialize_test_runner(self):
        auth_service_class = (MockTinaaAuthService if self.tinaa_config.MOCK_TINAA else TinaaAuthService)
        auth_service = auth_service_class(self.tinaa_config)

        self.context.nso_context = MediationLayerNSOContext(self.framework_config, auth_service).open()
        runner: FunctionalRuleTestRunner = FunctionalRuleTestRunner(self.context.nso_context)
        if self.framework_config.FORCE_SESSION:
            runner.stop_and_delete_all_tests()
        runner.open()
        self.context.runner = runner

        for device_record in self.context.device_inventory.inventory.devices:
            self.context.runner.add_device(self.context.device_inventory_content, device_record.model_family)

    def destroy_test_runner(self):
        for device_record in self.context.device_inventory.inventory.devices:
            self.context.runner.delete_device(self.context.device_inventory_content, device_record.model_family)
        
        self.context.runner.close()
        self.context.nso_context.close()

    def _get_valid_files_in_dir(self, path, file_pattern) -> [str]:
        ## Return Valid YML files in directory
        all_files = []
        for relative_dir, _, files in os.walk(path):
            for file in files:
                if not file_pattern or fnmatch.fnmatchcase(file,file_pattern):
                    file_path = relative_dir + '/' + file
                    all_files.append(file_path)
        return all_files

    def _create_table_from_files(self, testfiles, device_inventory) -> Table:
        ## Construct table that includes in each row:
        #      yml_file  | device_type | given | when | then

        available_devices = set()
        for device_record in device_inventory.inventory.devices:
            available_devices.add(device_record.model_family)
            
        table = Table(['testdir', 'ymlfile', 'device_type', "given", "when", "then"])
        for testfile in testfiles:
            rule_test_case: RuleTestCase = RuleTestCaseParser.parse(testfile)
            scen = rule_test_case.scenario
            row = None
            testdir, filename = testfile.rsplit('/',1)

            for device_type in scen.device_models:
                if device_type in available_devices:
                    row = [testdir, filename, device_type, str(scen.given), str(scen.when), str(scen.then)]
                    table.add_row(row, 1)
        return table
