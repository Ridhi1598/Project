from behave import *
import difflib
import json
import time
import os
import sys
import ssl
import pysftp
import gzip
import shutil
from os.path import dirname, abspath
import jsonschema as jsonschema
import requests
import datetime
from behave import given, when, then, step
from jsonschema import validate
from requests import HTTPError
from features.steps.globalVar import GlobalVar
from features.steps.bi.bi_restApis import *
from features.steps.api_steps_general import *
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from features.steps.globalVar import GlobalVar
from features.steps.ui_steps_general import page_title_validation, change_currentPage
from selenium.webdriver.support.select import Select
from common.util.payloadGenerator import payloadGenerator

# declared variables
from features.steps.globalVar import GlobalVar

api_endpoints = {}
request_headers = {}
response_codes = {}
response_texts = {}
response_json = {}
request_bodies = {}
api_url = None
responseVar = None
payload = {}
access_token = None
body = {}
testParams = {}
executedTestCases = []
request_Id = {}
index = None
testCaseData = {}
configFiles = {}
addUser = {}
regNewUser = {}
state = {}
roleAdmin = {}
roleRW = {}
roleRead = {}
loginStatus = None
requestState = None