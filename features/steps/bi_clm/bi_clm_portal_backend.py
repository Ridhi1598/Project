from behave import *
from features.steps.bi.bi_controller import *
from features.steps.bi_clm.bi_clm_uiFunctional import *
from common.util.api_test import ApiTest
from common.util.dbValidation import ES
from features.steps.bi_clm.bi_clm_ingestion import *
from features.steps.bi_clm.bi_clm_e2e import *
from features.steps.bi_clm.bi_clm_orchestrator import *

# declared variables
# end of declared variables

@step('I validate that a "{recordType}" record is "{status}" in "{entity}" database')
def fetch_db_record(context, recordType, status, entity):
    GlobalVar.requestType = GlobalVar.testParams.get(f'{entity}_{recordType}_RequestType')
    payloadFile = GlobalVar.testParams.get(f'{entity}_{recordType}_RequestBody')
    if bool(payloadFile):
        GlobalVar.api_dict['request_bodies'] = ApiTest.setBody(context, payloadFile, GlobalVar.testComponent[0].lower())
        GlobalVar.api_dict['request_bodies']['query']['bool']['should'][0]['bool']['filter'][0]['term']['customer_id_int'] = int(GlobalVar.testParams["customerId"])
    else:
        GlobalVar.api_dict['request_bodies'] = None
    reqURL = ApiTest.setEndpoint(context, set_url(context, entity), GlobalVar.testParams.get(
        f'{entity}_{recordType}_EndPoint'))
    GlobalVar.response = ApiTest.sendRequestAuth(context, GlobalVar.requestType, reqURL, GlobalVar.api_dict[
        'request_bodies'], context.config.get(f"{entity}_User"), context.config.get(f"{entity}_Pass"))
    print(GlobalVar.response.text)

    try:
        if "not" in status:
            assert GlobalVar.response.json()["hits"]["total"]["value"] == 0
        else:
            assert GlobalVar.response.json()["hits"]["total"]["value"] > 0
    except AssertionError:
        time.sleep(5)
        fetch_db_record(context, recordType, status, entity)

@step('I read "{id}" for the customer')
def fetch_id(context, id):
    GlobalVar.customerId = GlobalVar.response.json()["records"][0][id]
    print(GlobalVar.customerId)

@step('I validate response for expected "{field}"')
def validate_cust_res(context, field):
    res = GlobalVar.response.json()
    if field == "status" or field == "result" or field == "total-size":
        assert str(res[field]) == str(GlobalVar.testParams.get(field))
    if field == "customer_id":
        assert str(res["records"][0][field]) == GlobalVar.testParams.get("customerId")


@step('I validate the customer "{field}" is {scenario} in database')
def step_impl(context, field, scenario):
    if field == "id":
        assert GlobalVar.response.json()["hits"]["hits"][0]["_id"] == GlobalVar.customerId
    else:
        print(GlobalVar.response.json()["hits"]["hits"][0]["_source"][field], GlobalVar.api_dict["payload"][field])
        assert GlobalVar.response.json()["hits"]["hits"][0]["_source"][field] == GlobalVar.api_dict["payload"][field]


@step('I send request to "{recordType}" record in "{entity}" "{indexType}" record')
def action_record_status(context, recordType, entity, indexType):
    # read request method
    GlobalVar.requestType = GlobalVar.testParams.get(f'{entity}_{recordType}_RequestType')

    # read and update request body
    payloadFile = GlobalVar.testParams.get(f'{entity}_{recordType}_RequestBody')
    if bool(payloadFile):
        GlobalVar.api_dict['request_bodies'] = ApiTest.setBody(context, payloadFile, GlobalVar.testComponent[0].lower())
        # set service Id
        if indexType.lower() == "service":
            GlobalVar.api_dict['request_bodies']["customer-id"] = int(GlobalVar.testParams.get("customerId"))
    else:
        GlobalVar.api_dict['request_bodies'] = None

    print(GlobalVar.api_dict['request_bodies'])

    # read and update request endpoint
    reqURL = ApiTest.setEndpoint(context, set_url(context, entity), GlobalVar.testParams.get(
        f'{entity}_{recordType}_EndPoint').format(GlobalVar.testParams.get("serviceId")))

    # send request and store response
    GlobalVar.response = ApiTest.sendRequestAuth(context, GlobalVar.requestType, reqURL, GlobalVar.api_dict[
        'request_bodies'], context.config.get(f"{entity}_User"), context.config.get(f"{entity}_Pass"))
    print(GlobalVar.response.text)

    # validate response code
    if indexType.lower() != "service":
        assert ApiTest.validateResponseCode(context, GlobalVar.response, GlobalVar.testParams.get(f'{entity}_{recordType}_responseCode'))

    print("Wait for service record to get updated...")
    time.sleep(5)