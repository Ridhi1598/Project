Feature:
  This feature tests the api calls related to Velo

  Background:
    Given I generate access token for the authorization for Velo TCs
    When I set SDWAN "Velo" url

  Scenario: Customer List
    When I set Test Data for testcase "56" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/bsaf-telus-ext-customer" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: Read Customer(Fail)
    When I set Test Data for testcase "57" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/bsaf-telus-ext-customer=8?enterprise-id=123123" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    And I validate HTTP response code 404 for "GET" of SDWAN Functional Tcs

  Scenario: Read Customer
    When I set Test Data for testcase "58" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/bsaf-telus-ext-customer=8?enterprise-id=1036" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    Then I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: List Customer Templates
    When I set Test Data for testcase "59" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/bsaf-sdwan-templates?cust-name=Radha_test" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    Then I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: List Customer Device Licenses
    When I set Test Data for testcase "60" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/bsaf-sdwan-device-licenses?cust-name=Sli_1" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    Then I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: List All VPNs
    When I set Test Data for testcase "61" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/vpns?enterprise-id=2646" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    Then I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: List All VPNs(Fail)
    When I set Test Data for testcase "62" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/vpns?enterprise-id=123123" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    And I validate HTTP response code 404 for "GET" of SDWAN Functional Tcs

  Scenario: Read VPN
    When I set Test Data for testcase "63" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/vpns=Segment2?enterprise-id=2646" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    Then I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: Read VPN(Fail)
    When I set Test Data for testcase "64" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/vpns=non_existent_vpn?enterprise-id=2646" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    And I validate HTTP response code 404 for "GET" of SDWAN Functional Tcs

  Scenario: List Devices
    When I set Test Data for testcase "65" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/sites?enterprise-id=1036" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    Then I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: List Devices(Fail)
    When I set Test Data for testcase "66" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/sites?enterprise-id=123123" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    And I validate HTTP response code 404 for "GET" of SDWAN Functional Tcs

  Scenario: Read Device
    When I set Test Data for testcase "67" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/sites=14?enterprise-id=2724&device-id=SONIAENT-003-VIRTUAL-001" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    Then I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: Read Device(Fail)
    When I set Test Data for testcase "68" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/sites=14?enterprise-id=2724&device-id=non-existent-device" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    And I validate HTTP response code 404 for "GET" of SDWAN Functional Tcs

  Scenario: List All LANs
    When I set Test Data for testcase "69" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/sites=11/devices/device=SONIAENT-004-VIRTUAL-001/lan-access?enterprise-id=2724" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    Then I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: List All LANs(Fail)
    When I set Test Data for testcase "70" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/sites=11/devices/device=non-existent-device/lan-access?enterprise-id=2724" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    And I validate HTTP response code 404 for "GET" of SDWAN Functional Tcs

  Scenario: Read LAN
    When I set Test Data for testcase "71" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/sites=11/devices/device=SONIAENT-004-VIRTUAL-001/lan-access=GE2?enterprise-id=2724" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    Then I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: Read LAN(Fail)
    When I set Test Data for testcase "72" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/sites=11/devices/device=SONIAENT-004-VIRTUAL-001/lan-access=GE13?enterprise-id=2724" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    And I validate HTTP response code 404 for "GET" of SDWAN Functional Tcs

  Scenario: List All WANs
    When I set Test Data for testcase "73" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/sites=11/devices/device=Edge2/wan-access?enterprise-id=2646" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    Then I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: List All WANs(Fail)
    When I set Test Data for testcase "74" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/sites=11/devices/device=non-existent-device/wan-access?enterprise-id=2646" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    And I validate HTTP response code 404 for "GET" of SDWAN Functional Tcs

  Scenario: Read WAN
    When I set Test Data for testcase "75" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/sites=11/devices/device=Edge2/wan-access=SFP2?enterprise-id=2646" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    Then I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  Scenario: Read WAN
    When I set Test Data for testcase "96" of SDWAN Functional TCs
    Then I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services=12/sites=11/devices/device=Edge2/wan-access=SFP12?enterprise-id=2646" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    Then I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

