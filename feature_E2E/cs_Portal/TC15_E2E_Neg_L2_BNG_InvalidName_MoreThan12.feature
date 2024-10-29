Feature: Negative - Add BNG node - > 12 Chars
  This feature tests the negative scenario of adding BNG node name > 12 chars

  Scenario: Negative - Add BNG Topology More than 12 Chars Node Name  : Success
    Given I set data values against testcase "46"
    Given I should land on CS Home page
#    Given Landing Directly to the dashboard page
    And "Home" page title should be "Dashboard"
    And I expand the "L2Topology" sidebar
    And I navigate view by clicking on "SideNavigationBNG"
    And "BNG" page title should be "L2 Topology - BNG"
    And I navigate view by clicking on "AddBNGPair"
    And "BNG" page title should be "L2 Topology - BNG"
    When I enter the node Details and add "More12BNGNode"
    Then I verify what node has been added

