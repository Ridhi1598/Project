@nokia @tc217 @hs @invalidSpeed
Feature: TC_217 Sequence: Create, Update and Delete BI Service
  This feature tests the api calls related to creating a Bi service with invalid speed

  Background:
    Given I read service id for test case sequence

  @createUpdateBIService @TC217
  Scenario Outline: Create service with invalid speed: TC_"<testCaseNumber>"
    Given I read test data for "<testCaseNumber>"
    And I generate access token for authorization
    When I set BI "REST" url
    When I Set "requestType" api endpoint for testcase "<testCaseNumber>"
    When I Set HEADER param request "Content-Type" as "application/json" for BI
    And I Set HEADER param request "Authorization" as "access-token" for BI
    And Set request Body for BI
    And Send HTTP request for BI
    And Execute the request in case of update
    And I validate the controller response as "failed"
    And Validate the error message coming from "NSO"

  Examples:
      |testCaseNumber|
      |217           |