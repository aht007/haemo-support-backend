from django.urls import path

from .views import Csv_Parser_View

urlpatterns = [
    path('parse/', Csv_Parser_View.as_view(), name="parse_csv"),
]
