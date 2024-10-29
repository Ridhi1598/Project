@bngDecommission @rmq @dev
Feature: Verify the BNG devices are Decommissioned
  This features to validate the BNG Decommission is completed

  Scenario: Verify the BNG devices are Decommission
    Then I navigate to consumer Home page
    When "Home" page title should be "Dashboard"
    When I expand the "Onboarding" sidebar
    And I navigate view by clicking on "OnboardingBNG"
    Then "OnboardingBNG" page title should be "Onboarding - BNG"
    Then I validate EDTNABTFNG03 BNG status as DECOMISSION - COMPLETED

