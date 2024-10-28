@tc_95
Feature: Negative - BNG parameters should be disable
   This feature tests the negative scenario of validating the BNG parameters

  Scenario: BNG parameters should be disable
    Given I set data values against testcase "95"
#
#    When I should land on CS Home page
#    Then "Home" page title should be "Dashboard"
#    When I expand the "Onboarding" sidebar
#
    And I navigate view by clicking on "OnboardingBNG"
    Then "OnboardingBNG" page title should be "Onboarding - BNG"
    When I click on "OnboardANewBNGPair" button
#    Then I validate that the BNG parameters should be disable
