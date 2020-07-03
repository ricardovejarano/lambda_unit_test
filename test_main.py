import json
from main import *
from unittest import TestCase, mock
from datetime import datetime

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data

    return MockResponse(0)


class TestLambda(TestCase):

    URL_BASE = 'https://hidden-fortress-02723.herokuapp.com'
    API = '/attachment-total-costs-report'
    ACTUAL_YEAR = 2020
    YEAR_TO_DOWNLOAD = '2019'
    YEAR_TO_DOWNLOAD_WRONG = '2020'
    PAYLOAD = (('startDate', '2019-01-01 00:00:00.000 -05:00'), ('endDate', '2019-12-31 23:59:59.999 -05:00'))
    PAYLOAD_WRONG = (('startDate', '2020-01-01 00:00:00.000 -05:00'), ('endDate', '2020-12-31 23:59:59.999 -05:00'))
    RESPONSE_JSON = {'response': 'ok'}
    CODE_ZERO = 0
    CODE_ONE = 1
    CODE_200 = 200
    CODE_400 = 400
    CODE_500 = 500

    @mock.patch('main.get_now')
    def test_is_year_to_download_actual_less_1(self, now_mock):
        now_mock.return_value = self.ACTUAL_YEAR
        self.assertAlmostEqual(get_year_to_download(), self.YEAR_TO_DOWNLOAD)

    @mock.patch('main.get_now')
    def test_is_year_to_download_different_to_actual_year(self, now_mock):
        now_mock.return_value = self.ACTUAL_YEAR
        self.assertFalse(get_year_to_download() == self.YEAR_TO_DOWNLOAD_WRONG)

    @mock.patch('main.get_now')
    def test_year_to_download_is_string(self, now_mock):
        now_mock.return_value = self.ACTUAL_YEAR
        self.assertTrue(type(get_year_to_download()) is str)
        self.assertFalse(type(get_year_to_download()) is int)
    
    @mock.patch('main.get_year_to_download')
    def test_is_payload_correct(self, year_mock):
        year_mock.return_value = self.YEAR_TO_DOWNLOAD
        self.assertTrue(build_payload() == self.PAYLOAD)

    @mock.patch('main.get_year_to_download')
    def test_is_payload_wrong(self, year_mock):
        year_mock.return_value = self.YEAR_TO_DOWNLOAD
        self.assertFalse(build_payload() == self.PAYLOAD_WRONG)


    def test_determinate_response(self):
        self.assertAlmostEqual(determinate_response(self.CODE_ZERO), self.CODE_ZERO)
        self.assertTrue(determinate_response(self.CODE_ZERO) == self.CODE_ZERO)
        self.assertFalse(determinate_response(self.CODE_ONE) == self.CODE_ZERO)
        self.assertFalse(determinate_response(self.CODE_200) == self.CODE_ZERO)
        self.assertFalse(determinate_response(self.CODE_400) == self.CODE_ZERO)
        self.assertFalse(determinate_response(self.CODE_500) == self.CODE_ZERO)
        self.assertFalse(determinate_response(self.RESPONSE_JSON) == self.CODE_ZERO)

    @mock.patch('main.build_payload')
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_trigger(self, payload_mock, req_mock):    
        payload_mock.return_value = self.PAYLOAD
        req_mock.return_value = 0
        #print(type(object))
        #self.assertTrue(trigger_service() != self.CODE_ZERO) 
        json_data = trigger_service()
        self.assertEqual(json_data, self.CODE_ZERO)