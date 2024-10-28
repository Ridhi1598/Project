Feature: Negative - Add empty name OLT
  This feature tests the negative scenario of adding empty name OLT node

  Scenario: Negative - Add OLT Topology Blank Name  : Success
    Given I set data values against testcase "52"
    Given I should land on CS Home page
    Given Landing Directly to the dashboard page
    And "Home" page title should be "Dashboard"
    And I expand the "L2Topology" sidebar
    And I navigate view by clicking on "OLT"
    Then "OLT" page title should be "L2 Topology - OLT"
    When I navigate view by clicking on "AddOLT"
    Then "AddOLT" page title should be "L2 Topology - OLT"
    When I enter the node Details and add "EmptyOLTNode"
    And I verify the error message for empty OLT node name