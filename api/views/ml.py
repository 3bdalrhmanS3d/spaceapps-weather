from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from api.serializers import (
    MLPredictRequestSerializer, MLPredictResponseSerializer,
    MLInfoSerializer, MLExplainRequestSerializer, MLExplainResponseSerializer
)

class MLPredictView(GenericAPIView):
    serializer_class = MLPredictRequestSerializer

    @extend_schema(
        request=MLPredictRequestSerializer,
        responses=MLPredictResponseSerializer,
        description="ML-assisted probabilities for the selected profile."
    )
    def post(self, request):
        s = MLPredictRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response({
            "model": "v1_lgbm_5heads",
            "probabilities": {
                "very_hot": 0.33,
                "very_cold": 0.06,
                "very_windy": 0.20,
                "very_wet": 0.15,
                "very_uncomfortable": 0.26,
            }
        })

class MLInfoView(GenericAPIView):
    serializer_class = MLInfoSerializer

    @extend_schema(responses=MLInfoSerializer)
    def get(self, request):
        return Response({"active_model": {"key": "v1_lgbm_5heads", "algo": "lightgbm", "version": "1.0.0"}})

class MLExplainView(GenericAPIView):
    serializer_class = MLExplainRequestSerializer

    @extend_schema(
        request=MLExplainRequestSerializer,
        responses=MLExplainResponseSerializer,
        description="Return top features driving the probabilities."
    )
    def post(self, request):
        s = MLExplainRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response({"top_features": ["T2M_7d_mean", "RH2M_p95", "WS2M_p75", "PRCP_1d_max"]})
