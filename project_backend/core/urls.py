from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Initialize DefaultRouter
router = DefaultRouter()

# Register ViewSets with the router
router.register(r'power-plant-detail', views.PowerPlantDetailViewSet, basename='power-plant-detail')
router.register(r'gis-weather-data', views.GisWeatherViewSet, basename='gis-weather-data')


router.register(r'logger-power-gen', views.LoggerPowerGenViewSet, basename='logger-power-gen')
router.register(r'loggercategories', views.LoggerCategoryViewSet, basename='loggercategories')
router.register(r'curtailment-event', views.CurtailmentEventViewSet, basename='curtailment-event')

#loggers-plants-group Viewsets
router.register(r'loggers-plants-group', views.LoggerPlantGroupViewSet, basename='loggers-plants-group')

# Utility-related ViewSets
router.register(r'utility-monthly-revenue', views.UtilityMonthlyRevenueViewSet, basename='utility-monthly-revenue')
router.register(r'utility-monthly-expense', views.UtilityMonthlyExpenseViewSet, basename='utility-monthly-expense')
router.register(r'utility-daily-production', views.UtilityDailyProductionViewSet, basename='utility-daily-production')
router.register(r'utility-plants-list', views.UtilityPlantIdViewSet, basename='utility-plants-list')

router.register(r'mail-notifications', views.MailNotificationeViewSet, basename='mail-notification')


# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Register all ViewSet URLs
    path('power-plant-resource-choices/', views.PowerPlantDetailChoicesView.as_view(), name='PowerPlantDetailChoicesView'), 
    #path('csrf-token-endpoint/', views.csrf_token_view, name='csrf_token'),  # CSRF token endpoint
]
