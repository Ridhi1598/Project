Feature:
  This feature tests the api calls related to VLANs,LANs & WANs-Device Config

  Background:
    Then I generate access token for the authorization for Portal TCs
    Given I set SDWAN "Portal" url

  Scenario: VLANs(Device Config)
    When I set Test Data for testcase "47" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa/sdwan/vlan/view?service_id=600a35db-05cd-4d33-8130-aa4a078bc267&site_id=691be7df-a252-4dcd-9c6d-c9fa6751eaaf&device_id=test_device_doc1" for the Portal testcases
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: LANs(Device Config)
    When I set Test Data for testcase "48" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa/sdwan/vlan/view?service_id=600a35db-05cd-4d33-8130-aa4a078bc267&site_id=691be7df-a252-4dcd-9c6d-c9fa6751eaaf&device_id=test_device_doc1" for the Portal testcases
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: WAN Interfaces((Device Config)
    When I set Test Data for testcase "49" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I Set HEADER param request "sdwancookie" as "cookie_value" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa/sdwan/device/wan/interface/view?service_id=600a35db-05cd-4d33-8130-aa4a078bc267&site_id=691be7df-a252-4dcd-9c6d-c9fa6751eaaf&device_id=test_device_doc1" for the Portal testcases
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs