Feature: Display service history
  This feature tests the functionality related to displaying the current service history


  Scenario: Display current service history for service with previous versions
    Given I read test data for testcase
#    When I should land on "Home" page
    When I click on "servicesSidebar" button
    Then "Home" page title should be "Services"
    When I filter the "Services" by "CSID" and user "exist" in the results
    Then I click on "serviceHistory" icon
    And Wait for the "servicehistorypopup" popup to appear
    Then I click on "CloseServiceHistory" button
