Feature:
  This feature tests the api calls related to Add,Update & Delete VLAN

  Background:
    Then I generate access token for the authorization for Portal TCs
    Given I set SDWAN "Portal" url

  Scenario: Add VLAN
    When I set Test Data for testcase "50" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set POST api endpoint "/tinaa/sdwan/vlan/view?service_id=600a35db-05cd-4d33-8130-aa4a078bc267&site_id=691be7df-a252-4dcd-9c6d-c9fa6751eaaf&device_id=test_device_doc1&name=GE1" for the Portal testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs


  Scenario: Edit VLANs
    When I set Test Data for testcase "51" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa/sdwan/site/view?service_id=600a35db-05cd-4d33-8130-aa4a078bc267&site_id=691be7df-a252-4dcd-9c6d-c9fa6751eaaf" for the Portal testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: Delete VLAN
    When I set Test Data for testcase "52" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set DELETE api endpoint "/tinaa/sdwan/site/view?service_id=600a35db-05cd-4d33-8130-aa4a078bc267&site_id=691be7df-a252-4dcd-9c6d-c9fa6751eaaf" for the Portal testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs