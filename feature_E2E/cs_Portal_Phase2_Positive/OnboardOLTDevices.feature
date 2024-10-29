@cse2e
Feature: To add the L2 Topology - OLT
  This feature is to add the Nodes

  Scenario: tc_52: Create service : Success
    Given I read test data for e2e test case
    When I create "sftp" connection with "primarySE" "device" and download "before" "config" for "create" cs scenario
    Then I create "sftp" connection with "secondarySE" "device" and download "before" "config" for "create" cs scenario
    When I create "sftp" connection with "primaryBNG" "device" and download "before" "config" for "create" cs scenario
    Then I create "sftp" connection with "secondaryBNG" "device" and download "before" "config" for "create" cs scenario

  Scenario: TC25 Onboard OLT - Create OLT config - Dry Run
    Then I navigate to consumer Home page
    Then "Home" page title should be "Dashboard"
    When I expand the "Onboarding" sidebar
    And I navigate view by clicking on "OnboardingOLT"
    Then "OnboardingOLT" page title should be "Onboarding - OLT"
    Then I Search EDTNABTFOT39 OLT and click on Onboard CTA
    Then I Select the BNG Group CLLI ID EDTNABTFNG03-EDTNABTFNG04 OLT drop down value
    Then I click on Next CTA
    Then I validate that Validate text is displayed

  Scenario: TC24: Unlock OLT pair's L2 resources
    Then user click on Discard CTA
    Then I verify the Page URL contains dashboard/onboarding/onboarding-olt

  Scenario: TC25: Onboard OLT - Create OLT config - Dry Run
    Then I Search EDTNABTFOT39 OLT and click on Onboard CTA
    Then I Select the BNG Group CLLI ID EDTNABTFNG03-EDTNABTFNG04 OLT drop down value
    Then I click on Next CTA
    Then I validate that Validate text is displayed
    Then I enter OLT mac-address as 3c:8b:cd:7c:05:2e
    #Then I enter SE-x1 Interface Address as 10.157.3.193/27
    #Then I enter SE-x2 Interface Address as 10.157.3.194/27
    And I click on "DryRun" Button
    Then Wait and verify for OLT DryRun to be completed for EDTNABTFOT39

  Scenario: TC18: Onboard BNG - Create BNG Config - Dry Run - Download Config
    Then I click on OLT Download Config button
    #Then I unzip onboarding-olt-config.zip folder and move in Framework directory and Delete the actual downloaded zip folder from download folders

  Scenario: TC19: Onboard BNG - Create BNG Config - Dry Run - Reject Config
    Then I click on OLT Reject button
    Then I click on Yes Reject CTA on reject confirmation overlay
    Then I validate the Commit request reject message is display and close the overlay
    Then I validate EDTNABTFOT39 OLT status as DRY RUN - REJECTED

  Scenario: TC20: Onboard BNG - Push BNG config
    Then I Search EDTNABTFOT39 OLT and click on Onboard CTA
    Then I Select the BNG Group CLLI ID EDTNABTFNG03-EDTNABTFNG04 OLT drop down value
    Then I click on Next CTA
    Then I validate that Validate text is displayed
    Then I click on reload input fields toggle icon to reload all the input values
    And I click on "DryRun" Button
    Then Wait and verify for OLT DryRun to be completed for EDTNABTFOT39
    Then I click on OLT Commit button
    Then I click on commit CTA on commit confirmation overlay
    Then I validate the Commit request success message is display and close the overlay
    Then I verify the Page URL contains dashboard/onboarding/onboarding-olt
    Then I validate EDTNABTFOT39 OLT status as COMMIT - IN PROGRESS
    Then I wait until EDTNABTFOT39 OLT dry run is completed and disappear from the OLT list

  Scenario: tc_52: Create service : Success
    When I create "sftp" connection with "primarySE" "device" and download "after" "config" for "create" cs scenario
    Then I create "sftp" connection with "secondarySE" "device" and download "after" "config" for "create" cs scenario
    When I create "sftp" connection with "primaryBNG" "device" and download "after" "config" for "create" cs scenario
    Then I create "sftp" connection with "secondaryBNG" "device" and download "after" "config" for "create" cs scenario
    When I find the diff between the "before" and "after" config for "primarySE" for "create" cs service
    Then I find the diff between the "before" and "after" config for "secondarySE" for "create" cs service
    When I find the diff between the "before" and "after" config for "primaryBNG" for "create" cs service
    Then I find the diff between the "before" and "after" config for "secondaryBNG" for "create" cs service

    #Then I validate that the "config diff" is successfully matched with "expected config diff" for "primaryBNG" for "create" cs service
    Then I validate that the "config diff" is successfully matched with "expected config diff" for "primarySE" for "create" cs service
    Then I validate that the "config diff" is successfully matched with "expected config diff" for "secondaryBNG" for "create" cs service
    Then I validate that the "config diff" is successfully matched with "expected config diff" for "secondarySE" for "create" cs service

