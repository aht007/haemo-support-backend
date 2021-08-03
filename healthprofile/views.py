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
        profile = HealthProfileSerializer(profile, context=context).data
        profile['illnesses'] = IllnessSerializer(illness, context=context, many=True).data
        return Response(
            profile
        )

class CreateHealthProfile(APIView):

    def post(self, request, *args, **kwargs):
        context = {'request': request} 
        serializer = HealthProfileSerializer(data=request.data, context=context)
        if serializer.is_valid():
            profile = serializer.save()
            illness = profile.illness.all() or []
            profile = HealthProfileSerializer(profile, context=context).data
            profile['illnesses'] = IllnessSerializer(illness, context=context, many=True).data
            return Response(
                profile
            )
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
            profile = serializer.save()
            illness = profile.illness.all() or []
            profile = HealthProfileSerializer(profile, context=request).data
            profile['illnesses'] = IllnessSerializer(illness, context=request, many=True).data
            return Response(
                profile
            )
        return Response(
            code=400, data='Wrong Parameters'
        )

class AddIllnes(APIView):
    def post(self, request, *args, **kwargs):
        context = {'request': request} 
        serializer = IllnessSerializer(data=request.data, context=context)
        if serializer.is_valid():
            data = serializer.save()
            profile = HealthProfile.objects.get(pk=data.medical_profile_id.id)
            illness = profile.illness.all() or []
            profile = HealthProfileSerializer(profile, context=request).data
            profile['illnesses'] = IllnessSerializer(illness, context=request, many=True).data
            return Response(
                profile
            )
        return Response(
            code=400, data='Wrong Parameters'
        )        

class EditIllness(APIView):
    def get_object(self, pk):
        return Illness.objects.get(pk=pk)

    def patch(self, request, pk):
        object = self.get_object(pk)
        serializer = IllnessSerializer(object, data = request.data, partial=True)
        if serializer.is_valid():
            data = serializer.save()
            profile = HealthProfile.objects.get(pk=data.medical_profile_id.id)
            illness = profile.illness.all() or []
            profile = HealthProfileSerializer(profile, context=request).data
            profile['illnesses'] = IllnessSerializer(illness, context=request, many=True).data
            return Response(
                profile
            )

        return Response(
            code=400, data='Wrong Parameters'
        )

class RemoveIllness(APIView):
    def delete(self, request, pk):
        obj = Illness.objects.get(pk=pk)
        profile = HealthProfile.objects.get(pk=obj.medical_profile_id.id)
        obj.delete()
        illness = profile.illness.all() or []
        profile = HealthProfileSerializer(profile, context=request).data
        profile['illnesses'] = IllnessSerializer(illness, context=request, many=True).data
        return Response(
            profile
        )




# class GetAllIllness(APIView):
#     pass