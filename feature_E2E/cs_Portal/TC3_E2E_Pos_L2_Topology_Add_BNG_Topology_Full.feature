@BNGTopoCreate @cse2e
Feature: Add BNG Topology - BNG1, BNG2, SE-Y-1, SE-Y-2
  This feature tests the functionality of adding BNG Topology

  Scenario: Add BNG Topology : Success
    Given I set data values against testcase "40"
    Given I should land on CS Home page
    Given Landing Directly to the dashboard page
    #And "Home" page title should be "Dashboard"
    #And I expand the "L2Topology" sidebar
    #And I navigate view by clicking on "SideNavigationBNG"
    #And "BNG" page title should be "L2 Topology - BNG"
    #And I navigate view by clicking on "AddBNGPair"
    #And "BNG" page title should be "L2 Topology - BNG"
#    And I click "AddNewNode" button
    # Above step to be deleted later
#    And I enter the "nodeDetails" and add BNG1, BNG2, SE-Y-1, SE-Y-2
    # Above step to be deleted later
    #When I enter the node Details and add "BNGNode"
#    And I verify that BNG1, BNG2, SE-Y-1, SE-Y-2 have been added
    # Above step to be deleted later
   # Then I verify that the node has been added
   # And I add a new "LAG/TP" for the "BNGNode"
   # And I click on "Next" button
   # Then I add links between BNG1, BNG2, SE-Y-1 and SE-Y-2
