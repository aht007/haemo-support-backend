from django.urls import path

from .views import CsvParserView

urlpatterns = [
    path('parse-csv/', CsvParserView, name="parse_csv"),
]
