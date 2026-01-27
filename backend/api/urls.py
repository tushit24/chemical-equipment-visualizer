from django.urls import path
from .views import (
    CSVUploadView,
    DatasetHistoryView,
    DatasetPDFView,
)

urlpatterns = [
    path("upload/", CSVUploadView.as_view(), name="csv-upload"),
    path("history/", DatasetHistoryView.as_view(), name="dataset-history"),
    path("pdf/<int:pk>/", DatasetPDFView.as_view(), name="dataset-pdf"),
]
