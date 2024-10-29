@cse2e
Feature: To add the L2 Topology - OLT
  This feature is to add the Nodes

  Scenario Outline: TC1: L2 Topology - OLT - Add a node, Lag and remove Lag and Node
    Then I navigate to consumer Home page
    When "Home" page title should be "Dashboard"
    When I expand the "L2Topology" sidebar
    And I navigate view by clicking on "OLT" for CS
    Then "OLT" page title should be "L2 Topology - OLT"
    When I navigate view by clicking on "AddOLT" for CS
    Then "AddOLT" page title should be "L2 Topology - OLT"
    When I enter "<OLTName>" and add a OLT node
    When I enter "<SE-X-1>" and add a OLT node
    When I enter "<SE-X-2>" and add a OLT node
    Then I validate "<OLTName>" node is added successfully
    Then I validate "<SE-X-1>" node is added successfully
    Then I validate "<SE-X-2>" node is added successfully
    When I add "<Lag1>" Lag for "<OLTName>" Node
    When I add "<Lag2>" Lag for "<SE-X-1>" Node
    When I add "<Lag2>" Lag for "<SE-X-2>" Node
    Then I validate "<Lag1>" lag is added for "<OLTName>" Node
    Then I validate "<Lag2>" lag is added for "<SE-X-1>" Node
    Then I validate "<Lag2>" lag is added for "<SE-X-2>" Node
    Then I click on Next CTA
    Then I click on Node1 dropdown and select <SE-X-1>
    Then I click on Lag1 dropdown and select <Lag2>
    Then I click on Node2 dropdown and select <OLTName>
    Then I click on Lag2 dropdown and select <Lag1>
    Then I click on Add Link CTA
    Then I click on Node1 dropdown and select <SE-X-2>
    Then I click on Lag1 dropdown and select <Lag2>
    Then I click on Node2 dropdown and select <OLTName>
    Then I click on Lag2 dropdown and select <Lag1>
    Then I click on Add Link CTA
    Then I validate the link is added for <SE-X-1>, <Lag2>, <OLTName>, <Lag1>
    Then I validate the link is added for <SE-X-2>, <Lag2>, <OLTName>, <Lag1>
    When I delete the link for <SE-X-1> Node1
    Then I validate <SE-X-1> link is deleted
    Then I click on Node1 dropdown and select <SE-X-1>
    Then I click on Lag1 dropdown and select <Lag2>
    Then I click on Node2 dropdown and select <OLTName>
    Then I click on Lag2 dropdown and select <Lag1>
    Then I click on Add Link CTA

    Examples:
      | OLTName      | Lag1   | Lag2    | SE-X-1       | SE-X-2       |
      | EDTNABTFOT39 | lag-55 | lag-109 | EDTNABTFSE51 | EDTNABTFSE52 |