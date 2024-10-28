@deviceCatalog @tc1
Feature: Retrieve all SE Devices
  This feature tests the functional test cases related to retrieve and validate all the SE Devices

  Scenario: tc_1: Retrieve all SE Devices
    Given I read test data for Device catalog testcases
    When I set "device-catalog" url
    Then I generate access token for authorization
    When I set endpoint for "deviceCatalog" requests
    Then I Set headers "Content" and "Authorization"
    Then I Set query parameters for Device catalog requests
    When I Send HTTP request for "device-catalog" APIs
    Then Ensure that the HTTP response code is "200"
    Then I validate that the




