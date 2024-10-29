Feature: TC_1 : Create Session

  Scenario: Create dhcp user
    Given I set data values against testcase "1"
    And I send request to create new session
    And I send request to create "project" and "port"
    And I send request to create device list under created project using "emulateddevice" command
    And I send request to create "EthIIIf", "VlanIf" and "Ipv4If" under created device list
    And I send request to configure the created device list
    And I create dhcp block using "dhcpv4blockconfig" command
    And I run dhcp results using "ResultsSubscribeCommand" command
    Then I create sequencer using "sequencer" command
    And I create bind using "Dhcpv4BindCommand" and "Dhcpv4BindWaitCommand" commands
    And I create release using "Dhcpv4ReleaseCommand" and "Dhcpv4ReleaseWaitCommand" commands
    And I configure sequencer using "SequencerInsertCommand" command
    And I apply configs using "reservePort", "setupPortMappings" and "AttachPorts" commands
    When I start sequencer using "SequencerStartCommand" command
    And I close and disconnect session

