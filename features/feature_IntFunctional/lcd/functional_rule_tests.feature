@fixture.load_rule_tests
Feature: Audit Remediation Rule
  Validation of different functional tests using YAML

  Scenario Outline: Rule Test
    Given Feature under test is "<testdir>"
      And I load test in "<ymlfile>"
      And I set device_type to "<device_type>"
      And @"<given>"
      When I run the test
      and I receive test results
      and @"<when>"
      Then @"<then>"


    # Examples: Audit Rule Tests
    #    | dir  | ymlfile       | device_type         | given     | when     | then
    #    | dir1 | test-1.yml    | netsim_cisco_ios    | message   | message  | message
    #    | dir2 | test-2.yml    | netsim_cisco_ios    | message   | message  | message
