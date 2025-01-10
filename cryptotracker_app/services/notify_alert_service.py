import requests


class NotifyAlertService:

    def __init__(self):
        self.__base_url = 'http://localhost:8001'

    def send_alert(self, data):
        requests.post(
            url=f'{self.__base_url}/api/v1/alert/',
            json=data
        )
