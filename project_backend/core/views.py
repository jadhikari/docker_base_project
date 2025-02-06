from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from . import models
from . import serializers
from . import filters

"""
This is for CSRF toke.
"""
# from django.http import JsonResponse
# from django.views.decorators.csrf import ensure_csrf_cookie
# from django.middleware.csrf import get_token


"""
This is for CSRF toke.
"""
# @method_decorator(ensure_csrf_cookie, name='dispatch')
class BaseViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """Base viewset for utility models."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Automatically set the user to the authenticated user."""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Automatically update the user during the update."""
        serializer.save(user=self.request.user)


class LoggerPlantGroupViewSet(BaseViewSet):
    """View for managing LoggerPlantGroup API"""
    serializer_class = serializers.LoggerPlantGroupSerializer
    queryset = models.LoggerPlantGroup.objects.all()
    filter_backends = (DjangoFilterBackend,)

class GisWeatherViewSet(BaseViewSet):
    """View for managing LoggerPlantGroup API"""
    serializer_class = serializers.GisWeatherSerializer
    queryset = models.GisWeather.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.GisWeatherFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        group_name = self.request.query_params.get('group_name', None)
        if group_name:
            # Apply custom filtering based on the group name
            categories = models.PowerPlantDetail.objects.filter(group__group_name=group_name)
            queryset = queryset.filter(power_plant__in=categories)  # Use the correct field here
        return queryset
    


class PowerPlantDetailViewSet(BaseViewSet):
    """View for managing PowerPlantDetail API"""
    serializer_class = serializers.PowerPlantDetailSerializer
    queryset = models.PowerPlantDetail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.PowerPlantDetailFilter


class LoggerCategoryViewSet(BaseViewSet):
    """View for managing LoggerCategory API"""
    serializer_class = serializers.LoggerCategorySerializer
    queryset = models.LoggerCategory.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.LoggerCategoryFilter


class LoggerPowerGenViewSet(BaseViewSet):
    """View for managing LoggerPowerGen API"""
    queryset = models.LoggerPowerGen.objects.all()
    serializer_class = serializers.LoggerPowerGenSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.LoggerPowerGenFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        group_name = self.request.query_params.get('group_name', None)
        if group_name:
            # Apply custom filtering based on the group name
            categories = models.LoggerCategory.objects.filter(group__group_name=group_name)
            queryset = queryset.filter(logger_name__in=categories)
        return queryset


class CurtailmentEventViewSet(BaseViewSet):
    """View for managing CurtailmentEvent API"""
    queryset = models.CurtailmentEvent.objects.all()
    serializer_class = serializers.CurtailmentEventSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.CurtailmentEventFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        group_name = self.request.query_params.get('group_name', None)
        if group_name:
            # Apply custom filtering based on the group name
            queryset = queryset.filter(plant_id__group__group_name=group_name)
        return queryset



class UtilityPlantIdViewSet(BaseViewSet):
    """View for managing UtilityPlantId API"""
    queryset = models.UtilityPlantId.objects.all()
    serializer_class = serializers.UtilityPlantIdSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.UtilityPlantIdFilter


class UtilityMonthlyRevenueViewSet(BaseViewSet):
    """View for managing UtilityMonthlyRevenue API"""
    queryset = models.UtilityMonthlyRevenue.objects.all()
    serializer_class = serializers.UtilityMonthlyRevenueSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.UtilityMonthlyRevenueFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        group_name = self.request.query_params.get('group_name', None)
        if group_name:
            # Apply custom filtering based on the group name
            queryset = queryset.filter(plant_id__group__group_name=group_name)
        return queryset


class UtilityMonthlyExpenseViewSet(BaseViewSet):
    """View for managing UtilitieMonthlyExpense API"""
    queryset = models.UtilityMonthlyExpense.objects.all()
    serializer_class = serializers.UtilityMonthlyExpenseSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.UtilityMonthlyExpenseFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        group_name = self.request.query_params.get('group_name', None)
        if group_name:
            # Apply custom filtering based on the group name
            queryset = queryset.filter(plant_id__group__group_name=group_name)
        return queryset


class UtilityDailyProductionViewSet(BaseViewSet):
    """View for managing UtilitieDailyProduction API"""
    queryset = models.UtilityDailyProduction.objects.all()
    serializer_class = serializers.UtilityDailyProductionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.UtilityDailyProductionFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        group_name = self.request.query_params.get('group_name', None)
        if group_name:
            # Apply custom filtering based on the group name
            queryset = queryset.filter(plant_id__group__group_name=group_name)
        return queryset


class PowerPlantDetailChoicesView(APIView):
    def get(self, request, *args, **kwargs):
        # Returning the RESOURCE_CHOICES as a dictionary
        resource_choices = dict(models.PowerPlantDetail.RESOURCE_CHOICES)
        return Response({"resource_choices": resource_choices}, status=status.HTTP_200_OK)




# @ensure_csrf_cookie
# def csrf_token_view(request):
#     """Returns the CSRF token for the client."""
#     return JsonResponse({'csrfToken': get_token(request)})


"""
View for mail notification
"""
class MailNotificationeViewSet(BaseViewSet):
    queryset = models.MailNotificatione.objects.all()
    serializer_class = serializers.MailNotificationeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.MailNotificationeFilter
