import os
import filecmp
import sys


def delete_create_text_file(filetype, fileName, newfileData):
    myfile = fileName + ".txt"
    rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    print(rootPath)
    if os.path.isfile(myfile):
        os.remove(myfile)
        print("Old %s file Deleted successfully" % myfile)
    else:
        print("Error: %s file does not exist" % myfile)
    file = open(rootPath + '/resources/deviceConfigs/' + sys.argv[1] + '/' + filetype + '/' + fileName + '.txt', 'w')
    file.write(newfileData)
    print("New file created")


def compare_text_file(filetype, oldFile, newFile):
    cwd = os.getcwd()
    files = os.listdir(cwd)
    rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    file1 = rootPath + '/resources/deviceConfigs/' + sys.argv[1] + '/' + filetype + '/' + oldFile + ".txt"
    file2 = rootPath + '/resources/deviceConfigs/' + sys.argv[1] + '/' + filetype + '/' + newFile + ".txt"
    # Compare the os.stat() signature i.e the metadata of both files
    comp = filecmp.cmp(file1, file2)
    # Print the result of comparison
    print(comp)
    # Compare the contents of both files
    comp = filecmp.cmp(file1, file2, shallow=False)
    # Print the result of comparison
    print(comp)
    return comp
