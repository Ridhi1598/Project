Feature: Bulk provisioning of SDWAN service

@bulkAddDevices
    Scenario: Add devices in bulk
      Given I should land on Home page
      When "Home" page title should be ""
      When I filter and select a customer ""
      When I navigate view by clicking on "Configure"
      When "Configure" page title should be ""
      When Navigate to "DevicesPage"
      When I click on  "BulkAddDevice" button
