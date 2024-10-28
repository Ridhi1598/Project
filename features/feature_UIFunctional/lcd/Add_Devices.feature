Feature: Devices Management
  This feature tests the functionality related to adding a device

Background:
    Given I should land on Home page

  @addDevicesFail
  Scenario: Add device Failed
    When Validate the Add Device Homepage Title
    Then I navigate view by clicking on "GeneralOperations"
    Then I navigate view by clicking on "AddNewDevices"
    Then "AddDevices" page title should be "Add Devices"
    When Click on Add Device Button and fill device details for "Failure" scenario
    Then Add tag for a device
    Then I click on "SubmitButton" button
    Then Click on "OKButton" button and wait till device is added
    Then Validate that device status is not connected


  @addDevicesSuccess @demo
  Scenario: Add devices Successfully
    When Validate the Add Device Homepage Title
    When I navigate view by clicking on "GeneralOperations"
    When I navigate view by clicking on "AddNewDevices"
    When "AddDevices" page title should be "Add Devices"
    When Click on Add Device Button and fill device details for "Success" scenario
    When Add tag for a device
    When I click on "SubmitButton" button
    When Click on "OKButton" button and wait till device is added
    Then Validate the status of device for success
    Then I navigate view by clicking on "navigateToDevices"
    Then "NavigateDevices" page title should be "NAVIGATE DEVICES"
    Then Device should be connected and displayed in the list of devices
    Then I perform Commit action