#noinspection CucumberUndefinedStep
@APIDemo
Feature: Customers
  This feature tests the APIs related to customer management

  Background:
    Given I set LCD "REST" url

  @getSystemSettings
  Scenario: Get System Settings
    Given I Set POST posts api endpoint for "get_system_setting"
    When I Set HEADER param request "Content-Type" as "application/json"
    And I Set HEADER param request "Cookie" as "tinaa-cookie"
    And Set request Body for "get_system_setting"
    And Send POST HTTP request
    Then I receive valid HTTP response code 200 for "POST"
    And I validate the response schema with "getSystemSetting.json"

  @getTransaction
  Scenario: Get transaction
    Given I Set POST posts api endpoint for "get_trans"
    When I Set HEADER param request "Content-Type" as "application/json"
    And I Set HEADER param request "Cookie" as "tinaa-cookie"
    And Set request Body for "get_trans"
    And Send POST HTTP request
    Then I receive valid HTTP response code 200 for "POST"
    And I validate the response schema with "getTransaction.json"

  @readNewTransaction
  Scenario: Read new transaction
    Given I Set POST posts api endpoint for "new_trans"
    When I Set HEADER param request "Content-Type" as "application/json"
    And I Set HEADER param request "Cookie" as "tinaa-cookie"
    And Set request Body for "new_trans"
    And Send POST HTTP request
    Then I receive valid HTTP response code 200 for "POST"
    And I validate the response schema with "readNewTransaction.json"
    And I extract response value of "th"

  @getDeviceRegex
  Scenario: Get value of device regex
    And I Set POST posts api endpoint for "get_value"
    When I Set HEADER param request "Content-Type" as "application/json"
    And I Set HEADER param request "Cookie" as "tinaa-cookie"
    And Set request Body for "get_value"
    And Send POST HTTP request
    Then I receive valid HTTP response code 200 for "POST"
    And I validate the response schema with "getValue.json"

  @instantiateQuery
  Scenario: Instantiate query for getting list of customers
    Given I Set POST posts api endpoint for "start_query"
    When I Set HEADER param request "Content-Type" as "application/json"
    And I Set HEADER param request "Cookie" as "tinaa-cookie"
    And Set request Body for "start_query"
    And Send POST HTTP request
    Then I receive valid HTTP response code 200 for "POST"
    And I validate the response schema with "startQuery.json"
    And I extract response value of "qh"

  @runQuery
  Scenario: Run query
    And I Set POST posts api endpoint for "run_query"
    When I Set HEADER param request "Content-Type" as "application/json"
    And I Set HEADER param request "Cookie" as "tinaa-cookie"
    And Set request Body for "run_query"
    And Send POST HTTP request
    Then I receive valid HTTP response code 200 for "POST"
    And I validate the response schema with "runQuery.json"

  @stopQuery
  Scenario: Stop query
    And I Set POST posts api endpoint for "stop_query"
    When I Set HEADER param request "Content-Type" as "application/json"
    And I Set HEADER param request "Cookie" as "tinaa-cookie"
    And Set request Body for "stop_query"
    And Send POST HTTP request
    Then I receive valid HTTP response code 200 for "POST"
    And I validate the response schema with "stopQuery.json"
