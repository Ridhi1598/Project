@bngDecommission @rmq @dev
Feature: Verify the OLT devices are Decommissioned
  This features to validate the OLT Decommission is completed

   Scenario: TC18: Onboard BNG - Create BNG Config - Dry Run - Download Config
    Then I unzip onboarding-bng-config.zip folder and move in Framework directory and Delete the actual downloaded zip folder from download folders
