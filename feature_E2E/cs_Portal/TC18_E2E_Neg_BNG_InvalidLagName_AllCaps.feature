Feature: Negative - Add LAG/TP - All Caps Name
  This feature tests the negative scenario of adding LAG/TP with all caps name

  Scenario: Add BNG Topology : Success
    Given I set data values against testcase "49"
    Given I should land on CS Home page
    Given Landing Directly to the dashboard page
    And "Home" page title should be "Dashboard"
    And I expand the "L2Topology" sidebar
    And I navigate view by clicking on "SideNavigationBNG"
    And "BNG" page title should be "L2 Topology - BNG"
    And I navigate view by clicking on "AddBNGPair"
    And "BNG" page title should be "L2 Topology - BNG"
    When I enter the node Details and add "LagTestBNG"
    Then I verify that the node has been added
    And I add a new "LAG/TP" for the "LagTestBNG"
    And I verify the error message for allcaps lag name