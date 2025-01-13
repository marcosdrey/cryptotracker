import requests
from django.conf import settings


class MockWebhookService:
    def __init__(self):
        self.__url = settings.MOCK_WEBHOOK_URL

    def send_webhook_data(self, data):
        requests.post(
            url=self.__url,
            json=data
        )
