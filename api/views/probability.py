from rest_framework.views import APIView
from rest_framework.response import Response

class ProbabilityView(APIView):
    def post(self, request):
        # لاحقاً هنربط حساب الاحتمالات فعلياً
        return Response({
            "location": {"lat": request.data.get("lat"), "lon": request.data.get("lon")},
            "probabilities": {
                "very_hot": 0.41,
                "very_cold": 0.06,
                "very_windy": 0.18,
                "very_wet": 0.23,
                "very_uncomfortable": 0.32
            }
        })
