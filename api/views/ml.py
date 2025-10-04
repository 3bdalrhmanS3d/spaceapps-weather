from rest_framework.views import APIView
from rest_framework.response import Response
class MLPredictView(APIView):
    def post(self, request):
        return Response({"model":"v1_lgbm_5heads","probabilities":{}})
class MLInfoView(APIView):
    def get(self, request):
        return Response({"active_model":{"key":"v1_lgbm_5heads","algo":"lightgbm","version":"1.0.0"}})
class MLExplainView(APIView):
    def post(self, request):
        return Response({"top_features": []})
