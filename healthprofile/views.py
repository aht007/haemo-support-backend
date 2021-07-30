from healthprofile.serializers import HealthProfileSerializer
from healthprofile.models import Illness
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class GetHealthProfile(APIView):
    # to modify later
    def get(self, request, format=None):
        user = request.user
        profile = user.health_profile
        illness = profile.illness.all()
        print(illness)

class CreateHealthProfile(APIView):

    def post(self, request, *args, **kwargs):
        context = {'request': request} 
        serialaizer = HealthProfileSerializer(data=request.data, context=context)
        serialaizer.is_valid(raise_exception=True)
        profile = serialaizer.save()
        return Response({
            "healthProfile": HealthProfileSerializer(profile, context=self.get_serializer_context()).data
        })

class EditHealthProfile(APIView):
    pass

class AddIllnes(APIView):
    pass

class EditIllness(APIView):
    pass

class RemoveIllness(APIView):
    pass

# class GetAllIllness(APIView):
#     pass