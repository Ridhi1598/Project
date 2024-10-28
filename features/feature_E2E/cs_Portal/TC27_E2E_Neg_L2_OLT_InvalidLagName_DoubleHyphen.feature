Feature: Negative - Add LAG/TP - Double Hyphen
  This feature tests the negative scenario of adding OLT LAG/TP with double hyphen

  Scenario: Negative - Add OLT Topology - double hyphen lag name  : Success
    Given I set data values against testcase "58"
    Given I should land on CS Home page
    Given Landing Directly to the dashboard page
    And "Home" page title should be "Dashboard"
    And I expand the "L2Topology" sidebar
    And I navigate view by clicking on "OLT"
    Then "OLT" page title should be "L2 Topology - OLT"
    When I navigate view by clicking on "AddOLT"
    Then "AddOLT" page title should be "L2 Topology - OLT"
    When I enter the node Details and add "LagTestOLT"
    Then I verify that the node has been added
    And I add a new "LAG/TP" for the "LagTestOLT"
    And I verify the error message for double hyphen lag name