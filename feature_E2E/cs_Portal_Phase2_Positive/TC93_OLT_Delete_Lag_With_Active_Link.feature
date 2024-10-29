@tc_93
Feature: Negative - Delete lag with active link
   This feature tests the negative scenario of deleting the lag with active link

  Scenario: Negative - Delete lag with active link
    Given I set data values against testcase "93"
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
#    Then I click on "backOltArrow" button
    Then I click on "deleteLagIcon" button
    Then I validate the error message for deleting the Lag with active Link
