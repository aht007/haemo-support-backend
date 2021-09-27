"""
Views for CSV Parsing functionality
"""
from rest_framework import generics
from rest_framework.decorators import (authentication_classes,
                                       permission_classes)
from rest_framework.response import Response
from rest_framework import status

from .services import CsvParser


@authentication_classes([])
@permission_classes([])
class CsvParserView(generics.GenericAPIView):
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
                {}, status=status.HTTP_400_BAD_REQUEST
            )
