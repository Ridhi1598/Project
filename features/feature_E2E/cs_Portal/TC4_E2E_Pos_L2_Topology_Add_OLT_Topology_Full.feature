@OLTTopoCreate @cse2e
Feature: Add OLT Topology - OLT, SE-X-1, SE-X-2
  This feature tests the functionality of adding OLT Topology


  Scenario: Add OLT Topology : Success
    Given I set data values against testcase "41"
    Given I should land on CS Home page
    And "Home" page title should be "Dashboard"
    When I expand the "L2Topology" sidebar
    And I navigate view by clicking on "OLT"
    Then "OLT" page title should be "L2 Topology - OLT"
    When I navigate view by clicking on "AddOLT"
    Then "AddOLT" page title should be "L2 Topology - OLT"
    When I enter the node details and add "OLTNode"
    Then I verify that the node has been added
    And I add a new "LAG/TP" for the "OLTNode"
    And I click on "Next" button
    Then I add link OLT to the both SE-X-1 and SE-X-2
#    And I click on "Next" button
