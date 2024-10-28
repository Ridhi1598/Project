Feature:
  This feature tests the api calls related to Customer List,Customer Homepage & Network List

  Background:
    Then I generate access token for the authorization for Portal TCs
    Given I set SDWAN "Portal" url

  Scenario: Customer List
    When I set Test Data for testcase "33" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa/sdwan/customer/list" for the Portal testcases
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: Customer Homepage
    When I set Test Data for testcase "34" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa/sdwan/customer/list/069188ab-bc08-4b24-bf7e-d340c91d02eb" for the Portal testcases
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: Network List
    When I set Test Data for testcase "35" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa/sdwan/network/view?service_id=600a35db-05cd-4d33-8130-aa4a078bc267&cust_name=Sonia_Ent" for the Portal testcases
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs