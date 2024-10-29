@cse2e
Feature: To verify the BNG devices are onboarded
  This feature is to add the Nodes

  Scenario: TC21 and TC22 : verify the BNG devices are onboarded and count of the BNG services
    Then I navigate to consumer Home page
    Then "Home" page title should be "Dashboard"
    Then I count the number of BNG against Default Service Name
    When I navigate view by clicking on "ServiceFirstValue"
    And "Service Details" page title should be "Default"
    Then I Search EDTNABTFNG03-EDTNABTFNG04 BNG on dashboard default listing and verify the count of OLT is 0
    Then I verify the value of number of BNG services
