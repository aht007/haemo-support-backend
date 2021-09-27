"""
Views for CSV Parsing functionality
"""
from rest_framework import generics
from rest_framework.decorators import (authentication_classes,
                                       permission_classes)
from rest_framework.response import Response

from .services import CsvParser


@authentication_classes([])
@permission_classes([])
class Csv_Parser_View(generics.GenericAPIView):
    """
    Views for Csv Parsing
    """

    def post(self, request):
        """
        Actions for posting csv file for parsing
        """
        file = request.data.get('file', '')

        if file != '':
            csv_parser = CsvParser(file)
            data = csv_parser.parse_file()
            data_dict = {}
            data_dict['data'] = data
            data_dict['errors'] = csv_parser.error_messages
            return Response(
                data_dict
            )
        else:
            return Response(
                {}
            )
