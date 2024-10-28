from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.util.ymlReader import ReadYMLFile
from features.steps.globalVar import GlobalVar

elementsByPageName = {}

class BaseReader:
    def __init__(self, fileName):
        fileData = ReadYMLFile().read_configuration_file(fileName)
        self.distByPageName(fileData)

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

    def getElementByPropertyName(self, context, pageName, elementName, pageChild = "elements", propertyName = "elementName"):
        global elementsByPageName
        if pageName is not None:
            GlobalVar.currentPage = pageName
        for pageKey in elementsByPageName:
              if(pageKey == pageName):
                    pageElements = self.getElementValue(elementsByPageName[pageKey], pageChild)
                    if pageElements is not None:
                        elementObj = self.getElementValue(pageElements, propertyName, elementName)
                        if elementObj is not None:
                            return self.get_element_by_selector(context, elementObj.get("locatorProperty"), elementObj.get("value"))
        return None

    def getElementLocatorValue(self, context, pageName, elementName, pageChild = "elements", propertyName = "elementName"):
        global elementsByPageName
        for pageKey in elementsByPageName:
            if (pageKey == pageName):
                pageElements = self.getElementValue(elementsByPageName[pageKey], pageChild)
                if pageElements is not None:
                    elementObj = self.getElementValue(pageElements, propertyName, elementName)
                    if elementObj is not None:
                        return elementObj['value']
        return None

    def readElementByPropertyName(self, pageName, elementName, pageChild = "elements", propertyName = "elementName"):
        global elementsByPageName
        for pageKey in elementsByPageName:
              if(pageKey == pageName):
                    pageElements = self.getElementValue(elementsByPageName[pageKey], pageChild)
                    if pageElements is not None:
                        elementObj = self.getElementValue(pageElements, propertyName, elementName)
                        if elementObj is not None:
                            return elementObj
        return None

    def distByPageName(self, pages):
        global elementsByPageName
        for key, value in pages.items():
            elementsByPageName[key] = value
        #print(elementsByPageName)


    def get_element_by_selector(self, context, selectorType, value):
        if selectorType == 'xpath':
            if WebDriverWait(context.driver, 40).until(EC.presence_of_element_located((By.XPATH, value))):
                return context.driver.find_element(By.XPATH, value)
        elif selectorType == 'id':
            if WebDriverWait(context.driver, 40).until(EC.presence_of_element_located((By.ID, value))):
                return context.driver.find_element(By.ID, value)
        elif selectorType == 'css':
            if WebDriverWait(context.driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, value))):
                return context.driver.find_element(By.CSS_SELECTOR, value)
        elif selectorType == 'linktext':
            if WebDriverWait(context.driver, 40).until(EC.presence_of_element_located((By.LINK_TEXT, value))):
                return context.driver.find_element(By.LINK_TEXT, value)
        elif selectorType == 'class':
            if WebDriverWait(context.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, value))):
                return context.driver.find_element(By.CLASS_NAME, value)

    def fill_field(self, field, value):
        return field, value
