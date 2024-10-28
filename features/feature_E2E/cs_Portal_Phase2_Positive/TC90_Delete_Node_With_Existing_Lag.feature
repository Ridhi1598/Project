
  @tc_90
Feature: Negative - Delete node with existing lag
   This feature tests the negative scenario of deleting the node with existing lag

  Scenario: Negative - Delete node with existing lag
    Given I set data values against testcase "90"
#
#    When I should land on CS Home page
#    Then "Home" page title should be "Dashboard"
#    When I expand the "L2Topology" sidebar
#
    Then I navigate view by clicking on "OLT"
    When "OLT" page title should be "L2 Topology - OLT"
    Then I fetch the first OLT info from the table and select it
    Then Wait for the loader to disappear
    When I click on "firstDeleteNode" button
    Then Validate the error message for deleting the node that has an existing lag in it
