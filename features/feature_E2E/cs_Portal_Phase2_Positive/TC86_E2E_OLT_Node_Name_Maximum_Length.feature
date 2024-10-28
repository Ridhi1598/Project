Feature: Negative - OLT Node name minimum length
  This feature tests the negative scenario of OLT Node name maximum length

Scenario: Negative - OLT Node name minimum length
  Given I set data values against testcase "86"
#  When I should land on CS Home page
#  Then I go to "Home" page
#  When "Home" page title should be "Dashboard"
#  Then I expand the "L2Topology" sidebar
  When I navigate view by clicking on "OLT"
  Then "OLT" page title should be "L2 Topology - OLT"
  When I navigate view by clicking on "AddOLT"
  Then I click on "addNewNode" button
  When I fill the required parameter for "maximum_length" of OLT name
  And I validate that the olt name should contain only 12 characters

