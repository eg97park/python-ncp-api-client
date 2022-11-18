"""
This module provides NAVER Cloud Platform RESTful API client.
"""
import hashlib
import hmac
import base64
import time
import urllib.parse
import requests


class GeneralClient:
    """
    This class is used to make a request to the NAVER Cloud Platform RESTful API server.
    """
    def __init__(self, access_key, secret_key, url, uri):
        """
        It initializes the class with the access key, secret key, base URL, and base URI.
        
        Args:
          access_key: The access key of API.
          secret_key: The secret key of API.
          url: The URL of the service API.
          uri: The URI of the API endpoint you're calling.
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.base_url = url
        self.base_uri = uri

    def make_signature(self, method, uri):
        """
        It takes a method and a URI, and returns a timestamp and a signing key.
        
        Args:
          method: The HTTP method. (GET, POST)
          uri: The URI of the API endpoint you're calling.
        
        Returns:
          The used timestamp and signingKey.
        """
        timestamp = str(int(time.time() * 1000))
        b_secret_key = bytes(self.secret_key, 'UTF-8')
        b_message = bytes(method + " " + uri + "\n" + timestamp + "\n" + self.access_key, 'UTF-8')
        signed_key = base64.b64encode(hmac.new(b_secret_key, b_message, digestmod=hashlib.sha256).digest())
        return timestamp, signed_key

    def query(self, api, method, aheaders=None, params=None, body=None):
        """
        It sends a request to the API server with the generated signature.
        
        Args:
          api: The API name to be called.
          method: The HTTP method. (GET, POST)
          aheaders: Additional headers to be added to the request.
          params: Additional parameters to be added to the request.
          body: Additional body json to be added to the request (POST).

        Returns:
          If result can be parsed by json, return json object.
          If not, return recieved data as text(str). Most of cases, xml.
        """
        uri = self.base_uri + api
        if params is not None:
            uri += '?' + urllib.parse.urlencode(params)
        timestamp, signed_key = self.make_signature(method, uri)

        headers = {
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': self.access_key,
            'x-ncp-apigw-signature-v2': signed_key
        }
        if aheaders is not None:
            headers.update(aheaders)

        result = None
        if method == 'GET':
            result = requests.get(url=self.base_url + uri, headers=headers)
        elif method == 'POST':
            result = requests.post(url=self.base_url + uri, headers=headers, json=body)
        elif method == 'DELETE':
            result = requests.delete(url=self.base_url + uri, headers=headers, json=body)
        elif method == 'PUT':
            result = requests.put(url=self.base_url + uri, headers=headers, json=body)
        else:
            raise ValueError
        
        try:
            return result.json()
        except ValueError:
            return result.text

class ClouadActivityTracerClient:
    """
    This class is used to make a request to the Cloud Activity Tracer RESTful API server of NAVER Cloud Platform.
    """
    def __init__(self, access_key, secret_key):
        """
        It initializes the class with the access key, and secret key.
        
        Args:
          access_key: The access key of API.
          secret_key: The secret key of API.
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.base_url = 'https://cloudactivitytracer.apigw.ntruss.com'
        self.base_uri = '/api/v1/'
        self.url = 'https://cloudactivitytracer.apigw.ntruss.com/api/v1/activities'
        self.uri = '/api/v1/activities'

    def make_signature(self, method, uri):
        """
        It takes a method and a URI, and returns a timestamp and a signing key.
        
        Args:
          method: The HTTP method. (GET, POST)
          uri: The URI of the API endpoint you're calling.
        
        Returns:
          The used timestamp and signingKey.
        """
        timestamp = str(int(time.time() * 1000))
        b_secret_key = bytes(self.secret_key, 'UTF-8')
        b_message = bytes(method + " " + uri + "\n" + timestamp + "\n" + self.access_key, 'UTF-8')
        signed_key = base64.b64encode(hmac.new(b_secret_key, b_message, digestmod=hashlib.sha256).digest())
        return timestamp, signed_key

    def query(self, from_event_time=None, to_event_time=None, nrn=None, page_index=None, page_size=None):
        """
        It sends a request to the Cloud Activity Tracer API server with the generated signature.
        
        Args:
          from_event_time: The start timestamp of the event to be queried. The default value is 30 days before.
          to_event_time: The end timestamp of the event to be queried. The default value is now.
          nrn: NRN(Ncloud Resource Names).
          page_index: The page index number of results. The default value is 0, and startring from 0.
          page_size: The number of logs to return per page. The default value is 20, and max value is 100.
        
        Returns:
          If result can be parsed by json, return json object.
          If not, return recieved data as text(str). Most of cases, xml with error message.
        """
        timestamp, signed_key = self.make_signature('POST', self.uri)
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': self.access_key,
            'x-ncp-apigw-signature-v2': signed_key
        }

        body = {}
        if from_event_time is not None:
            body.update({'fromEventTime': from_event_time})
        if to_event_time is not None:
            body.update({'toEventTime': to_event_time})
        if nrn is not None:
            body.update({'nrn': nrn})
        if page_index is not None:
            body.update({'pageIndex': page_index})
        if page_size is not None:
            body.update({'pageSize': page_size})

        result = requests.post(url=self.url, headers=headers, json=body)
        try:
            return result.json()
        except ValueError:
            return result.text
