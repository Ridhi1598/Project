Feature: Negative - Add empty name OLT
  This feature tests the negative scenario of adding empty name OLT node

  Scenario: Negative - Add OLT Topology Blank Name
    Given I set data values against testcase "52"
    When I should land on CS Home page
    Then I go to "Home" page
    Then "Home" page title should be "Dashboard"
    Then I expand the "L2Topology" sidebar
    When I navigate view by clicking on "OLT"
    Then "OLT" page title should be "L2 Topology - OLT"
    When I navigate view by clicking on "AddOLT"
    Then I click on "addNewNode" button
    When I click on "add" button
    Then I validate the error message for "emptyOLT" test
