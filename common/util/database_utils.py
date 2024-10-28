import urllib.request
import ssl
import json

def query_bi_mocking_server():
    # Prepare the data
    data = {
        "controller_name": "polling",
        "query": "SELECT * FROM public.polling_engine_bsaf_request_tracker WHERE id = '0428d69a-43d5-4533-80c7-8962fd5fdabf'"
    }

    # Specify the URL
    url = "https://bi-mocking-server.qa.app01.toll6.tinaa.tlabs.ca/query-v2"

    try:
        # Disable SSL certificate verification
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # Encode data to JSON
        data_json = json.dumps(data).encode('utf-8')

        # Send a POST request to the BI Mocking Server endpoint with SSL verification disabled
        req = urllib.request.Request(url, data=data_json, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, context=context) as response:
            response_data = response.read().decode('utf-8')

        # Parse JSON response
        response_json = json.loads(response_data)
        return response_json

    except urllib.error.URLError as e:
        print("URL Error:", e)
        return None
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

# Example usage
response_data = query_bi_mocking_server()
if response_data:
    print(response_data)
