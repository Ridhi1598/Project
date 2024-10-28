from stcrestclient import stchttp


class STC:
    def create_session(self, server, port, userName, sessionName):
        """
        Creates a new session for a user
        :param server: localhost
        :param port: 8888
        :param userName: user name value
        :param sessionName:  session name
        :return: session id
        """
        global stc
        stc = stchttp.StcHttp(server=server, port=port)
        sessionId = stc.new_session(user_name=userName, session_name=sessionName, kill_existing=True)
        print("sessionId", sessionId)
        joinSessionId = stc.join_session(sessionId)
        print("joinSessionId", joinSessionId)

    def create_project(self, projectCommand, portCommand, chassis_ip, chassis_port):
        """
        Creates a new project and port handle using create command
        :param projectCommand: command to create project
        :param portCommand: command to create port handle
        :param chassis_ip: ip address of the chassis
        :param chassis_port: port to be used
        :return: values of newly created project and port handle
        """
        projectName = stc.create(projectCommand)
        print("project", projectName)

        portHandle = stc.create(portCommand, under=projectName)
        print("port_handle", portHandle)

        stc.config(portHandle, location="//{}/{}".format(chassis_ip, chassis_port))
        return projectName, portHandle

    def create_deviceList(self, deviceListCommand, projectName, portHandle, DeviceCount):
        """
        Creates emulateddevice list under the created project using port handle
        :param deviceListCommand: command to create device list
        :param projectName: project name under which list is to be created
        :param portHandle: port handle created under the project
        :param DeviceCount: number of devices to be created in the device list
        :return: device list
        """
        deviceList = stc.create(
            deviceListCommand, under=projectName, affiliatedPort=portHandle, DeviceCount=DeviceCount)
        print("deviceList", deviceList)
        return deviceList

    def create_deviceEthIIIf(self, EthIIIfCommand, deviceList):
        ethiiIf = stc.create(EthIIIfCommand, under=deviceList)
        print("EthIIIf", ethiiIf)
        return ethiiIf

    def create_deviceVlanIf(self, VlanIfCommand, deviceList, ethiiIf):
        vlanIF = stc.create(VlanIfCommand, under=deviceList, StackedOn=ethiiIf)
        print("vlanIF", vlanIF)
        return vlanIF

    def create_deviceIpv4If(self, Ipv4IfCommand, deviceList, vlanIF):
        ipv4If = stc.create(Ipv4IfCommand, under=deviceList, StackedOn=vlanIF)
        print("ipv4If", ipv4If)
        return ipv4If

    def configure_device(self, deviceList, ipv4If):
        stc.config(deviceList, PrimaryIf=ipv4If, ToplevelIf=ipv4If)


    def create_dhcp_block(self, dhcpCommand, deviceList, CircuitId, EnableCircuitId, EnableRelayAgent, UsesIf):
        dhcp_block = stc.create(
            dhcpCommand,
            under=deviceList,
            CircuitId=CircuitId,
            EnableCircuitId=EnableCircuitId,
            EnableRelayAgent=EnableRelayAgent,
            UsesIf=UsesIf,
        )
        print("dhcp_block", dhcp_block)

    def run_dhcp_results(self, dhcpResultCommand, projectName, portHandle, resultType, configType, ViewAttributeList, interval):
        dhcp_results = stc.perform(
            dhcpResultCommand,
            parent=projectName,
            resultParent=portHandle,
            resultType=resultType,
            configType=configType,
            ViewAttributeList=ViewAttributeList,
            interval=interval,
        )
        print("dhcp_results", dhcp_results)

    def create_sequencer(self, sequencerCommand, systemValue):
        sequencer = stc.create(sequencerCommand, under=systemValue)
        print("sequencer", sequencer)
        return sequencer

    def create_bind(self, bindCommand, bindWaitCommand, sequencer, dhcp_block, deviceList, waitTime):
        bind = stc.create(bindCommand, under=sequencer, BlockList=dhcp_block)
        print("bind", bind)
        bind_wait = stc.create(
            bindWaitCommand,
            under=sequencer,
            ObjectList=deviceList,
            WaitTime=waitTime,
        )
        print("bind_wait", bind_wait)
        return bind, bind_wait

    def create_release(self, releaseCommand, releaseWaitCommand, sequencer, dhcp_block, deviceList, waitTime):
        release = stc.create(releaseCommand, under=sequencer, blockList=dhcp_block)
        print("release", release)

        release_wait = stc.create(
            releaseWaitCommand,
            under=sequencer,
            ObjectList=deviceList,
            WaitTime=waitTime,
        )
        print("release_wait", release_wait)
        return release, release_wait

    def configure_sequencer(self, sequencerInsertCommand, bind, bind_wait, release, release_wait):
        output = stc.perform(
            sequencerInsertCommand, commandList=[bind, bind_wait, release, release_wait]
        )
        print("output", output)

    def apply_configs(self, chassis_ip, chassis_port, reservePortCommand, portMappingsCommand, attachPortsCommand, portHandle, autoConnectValue, sequencer):
        stc.connect(chassis_ip)
        stc.perform(reservePortCommand, location="//{}/{}".format(chassis_ip, chassis_port))
        stc.perform(portMappingsCommand)

        print("------Attaching ports")
        stc.perform(attachPortsCommand, portList=[portHandle], autoConnect=autoConnectValue)
        stc.apply()
        print(stc.get(sequencer))

    def start_sequencer(self, sequencerStartCommand, dhcp_results, resultHandle, resultHandleArgs, bindRateHandleArgs, sequencer):
        for i in range(3):
            print("----------------\n", stc.get(sequencer))
            print("waiting for bind")
            a = stc.perform(sequencerStartCommand)
            print(a)
            print("starting release")
            stc.wait_until_complete()
            results = stc.get(dhcp_results[resultHandle], resultHandleArgs)
            bindRate = stc.get(results, bindRateHandleArgs)
            print("Bind rate: {}".format(bindRate))

    def close_session(self, chassis_ip, deviceList, port_handle, project):
        stc.disconnect(chassis_ip)
        stc.delete(deviceList)
        stc.delete(port_handle)
        stc.delete(project)
        stc.end_session()

