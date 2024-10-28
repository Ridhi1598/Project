#noinspection CucumberUndefinedStep
   Feature: Unauthorized access
     This feature tests the functionality related Unauthorised acess

     @unAuthorizedAccess
      Scenario: Validate the Unauthorised access and logout
       Given I should land on Home page for Unauthorized access
       When "UnAuthorizedAccess" page title should be "Unauthorized!"
       Then I navigate view by clicking on "logoutButton"
       Then wait till the Login page is loaded
