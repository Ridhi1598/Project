@tc2 @cs-polling-engine
Feature:Validate BNG birth certificate 
  This feature validates the BNG birth certificate

   Scenario Outline: tc_2: This scenario validates the BNG birth certificate
   Given I read test data for BNG controller testcases
   When "Publish" "<tc_num><published>" request message to "RMQ" "polling_engine" queue for polling engine
   Then Get and verify the "created" request record by "id" from table "polling_engine_bng_birth_certificate" with "failed" state
   Then Get and verify the "created" request record by "parent_request_tracker_id" from table "polling_engine_external_request_tracker" with "completed" state
   And Get and verify the "created" request record by "bng_group_id" from table "polling_engine_bng_birth_certificate" with "completed" state
   And Verify the "odd_bng_validation_response" value from "polling_engine_bng_birth_certificate"

    Examples:
     |tc_num | published                       |                                                                
     |tc_2  | _Validate_BNG_birth_certificate_failed |