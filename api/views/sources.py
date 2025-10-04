from rest_framework.views import APIView
from rest_framework.response import Response
class SourcesView(APIView):
    def get(self, request):
        return Response({
            "sources":[
                {"product":"POWER_DAILY_CORE","provider":"NASA","access":"api"},
                {"product":"GESDISC_OPeNDAP","provider":"NASA","access":"opendap"},
                {"product":"GIOVANNI","provider":"NASA","access":"giovanni"},
                {"product":"DATA_RODS_HYDRO","provider":"NASA","access":"datarods"},
                {"product":"WORLDVIEW","provider":"NASA","access":"imagery"}
            ]
        })
