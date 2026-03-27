from rest_framework import serializers

class SampleResultSerializer(serializers.Serializer):
    run_id = serializers.CharField(max_length=50, required=False)
    dummy_val = serializers.CharField(required=False, allow_blank=True)
