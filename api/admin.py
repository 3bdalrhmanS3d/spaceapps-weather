from django.contrib import admin
from .models import (
    Profile, FavoritePlace, ThresholdProfile, SavedQuery,
    ExportJob, DataSource, SourceRequest, MLModel, MLRun
)

admin.site.register(Profile)
admin.site.register(FavoritePlace)
admin.site.register(ThresholdProfile)
admin.site.register(SavedQuery)
admin.site.register(ExportJob)
admin.site.register(DataSource)
admin.site.register(SourceRequest)
admin.site.register(MLModel)
admin.site.register(MLRun)
