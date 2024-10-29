Feature: Negative - Add LAG/TP - Check lag name character limit for BNG
  This feature tests the lag name character limit for BNG

  Scenario: Add BNG Topology : Success
    Given I set data values against testcase "59"
    Given I should land on CS Home page
    Given Landing Directly to the dashboard page
    And "Home" page title should be "Dashboard"
    And I expand the "L2Topology" sidebar
    And I navigate view by clicking on "SideNavigationBNG"
    And "BNG" page title should be "L2 Topology - BNG"
    And I navigate view by clicking on "AddBNGPair"
    And "BNG" page title should be "L2 Topology - BNG"
    When I enter the node Details and add "BNG7PlusLag"
    Then I verify that the node has been added
    And I add a new "LAG/TP" for the "BNG7PlusLag"
