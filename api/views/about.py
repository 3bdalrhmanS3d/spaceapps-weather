from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from api.serializers import DisclaimerSerializer

DISCLAIMER = (
    "NASA does not endorse any non-U.S. Government entity and is not responsible for information "
    "contained on non-U.S. Government websites. Users must comply with each data source's terms."
)

class AboutView(GenericAPIView):
    serializer_class = DisclaimerSerializer

    @extend_schema(responses=DisclaimerSerializer)
    def get(self, request):
        return Response({"disclaimer": DISCLAIMER})
