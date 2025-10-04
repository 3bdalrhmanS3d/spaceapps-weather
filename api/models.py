from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=120, blank=True, default="")
    phone = models.CharField(max_length=40, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name or self.user.username


class FavoritePlace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    name = models.CharField(max_length=120)
    lat = models.FloatField()
    lon = models.FloatField()
    notes = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["lat", "lon"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.lat:.3f},{self.lon:.3f})"


class ThresholdProfile(models.Model):
    """
    thresholds مثال:
    {
      "very_hot": {"T2M": {">=": 35}},
      "very_cold": {"T2M": {"<=": 0}},
      "very_windy": {"WS2M": {">=": 10}},
      "very_wet": {"PRCP": {">=": 10}},
      "very_uncomfortable": {"HI": {">=": 38}}
    }
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="threshold_profiles")
    name = models.CharField(max_length=120)
    thresholds = models.JSONField(default=dict)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "name")]
        indexes = [models.Index(fields=["user"])]

    def __str__(self):
        owner = self.user.username if self.user_id else "global"
        return f"{owner}:{self.name}"


class SavedQuery(models.Model):
    """
    يخزن استعلامات المستخدم (نقطة/مدى أيام/متغيرات) لإعادة الاستخدام
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_queries")
    lat = models.FloatField()
    lon = models.FloatField()
    day_of_year = models.PositiveSmallIntegerField(null=True, blank=True)  # 1..366 (اختياري)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    variables = models.JSONField(default=list)  # ["T2M","RH2M","WS2M","PRCP"]
    profile = models.ForeignKey(ThresholdProfile, on_delete=models.SET_NULL, null=True, blank=True)
    params = models.JSONField(default=dict)     # أي باراميتر إضافي (years_back, window_days...)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["lat", "lon"]),
        ]


class ExportJob(models.Model):
    """
    مهمة تصدير بيانات (CSV/JSON) لنتيجة الاستعلام
    """
    FORMAT_CHOICES = (
        ("csv", "CSV"),
        ("json", "JSON"),
    )
    STATUS_CHOICES = (
        ("queued", "Queued"),
        ("running", "Running"),
        ("done", "Done"),
        ("failed", "Failed"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="export_jobs")
    query = models.ForeignKey(SavedQuery, on_delete=models.CASCADE, related_name="exports")
    fmt = models.CharField(max_length=10, choices=FORMAT_CHOICES, default="csv")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="queued")
    file_path = models.CharField(max_length=300, blank=True, default="")
    meta = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["user"]), models.Index(fields=["status"])]


class DataSource(models.Model):
    """
    توصيف مصادر البيانات (POWER, OPeNDAP, Giovanni, ...)
    """
    name = models.CharField(max_length=80, unique=True)          # e.g. POWER_DAILY_CORE
    provider = models.CharField(max_length=80, default="NASA")   # e.g. NASA
    access = models.CharField(max_length=40, default="api")      # api/opendap/giovanni/datarods/imagery
    base_url = models.CharField(max_length=300, blank=True, default="")
    extra = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SourceRequest(models.Model):
    """
    لوج طلبات المصادر (لـ debug والـ usage)
    """
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="requests")
    url = models.CharField(max_length=500)
    status_code = models.IntegerField(null=True, blank=True)
    duration_ms = models.IntegerField(null=True, blank=True)
    ok = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["source"]),
            models.Index(fields=["created_at"]),
        ]


class MLModel(models.Model):
    """
    ريجستري لنماذج ML
    """
    key = models.CharField(max_length=120, unique=True)   # v1_lgbm_5heads
    algo = models.CharField(max_length=80, default="lightgbm")
    version = models.CharField(max_length=40, default="1.0.0")
    is_active = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict)             # feature_names, training_window, metrics...
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.key} ({self.version})"


class MLRun(models.Model):
    """
    لوج تنبؤات النموذج
    """
    model = models.ForeignKey(MLModel, on_delete=models.SET_NULL, null=True, related_name="runs")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="ml_runs")
    input_payload = models.JSONField(default=dict)   # lat/lon/day/vars/thresholds...
    output_payload = models.JSONField(default=dict)  # probabilities, explanation...
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["user"]),
        ]
