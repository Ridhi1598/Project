#@@ -0,0 +1,36 @@
Feature:
  This feature tests the api calls related to read Device Overview and Device Overview Edit

  Background:
    Then I generate access token for the authorization for Portal TCs
    Given I set SDWAN "Portal" url

  Scenario: Device Overview
    When I set Test Data for testcase "45" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa/sdwan/overview/site?service_id=600a35db-05cd-4d33-8130-aa4a078bc267&site_id=691be7df-a252-4dcd-9c6d-c9fa6751eaaf&cust_name=Sonia_Ent" for the Portal testcases
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: Device Overview Edit
    When I set Test Data for testcase "46" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa/sdwan/site/view?service_id=f14ad1bc-3667-466b-98ea-b19b93d96278&site_id=a16b7426-b6f0-4b8a-ae7a-a048828a3efb" for the Portal testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs
