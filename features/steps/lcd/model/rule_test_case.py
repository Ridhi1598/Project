import json

import yaml

class RuleTestCaseScenario(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseScenario'

    def __init__(self,
            title: str,
            suite_name: str,
            device_models: [str],
            given: str,
            when: str,
            then: str):

        self.title = title
        self.suite_name = suite_name
        self.device_models: [str] = list(map(str, device_models))

        # BDD definitions
        self.given: str = given
        self.when: str = when
        self.then: str = then


class RuleTestCaseDeviceRemediationItem(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseDeviceRemediationItem'

    def __init__(self,
            path: str,
            subtree: dict):
        self.path: str = path
        self.subtree: dict = subtree
    
class RuleTestCaseDeviceRemediation(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseDeviceRemediation'

    def __init__(self, items: [RuleTestCaseDeviceRemediationItem]):
        self.items = items


class RuleTestCaseDeviceConfigItem(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseDeviceConfigItem'

    def __init__(self,
            section: str,
            filter: str,
            config: dict):
        self.section: str = section
        self.filter: str = filter
        self.config: dict = config
    

class RuleTestCaseDeviceConfig(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseDeviceConfig'

    def __init__(self, items: [RuleTestCaseDeviceConfigItem]):
        self.items = items


class RuleTestCaseDeviceNSOConfigItem(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseDeviceNSOConfigItem'

    def __init__(
            self,
            section: str,
            path: str,
            config_subtree: str,
        ):
        self.section: str = section
        self.path: str = path
        self.config_subtree: str = config_subtree

class RuleTestCaseDeviceNSOConfig(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseDeviceNSOConfig'

    def __init__(self, items: [RuleTestCaseDeviceNSOConfigItem]):
        self.items = items


class RuleTestCaseDeviceTeardownConfig(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseDeviceTeardownConfig'

    def __init__(self, auto : bool, items: [RuleTestCaseDeviceConfigItem]):
        self.auto = auto
        self.items = items

class RuleTestCaseParamTreeItem(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseParamTreeItem'

    def __init__(self,
            level: str,
            level_key: str,
            path: str,
            subtree: str):
        
        # Possible file syntax: base[=value] example: vrf=VRF1 OR device OR bgp
        self.level: str = level # param tree level (device, customer, global, vrf, ...)
        self.level_key: str = level_key # optional param tree level key
        self.path: str = path
        self.subtree: str = subtree

class RuleTestCaseParamTree(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseParamTree'

    def __init__(self, items: [RuleTestCaseParamTreeItem]):
        self.items = items

class ActionType():
    AUDIT_REMEDIATION = 'AUDIT_REMEDIATION'
    ONBOARDING = 'ONBOARDING'
    #AUDIT_ONLY = 3
    #ONBOARDING_AUDIT_REMEDIATION = 4

class RuleTestCaseAction(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseAction'
    def __init__(self,
            type: ActionType,
            rule_name: str):
        self.type: ActionType = type
        self.rule_name: str = rule_name

class AssertionType():
    EXACT = 'EXACT' # DEFAULT
    CONTAINS = 'CONTAINS'

class AssertValue(yaml.YAMLObject):
    yaml_tag = u'!AssertValue'

    def __init__(self,
            assertion_type: AssertionType, 
            value):
        self.assertion_type = assertion_type
        self.value = value

class RuleTestCaseRemediationResultAssertion(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseRemediationResultAssertion'

    def __init__(self,
            status: str,
            errors: AssertValue,
            messages: AssertValue,
            remediation: RuleTestCaseDeviceConfigItem):
        self.status: str = status
        self.errors: AssertValue = errors
        self.messages: AssertValue = messages
        self.remediation: [RuleTestCaseDeviceConfigItem] = remediation

class RuleTestCaseOnboardingResultAssertion(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseOnboardingResultAssertion'
    
    def __init__(self,
            status: str,
            errors: AssertValue,
            messages: AssertValue,
            param_tree: RuleTestCaseParamTree):
        self.status: str = status
        self.errors: AssertValue = errors
        self.messages: AssertValue = messages
        self.param_tree: RuleTestCaseParamTree = param_tree


class RuleTestCaseAuditResultAssertion(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseAuditResultAssertion'

    def __init__(self,
            status: str,
            errors: AssertValue,
            messages: AssertValue):
        self.status: str = status
        self.errors: AssertValue = errors
        self.messages: AssertValue = messages


class RuleTestCaseAssertions(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCaseAssertions'
    def __init__(self,
            audit_result: RuleTestCaseAuditResultAssertion,
            remediation_result: RuleTestCaseRemediationResultAssertion,
            onboarding_result: RuleTestCaseOnboardingResultAssertion):
        self.audit_result = audit_result
        self.remediation_result = remediation_result
        self.onboarding_result = onboarding_result
    

class RuleTestCase(yaml.YAMLObject):
    yaml_tag = u'!RuleTestCase'

    # you can initialize attributes here, the constructor doesn't throw exceptions
    # or validate values or initialize values
    scenario = None
    device_config = None
    param_tree = None
    assertions = None

    def __init__(self,
            scenario: RuleTestCaseScenario,
            device_config: RuleTestCaseDeviceConfig,
            param_tree: RuleTestCaseParamTree,
            action: RuleTestCaseAction,
            assertions: RuleTestCaseAssertions,
            filename: str
            ):

        if scenario is None:
            raise ValueError("Expecting scenario")
        if action is None:
            raise ValueError("Expecting action")
        if assertions is None:
            raise ValueError("Expecting assertions")

        self.scenario = scenario
        self.device_config = device_config
        self.param_tree = param_tree
        self.action = action
        self.assertions = assertions
        self.filename = filename

    def __repr__(self):
        return str(self.scenario.title)
        

