import sys
import os

class envDataGenerator:
    def __init__(self):
        print("initialized")

    def listToStr(self, listName):
        failList = ''
        for index in range(0, len(listName)):
            failList += '    ->' + listName[index] + '\n'
        return failList

    def dictToStr(self, dictName, failTestList=''):
        count = 1
        for i in dictName.keys():
            failValueList = envDataGenerator.listToStr(self, dictName[i])
            failTestList += '    ' + str(count) + '. ' + str(i) + ' :\n' + failValueList + '\n'
            count += 1
        failTestList = 'Please find the list of failing test scenarios along with their feature: \n \n' + failTestList
        return failTestList


    def defineTestType(self, filePath):
        testType = None
        testComponent = None

        if './' in filePath:
            if 'E2E' in filePath:
                testType = 'E2E_Regression'
                testComponent = 'E2E'
            elif 'UI' in filePath:
                testType = 'UI_Functional'
                testComponent = 'UI'
            elif 'Int' in filePath:
                testType = 'Integration_Functional'
            elif 'API' in filePath:
                testComponent = filePath.split('/')[4]
                testType = testComponent.upper() + '_Functional'
            elif 'NED' in filePath:
                testType = 'NED_Upgrade_Functional'

        elif '@' in filePath:
            if "clm" not in filePath: testName = (filePath.split('/')[2]).split('_')
            else: testName = (filePath.split('/')[2]).split('_seq')
            test = (testName[0]).split(sys.argv[1])
            if 'E2E' in test:
                testType = 'E2E_Regression'
                testComponent = 'E2E'
            elif 'UI' in test:
                testType = 'UI_Functional'
                testComponent = test[1]
            elif 'Int' in test:
                testType = 'Integration_Functional'
            elif 'NED' in test:
                testType = 'NED_Upgrade_Functional'
            else:
                testComponent = test[1]
                testType = testComponent.upper() + '_Functional'

        # else:
        #     if 'sequence' in filePath:
        #         testName = (filePath.split('/')[2]).split('_')
        #         test = (testName[0]).split(sys.argv[1])
        #         if 'E2E' in test:
        #             testType = 'E2E_Regression'
        #         elif 'UI' in test:
        #             testType = 'UI_Functional'
        #             testComponent = test[1]
        #         elif 'Int' in test:
        #             testType = 'Integration_Functional'
        #         elif 'NED' in test:
        #             testType = 'NED_Upgrade_Functional'
        #         else:
        #             testComponent = test[1]
        #             testType = testComponent.upper() + '_Functional'
        #     else:
        #         if 'E2E' in filePath:
        #             testType = 'E2E_Regression'
        #         elif 'UI' in filePath:
        #             testType = 'UI_Functional'
        #             testComponent = 'UI'
        #         elif 'Int' in filePath:
        #             testType = 'Integration_Functional'
        #         elif 'API' in filePath:
        #             testComponent = filePath.split('/')[3]
        #             testType = testComponent.upper() + '_Functional'
        #         elif 'NED' in filePath:
        #             testType = 'NED_Upgrade_Functional'

        if testComponent is None:
            return testComponent, testType
        else:
            return testComponent.lower(), testType

    def features_counter(self, file):
        count = 0
        file = (os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + "/" + file.partition('@')[2]).strip()
        with open(file, "r") as testFile:
            data = testFile.readlines()
            for line in data:
                if "../../" in line:
                    count += 1
            return count
