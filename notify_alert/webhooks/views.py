import json
from rest_framework.views import APIView, Response, status
from services.mock_webhook import MockWebhookService
from webhooks.models import Webhook


class WebhookNotifyAlertView(APIView):

    def post(self, request):
        data = request.data
        mock_webhook_service = MockWebhookService()
        mock_webhook_service.send_webhook_data(data)

        Webhook.objects.create(
            event_type=data.get('event_type'),
            event_text=json.dumps(data, ensure_ascii=False)
        )

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
