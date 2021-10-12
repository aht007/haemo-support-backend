"""
Views for CSV Parsing functionality
"""
# from rest_framework import generics, permissions
# from rest_framework.decorators import permission_classes
# from rest_framework.response import Response
# from rest_framework import status

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services import CsvParser
from django.views.decorators.csrf import csrf_exempt

from asgiref.sync import async_to_sync

# @permission_classes([permissions.IsAdminUser])
# class CsvParserView(generics.GenericAPIView):
#     """
#     Views for Csv Parsing
#     """

#     def post(self, request):
#         """
#         Actions for posting csv file for parsing
#         """
#         file = request.data.get('file', '')

#         if file != '':
#             csv_parser = CsvParser(file)
#             data = csv_parser.parse_file()
#             data_dict = {}
#             data_dict['data'] = data
#             data_dict['errors'] = csv_parser.error_messages
#             return Response(
#                 data_dict
#             )
#         else:
#             return Response(
#                 {"error": "You need to upload a CSV file"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )


@csrf_exempt
@require_POST
@async_to_sync
async def CsvParserView(request):
    if 'file' not in request.FILES:
        return JsonResponse({"error": "You need to upload a CSV file"},
                            status=400)
    file = request.FILES['file']
    csv_parser = CsvParser(file)
    data = csv_parser.parse_file()
    data_dict = {}
    data_dict['data'] = data
    data_dict['errors'] = csv_parser.error_messages
    return JsonResponse(
        data_dict
    )
