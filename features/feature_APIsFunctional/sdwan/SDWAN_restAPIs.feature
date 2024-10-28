@demo
Feature: SDWAN restAPIs
  This features tests the functionality related SDWAN APIs

  Background:
    Given I set SDWAN "REST" url

  @sdwanLogin
  Scenario: LogIn Scenerio
    Given I Set POST posts api endpoint for "/login/enterpriseLogin"
    When I Set HEADER param request "Content-Type" as "application/json"
    And Set request Body for "login" API of SDWAN
    And Send POST HTTP request for Login
    Then I receive valid HTTP response code 200 for "POST"

 @readAllEnterprises
 Scenario: Read all enterprises(customers)
    Given I Set POST posts api endpoint for "/enterpriseProxy/getEnterpriseProxyEnterprises"
    When I Set HEADER param request "Content-Type" as "application/json"
      And Set request Body for "blankBody" API of SDWAN
    And I Set HEADER param request "sdwancookie" as "Cookie" for SDWAN
    And Send POST HTTP request
    Then I receive valid HTTP response code 200 for "POST"
    And I validate the response schema with "getEnterpriseProxyEnterprises.json"

 @getGivenEnterprises
  Scenario: Get a given enterprise
    Given I Set POST posts api endpoint for "/enterprise/getEnterprise"
    When I Set HEADER param request "Content-Type" as "application/json"
    And Set request Body for "get_given_enterprises" API of SDWAN
    And I Set HEADER param request "sdwancookie" as "Cookie"
    And Send POST HTTP request
    Then I receive valid HTTP response code 200 for "POST"
    And I validate the response schema with "get_a_given_enterprise.json"


  @readAllSegmentsUnderAnEnterprise
  Scenario: Get a given enterprise
    Given I Set POST posts api endpoint for "/enterprise/getEnterpriseNetworkSegments"
    When I Set HEADER param request "Content-Type" as "application/json"
    And Set request Body for "read_all_segment_under_an_enterprise" API of SDWAN
    And I Set HEADER param request "sdwancookie" as "Cookie"
    And Send POST HTTP request
    Then I receive valid HTTP response code 200 for "POST"
    And I validate the response schema with "read_all_segment_under_an_enterprise.json"

    @getAllEdgesUnderAnEnterprise
    Scenario: Get all edges under an enterprise
      Given I Set POST posts api endpoint for "/enterprise/getEnterpriseEdgeList"
      When I Set HEADER param request "Content-Type" as "application/json"
      And Set request Body for "get_all_edges_under_an_enterprise" API of SDWAN
      And I Set HEADER param request "sdwancookie" as "Cookie"
      And Send POST HTTP request
      Then I receive valid HTTP response code 200 for "POST"
      And I validate the response schema with "get_all_edges_under_an_enterprise.json"

    @getAGivenEdge
    Scenario: Get all edges under an enterprise
      Given I Set POST posts api endpoint for "/edge/getEdge"
      When I Set HEADER param request "Content-Type" as "application/json"
      And Set request Body for "get_a_given_edge" API of SDWAN
      And I Set HEADER param request "sdwancookie" as "Cookie"
      And Send POST HTTP request
      Then I receive valid HTTP response code 200 for "POST"
      And I validate the response schema with "get_a_given_edge.json"

    @getEdgeConfigurationStack
    Scenario: Get all edges under an enterprise
      Given I Set POST posts api endpoint for "/edge/getEdgeConfigurationStack"
      When I Set HEADER param request "Content-Type" as "application/json"
      And Set request Body for "get_edge_configuration_stack" API of SDWAN
      And I Set HEADER param request "sdwancookie" as "Cookie"
      And Send POST HTTP request
      Then I receive valid HTTP response code 200 for "POST"
      And I validate the response schema with "get_edge_configuration_stack.json"
