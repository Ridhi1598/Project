Feature: Display Live BNGs under given service type
  This feature tests flow from the CS portal to display live BNGs under given service type

  Scenario: Display live BNGs under given service : Success
    Given I set data values against testcase "1"
    Given I should land on CS Home page
    And "Home" page title should be "Dashboard"
    Then I count the number of BNG against Default Service Name
    When I navigate view by clicking on "ServiceFirstValue"
    And "Service Details" page title should be "Default"
    Then I verify the value of number of BNG services
