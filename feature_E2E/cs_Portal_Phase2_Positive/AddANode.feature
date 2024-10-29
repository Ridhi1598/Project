@cse2e
Feature: To add the L2 Topology - OLT
  This feature is to add the Nodes

  Scenario Outline: TC1: L2 Topology - OLT - Add a node, Lag and remove Lag and Node
    Then I navigate to consumer Home page
    When "Home" page title should be "Dashboard"
    When I expand the "L2Topology" sidebar
    And I navigate view by clicking on "OLT" for CS
    Then "OLT" page title should be "L2 Topology - OLT"
    When I navigate view by clicking on "AddOLT" for CS
    Then "AddOLT" page title should be "L2 Topology - OLT"
    When I enter "<OLTName>" and add a OLT node
    Then I validate "<OLTName>" node is added successfully
    When I add "<Lag1>" Lag for "<OLTName>" Node
    Then I validate "<Lag1>" lag is added for "<OLTName>" Node
    Then I delete "<Lag1>" lag for "<OLTName>" Node
    Then I validate "<Lag1>" lag is deleted for "<OLTName>" Node
    When I delete "<OLTName>" node
    Then I validate "<OLTName>" node is deleted successfully
    Examples:
      | OLTName      | Lag1   |
      | EDTNABTFOT33 | lag-55 |