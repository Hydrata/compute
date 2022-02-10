from rest_framework import serializers

from compute_anuga.models import Compute


class ComputeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Compute
        fields = '__all__'
