import os
import sys
import difflib
from chardet import detect
import json

from features.steps.globalVar import GlobalVar


class FileCompare:
    def __init__(self):
        print("initialized")

    def compare_config_files(self, oldFileName, newFileName, diffFileLocation, testcase, accesstype):
        filetosave = diffFileLocation + f'/config_Diff_{testcase}'
        if accesstype == 'MWR':
            filetosave = diffFileLocation + '/config_DiffBaseDevice_' + testcase
        with open(oldFileName, 'rb') as f:
            rawdata = f.read()
        encoding_type = detect(rawdata)['encoding']
        with open(oldFileName, 'r', encoding=encoding_type) as OldFile:
            with open(newFileName, 'r', encoding=encoding_type) as NewFile:
                diff = difflib.unified_diff(OldFile.readlines(), NewFile.readlines(),
                                            fromfile='hosts0', tofile='hosts1', n=0)
                with open(filetosave, 'w') as file_out:
                    for line in diff:
                        for prefix in ('---', '+++', '@@'):
                            if line.startswith(prefix): break
                        else:
                            file_out.write(line)
        return filetosave

    def compare_config_files_with_base(self, oldFileName, newFileName, diffFileLocation, testcase, accesstype,
                                       testScenario):
        filetosave = diffFileLocation + '/config_Diff_From_Base_' + testcase
        if accesstype == 'MWR' or 'mwr' in testScenario:
            filetosave = diffFileLocation + '/baseDevice_config_Diff_From_Base_' + testcase

        with open(oldFileName, 'r') as OldFile:
            with open(newFileName, 'r') as NewFile:
                diff = difflib.unified_diff(OldFile.readlines(), NewFile.readlines(),
                                            fromfile='hosts0', tofile='hosts1', n=0)
                with open(filetosave, 'w') as file_out:
                    for line in diff:
                        for prefix in ('---', '+++', '@@'):
                            if line.startswith(prefix):
                                break
                            elif 'Generated' in line or 'Finished' in line or '    }' in line \
                                    or 'authentication-key' in line or 'exit' in line or 'Last commit' in line \
                                    or 'Last changed' in line or 'disable' in line or 'community 670 members 852:670;' in line \
                                    or 'community 675 members 852:675;' in line:
                                break
                        else:
                            file_out.write(line)

        # Check for duplicates in the outFile
        file_size = os.path.getsize(filetosave)
        if file_size != 0:
            with open(filetosave, 'r') as RecheckFile:
                lines = RecheckFile.readlines()
                newLinesDict = {}
                for i in range(0, len(lines)):
                    newLine = lines[i][2:].strip("\n").lower()
                    if newLine in newLinesDict:
                        newLinesDict[newLine] += 1
                    else:
                        newLinesDict[newLine] = 1
                count = 0
                for line in newLinesDict:
                    if newLinesDict[line] % 2 != 0:
                        if "address ::ffff:c0a8:" in line or "address ::ffff:192.168." in line:
                            pass
                        else:
                            print(line, "\n")
                            count += 1
                assert count == 0
                print("Configs matched successfully for testcase {}".format(testcase))
        else:
            print("Configs matched successfully for testcase {}".format(testcase))

    def find_config_diff(self, beforeFile, afterFile, testcase, type, action):
        diffFile = ''.join([os.getcwd(),
                            f"/resources/deviceConfigs/{sys.argv[1]}/reConfigs/TC_{testcase}/tc{testcase}_diff_{type}_{action}_{sys.argv[2]}.txt"])

        with open(beforeFile, 'r') as OldFile:
            with open(afterFile, 'r') as NewFile:
                diff = difflib.unified_diff(OldFile.readlines(), NewFile.readlines(),
                                            fromfile='hosts0', tofile='hosts1', n=0)
                with open(diffFile, 'w') as file_out:
                    for line in diff:
                        for prefix in ('---', '+++', '@@'):
                            if line.startswith(prefix): break
                        else:
                            file_out.write(line)
        return diffFile

    def compare_config_diff(self, configDiff, testcase, type, action):
        validatedDiff = ''.join([os.getcwd(),
                                 f"/resources/deviceConfigs/{sys.argv[1]}/reBaseDiff/TC_{testcase}/tc{testcase}_{type}_validatedDiff_{action}_{sys.argv[2]}.txt"])
        diffFile = ''.join([os.getcwd(),
                            f"/resources/deviceConfigs/{sys.argv[1]}/reConfigs/TC_{testcase}/tc{testcase}_diffFromValidatedDiff_{type}_{action}_{sys.argv[2]}.txt"])

        with open(validatedDiff, 'r') as OldFile:
            with open(configDiff, 'r') as NewFile:
                diff = difflib.unified_diff(OldFile.readlines(), NewFile.readlines(),
                                            fromfile='hosts0', tofile='hosts1', n=0)
                with open(diffFile, 'w') as file_out:
                    for line in diff:
                        for prefix in ('---', '+++', '@@'):
                            if line.startswith(prefix):
                                break
                            elif 'Generated' in line or 'Finished' in line or '    }' in line \
                                    or 'authentication-key' in line or 'exit' in line \
                                    or 'group "CUSTOMER' in line\
                                    or 'eBGP customers with' in line:
                                break
                        else:
                            file_out.write(line)

        # Check for duplicates in the outFile
        file_size = os.path.getsize(diffFile)
        if file_size !=0:
            with open(diffFile, 'r') as RecheckFile:
                lines = RecheckFile.readlines()
                newLinesDict = {}
                for i in range(0, len(lines)):
                    newLine = lines[i][2:].strip("\n")
                    if newLine in newLinesDict:
                        newLinesDict[newLine] += 1
                    else:
                        newLinesDict[newLine] = 1
                count = 0
                for line in newLinesDict:
                    if newLinesDict[line] % 2 != 0:
                        if "address ::ffff:c0a8:" in line or "address ::ffff:192.168." in line or "epipe" in line or "eth-tag " in line or "evi " in line or "route-distinguisher" in line or "route-target export target" in line:
                            pass
                        else:
                            print(line, "\n")
                            count += 1
                assert count == 0
                print(f"{type} configs matched successfully for testcase {testcase}")
                return True
        else:
            print(f"{type} configs matched successfully for testcase {testcase}")
            return True

    def compare_display_diff(self, config, testcase, configType, featureName):
        # define validated diff file location
        validatedDiff = ''.join([os.getcwd(), f"/resources/deviceConfigs/{sys.argv[1]}/reBaseDiff/TC_{testcase}/tc{testcase}_validated_{GlobalVar.scenario}_config_{sys.argv[2]}.json"])

        # open and read the json file
        with open(validatedDiff, 'r') as resFile:
            resText = json.load(resFile)

        if configType.lower() == "expected" and "mwr" in featureName:
            # compare and match the response from the validated diff
            assert config[configType][GlobalVar.testParams.get("priEvpn")] == resText[f"{configType}-config"][GlobalVar.testParams.get("priEvpn")]
            print(f'{configType} config matched for {GlobalVar.testParams.get("primary")}: True')

            assert config[configType][GlobalVar.testParams.get("secEvpn")] == resText[f"{configType}-config"][GlobalVar.testParams.get("secEvpn")]
            print(f'{configType} config matched for {GlobalVar.testParams.get("primary")}: True')

        else:
            # compare and match the response from the validated diff
            assert config[configType][GlobalVar.testParams.get("priEvpn")][GlobalVar.testParams.get("primary")] == resText[f"{configType}-config"][GlobalVar.testParams.get("priEvpn")][GlobalVar.testParams.get("primary")]
            print(f'{configType} config matched for {GlobalVar.testParams.get("primary")}: True')

            assert config[configType][GlobalVar.testParams.get("priEvpn")][GlobalVar.testParams.get("secondary")] == resText[f"{configType}-config"][GlobalVar.testParams.get("priEvpn")][GlobalVar.testParams.get("secondary")]
            print(f'{configType} config matched for {GlobalVar.testParams.get("secondary")}: True')

            assert config[configType][GlobalVar.testParams.get("secEvpn")][GlobalVar.testParams.get("primary")] == resText[f"{configType}-config"][GlobalVar.testParams.get("secEvpn")][GlobalVar.testParams.get("primary")]
            print(f'{configType} config matched for {GlobalVar.testParams.get("primary")}: True')

            assert config[configType][GlobalVar.testParams.get("secEvpn")][GlobalVar.testParams.get("secondary")] == resText[f"{configType}-config"][GlobalVar.testParams.get("secEvpn")][GlobalVar.testParams.get("secondary")]
            print(f'{configType} config matched for {GlobalVar.testParams.get("secondary")}: True')

        assert config[configType][GlobalVar.testParams.get("priL3vpn")] == resText[f"{configType}-config"][GlobalVar.testParams.get("priL3vpn")]
        print(f'{configType} config matched for {GlobalVar.testParams.get("priL3vpn")}: True')

        assert config[configType][GlobalVar.testParams.get("secL3vpn")] == resText[f"{configType}-config"][GlobalVar.testParams.get("secL3vpn")]
        print(f'{configType} config matched for {GlobalVar.testParams.get("secL3vpn")}: True')

        if "mwr" in featureName:
            print("Runtime Config ==:\n", config[configType][GlobalVar.testParams.get("mwrL3vpn")])
            print("Validated Config ==:\n", resText[f"{configType}-config"][GlobalVar.testParams.get("mwrL3vpn")])

            assert config[configType][GlobalVar.testParams.get("mwrL3vpn")] == resText[f"{configType}-config"][
                GlobalVar.testParams.get("mwrL3vpn")]
            print(f'config matched for {GlobalVar.testParams.get("mwrL3vpn")}: True')

        # return true if all assertions are success
        return True


    def display_config_diff(self, configFileLoc, testcase):
        # define validated diff file location
        validatedConfigFile = ''.join([os.getcwd(), f"/resources/deviceConfigs/{sys.argv[1]}/reBaseDiff/TC_{testcase}/tc{testcase}_validated_{GlobalVar.scenario}_config_{sys.argv[2]}.json"])

        validatedConfig = json.load(open(validatedConfigFile, "r"))
        runtimeConfig = json.load(open(configFileLoc, "r"))

        assert validatedConfig == runtimeConfig
        return True
