import django_filters
from django_filters import DateFilter, CharFilter
from . import models
from django.utils.dateparse import parse_date
from datetime import timedelta


class LoggerPowerGenFilter(django_filters.FilterSet):
    year_month = django_filters.CharFilter(method='filter_by_year_month')
    year_month_date = django_filters.CharFilter(method='filter_by_year_month_date')
    logger_name = django_filters.CharFilter(method='filter_by_logger_names')

    class Meta:
        model = models.LoggerPowerGen
        fields = ['year_month', 'year_month_date', 'logger_name']

    def filter_by_year_month(self, queryset, name, value):
        """Filter queryset by year and month, returning data within the month."""
        try:
            year, month = map(int, value.split('-'))
            start_date = parse_date(f'{year}-{month:02d}-01')

            # Calculate the end date for the month
            next_month = start_date.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)

            return queryset.filter(date__range=[start_date, end_date])
        except ValueError:
            return queryset.none()

    def filter_by_year_month_date(self, queryset, name, value):
        """Filter queryset by exact date or entire month if only year and month are provided."""
        try:
            parts = value.split('-')
            year, month = int(parts[0]), int(parts[1])
            day = int(parts[2]) if len(parts) > 2 else None

            if day:
                start_date = parse_date(f'{year}-{month:02d}-{day:02d}')
                return queryset.filter(date=start_date)
            else:
                start_date = parse_date(f'{year}-{month:02d}-01')
                end_date = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

                return queryset.filter(date__range=[start_date, end_date])
        except (ValueError, TypeError):
            return queryset.none()

    def filter_by_logger_names(self, queryset, name, value):
        """Filter queryset by multiple logger names."""
        names = value.split(',')
        categories = models.LoggerCategory.objects.filter(logger_name__in=names)
        return queryset.filter(logger_name__in=categories)


class BaseUtilityFilter(django_filters.FilterSet):
    rd = django_filters.CharFilter(method='filter_by_year_month')
    plant_id = django_filters.CharFilter(method='filter_by_plant_id')
    group_name = django_filters.CharFilter(method='filter_by_group_name')

    class Meta:
        fields = ['rd', 'plant_id', 'group_name']

    def filter_by_year_month(self, queryset, name, value):
        """Filter queryset by year and month if format is `YYYY-MM`."""
        if len(value) == 7 and value.count('-') == 1:
            return queryset.filter(rd__startswith=value)
        return queryset.none()

    def filter_by_plant_id(self, queryset, name, value):
        """Filter queryset by plant IDs."""
        plant_ids = [plant_id.strip() for plant_id in value.split(',')]
        return queryset.filter(plant_id__plant_id__in=plant_ids)

    def filter_by_group_name(self, queryset, name, value):
        """Filter queryset by group name."""
        return queryset.filter(plant_id__group__group_name=value)


class UtilityMonthlyRevenueFilter(BaseUtilityFilter):
    class Meta(BaseUtilityFilter.Meta):
        model = models.UtilityMonthlyRevenue


class UtilityMonthlyExpenseFilter(BaseUtilityFilter):
    class Meta(BaseUtilityFilter.Meta):
        model = models.UtilityMonthlyExpense


class UtilityDailyProductionFilter(BaseUtilityFilter):
    class Meta(BaseUtilityFilter.Meta):
        model = models.UtilityDailyProduction


class CurtailmentEventFilter(BaseUtilityFilter):
    class Meta(BaseUtilityFilter.Meta):
        model = models.CurtailmentEvent


class LoggerCategoryFilter(django_filters.FilterSet):
    logger_name = django_filters.CharFilter(method='filter_by_logger_name')
    group_name = django_filters.CharFilter(method='filter_by_group_name')

    class Meta:
        model = models.LoggerCategory
        fields = ['logger_name', 'group_name']

    def filter_by_logger_name(self, queryset, name, value):
        """Filter LoggerCategory by logger names."""
        names = value.split(',')
        return queryset.filter(logger_name__in=names)

    def filter_by_group_name(self, queryset, name, value):
        """Filter LoggerCategory by group name."""
        return queryset.filter(group__group_name=value)


class UtilityPlantIdFilter(django_filters.FilterSet):
    plant_id = django_filters.CharFilter(method='filter_by_plant_id')
    group_name = django_filters.CharFilter(method='filter_by_group_name')

    class Meta:
        model = models.UtilityPlantId
        fields = ['plant_id', 'group_name']

    def filter_by_plant_id(self, queryset, name, value):
        """Filter by plant ID."""
        plant_ids = value.split(',')
        return queryset.filter(plant_id__in=plant_ids)

    def filter_by_group_name(self, queryset, name, value):
        """Filter by group name."""
        return queryset.filter(group__group_name=value)


class PowerPlantDetailFilter(django_filters.FilterSet):
    system_name = django_filters.CharFilter(method='filter_by_system_name')
    group_name = django_filters.CharFilter(method='filter_by_group_name')

    class Meta:
        model = models.PowerPlantDetail
        fields = ['system_name', 'group_name']

    def filter_by_system_name(self, queryset, name, value):
        """Filter PowerPlantDetail by system name."""
        names = value.split(',')
        return queryset.filter(system_name__in=names)

    def filter_by_group_name(self, queryset, name, value):
        """Filter PowerPlantDetail by group name."""
        return queryset.filter(group__group_name__icontains=value)


class GisWeatherFilter(django_filters.FilterSet):
    year_month = django_filters.CharFilter(method='filter_by_year_month')
    power_plant = django_filters.NumberFilter(field_name='power_plant', lookup_expr='exact')

    class Meta:
        model = models.GisWeather
        fields = ['year_month', 'power_plant']
    
    def filter_by_year_month(self, queryset, name, value):
        """Filter queryset by year and month, returning data within the month."""
        try:
            year, month = map(int, value.split('-'))
            start_date = parse_date(f'{year}-{month:02d}-01')

            # Calculate the end date for the month
            next_month = start_date.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)

            return queryset.filter(date__range=[start_date, end_date])
        except ValueError:
            return queryset.none()

"""
Filter for the mail notificatioin by using date(to and From) or impact_category
"""      
class MailNotificationeFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date", lookup_expr="gte", label="From Date")
    end_date = DateFilter(field_name="date", lookup_expr="lte", label="To Date")
    impact_category = CharFilter(field_name="impact_category", lookup_expr="icontains", label="Impact Category")

    class Meta:
        model = models.MailNotificatione
        fields = ['start_date', 'end_date', 'impact_category']
