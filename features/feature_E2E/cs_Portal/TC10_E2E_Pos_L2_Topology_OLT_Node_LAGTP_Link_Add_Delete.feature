Feature: Add delete OLT Topology - OLT, SE-X-1, SE-X-2
  This feature tests the functionality of adding deleting OLT Topology


  Scenario: Add OLT Topology : Success
    Given I set data values against testcase "42"
    Given I should land on CS Home page
    Then "Home" page title should be "Dashboard"
    When I expand the "L2Topology" sidebar
    And I navigate view by clicking on "OLT"
    Then "OLT" page title should be "L2 Topology - OLT"
    When I navigate view by clicking on "AddOLT"
    Then "AddOLT" page title should be "L2 Topology - OLT"
    When I enter the node details and add "OLTRandomNode"
    Then I verify that the node has been added
    And I add a new "LAG/TP" for the "OLTNode"
    And I click on "Next" button
    Then I add link OLT to the both SE-X-1 and SE-X-2
    And  I delete the added link Between "OLT" and SE
    And I navigate view by clicking on "OLT"
    Then I search for added OLT and click on "OLT"
    Then I click on Node and delete corresponding lag
    And I delete added node and SE
    Then I verify that the node has been deleted

  