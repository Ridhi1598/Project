Feature: TC_52 Sequence: Create service : Success
  This feature tests the functionality related to create the Service : success

  Scenario: TC_52  - Create service : Success
    Given I read test data for testcase
    When I create "sftp" connection with "primarySE" "device" and download "before" "config" for "create" cs scenario
    Then I create "sftp" connection with "secondarySE" "device" and download "before" "config" for "create" cs scenario
    When I create "sftp" connection with "primaryBNG" "device" and download "before" "config" for "create" cs scenario
    Then I create "sftp" connection with "secondaryBNG" "device" and download "before" "config" for "create" cs scenario

         #   OPERATION THAT WILL HAPPEN IN BETWEEN
         #   BNG E2E Testcase
        #   BNG E2E Testcase

    When I create "sftp" connection with "primarySE" "device" and download "after" "config" for "create" cs scenario
    Then I create "sftp" connection with "secondarySE" "device" and download "after" "config" for "create" cs scenario
    When I create "sftp" connection with "primaryBNG" "device" and download "after" "config" for "create" cs scenario
    Then I create "sftp" connection with "secondaryBNG" "device" and download "after" "config" for "create" cs scenario
    When I find the diff between the "before" and "after" config for "primarySE" for "create" cs service
    Then I find the diff between the "before" and "after" config for "secondarySE" for "create" cs service
    When I find the diff between the "before" and "after" config for "primaryBNG" for "create" cs service
    Then I find the diff between the "before" and "after" config for "secondaryBNG" for "create" cs service
#    Then I validate that the "config diff" is successfully matched with "expected config diff" for "primary" for "<action>" cs service
#    Then I validate that the "config diff" is successfully matched with "expected config diff" for "secondary" for "<action>" cs service

