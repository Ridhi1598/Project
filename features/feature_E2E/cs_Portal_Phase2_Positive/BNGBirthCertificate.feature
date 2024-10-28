@cse2e
Feature: Validate the BNG Certificate functionality
  This feature is to add the Nodes

  Scenario: DashBoard - Default -Validate user able to click on Birth certificate Icon and navigate to BNG birth certificate generation page
    Then I navigate to consumer Home page
    Then "Home" page title should be "Dashboard"
    When I navigate view by clicking on "ServiceFirstValue"
    And "Service Details" page title should be "Default"
    Then I Search EDTNABTFNG03-EDTNABTFNG04 BNG on dashboard default listing and verify the count of OLT is 1
    Then I click on Birth Certificate Action Icon
    And "BNG birth certificate" page title should be "EDTNABTFNG03-EDTNABTFNG04"
   # Then I Search EDTNABTFNG03-EDTNABTFNG04 BNG on birth certificate page and validate BNG is displayed

    When I select AAA Radius validation
    Then I validate EDTNABTFNG03, EDTNABTFNG04, Errors tabs is displayed
    Then I select EDTNABTFNG03 tab and validate the content is available
    Then I select EDTNABTFNG04 tab and validate the content is available
    Then I select Errors tab and validate the content is available

    When I select Lag Validation
    Then I validate EDTNABTFNG03, EDTNABTFNG04, Errors tabs is displayed
    Then I select EDTNABTFNG03 tab and validate the content is available
    Then I select EDTNABTFNG04 tab and validate the content is available
    Then I select Errors tab and validate the content is available


    When I select NPC and MZ diameter nodes validation
    Then I validate EDTNABTFNG03, EDTNABTFNG04, Errors tabs is displayed
    Then I select EDTNABTFNG03 tab and validate the content is available
    Then I select EDTNABTFNG04 tab and validate the content is available
    Then I select Errors tab and validate the content is available

    When I select Redundancy Multi-Chassis validation
    Then I validate EDTNABTFNG03, EDTNABTFNG04, Errors tabs is displayed
    Then I select EDTNABTFNG03 tab and validate the content is available
    Then I select EDTNABTFNG04 tab and validate the content is available
    Then I select Errors tab and validate the content is available

   Scenario: DashBoard - Default -Validate user able to click on Birth certificate Icon and navigate to BNG birth certificate generation page
    Then I click on BNG regenerate birth certificate icon and validate regenrate birth certificate message is display
    Then I verify the Page URL contains dashboard/dashboard-list-bng-groups


