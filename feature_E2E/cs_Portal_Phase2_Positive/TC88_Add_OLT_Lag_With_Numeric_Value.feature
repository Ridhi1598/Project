@tc_88
Feature: Negative - Add OLT Lag with numeric value
   This feature tests the negative scenario of adding the new OLT Lag with numeric value

  Scenario: Negative - Add OLT Lag with numeric value
    Given I set data values against testcase "88"
#    When I should land on CS Home page
#    Then "Home" page title should be "Dashboard"
#    When I expand the "L2Topology" sidebar
    Then I navigate view by clicking on "OLT"
    When "OLT" page title should be "L2 Topology - OLT"
    Then I fetch the first OLT info from the table and select it
    Then Wait for the loader to disappear
    When I click on "firstAddedNewNode" button
    Then I click on "addNewLag" button
    Then I enter a "numeric" value for adding the new OLT lag
    When I click on "newLagAdd" button
    Then I validate the error message for "lagLowerCase" test