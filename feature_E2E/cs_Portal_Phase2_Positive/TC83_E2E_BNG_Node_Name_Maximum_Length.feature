Feature: Negative - Add empty BNG name
  This feature tests the negative scenario of BNG node name with maximum length

  Scenario: Negative - Add BNG node name with maximum length
    Given I set data values against testcase "83"
#    When I should land on CS Home page
#    Then I go to "Home" page
#    Then "Home" page title should be "Dashboard"
#    Then I expand the "SideNavigationOnboarding" sidebar
#    When I navigate view by clicking on "onboardingBng"
    When I navigate view by clicking on "OnboardingBNG"
    Then "OnboardingBNG" page title should be "Onboarding - BNG"
    Then I click on "onboardNewBNGPair" button
    When I click on "firstBNG" button
    Then I fill the required parameter for "maximum_length" of BNG name
    Then I click on "firstBNGAdd" button
    Then I validate the error message for "maximum_length_bng" test