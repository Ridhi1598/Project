@nokia @tc10 @ipv6remove @dsl
Feature: TC_10 Sequence: Create, Update and Delete BI Service
  This feature tests the api calls related to creating, updating and deleting a Bi service

  Background: Read Service Id
  Given I read service id for test case sequence

  @createUpdateDeleteBIService @TC10
  Scenario Outline: Create/Update service with valid payload and in valid state: TC_"<testCaseNumber>"
    Given I read test data for "<testCaseNumber>"
    And I generate access token for authorization
    When I set BI "REST" url
    When I Set "requestType" api endpoint for testcase "<testCaseNumber>"
    When I Set HEADER param request "Content-Type" as "application/json" for BI
    And I Set HEADER param request "Authorization" as "access-token" for BI
    And Set request Body for BI
    And Send HTTP request for BI
    And Execute the request in case of update
    And I validate the controller response as "completed"
    Then I download config files for testcase "<testCaseNumber>"
    And I validate the generated configurations

  Examples:
      |testCaseNumber|
      |10            |
      |34            |
      |48            |

  @createUpdateBIService @TC10 @deleteService
  Scenario: Delete the created service for TC_10 which is in valid state
    Given I read test data for "89"
    And I generate access token for authorization
    When I set BI "REST" url
    When I Set "requestType" api endpoint for testcase "89"
    When I Set HEADER param request "Content-Type" as "application/json" for BI
    And I Set HEADER param request "Authorization" as "access-token" for BI
    And Set request Body for BI
    And Send HTTP request for BI
    And I validate the controller response as "completed"