Feature: Display Live OLTs under given service type
  This feature tests flow from the CS portal to display live OLTs under given BNG group

  Scenario: Display live OLTs under BNG group : Success
    Given I set data values against testcase "2"
    And I should land on CS Home page
    And "Home" page title should be "Dashboard"
    And I navigate view by clicking on "ServiceFirstValue"
    And "Service Details" page title should be "Default"
    Then I search for "BG2" BNG Group ID and captured the total OLT count mapped to it
    When I navigate view by clicking on "SearchedBNGGroupId"
    And "OLT Mapped Details" page title should be "OLT Mapped To BG2"
    Then I verify the value of number of OLT mapped to BNG group Id