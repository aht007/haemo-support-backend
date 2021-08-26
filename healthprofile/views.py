from healthprofile.serializers import (HealthProfileSerializer,
                                       IllnessSerializer)
from healthprofile.models import HealthProfile, Illness
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics


class IsUserOwnerHealthProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, health_profile_obj):
        return (health_profile_obj.user_id.id == request.user.id)


class HealthProfileView(generics.GenericAPIView):
    permission_classes = [
        IsUserOwnerHealthProfile
    ]

    # to get Logged in User's Health profile
    def get(self, request, format=None):
        user = request.user
        context = {'request': request}
        if(hasattr(user, 'health_profile')):
            profile = user.health_profile
        else:
            profile = {}
        if(hasattr(profile, 'illness')):
            illness = profile.illness.all()
        else:
            illness = []
        profile = HealthProfileSerializer(profile, context=context).data
        profile['illnesses'] = IllnessSerializer(
            illness, context=context, many=True).data
        return Response(
            profile
        )

    # create a new health profile
    def post(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = HealthProfileSerializer(
            data=request.data, context=context)
        if serializer.is_valid():
            profile = serializer.save()
            illness = profile.illness.all() or []
            profile = HealthProfileSerializer(profile, context=context).data
            profile['illnesses'] = IllnessSerializer(
                illness, context=context, many=True).data
            return Response(
                profile
            )
        return Response(
            code=400, data='Wrong Parameters'
        )
    # get health profile object for a specific pk

    def get_object(self, pk):
        return HealthProfile.objects.get(user_id=pk)

    # edit health profile
    def patch(self, request, pk):
        object = self.get_object(pk)
        self.check_object_permissions(self.request, object)
        serializer = HealthProfileSerializer(
            object, data=request.data, partial=True)
        if serializer.is_valid():
            profile = serializer.save()
            illness = profile.illness.all() or []
            profile = HealthProfileSerializer(profile, context=request).data
            profile['illnesses'] = IllnessSerializer(
                illness, context=request, many=True).data
            return Response(
                profile
            )
        return Response(
            code=400, data='Wrong Parameters'
        )


class IsUserOwnerIllnessProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, illness_profile_obj):
        return (illness_profile_obj.medical_profile_id
                .user_id.id == request.user.id)


class IllnessView(APIView):
    permission_classes = [
       IsUserOwnerIllnessProfile
    ]

    # add a new illness
    def post(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = IllnessSerializer(data=request.data, context=context)
        if serializer.is_valid():
            data = serializer.save()
            profile = HealthProfile.objects.get(pk=data.medical_profile_id.id)
            self.check_object_permissions(self.request, profile)
            illness = profile.illness.all() or []
            profile = HealthProfileSerializer(profile, context=request).data
            profile['illnesses'] = IllnessSerializer(
                illness, context=request, many=True).data
            return Response(
                profile
            )
        return Response(
            data='Wrong Parameters'
        )

    # get illness for a specific primary key
    def get_object(self, pk):
        return Illness.objects.get(pk=pk)

    # edit an illness object
    def patch(self, request, pk):
        object = self.get_object(pk)
        self.check_object_permissions(self.request, object)
        serializer = IllnessSerializer(object, data=request.data, partial=True)
        if serializer.is_valid():
            data = serializer.save()
            profile = HealthProfile.objects.get(pk=data.medical_profile_id.id)
            illness = profile.illness.all() or []
            profile = HealthProfileSerializer(profile, context=request).data
            profile['illnesses'] = IllnessSerializer(
                illness, context=request, many=True).data
            return Response(
                profile
            )

        return Response(
            code=400, data='Wrong Parameters'
        )
    # delete an illness using primary key

    def delete(self, request, pk):
        obj = Illness.objects.get(pk=pk)
        self.check_object_permissions(self.request, object)
        profile = HealthProfile.objects.get(pk=obj.medical_profile_id.id)
        obj.delete()
        illness = profile.illness.all() or []
        profile = HealthProfileSerializer(profile, context=request).data
        profile['illnesses'] = IllnessSerializer(
            illness, context=request, many=True).data
        return Response(
            profile
        )
