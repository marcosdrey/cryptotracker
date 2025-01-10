from rest_framework.views import APIView, Response, status


class WebhookNotifyAlertView(APIView):

    def post(self, request):
        data = request.data
        print(data)
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
