from rest_framework.views import APIView
from rest_framework.response import Response

class TimeseriesView(APIView):
    def post(self, request):
        # لاحقاً هنبدّل بالداتا الحقيقية
        return Response({
            "series": [
                {"date": "2012-01-01", "T2M": 18.3},
                {"date": "2012-01-02", "T2M": 19.1},
            ],
            "trend": {"direction": "+", "slope": 0.02}
        })
