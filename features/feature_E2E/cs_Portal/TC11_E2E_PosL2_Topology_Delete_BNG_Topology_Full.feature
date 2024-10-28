Feature: Add and Delete OLT Topology - BNG1, BNG2, SE-Y-1, SE-Y-2
  This feature tests the functionality of adding and deleting BNG Topology

  Scenario: Delete Node, TP/LAG, Link : Success
    Given I set data values against testcase "39"
    Given I should land on CS Home page
    And "Home" page title should be "Dashboard"
    And I expand the "L2Topology" sidebar
    And I navigate view by clicking on "SideNavigationBNG"
    And "BNG" page title should be "L2 Topology - BNG"
    And I search for added topology and click on "BNG" name
    And I select the "BNG" node
    And I click on "Next" button
    And I delete the added link Between "BNGs" and SE
    Then I click on Node and delete corresponding lag
    And I delete added node and SE
    Then I verify that the "OLT topology" has been deleted