# Created by Amer Hamza at 22-10-2021
Feature: Service Dashboard Results Per row validation
  This feature test the functionality of action history modal
  validate the row for every request id

  Scenario: Checking the functionality of Column field
    Given I should land on BI Home page
    Given "Home" page title should be "BI service dashboard"
    Then I navigate History Modal by clicking on "ActionButton"
    Then Validate "Request Id" are present in "History Modal"
    Then Validate "Operation Type" are present in "History Modal"
    Then Validate "Operation Result" are present in "History Modal"
    Then Validate "Operation Time" are present in "History Modal"
    Then Validate "Origin" are present in "History Modal"
    Then Validate "User ID" are present in "History Modal"
    Then Validate "Actions" are present in "History Modal"