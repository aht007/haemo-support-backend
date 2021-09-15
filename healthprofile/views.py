"""
Health Profile View
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics

from healthprofile.serializers import (HealthProfileSerializer,
                                       IllnessSerializer)
from healthprofile.models import HealthProfile, Illness


class IsUserOwnerHealthProfile(permissions.BasePermission):
    """
    Check User Permission for current Object
    """

    def has_object_permission(self, request, view, health_profile_obj):
        return health_profile_obj.user_id.id == request.user.id


class HealthProfileView(generics.GenericAPIView):
    """
    View for Creating, Updating and Retrieving Heatlh profile
    """
    permission_classes = [
        IsUserOwnerHealthProfile
    ]

    def get(self, request):
        """
        Get requesting User's Heatlh Profile
        """
        user = request.user
        context = {'request': request}
        if hasattr(user, 'health_profile'):
            profile = user.health_profile
        else:
            profile = {}
        if hasattr(profile, 'illness'):
            illness = profile.illness.all()
        else:
            illness = []
        profile = HealthProfileSerializer(profile, context=context).data
        profile['illnesses'] = IllnessSerializer(
            illness, context=context, many=True).data
        return Response(
            profile
        )

    def post(self, request, *args, **kwargs):
        """
        Create Heatlh Profile for request User
        """
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

    def get_object(self, pk):
        """
        return heatlh profile for specified pk
        """
        return HealthProfile.objects.get(user_id=pk)

    def patch(self, request, pk):
        """
        Patch request to update Health profile
        """
        to_edit_instance = self.get_object(pk)
        self.check_object_permissions(self.request, to_edit_instance)
        serializer = HealthProfileSerializer(
            to_edit_instance, data=request.data, partial=True)
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
    """
    Check user authorization on illness object
    """

    def has_object_permission(self, request, view, illness_profile_obj):
        print(illness_profile_obj)
        return (illness_profile_obj.medical_profile_id
                .user_id.id == request.user.id)


class IllnessView(APIView):
    """
    Illness Views
    """
    permission_classes = [
        IsUserOwnerIllnessProfile
    ]

    def post(self, request, *args, **kwargs):
        """
        Add an Illness
        """
        context = {'request': request}
        serializer = IllnessSerializer(data=request.data, context=context)
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
            data='Wrong Parameters'
        )

    def get_object(self, pk):
        """
        Get Illness for speicifed Pk
        """
        return Illness.objects.get(pk=pk)

    def patch(self, request, pk):
        """
        Edit an Illness Object
        """
        toEditObj = self.get_object(pk)
        self.check_object_permissions(self.request, toEditObj)
        serializer = IllnessSerializer(
            toEditObj, data=request.data, partial=True)
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

    def delete(self, request, pk):
        """
        Delete An Illness Ojbect for Specified Pk
        """
        obj = Illness.objects.get(pk=pk)
        self.check_object_permissions(self.request, obj)
        profile = HealthProfile.objects.get(pk=obj.medical_profile_id.id)
        obj.delete()
        illness = profile.illness.all() or []
        profile = HealthProfileSerializer(profile, context=request).data
        profile['illnesses'] = IllnessSerializer(
            illness, context=request, many=True).data
        return Response(
            profile
        )
