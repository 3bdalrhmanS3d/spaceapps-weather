from rest_framework.views import APIView
from rest_framework.response import Response
DISCLAIMER = ("NASA does not endorse any non-U.S. Government entity and is not responsible "
              "for information contained on non-U.S. Government websites. Users must comply "
              "with each data source’s terms.")
class AboutView(APIView):
    def get(self, request):
        return Response({"disclaimer": DISCLAIMER})
