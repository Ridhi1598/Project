Feature: Customer Groups
    This feature tests the functionality related to customer groups

    @customerGroups @RR
    Scenario: Customer Groups
      Given I should land on Home page
      When "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
      Then I navigate view by clicking on "ManageAuditConfigs"
      Then "ManageAuditConfigs" page title should be "MANAGE AUDIT CONFIGURATIONS"
      When I click on "CustomerGroupTab" tab
      When I click on "Add" button and add customer group
      When I perform Commit action
      When Validate that customer group is displayed in the list
      Then filter the Customer group by name and select first result
      Then validate the Logging Server and get the value
      Then I navigate view by clicking on "linkAuditRemediation"
      Then I navigate view by clicking on "linkManageAuditConfig"
      Then filter the Customer by name and select first result
      And I assign a customer group to the selected customer
      And I define "logging server" value under the selected customer
      Then I perform Commit action