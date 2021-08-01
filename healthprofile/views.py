from healthprofile.serializers import HealthProfileSerializer, IllnessSerializer
from healthprofile.models import HealthProfile, Illness
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class GetHealthProfile(APIView):
    # to modify later
    def get(self, request, format=None):
        user = request.user
        context = {'request': request} 
        profile = user.health_profile or {}
        illness = profile.illness.all() or []
        return Response({
            'profile': HealthProfileSerializer(profile, context=context).data,
            'illnesses': IllnessSerializer(illness, context=context, many=True).data
        })

class CreateHealthProfile(APIView):

    def post(self, request, *args, **kwargs):
        context = {'request': request} 
        serializer = HealthProfileSerializer(data=request.data, context=context)
        if serializer.is_valid():
            profile = serializer.save()
            return Response({
                "healthProfile": HealthProfileSerializer(profile, context=context).data
            })
        return Response(
            code=400, data='Wrong Parameters'
        )        

class EditHealthProfile(APIView):
    def get_object(self, pk):
        return HealthProfile.objects.get(user_id=pk)

    def patch(self, request, pk):
        object = self.get_object(pk)
        serializer = HealthProfileSerializer(object, data=request.data, partial=True)
        if serializer.is_valid():
            data = serializer.save()
            return Response({
                "healthProfile": HealthProfileSerializer(data, context= request).data
            })
        return Response(
            code=400, data='Wrong Parameters'
        )

class AddIllnes(APIView):
    pass

class EditIllness(APIView):
    pass

class RemoveIllness(APIView):
    pass

# class GetAllIllness(APIView):
#     pass