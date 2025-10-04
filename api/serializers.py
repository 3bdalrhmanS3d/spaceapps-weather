from rest_framework import serializers

# --- generic small payloads ---
class HealthSerializer(serializers.Serializer):
    status = serializers.CharField()

class DisclaimerSerializer(serializers.Serializer):
    disclaimer = serializers.CharField()

class ConfigDefaultsSerializer(serializers.Serializer):
    window_days = serializers.IntegerField()
    years_back = serializers.IntegerField()

class ConfigSerializer(serializers.Serializer):
    defaults = ConfigDefaultsSerializer()
    variables = serializers.ListField(child=serializers.CharField())
    units = serializers.DictField(child=serializers.CharField())
    profiles = serializers.ListField(child=serializers.CharField())
    nasa_only = serializers.BooleanField()

class SourceItemSerializer(serializers.Serializer):
    product = serializers.CharField()
    provider = serializers.CharField()
    access = serializers.CharField()

class SourcesSerializer(serializers.Serializer):
    sources = SourceItemSerializer(many=True)

# --- probability ---
class ProbabilityRequestSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    date = serializers.DateField()          # يوم النشاط
    window_days = serializers.IntegerField(required=False, default=7)
    variables = serializers.ListField(
        child=serializers.CharField(), required=False, default=["T2M","RH2M","WS2M","PRCP"]
    )

class ProbabilityBucketsSerializer(serializers.Serializer):
    very_hot = serializers.FloatField()
    very_cold = serializers.FloatField()
    very_windy = serializers.FloatField()
    very_wet = serializers.FloatField()
    very_uncomfortable = serializers.FloatField()

class ProbabilityResponseSerializer(serializers.Serializer):
    location = serializers.DictField()
    buckets = ProbabilityBucketsSerializer()
    notes = serializers.ListField(child=serializers.CharField(), required=False)

# --- time-series ---
class TimeseriesRequestSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    variable = serializers.CharField()  # e.g. T2M
    start = serializers.DateField()
    end = serializers.DateField()
    agg = serializers.ChoiceField(choices=["daily","weekly","monthly"], default="daily")

class TimeseriesPointSerializer(serializers.Serializer):
    date = serializers.DateField()
    value = serializers.FloatField(allow_null=True)

class TrendSerializer(serializers.Serializer):
    direction = serializers.ChoiceField(choices=["+","-","0"])
    slope = serializers.FloatField()

class TimeseriesResponseSerializer(serializers.Serializer):
    variable = serializers.CharField()
    series = TimeseriesPointSerializer(many=True)
    trend = TrendSerializer()

# --- export ---
class ExportRequestSerializer(serializers.Serializer):
    format = serializers.ChoiceField(choices=["csv","json"], default="csv")
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    variables = serializers.ListField(child=serializers.CharField())

class ExportResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    download_url = serializers.CharField()

class ExportDownloadSerializer(serializers.Serializer):
    export_id = serializers.CharField()

# --- ML ---
class MLPredictRequestSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    date = serializers.DateField()
    profile = serializers.ChoiceField(choices=["default","festival","runner","hiker","fisher"], default="default")

class MLPredictResponseSerializer(serializers.Serializer):
    model = serializers.CharField()
    probabilities = ProbabilityBucketsSerializer()

class MLInfoSerializer(serializers.Serializer):
    active_model = serializers.DictField()

class MLExplainRequestSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    date = serializers.DateField()

class MLExplainResponseSerializer(serializers.Serializer):
    top_features = serializers.ListField(child=serializers.CharField())

# --- Auth ---
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=False, allow_blank=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField(allow_blank=True)
