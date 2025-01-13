from rest_framework.views import APIView, Response, status
from services.mock_webhook import MockWebhookService


class WebhookNotifyAlertView(APIView):

    def post(self, request):
        data = request.data
        mock_webhook_service = MockWebhookService()
        mock_webhook_service.send_webhook_data(data)
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
