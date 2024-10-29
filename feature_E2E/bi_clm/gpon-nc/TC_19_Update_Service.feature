@updateCLMService @TC19 @pon
Feature: TC_19 Sequence: BI_CLM Update Service
  This feature tests the end to end functionality of update, display and execute request

  Scenario Outline: TC_19 - <action> Service - Telus Managed IPv4 only BGP Default Full Routes to Dual Stack
    Given I read test data for testcase
    When I validate that "service" is in expected state for "<action>" operation
    When I create "sftp" connection with "primary" "device" and download "before" "config" for "<action>" scenario
    When I create "sftp" connection with "secondary" "device" and download "before" "config" for "<action>" scenario
    And I generate access token for authorization
    When I send request for "<action>" "service" via "<component>"
    Then I extract response value for "requestId"
    And I "monitor" that the request "state" is "completed"
    Then Validate the "current" and "expected" "config" in case of "display"
    When I fetch "service" record for "<action>" operation from "ES" records
    Then I validate that service record state for "<action>" is as expected
    When I create "sftp" connection with "primary" "device" and download "after" "config" for "<action>" scenario
    When I create "sftp" connection with "secondary" "device" and download "after" "config" for "<action>" scenario
    When I find the diff between the "before" and "after" config for "primary" for "<action>" service
    When I find the diff between the "before" and "after" config for "secondary" for "<action>" service
    Then I validate that the "config diff" is successfully matched with "expected config diff" for "primary" for "<action>" service
    Then I validate that the "config diff" is successfully matched with "expected config diff" for "secondary" for "<action>" service

  Examples:
      |action           |component  |
      |create           |api-gateway|
      |create-display   |ingestion  |
      |create-execute   |ingestion  |
      |update           |ingestion  |
      |update-display   |ingestion  |
      |update-execute   |ingestion  |
      |delete           |api-gateway|
      |delete-display   |ingestion  |
      |delete-execute   |ingestion  |