import csv
import os
import sys
import codecs

class ReadCSVFile:
    def read_csv_file(self, filePath):
        listCSVData = []
        rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + '/resources/TestData/'
        try:
            if filePath is not None:
                rootPath += filePath
                with codecs.open(rootPath, "r", encoding='utf-8', errors='ignore') as csvFile:
                    csvReader = csv.DictReader(csvFile)
                    for row in csvReader:
                        listCSVData.append(row)
                    return listCSVData
            else:
                return "File path is not provided"
        except:
            print("Unexpected error:", sys.exc_info()[0], 'File/Data is invalid')
            raise