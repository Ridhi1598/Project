Feature: Input validations for update service
  This feature tests the input validations for

  Scenario Outline: Input validations for update service
    Given I set data values against testcase "87"
    Given I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then Filter and search the "serviceId" for update request
    And Open "Parameter Information" box by expanding the row
    When I clear "<fieldName>" field and click "Save" button
    Then Validate error message for "<fieldName>" field should be "<errorMessage>"

 Examples:
    |fieldName          |errorMessage                         |
    |IPV4ProviderPrefix0|IPV4 Provider Prefixes is required!  |
    |QOSIngress         |Please provide input value in number!|
    |QosEgress          |Please provide input value in number!|
    |port               |Port is required!                    |
    |IPV4CustomerPrefix0|IPV4 Customer Prefixes is required!  |