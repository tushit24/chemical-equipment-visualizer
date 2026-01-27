import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView

from .models import Dataset
from .serializers import DatasetSerializer


class CSVUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "CSV file is required"}, status=400)

        try:
            df = pd.read_csv(file)
        except Exception:
            return Response({"error": "Invalid CSV file"}, status=400)

        summary = {
            "total_equipment": len(df),
            "average_flowrate": round(df['Flowrate'].mean(), 2),
            "average_pressure": round(df['Pressure'].mean(), 2),
            "average_temperature": round(df['Temperature'].mean(), 2),
            "equipment_type_distribution": df['Type'].value_counts().to_dict()
        }

        # Save to DB
        Dataset.objects.create(
            filename=file.name,
            total_equipment=summary["total_equipment"],
            average_flowrate=summary["average_flowrate"],
            average_pressure=summary["average_pressure"],
            average_temperature=summary["average_temperature"],
            type_distribution=summary["equipment_type_distribution"]
        )

        return Response(summary)

class DatasetHistoryView(ListAPIView):
    queryset = Dataset.objects.order_by('-uploaded_at')[:5]
    serializer_class = DatasetSerializer
