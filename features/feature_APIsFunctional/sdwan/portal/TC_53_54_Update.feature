Feature:
  This feature tests the api calls related to edit LAN & edit WAN interface

  Background:
    Then I generate access token for the authorization for Portal TCs
    Given I set SDWAN "Portal" url

  Scenario: Edit LAN Interfaces
    When I set Test Data for testcase "53" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa/sdwan/site/view?service_id=7e23c87a-48a3-4b0d-9f7c-d3ef913a90af&site_id=7db78f4b-e09d-4948-a65f-ebd071b8aac0" for the Portal testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: Edit WAN Interfaces
    When I set Test Data for testcase "54" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa.tlabs.ca/tinaa/sdwan/site/view?service_id=7e23c87a-48a3-4b0d-9f7c-d3ef913a90af&site_id=7db78f4b-e09d-4948-a65f-ebd071b8aac0" for the Portal testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs