import json
import os
import sys


class ConfigReader:
    def configFileReader(self, fileName):
        rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + '/resources/config/'
        rootPath += fileName
        with open(rootPath) as config_file:
            data = json.load(config_file)
        return data
