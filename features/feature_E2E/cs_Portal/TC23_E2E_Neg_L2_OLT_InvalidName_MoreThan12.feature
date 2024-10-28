Feature: Negative - Add OLT node - > 12 Chars
  This feature tests the negative scenario of adding OLT node name > 12 chars

  Scenario: Negative - Add OLT Topology More than 12 Chars Node Name  : Success
    Given I set data values against testcase "54"
    Given I should land on CS Home page
    Given Landing Directly to the dashboard page
    And "Home" page title should be "Dashboard"
    And I expand the "L2Topology" sidebar
    And I navigate view by clicking on "OLT"
    Then "OLT" page title should be "L2 Topology - OLT"
    When I navigate view by clicking on "AddOLT"
    Then "AddOLT" page title should be "L2 Topology - OLT"
    When I enter the node Details and add "More12OLTNode"
    Then I verify what node has been added