@portal @tc107
Feature: Login with Read-only user
  This feature tests the functionality related with Read-User

  Scenario: Login - Read user
    Given I set data values against testcase "107"
#    When I should land on CS Home page
#    Then "Home" page title should be "Dashboard"
    When I login into the application with read-only user
    Then I go to "Home"
    Then I validate that the "UserManagement" option should not be visible for read-only user

  Scenario: This scenario validates that the OTL page is visible for the read-only user
    When I click on "L2Topology" button
    Then I click on "OLT" button
    Then "OLT" page title should be "L2 Topology - OLT"


  Scenario: This scenario validates that the Onboarding BNG page is visible for the read-only user and ensures that the 'Onboard' button is disabled as well
    When I go to "Home"
    Then I expand the "Onboarding" sidebar
    And I navigate view by clicking on "OnboardingBNG"
    Then "OnboardingBNG" page title should be "Onboarding - BNG"
    Then I am searching for the first BNG on the BNG Onboarding BNG page
    Then Verify that "Onboard" button is disable

  Scenario: This scenario validates that the Onboarding OLT page is visible for the read-only user and ensures that the 'Onboard' button is disabled as well
    When I go to "Home"
    And I navigate view by clicking on "OnboardingOLT"
    Then "OnboardingOLT" page title should be "Onboarding - OLT"
    Then I am searching for the first OLT on the BNG Onboarding OLT page
    Then Verify that "Onboard" button is disable

  Scenario: This scenario validates that the L2-Topology page is visible. Also, it confirms that the read-only user should not be able to see the delete button for the nodes and ensures that the 'Add New' button is disabled as well
    When I go to "Home"
    Then I expand the "L2Topology" sidebar
    When I navigate view by clicking on "OLT" for CS
    Then "OLT" page title should be "L2 Topology - OLT"
    When I search for available "OLT" to "Onboarding"
    Then I click on "firstOLT" button
    Then Verify that "addNewNode" button is disable
    When I confirm that the selected OLT is as expected
    When I validate that the delete icon is not visible for the "nodes"
    Then I validate the expected OLT should exist in the Node table


  Scenario: This scenario validates that the L2-Topology page is visible for the read-only user and ensures that the 'Add new Lag' button is disabled as well
    When I go to "OLT"
    Then I validate that the expected lag should exist in the Termination points
    Then I validate that the delete icon is not visible for the "lag"
    Then Verify that "addNewLag" button is disable


  Scenario: This scenario validates that the Link should be visible for the read-only user and ensures that the 'Add Link' button is disabled as well
    When I click on "Next" button
    Then I validate that the link should be added in the selected lag
    Then Verify that "addLink" button is disable


  Scenario: This scenario validates that the read-only user should not be able to see the delete button for the link
    Given I go to "OLT"
    When I validate that the delete icon is not visible for the "link"

 @tc12
  Scenario: This scenario validates that the Onboard a new BNG pair button should be disabled
    Given I expand the "Onboarding" sidebar
    When I navigate view by clicking on "OnboardingBNG"
    Then "OnboardingBNG" page title should be "Onboarding - BNG"
    Then Verify that "OnboardANewBNGPair" button is disable

  Scenario: This scenario validates that the Add OLT button should be disabled
    When I click on "L2Topology" button
    Then I click on "OLT" button
    Then "OLT" page title should be "L2 Topology - OLT"
    Then Verify that "AddOLT" button is disable


