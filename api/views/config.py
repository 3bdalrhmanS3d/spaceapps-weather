from rest_framework.views import APIView
from rest_framework.response import Response

class ConfigView(APIView):
    def get(self, request):
        return Response({
            "defaults": {"window_days":7, "years_back":20},
            "variables": ["T2M","RH2M","WS2M","PRCP"],
            "units": {"T2M":"°C","RH2M":"%","WS2M":"m/s","PRCP":"mm/day"},
            "profiles": ["default","festival","runner","hiker","fisher"],
            "nasa_only": True
        })
