"""
Simple usage of https://api.ncloud-docs.com/docs/common-ncpapi.
"""
import time
import json

from ncp.client import GeneralClient, ClouadActivityTracerClient


ACCESS_KEY = 'AAAAAAAAAAAAAAAAAAAA'
SECRET_KEY = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

if __name__ == '__main__':
    print(f'Use access key={ACCESS_KEY}, secret_key={SECRET_KEY}')

    # Example of general NCP API client.
    # URL: https://api.ncloud-docs.com/docs/get-caller-identity.
    ncp_api_client = GeneralClient(
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        url='https://sts.apigw.ntruss.com',
        uri='/api/v1'
    )

    result = ncp_api_client.query(
        api='/caller-identity',
        method='GET'
    )
    print(f'{json.dumps(result, indent=4, ensure_ascii=False)}')


    # Example of specialized NCP Cloud Activity Tracer API client.
    FROM_EVENT_TIME = int(time.time() * 1000) - 7776000000
    TO_EVENT_TIME = int(time.time() * 1000)

    cat_handler = ClouadActivityTracerClient(
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY
    )

    # Get one Cloud Activity Tracer logs.
    query_result = cat_handler.query(page_index=1, page_size=1)['items'][0]
    print(f'{json.dumps(query_result, indent=4, ensure_ascii=False)}')

    # Get all Cloud Activity Tracer logs in given period of timestamp. (90 days ago ~)
    print(f'FROM_EVENT_TIME={FROM_EVENT_TIME}, TO_EVENT_TIME={TO_EVENT_TIME}')

    page_index = 0
    while True:
        query_result = cat_handler.query(page_index=0, page_size=100, from_event_time=FROM_EVENT_TIME, to_event_time=TO_EVENT_TIME)
        json_list = query_result['items']
        for json_elem in json_list:
            time.sleep(1)
            print(f'{json.dumps(json_elem, indent=4, ensure_ascii=False)}')

        if query_result['hasMore'] is False:
            break
        else:
            page_index += 1

    