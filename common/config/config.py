import json
import sys

import pytest


@pytest.fixture(scope='session')
def config():
    with open('resources/'+sys.argv[1]+'_appConfig.json') as config_file:
        data = json.load(config_file)
    return data

