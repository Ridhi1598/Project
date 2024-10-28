Feature:
  This feature tests the api calls related to Portal Login session

  Background:
    Then I generate access token for the authorization for Portal TCs
    Given I set SDWAN "Portal" url

  Scenario: Portal login session
    When I set Test Data for testcase "32" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/" for the Portal testcases
    And Send GET Http request for the functional TCS of SDWAN Portal
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs


#  Scenario: Customer List
#    When I set Test Data for testcase "33" of SDWAN Functional TCs
#    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
#    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
#    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
#    And I set GET api endpoint "/tinaa/sdwan/customer/list" for the Portal testcases
#    And Send HTTP request for the Portal testcase
#    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs





