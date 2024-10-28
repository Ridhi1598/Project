@tc1 @cs-polling-engine
Feature:Validate BNG birth certificate 
  This feature validates the BNG birth certificate

   Scenario Outline: tc_1: This scenario validates the BNG birth certificate
   Given I read test data for BNG controller testcases
   When "Publish" "<tc_num><published>" request message to "RMQ" "polling_engine" queue for polling engine

    #Then Get and verify the "created" request record by "id" from table "polling_engine_bng_birth_certificate" with "completed" state.

    Examples:
     |tc_num | published                       |                                                                
     |tc_1   | _Validate_BNG_birth_certificate_success |

     
   