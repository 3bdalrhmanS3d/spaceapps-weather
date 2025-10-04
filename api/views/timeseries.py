from rest_framework.views import APIView
from rest_framework.response import Response
class TimeseriesView(APIView):
    def post(self, request):
        return Response({"series": [], "trend": {"direction":"-","slope":0}})
