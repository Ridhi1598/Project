Feature: Work-order id column is added on Work Orders page

  Scenario: This scenario test the presence of Work-Order ID and absence of Request ID
    Given I read test data for testcase
    When I should land on "Home" page
    Then "Home" page title should be "Services"
    When I click on "WorkOrders" button
    Then I go to "WorkOrders" page
    When I find the "presence" of "WorkOrderID" column
    Then I find the "absence" of "RequestID" column
