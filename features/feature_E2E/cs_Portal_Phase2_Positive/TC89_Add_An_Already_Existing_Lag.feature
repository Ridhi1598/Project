@tc_89
Feature: Negative - AAdd an already existing lag
   This feature tests the negative scenario of adding an already existing lag

  Scenario: Negative - Add an already existing lag
    Given I set data values against testcase "89"
#
#    When I should land on CS Home page
#    Then "Home" page title should be "Dashboard"
#    When I expand the "L2Topology" sidebar
#
    Then I navigate view by clicking on "OLT"
    When "OLT" page title should be "L2 Topology - OLT"
    Then I fetch the first OLT info from the table and select it
    Then Wait for the loader to disappear
    When I click on "firstAddedNewNode" button
    Then I click on "addNewLag" button
    Then I enter a "numeric" value for adding the new OLT lag
    When I click on "newLagAdd" button
    Then I validate the error message for "duplicateLag" test