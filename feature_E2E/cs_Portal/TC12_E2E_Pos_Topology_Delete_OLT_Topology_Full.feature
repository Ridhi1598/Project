Feature: Add and Delete OLT Topology - OLT, SE-Y-1, SE-Y-2
  This feature tests the functionality of adding and deleting OLT Topology

  Scenario: Add and delete OLT Topology : Success
    Given I set data values against testcase "39"
    Given I should land on CS Home page
    And "Home" page title should be "Dashboard"
    And I expand the "L2Topology" sidebar
    And I navigate view by clicking on "SideNavigationOLT"
    Then "OLT" page title should be "L2 Topology - OLT"
    And I search for added topology and click on "OLT" name
    And I select the "OLT" node
    And I click on "Next" button
    And I delete the added link Between "OLT" and SE
    Then I click on Node and delete corresponding lag
    And I delete added node and SE
    Then I verify that the "OLT topology" has been deleted


