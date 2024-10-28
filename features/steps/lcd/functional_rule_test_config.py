import os
import sys


class FunctionalRuleTestConfig:
    FUNCTIONAL_RULE_TEST_DIR = 'features/steps/lcd/rule_tests/'
    FUNCTIONAL_TESTING_DEVICE_INVENTORY = 'features/steps/lcd/rule_tests/device-inventory.yml'
    if sys.argv[2]=='dev':
        FUNCTIONAL_TESTING_MEDIATION_HOSTNAME = 'https://lcd-mediation.develop.app01.toll6.tinaa.tlabs.ca'
    if sys.argv[2]=='preprod':
        FUNCTIONAL_TESTING_MEDIATION_HOSTNAME = 'https://lcd-mediation.preprod.app01.toll6.tinaa.tlabs.ca'
    USE_CERTS = False
    FORCE_SESSION = False
    if USE_CERTS:
        CERTS_PATH = os.environ['FUNCTIONAL_TESTING_MEDIATION_CERTS_PATH']
        # MEDIATION_CLIENT_CERTIFICATE = CERTS_PATH + '/' + 'client_certificate.pem'
        # MEDIATION_CLIENT_KEY = CERTS_PATH + '/' + 'client_key.pem'
        MEDIATION_CA_CERTIFICATE = CERTS_PATH + '/' + 'ca_certificate.pem'
