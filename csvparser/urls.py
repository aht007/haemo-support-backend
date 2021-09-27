from django.urls import path

from .views import CsvParserView

urlpatterns = [
    path('parse_csv/', CsvParserView.as_view(), name="parse_csv"),
]
