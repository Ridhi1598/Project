@tc3 @cs-polling-engine
Feature:Validate BNG birth certificate 
  This feature validates the BNG birth certificate

  Scenario: tc_3: Inject data in postgres db
      Given I read test data for BNG controller testcases
      When "Insert" "bng_group_id" value in postgres db
   
   Scenario Outline: tc_3: This scenario validates the BNG birth certificate
      Given I read test data for BNG controller testcases
      When "Publish" "<tc_num><published>" request message to "RMQ" "polling_engine" queue for polling engine
      Then Get and verify the "created" request record by "id" from table "polling_engine_bsaf_request_tracker" with "failed" state
      Then Get and verify the "created" request record by "parent_request_tracker_id" from table "polling_engine_external_request_tracker" with "completed" state
      And Get and verify the "created" request record by "bng_group_id" from table "polling_engine_bng_birth_certificate" with "failed" state
      And Verify the "odd_bng_validation_response" value from "polling_engine_bng_birth_certificate"
      And Verify the "even_bng_validation_response" value from "polling_engine_bng_birth_certificate"
      And Verify the "validation_result" value from "polling_engine_bng_birth_certificate"

    Examples:
     |tc_num | published                       |                                                                
     |tc_3  | _Validate_BNG_birth_certificate_failed_integration |

 Scenario: tc_3: Remove data from postgres db
      Given I read test data for BNG controller testcases
      When "Delete" "bng_group_id" value in postgres db