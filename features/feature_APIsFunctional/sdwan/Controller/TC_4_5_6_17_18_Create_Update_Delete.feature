Feature: SDWAN VPN APIs
  This feature tests the api calls related to Create Patch and Delete SDWAN VPN

  Background:
    Given I generate access token for the authorization of SDWAN Functional Tcs
    When I set SDWAN "Functional" url

  @TC4 @TC15 @ReadService
  Scenario: Generate Access token and Read Services
    When I set Test Data for testcase "15" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs
    Then I extract response value of service-id and cust-id for SDWAN Functional TCs

  @TC4 @TC17 @ReadVPN
  Scenario: Read VPNs
    When I set Test Data for testcase "17" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    Then I set GET api endpoint "/tinaa-sdwan-services/{service-id}/vpns" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs
    Then I extract the vpn-id from the lists all SDWAN VPNs in given SDWAN service

  @TC4 @CreateVPN
  Scenario: creates a SDWAN VPN in given SDWAN service
    When I set Test Data for testcase "4" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    Then I Set POST posts api endpoint for "/tinaa-sdwan-services/{service-id}/vpns" API of sdwan Functional
    And Set request Body for SDWAN Functional TCs
    And Set the Updated values of payload for creates a SDWAN VPN
    And Send HTTP request for SDWAN Functional TCs

  @TC4 @TC18 @ReadListofVPN
  Scenario: Returns a list of VPNs in given SDWAN service
    When I set Test Data for testcase "18" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services/{service-id}/vpns/{vpn-id}" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  @TC4 @TC5 @UpdateVPN
  Scenario: updates a SDWAN VPN in given SDWAN service
    When I set Test Data for testcase "5" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa-sdwan-services/{service-id}/vpns/{vpn-id}" for SDWAN Functional TCs
    And Set request Body for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs
    Then Set the Updated values of payload to update a SDWAN VPN
    And Send HTTP request for SDWAN Functional TCs
    Then I extract requestId from response of "PUT" request for ElasticSearch Database Validation
    Then I perform ElasticSearch Database Validation for "PUT" request

#  @TC4 @TC6 @DeleteVPN
#  Scenario: Delete VPN by Id
#    When I set Test Data for testcase "6" of SDWAN Functional TCs
#    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
#    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
#    When I set Delete api endpoint "/tinaa-sdwan-services/{service-id}/vpns/{vpn-id}" for SDWAN Functional Tcs
#    And Send HTTP request for SDWAN Functional TCs
#    When I receive valid HTTP response code 200 for "DELETE" of SDWAN Functional TCs