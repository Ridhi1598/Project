Feature: Negative - Add LAG/TP - Check lag name character limit for OLT
  This feature tests the lag name character limit for OLT

  Scenario: Add OLT Topology : Success
    Given I set data values against testcase "60"
    Given I should land on CS Home page
    Given Landing Directly to the dashboard page
    And "Home" page title should be "Dashboard"
    And I expand the "L2Topology" sidebar
    And I navigate view by clicking on "OLT"
    Then "OLT" page title should be "L2 Topology - OLT"
    When I navigate view by clicking on "AddOLT"
    Then "AddOLT" page title should be "L2 Topology - OLT"
    When I enter the node Details and add "OLT7PlusLag"
    Then I verify that the node has been added
    And I add a new "LAG/TP" for the "OLT7PlusLag"