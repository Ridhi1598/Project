@createMWRService @TC26 @pon @mwr
Feature: TC_26 Sequence: BI_CLM Add MWR Service
  This feature tests the end to end functionality of service creation and adding mwr

  Scenario Outline: TC_26 - <action> Service - Provider Managed ipv4 BGP Default Routes
    Given I read test data for testcase
    When I validate that "service" is in expected state for "<action>" operation
    When I create "sftp" connection with "mwr" "device" and download "before" "config" for "<action>" scenario
    When I create "sftp" connection with "primary" "device" and download "before" "config" for "<action>" scenario
    When I create "sftp" connection with "secondary" "device" and download "before" "config" for "<action>" scenario
    And I generate access token for authorization
    When I send request for "<action>" "service" via "<component>"
    Then I extract response value for "requestId"
    And I "monitor" that the request "state" is "completed"
    Then Validate the "current" and "expected" "config" in case of "display"
    When I fetch "service" record for "<action>" operation from "ES" records
    Then I validate that service record state for "<action>" is as expected
    When I create "sftp" connection with "mwr" "device" and download "after" "config" for "<action>" scenario
    When I create "sftp" connection with "primary" "device" and download "after" "config" for "<action>" scenario
    When I create "sftp" connection with "secondary" "device" and download "after" "config" for "<action>" scenario
    When I find the diff between the "before" and "after" config for "mwr" for "<action>" service
    When I find the diff between the "before" and "after" config for "primary" for "<action>" service
    When I find the diff between the "before" and "after" config for "secondary" for "<action>" service
    Then I validate that the "config diff" is successfully matched with "expected config diff" for "mwr" for "<action>" service
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
      |add_mwr          |api-gateway|
      |rollback         |ingestion  |
      |rollback-display |ingestion  |
      |rollback-execute |ingestion  |
      |delete           |api-gateway|
      |delete-display   |ingestion  |
      |delete-execute   |ingestion  |