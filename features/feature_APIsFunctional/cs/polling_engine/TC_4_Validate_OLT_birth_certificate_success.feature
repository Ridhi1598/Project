@tc4 @cs-polling-engine
Feature:Validate OLT birth certificate 
  This feature validates the OLT birth certificate

  #  Scenario: tc_4: Onboard bng_group_id in postgres db
  #   Given I read test data for BNG controller testcases
  #   When "Insert" "bng_group_id" value in postgres db


   Scenario Outline: tc_4: This scenario validates the BNG birth certificate
   Given I read test data for BNG controller testcases
   When "Publish" "<tc_num><published>" request message to "RMQ" "polling_engine" queue for polling engine
   Then Get and verify the "created" request record by "id" from table "polling_engine_bsaf_request_tracker" with "completed" state
   Then Get and verify the "created" request record by "parent_request_tracker_id" from table "polling_engine_external_request_tracker" with "completed" state
   And Verify the "odd_bng_validation_response" value from "polling_engine_olt_birth_certificate"
 

    Examples:
     |tc_num | published                       |                                                                
     |tc_4   | _Validate_OLT_birth_certificate_success |


    # Scenario: tc_4: Remove bng_group_id from postgres db
    # Given I read test data for BNG controller testcases
    #  When "Delete" "bng_group_id" value in postgres db