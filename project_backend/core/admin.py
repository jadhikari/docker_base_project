from django.contrib import admin
from . import models
from django.contrib.auth import get_user_model


"""
Base admin class for models with a `user` field
"""
class BaseModelAdmin(admin.ModelAdmin):
    """Admin model that ensures the user field is correctly set."""

    def save_model(self, request, obj, form, change):
        """Assign the logged-in admin user when saving, even if the user is already set."""
        if request.user.is_authenticated:
            obj.user = request.user  # Always update the user to the current admin
        super().save_model(request, obj, form, change)

    list_filter = ('status', 'user', 'created_at', 'updated_at')  # Filter options
    search_fields = ('user__email',)  # Allow searching by user email


"""
Admin view for Power Plant Details
"""
@admin.register(models.PowerPlantDetail)
class PowerPlantDetailAdmin(BaseModelAdmin):
    list_display = ('system_name', 'system_id', 'group', 'country_name', 'latitude', 'longitude', 'azimuth', 'tilt', 'capacity_dc', 'status', 'created_at', 'updated_at', 'user')
    search_fields = ('system_name', 'system_id', 'country_name')


"""
Admin view for GIS Weather Data
"""
@admin.register(models.GisWeather)
class GisWeatherAdmin(BaseModelAdmin):  # Fixed duplicate class name
    list_display = ('power_plant', 'date', 'ghi', 'gti', 'pvout', 'status', 'created_at', 'updated_at', 'user')
    search_fields = ('power_plant__logger_name', 'date')


"""
Admin view for Logger Plant Groups
"""
@admin.register(models.LoggerPlantGroup)
class LoggerPlantGroupAdmin(BaseModelAdmin):
    list_display = ('group_name', 'status', 'created_at', 'updated_at', 'user')
    search_fields = ('group_name',)


"""
Admin view for Logger Categories
"""
@admin.register(models.LoggerCategory)
class LoggerCategoryAdmin(BaseModelAdmin):
    list_display = ('logger_name', 'group', 'alter_plant_id', 'status', 'created_at', 'updated_at', 'user')
    search_fields = ('logger_name', 'alter_plant_id')


"""
Admin view for Logger Power Generation
"""
@admin.register(models.LoggerPowerGen)
class LoggerPowerGenAdmin(BaseModelAdmin):
    list_display = ('logger_name', 'power_gen', 'date', 'status', 'created_at', 'updated_at', 'user')
    search_fields = ('logger_name__logger_name', 'date')


"""
Admin view for Curtailment Events
"""
@admin.register(models.CurtailmentEvent)
class CurtailmentEventAdmin(BaseModelAdmin):
    list_display = ('plant_id', 'date', 'start_time', 'end_time', 'rd', 'status', 'created_at', 'updated_at', 'user')
    search_fields = ('plant_id', 'rd')


"""
Admin view for Utility Plant ID
"""
@admin.register(models.UtilityPlantId)
class UtilityPlantIdAdmin(BaseModelAdmin):
    list_display = ('plant_id', 'group', 'status', 'created_at', 'updated_at', 'user')
    search_fields = ('plant_id',)


"""
Admin view for Utility Monthly Revenue
"""
@admin.register(models.UtilityMonthlyRevenue)
class UtilityMonthlyRevenueAdmin(BaseModelAdmin):
    list_display = ('plant_id', 'contract_id', 'start_date', 'end_date', 'power_capacity_kw', 'sales_days', 'sales_electricity_kwh', 'sales_amount_jpy', 'tax_jpy', 'average_daily_sales_kwh', 'rd', 'status', 'created_at', 'updated_at', 'user')
    search_fields = ('plant_id', 'contract_id')


"""
Admin view for Utility Monthly Expense
"""
@admin.register(models.UtilityMonthlyExpense)
class UtilityMonthlyExpenseAdmin(BaseModelAdmin):
    list_display = ('plant_id', 'used_electricity_kwh', 'used_amount_jpy', 'tax_jpy', 'rd', 'status', 'created_at', 'updated_at', 'user')
    search_fields = ('plant_id',)


"""
Admin view for Utility Daily Production
"""
@admin.register(models.UtilityDailyProduction)
class UtilityDailyProductionAdmin(BaseModelAdmin):
    list_display = ('plant_id', 'power_production_kwh', 'production_date', 'rd', 'status', 'created_at', 'updated_at', 'user')
    search_fields = ('plant_id', 'production_date')


"""
Admin view for Mail Notifications
"""
@admin.register(models.MailNotificatione)
class MailNotificationeAdmin(BaseModelAdmin):
    list_display = ('from_field', 'to', 'date', 'mail_date_time', 'subject', 'body', 'impact_category', 'memo', 'status', 'created_at', 'updated_at', 'user')
    search_fields = ('from_field', 'to', 'subject')

