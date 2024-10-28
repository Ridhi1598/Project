@tc_91
Feature: Negative - OLT add link no value
   This feature tests the negative scenario of adding olt add link with no value

  Scenario: Negative - OLT add link no value
    Given I set data values against testcase "91"
#
#    When I should land on CS Home page
#    Then "Home" page title should be "Dashboard"
#    When I expand the "L2Topology" sidebar
#
    Then I navigate view by clicking on "OLT"
    When "OLT" page title should be "L2 Topology - OLT"
    Then I click on "addOLT" button
    When "AddOLT" page title should be "L2 Topology - OLT"
    Then I click on "AddNewNode" button
    When I fill the required details to add a "first" new node
    Then I click on "addNode" button
    Then I validate that the created node should exist in the nodes table at "first" place
    When I click on "AddNewLag" button
    Then I fill the required details to add a "first" lag
    When I click on "addLag" button
    Then I click on "AddNewNode" button
    When I fill the required details to add a "second" new node
    Then I click on "addNode" button
    Then I validate that the created node should exist in the nodes table at "second" place
    When I click on "AddNewLag" button
    Then I fill the required details to add a "second" lag
    When I click on "addLag" button
    Then I click on "next" button
    Then I validate that none of the dropdowns should have any values selected