import requests
import requests_mock
from datetime import datetime

def get_now():
    return int(datetime.now().strftime("%Y"))

def get_year_to_download():
    actual_year = get_now()
    year = str(actual_year - 1)    
    return year

def build_payload():
    year_to_download = get_year_to_download()

    startDate_param_name = 'startDate'
    endDate_param_name = 'endDate'

    startDate_param_value = year_to_download + "-01-01 00:00:00.000 -05:00"
    endDate_param_value = year_to_download + "-12-31 23:59:59.999 -05:00"

    payloadRequest = ((startDate_param_name, startDate_param_value),
            (endDate_param_name, endDate_param_value))
    return payloadRequest

def determinate_response(response):
    if response == 0:
        print ("estado:controlm_exitoso_0000")
        return (0)
    else:
        print ("estado:controlm_no_exitoso_0000")
        return (1)



def trigger_service():
    payload = build_payload()
    url_base = 'https://hidden-fortress-02723.herokuapp.com'
    api = '/attachment-total-costs-report'
    try:
        response = requests.get(url_base + api, params=payload, headers={'Content-Type':'application/json'}).json()
    except requests.exceptions.Timeout:
        print('Timeout error')
        exit(1)
    except requests.exceptions.TooManyRedirects:
        print('TooManyRedirects')
        exit(1)
    except requests.exceptions.RequestException as e:
        print(e)
        exit(1)
    json_response = response
    return determinate_response(json_response)


def do_work():
    return trigger_service()

if __name__ == '__main__':
    do_work()   
