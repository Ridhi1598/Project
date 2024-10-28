import os
import sys
import yaml
from envyaml import EnvYAML



class ReadYMLFile:
    def read_configuration_file(self, filepath=None):
        rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + '/OR/'+sys.argv[1]+"/"
        try:
            if filepath is not None:
                rootPath += filepath
                with open(rootPath) as file:
                    return yaml.load(file, Loader=yaml.FullLoader)
            else:
                return "File path is not provided"
        except:
            print("Unexpected error:", sys.exc_info()[0], 'File/Data is invalid')
            raise


    def yaml_read(self, filepath=None):
        rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + f'/resources/payload/{sys.argv[1]}/v1_service/'
        try:
            if filepath is not None:
                rootPath += filepath
                with open(rootPath) as file:
                    return yaml.load(file, Loader=yaml.FullLoader)
            else:
                return "File path is not provided"
        except:
            print("Unexpected error:", sys.exc_info()[0], 'File/Data is invalid')
            raise


    def getElementValue(self, data, property, propElement=None):
        dataType = type(data)
        if dataType is dict:
            return data.get(property)
        elif dataType is list:
            for item in data:
                value = self.getElementValue(item, property)
                if propElement == value:
                    return item
        else:
            return data

    def readEnvVar(self):
        rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        envDict = EnvYAML('{}/resources/config/secrets/env.yaml'.format(rootPath))
        return envDict
