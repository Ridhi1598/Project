Feature:
  This feature tests the api calls related to Device List

  Background:
    Then I generate access token for the authorization for Portal TCs
    Given I set SDWAN "Portal" url

  Scenario: Device List
    When I set Test Data for testcase "39" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa/sdwan/site/view?service_id=600a35db-05cd-4d33-8130-aa4a078bc267&cust_name=Sonia_Ent" for the Portal testcases
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs