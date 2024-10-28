import yaml

from .rule_test_case import RuleTestCase

class RuleTestCaseParser:

    @classmethod
    def parse(cls, file_path) -> RuleTestCase:

        with open(file_path) as f:
            rule_test_case : RuleTestCase = yaml.load(f, Loader=yaml.FullLoader)
            rule_test_case.filename = file_path
            return rule_test_case


    @classmethod
    def parse_str(cls, content) -> RuleTestCase:
        rule_test_case : RuleTestCase = yaml.load(content, Loader=yaml.FullLoader)
        rule_test_case.filename = "restapi_call"
        return rule_test_case

