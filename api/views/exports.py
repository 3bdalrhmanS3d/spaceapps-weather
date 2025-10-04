import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
class ExportView(APIView):
    def post(self, request):
        export_id = str(uuid.uuid4())
        return Response({"status":"ready","download_url":f"/api/v1/export/{export_id}/download"})
class ExportDownloadView(APIView):
    def get(self, request, export_id):
        return Response({"export_id": str(export_id)})
