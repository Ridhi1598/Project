import os
import shutil
import pysftp
from envyaml import EnvYAML
import time
import datetime

def create_file():
    for test in range(74, 105):
        fl = f"D:\\TINAA\\lcd\\resources\\payload\\bi_clm\\e2e\\e2e_tc{test}_qa.json"
        open(fl, "w")


def copy_file():
    for test in range(40, 41):
        src = f"D:\\TINAA\\lcd\\resources\\deviceConfigs\\bi_clm\\reBaseDiff\\TC_{test}\\tc{test}_create-display_config_qa.json"
        dest = f"D:\\TINAA\\lcd\\resources\\deviceConfigs\\bi_clm\\reBaseDiff\\TC_{test}\\tc{test}_validated_create-display_config_qa.json"
        path = shutil.copy(src, dest)
        print(path)

def rename_file():
    for test in range(38, 39):
        src = f"D:\\TINAA\\lcd\\resources\\deviceConfigs\\bi_clm\\reBaseDiff\\TC_{test}\\tc{test}_diff_sx_delete-execute_qa.txt"
        dest = f"D:\\TINAA\\lcd\\resources\\deviceConfigs\\bi_clm\\reBaseDiff\\TC_{test}\\tc{test}_sx_validatedDiff_delete-execute_qa.txt"
        os.rename(src, dest)
        print(dest)

def download_file_from_remote(host, scenario, action):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    try:
        connection = pysftp.Connection(host=host, username="x322195", password="Telus2024", cnopts=cnopts)
        remoteWorkingDirectory = "/cf3:/"
        source_file = "config.cfg"
        print(f"connection established : {connection}")
        connection.cwd(remoteWorkingDirectory)

        dest_Folder = "D:\\TINAA\\deviceConfig"
        if not os.path.exists(dest_Folder):
            os.mkdir(dest_Folder)
        currTime = datetime.date.today()
        dest_file = ''.join([dest_Folder, f"/{host}_config_{scenario}_{action}_{currTime}.txt"])

        try:
            # download and return the config file
            connection.get(source_file, dest_file)
            if os.path.exists(dest_file):
                print(f"File downloaded: {dest_file}")
                connection.close()

        except IOError as err:
            print(err)

    except Exception as e:
        raise Exception(e)

# download_file_from_remote("EDTABTFSX01", "before", "create")
# rename_file()

create_file()