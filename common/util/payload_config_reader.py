from common.util.ymlReader import ReadYMLFile

valueByName = {}

class PayloadConfigReader:
    def __init__(self, fileName):
        fileData = ReadYMLFile().yaml_read(fileName)
        self.distByTestcaseName(fileData)

    def getValue(self, data, property, propElement=None):
        dataType = type(data)
        if dataType is dict:
            return data.get(property)
        elif dataType is list:
            for item in data:
                value = self.getValue(item, property)
                if propElement == value:
                    return item
        else:
            return data

    def getValueByName(self, pageName, elementName, pageChild = "elements", propertyName = "elementName"):
        global valueByName
        for pageKey in valueByName:
              if(pageKey == pageName):
                    pageElements = self.getValue(valueByName[pageKey], pageChild)
                    if pageElements is not None:
                        elementObj = self.getValue(pageElements, propertyName, elementName)
                        if elementObj is not None:
                            return elementObj
        return None

    def distByTestcaseName(self, pages):
        global valueByName
        for key, value in pages.items():
            valueByName[key] = value


