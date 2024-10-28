@bngDecommission @rmq @dev
Feature: Verify the OLT devices are Decommissioned
  This features to validate the OLT Decommission is completed

  Scenario: Verify the OLT devices are Decommission
    Then I navigate to consumer Home page
    Then "Home" page title should be "Dashboard"
    When I expand the "Onboarding" sidebar
    And I navigate view by clicking on "OnboardingOLT"
    Then "OnboardingOLT" page title should be "Onboarding - OLT"
    Then I validate EDTNABTFOT39 OLT status as DECOMISSION - COMPLETED