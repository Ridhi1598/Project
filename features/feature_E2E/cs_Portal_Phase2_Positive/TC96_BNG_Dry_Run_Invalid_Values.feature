@tc_96
Feature: Negative - BNG dry run with invalid values
   This feature tests the negative scenario of BNG dry run with invalid values

  Scenario: BNG dry run with invalid values
    Given I set data values against testcase "96"
#
#    When I should land on CS Home page
#    Then "Home" page title should be "Dashboard"
#    When I expand the "Onboarding" sidebar
#
    And I navigate view by clicking on "OnboardingBNG"
    Then "OnboardingBNG" page title should be "Onboarding - BNG"
    When I click on "OnboardANewBNGPair" button
    Then I provided the necessary information to create a BNG dry run using incorrect values
#    When I click on "Next" button