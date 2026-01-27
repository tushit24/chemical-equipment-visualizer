from rest_framework import serializers
from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            'id',
            'filename',
            'total_equipment',
            'average_flowrate',
            'average_pressure',
            'average_temperature',
            'type_distribution',
            'uploaded_at',
        ]
