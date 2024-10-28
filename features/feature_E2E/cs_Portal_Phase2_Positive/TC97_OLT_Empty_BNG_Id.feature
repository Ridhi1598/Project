@tc_97
Feature: Negative - Olt empty BNG-ID
   This feature tests the negative scenario of Olt empty BNG-ID

  Scenario: tc_97: Negative - Olt empty BNG-ID
    Given I set data values against testcase "97"
#
#    When I should land on CS Home page
#    Then "Home" page title should be "Dashboard"
#
    When I expand the "L2Topology" sidebar
    Then I navigate view by clicking on "OLT"
#    Then Wait for the loader to disappear
    When "OLT" page title should be "L2 Topology - OLT"
    Then I click on "addOLT" button
    When "AddOLT" page title should be "L2 Topology - OLT"
    Then I click on "AddNewNode" button
    When I fill the required details to add a "first" new node
    Then I click on "addNode" button
    Then I validate that the created node should exist in the nodes table at "first" place
    When I click on "AddNewLag" button
    Then I fill the required details to add a "first" lag
    When I click on "addLag" button
    Then I click on "AddNewNode" button
    When I fill the required details to add a "second" new node
    Then I click on "addNode" button
    Then I validate that the created node should exist in the nodes table at "second" place
    When I click on "AddNewLag" button
    Then I fill the required details to add a "second" lag
    When I click on "addLag" button
    Then I click on "AddNewNode" button
    When I fill the required details to add a "third" new node
    Then I click on "addNode" button
    Then I validate that the created node should exist in the nodes table at "third" place
    When I click on "AddNewLag" button
    Then I fill the required details to add a "third" lag
    When I click on "addLag" button
    Then I click on "next" button
    Then I choose the dropdown options to add a duplicate node
    When I click on "add" button
    Then Wait for the loader to disappear
    Then I fill the required information from the dropdown to add "EDTNABTFOT39" & "EDTNABTFOT52" node
    When I click on "add" button
    Then Wait for the loader to disappear
    Then I go to "Home"
    When I expand the "Onboarding" sidebar
    Then I navigate view by clicking on "OnboardingOLT"
    Then "OnboardingOLT" page title should be "Onboarding - OLT"
    When I search for available "OLT" to "Onboarding"
    Then I click on "Onboard" button
#    When I click on "Next" button
#    Then I validate the error message while onboarding the OLT without selecting a value from the dropdown
