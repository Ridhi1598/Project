@cse2e
Feature: To add the L2 Topology - OLT
  This feature is to add the Nodes

  Scenario: tc_51: Create service : Success
    Given I read test data for e2e test case
    When I create "sftp" connection with "primaryBNG" "device" and download "before" "config" for "create" cs scenario
    Then I create "sftp" connection with "secondaryBNG" "device" and download "before" "config" for "create" cs scenario

  Scenario: TC14 and TC15 Add BNG Pair & Lock and Validate BNG pair's L2 resources (pre-config validation checks)
    Then I navigate to consumer Home page
    When "Home" page title should be "Dashboard"
    When I expand the "Onboarding" sidebar
    And I navigate view by clicking on "OnboardingBNG"
    Then "OnboardingBNG" page title should be "Onboarding - BNG"
    And I click on "OnboardANewBNGPair" button
    Then I add BNG1 as EDTNABTFNG03
    Then I select EDTNABTFNG03 as BNG1
    Then I add BNG2 as EDTNABTFNG04
    Then I select EDTNABTFNG04 as BNG2
    When I wait for "15" seconds
    Then I click on Next CTA
    Then I validate that Validate text is displayed


  Scenario: TC16: Unlock BNG pair's L2 resources
    Then user click on Discard CTA
    Then I verify the Page URL contains dashboard/onboarding/onboarding-bng

  Scenario: TC17: Onboard BNG - Create BNG Config - Dry Run
    And I click on "OnboardANewBNGPair" button
    Then I add BNG1 as EDTNABTFNG03
    Then I select EDTNABTFNG03 as BNG1
    Then I add BNG2 as EDTNABTFNG04
    Then I select EDTNABTFNG04 as BNG2
    Then I click on Next CTA
    Then I validate that Validate text is displayed
Then I enter below data for IPV4 Address Pool Servers ODD Input fields
      | LabelName            | InputValue      |
      | IP Address           | 10.195.0.57/32  |
      | v4 DYNAMIC           | 10.160.61.32/27 |
      | v4 NAT444            | 100.80.13.0/27  |
      | v4 STATIC UNREG      | 10.160.63.0/27  |
      | v4 BVOICE UNREG      | 10.159.64.0/27  |
      | v4 CPEMGMT           | 10.159.63.96/27 |
      | v4 STB               | 100.81.13.0/27  |
      | v4 STATIC REGISTERED | 10.160.63.64/27 |
      | v4 BVOICE REGISTERED | 11.160.63.64/27 |
    Then I enter below data for IPV4 Address Pool Servers EVEN Input fields
      | LabelName            | InputValue      |
      | IP Address           | 10.195.0.58/32  |
      | v4 DYNAMIC           | 10.160.61.0/27  |
      | v4 NAT444            | 100.80.13.32/27 |
      | v4 STATIC UNREG      | 10.160.63.32/27 |
      | v4 BVOICE UNREG      | 10.158.64.0/27  |
      | v4 CPEMGMT           | 10.158.63.96/27 |
      | v4 STB               | 100.81.13.32/27 |
      | v4 STATIC REGISTERED | 10.160.63.96/27 |
      | v4 BVOICE REGISTERED | 11.160.63.96/27 |

    Then I enter below data for IPV4 Address Pool Servers DV Input fields
      | LabelName  | InputValue      |
      | IP Address | 10.195.0.24/32  |
      | v4 DV ODD  | 10.160.62.64/27 |
      | v4 DV EVEN | 10.160.62.96/27 |
    Then I enter below data for IPV6 Address Pool Servers V6-ODD Input fields
      | LabelName  | InputValue               |
      | IP Address | 2001:568:801:100::57/128 |
      | DYNAMIC    | 2001:568:82f:1000::/52   |
    Then I enter below data for IPV6 Address Pool Servers V6-EVEN Input fields
      | LabelName  | InputValue               |
      | IP Address | 2001:568:801:100::58/128 |
      | DYNAMIC    | 2001:568:82f::/52        |
    Then I enter below data for BNG Addresses Input fields
      | LabelName                                  | InputValue  |
      | System interface IP address - EDTNABTFNG03 | 10.0.0.1    |
      | MZ loopback interface IP address           | 192.168.2.1 |
      | System interface IP address - EDTNABTFNG04 | 10.0.0.2    |
      | MZ loopback interface IP address           | 192.168.2.2 |
    Then I enter HSIA IES Address as 172.25.99.88/31
    Then I enter VOICE IES Address as 10.198.1.2/31
    And I click on "DryRun" Button
    Then wait and verify the BNG dry run is completed for EDTNABTFNG03 : EDTNABTFNG04

  Scenario: TC18: Onboard BNG - Create BNG Config - Dry Run - Download Config
    Then I click on OLT Download Config button
    #Then I unzip onboarding-bng-config.zip folder and move in Framework directory and Delete the actual downloaded zip folder from download folders

  Scenario: TC19: Onboard BNG - Create BNG Config - Dry Run - Reject Config
    Then I click on OLT Reject button
    Then I click on Yes Reject CTA on reject confirmation overlay
    Then I validate the Commit request reject message is display and close the overlay
    Then I validate EDTNABTFNG03 BNG status as DRY RUN - REJECTED

  Scenario: TC20: Onboard BNG - Push BNG config
    Then I Search EDTNABTFNG03 BNG and click on Onboard CTA
    Then I click on Next CTA
    Then I validate that Validate text is displayed
    Then I click on reload input fields toggle icon to reload all the input values
    And I click on "DryRun" Button
    When I wait for "60" seconds
    Then wait and verify the BNG dry run is completed for EDTNABTFNG03 : EDTNABTFNG04
    Then I click on OLT Commit button
    Then I click on commit CTA on commit confirmation overlay
    Then I validate the Commit request success message is display and close the overlay
    Then I verify the Page URL contains dashboard/onboarding/onboarding-bng
    Then I validate EDTNABTFNG03 BNG status as COMMIT - IN PROGRESS
    Then I wait until EDTNABTFNG03 BNG dry run is completed and disappear from the BNG list

  Scenario: tc_51: Create service : Success
    When I create "sftp" connection with "primaryBNG" "device" and download "after" "config" for "create" cs scenario
    Then I create "sftp" connection with "secondaryBNG" "device" and download "after" "config" for "create" cs scenario
    When I find the diff between the "before" and "after" config for "primaryBNG" for "create" cs service
    Then I find the diff between the "before" and "after" config for "secondaryBNG" for "create" cs service
    Then I validate that the "config diff" is successfully matched with "expected config diff" for "primaryBNG" for "create" cs service
    Then I validate that the "config diff" is successfully matched with "expected config diff" for "secondaryBNG" for "create" cs service
