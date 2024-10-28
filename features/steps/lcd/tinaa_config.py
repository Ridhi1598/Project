import os

class TinaaAuthServiceConfig:
    MOCK_TINAA = False
    USE_CERTS = False

    if not MOCK_TINAA:
        CLIENT_ID = 'bsaf-sdar-test'
        CLIENT_SECRET = '6e30b4f0-8898-478e-85c6-6f402f3075be'
        GENERATOR_URL = 'https://auth.app01.toll6.tinaa.tlabs.ca/auth/realms/tinaa/protocol/openid-connect/token'
        GUARDING_TIME = 120

    if USE_CERTS:
        CERTS_PATH = os.environ['TINAA_CERTS_PATH']
    