from django.urls import path
from api.views.health import HealthView
from api.views.config import ConfigView
from api.views.about import AboutView
from api.views.sources import SourcesView
from api.views.probability import ProbabilityView
from api.views.timeseries import TimeseriesView
from api.views.exports import ExportView, ExportDownloadView
from api.views.ml import MLPredictView, MLInfoView, MLExplainView
from api.auth_views import RegisterView, LoginView, MeView

urlpatterns = [
    path("health", HealthView.as_view()),
    path("config", ConfigView.as_view()),
    path("about", AboutView.as_view()),
    path("sources", SourcesView.as_view()),
    path("probability", ProbabilityView.as_view()),
    path("timeseries", TimeseriesView.as_view()),
    path("export", ExportView.as_view()),
    path("export/<uuid:export_id>/download", ExportDownloadView.as_view()),
    path("ml/predict", MLPredictView.as_view()),
    path("ml/info", MLInfoView.as_view()),
    path("ml/explain", MLExplainView.as_view()),

    # Auth
    path("auth/register", RegisterView.as_view()),
    path("auth/login", LoginView.as_view()),
    path("auth/me", MeView.as_view()),
]
