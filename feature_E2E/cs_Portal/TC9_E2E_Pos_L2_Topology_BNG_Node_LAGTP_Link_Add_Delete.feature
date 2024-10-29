Feature: Add and Delete Topology - BNG1, BNG2, Lag1, Lag2, Link
  This feature tests the functionality of adding and deleting L2 topology elements

  Scenario: Add BNG Topology : Success
    Given I set data values against testcase "43"
    Given I should land on CS Home page
    And "Home" page title should be "Dashboard"
    And I expand the "L2Topology" sidebar
    And I navigate view by clicking on "SideNavigationBNG"
    And "BNG" page title should be "L2 Topology - BNG"
    And I navigate view by clicking on "AddBNGPair"
    And "BNG" page title should be "L2 Topology - BNG"
    When I enter the node Details and add "TestNodes"
    Then I verify that the node has been added
    And I add a new "LAG/TP" for the "TestNodes"
    And I click on "Next" button
    Then I add link between the 2 BNGs