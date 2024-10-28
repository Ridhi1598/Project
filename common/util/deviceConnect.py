import os
import sys
import netmiko
import time
from netmiko import ConnectHandler, file_transfer
from common.util.config import ConfigReader
import pysftp


class DeviceConnect:
    def __int__(self):
        self.__int__()

    def connect(self, deviceConnectionInfo, device):
        try:
            ssh_connection = ConnectHandler(**deviceConnectionInfo)
            prompt = ssh_connection.find_prompt(delay_factor=30.0)

            print("SSH-Connection is successful. Prompt: {}".format(ssh_connection.find_prompt(delay_factor=10.0)))
            if device in str(prompt):
                print("SSH connection established with device IP {}".format(deviceConnectionInfo["ip"]))
                print("Connection Prompt: {}".format(prompt))
            else:
                print("Error establishing connection")
            return ssh_connection
        except Exception as e:
            raise Exception(e)

    def stop(self, connection, connType):
        if connType == "ssh":
            connection.disconnect()
        elif connType == "sftp":
            connection.close()

    def sftp(self, deviceInfo):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        try:
            return pysftp.Connection(host=deviceInfo["host"], username=deviceInfo["username"],
                                     password=deviceInfo["password"], cnopts=cnopts)
        except Exception as e:
            raise Exception(e)

    def fetch_config(self, connection, scenario, testCase, type, deviceName, action):
        remoteWorkingDirectory = "/cf3:/"
        source_file = "config.cfg"

        # create directory and mention path
        connection.cwd(remoteWorkingDirectory)
        dest_Folder = ''.join([os.getcwd(), f"/resources/deviceConfigs/{sys.argv[1]}/reConfigs/TC_{testCase}"])
        if not os.path.exists(dest_Folder):
            os.mkdir(dest_Folder)
        dest_file = ''.join([dest_Folder, f"/tc{testCase}_{type}_config_{scenario}_{action}_{sys.argv[2]}.txt".lower()])

        try:
            # download and return the config file
            connection.get(source_file, dest_file)
            if os.path.exists(dest_file):
                return dest_file
        except IOError as err:
            print(err)
