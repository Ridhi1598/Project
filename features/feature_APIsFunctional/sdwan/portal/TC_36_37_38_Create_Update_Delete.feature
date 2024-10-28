Feature:
  This feature tests the api calls related to Add,Edit & Delete Network

  Background:
    Then I generate access token for the authorization for Portal TCs
    Given I set SDWAN "Portal" url

  Scenario: Add Network
    When I set Test Data for testcase "36" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set POST api endpoint "/tinaa/sdwan/network/view?service_id=600a35db-05cd-4d33-8130-aa4a078bc267" for the Portal testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: Edit Network
    When I set Test Data for testcase "37" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa/sdwan/network/view?service_id=7e23c87a-48a3-4b0d-9f7c-d3ef913a90af&vpn_id=FIM_segment" for the Portal testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: Delete Network
    When I set Test Data for testcase "38" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set DELETE api endpoint "/tinaa/sdwan/network/view?service_id=600a35db-05cd-4d33-8130-aa4a078bc267&vpn_id=BZZ_segment" for the Portal testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs