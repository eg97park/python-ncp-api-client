"""
This module provides some useful functions about NAVER Cloud Platform RESTful API.
"""
import json
import time
import datetime

from .client import GeneralClient


def check_api_key(settings:dict) -> bool:
    """
    It checks if the NCP api key is valid.
    
    Args:
      SETTINGS (dict): credentials.
    
    Returns:
      bool: vailidity of given NCP api key.
    """
    try:
        ncp_api_client = GeneralClient(
            access_key=settings['NCP_API']['ACCESS_KEY'],
            secret_key=settings['NCP_API']['SECRET_KEY'],
            url='https://sts.apigw.ntruss.com',
            uri='/api/v1'
        )

        result = ncp_api_client.query(
            api='/caller-identity',
            method='GET'
        )

        _ = result['id']
    except:
        # Wrong NCP api key.
        print(f'[{datetime.datetime.fromtimestamp(int(time.time()))} {__file__} {__name__}]\n'\
            f":Wrong NCP api key.\n"
            f"access_key={settings['NCP_API']['ACCESS_KEY']}\n"
            f"secret_key={settings['NCP_API']['SECRET_KEY']}\n"
        )
        print(f'[{datetime.datetime.fromtimestamp(int(time.time()))} {__file__} {__name__}]\n'\
            f':NCP message={json.dumps(result, indent=4, ensure_ascii=False)}\n'
        )
        return False
    return True
