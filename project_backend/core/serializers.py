from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model


class BaseModelSerializer(serializers.ModelSerializer):
    """Base serializer that handles automatic user assignment."""

    def save(self, **kwargs):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            kwargs['user'] = request.user if request.user.is_authenticated else get_user_model().objects.filter(id=1).first()
        return super().save(**kwargs)



"""
serializers for PowerPlantDetail
"""
class PowerPlantDetailSerializer(BaseModelSerializer):
    """Serializer for PowerPlantDetail."""
    RESOURCE_CHOICES = models.PowerPlantDetail.RESOURCE_CHOICES
    user = serializers.StringRelatedField()
    group_name = serializers.CharField(source='group.group_name',read_only=True)

    class Meta:
        model = models.PowerPlantDetail
        fields = '__all__'
        read_only_fields = ['user', 'group_name']

    # Add a custom field to expose the choices
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['resource_choices'] = dict(self.RESOURCE_CHOICES)
        return representation


"""
serializers for gis weather
"""
class GisWeatherSerializer(BaseModelSerializer):
    """Serializer for PowerPlantDetail."""
    user = serializers.StringRelatedField()
    power_plant_id = serializers.PrimaryKeyRelatedField(
        queryset=models.PowerPlantDetail.objects.all(),
        source='power_plant',  # Maps to the power_plant field in the model
        write_only=True,       # Used for input (when pushing data)
    )
    power_plant_name = serializers.StringRelatedField(
        source='power_plant',  # Uses the string representation for output
        read_only=True         # Used for output (response only)
    )

    class Meta:
        model = models.GisWeather
        fields = ['user', 'power_plant_id', 'power_plant_name', 'ghi', 'gti', 'pvout', 'date']
        read_only_fields = ['user', 'power_plant_name']



"""
serializers for logger and plant group
"""
class LoggerPlantGroupSerializer(BaseModelSerializer):
    """Serializer for PowerPlantDetail."""
    user = serializers.StringRelatedField()

    class Meta:
        model = models.LoggerPlantGroup
        fields = '__all__'
        read_only_fields = ['id']


"""
serializers for solar power plan
"""

class LoggerCategorySerializer(BaseModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=models.LoggerPlantGroup.objects.all())
    status = serializers.BooleanField()
    user = serializers.StringRelatedField()

    class Meta:
        model = models.LoggerCategory
        fields = '__all__'
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        group = validated_data.get('group', None)
        if group:
            instance.group = group  # Correctly assign the foreign key ID

        # Update other fields if provided
        instance.logger_name = validated_data.get('logger_name', instance.logger_name)
        instance.alter_plant_id = validated_data.get('alter_plant_id', instance.alter_plant_id)
        instance.status = validated_data.get('status', instance.status)
        instance.user = validated_data.get('user', instance.user)

        # Save the instance with updated data
        instance.save()
        return instance


class LoggerPowerGenSerializer(BaseModelSerializer):
    """Serializer for LoggerPowerGen."""
    logger_name = serializers.CharField(source='logger_name.logger_name')  # Use the logger_name field from LoggerCategory
    user = serializers.StringRelatedField()

    class Meta:
        model = models.LoggerPowerGen
        fields = ['id', 'logger_name', 'power_gen', 'date', 'status', 'created_at', 'updated_at', 'user']
        read_only_fields = ['id']

    def create(self, validated_data):
        logger_name_data = validated_data.pop('logger_name')
        logger_name, created = models.LoggerCategory.objects.get_or_create(logger_name=logger_name_data['logger_name'])
        validated_data['logger_name'] = logger_name
        return models.LoggerPowerGen.objects.create(**validated_data)


class CurtailmentEventSerializer(BaseModelSerializer):
    """Serializer for CurtailmentEvent."""
    plant_id = serializers.CharField(source='plant_id.plant_id')
    user = serializers.StringRelatedField()

    class Meta:
        model = models.CurtailmentEvent
        fields = [
            'id', 'plant_id', 'date', 'start_time', 'end_time',
            'rd', 'status', 'user', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        # Extract plant_id data and get or create the corresponding UtilityPlantId instance
        plant_id_data = validated_data.pop('plant_id')
        plant_id, created = models.UtilityPlantId.objects.get_or_create(plant_id=plant_id_data['plant_id'])
        validated_data['plant_id'] = plant_id
        
        # Create and return a CurtailmentEvent instance instead of UtilityMonthlyRevenue
        return models.CurtailmentEvent.objects.create(**validated_data)


"""
serializers for Utilitie
"""
class UtilityPlantIdSerializer(BaseModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=models.LoggerPlantGroup.objects.all())  # Display group name
    user = serializers.StringRelatedField()

    class Meta:
        model = models.UtilityPlantId
        fields = '__all__'
        read_only_fields = ['id']
    
    def update(self, instance, validated_data):
        group = validated_data.get('group', None)
        if group:
            instance.group = group  # Correctly assign the foreign key ID

        # Update other fields if provided
        instance.plant_id = validated_data.get('logger_name', instance.plant_id)
        instance.alter_plant_id = validated_data.get('alter_plant_id', instance.alter_plant_id)
        instance.user = validated_data.get('user', instance.user)

        # Save the instance with updated data
        instance.save()
        return instance


class UtilityMonthlyRevenueSerializer(BaseModelSerializer):
    """Serializer for UtilityMonthlyRevenue."""
    plant_id = serializers.CharField(source='plant_id.plant_id')
    user = serializers.StringRelatedField()

    class Meta:
        model = models.UtilityMonthlyRevenue
        fields = [
            'id', 'plant_id', 'contract_id', 'start_date', 'end_date',
            'power_capacity_kw', 'sales_days', 'sales_electricity_kwh',
            'sales_amount_jpy', 'tax_jpy', 'average_daily_sales_kwh', 'rd', 'status',
            'user', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        plant_id_data = validated_data.pop('plant_id')
        plant_id, created = models.UtilityPlantId.objects.get_or_create(plant_id=plant_id_data['plant_id'])
        validated_data['plant_id'] = plant_id
        return models.UtilityMonthlyRevenue.objects.create(**validated_data)


class UtilityMonthlyExpenseSerializer(BaseModelSerializer):
    """Serializer for UtilityMonthlyExpense."""
    plant_id = serializers.CharField(source='plant_id.plant_id')
    user = serializers.StringRelatedField()

    class Meta:
        model = models.UtilityMonthlyExpense
        fields = [
            'id', 'plant_id', 'used_electricity_kwh', 'used_amount_jpy', 'tax_jpy',
            'rd', 'status', 'user', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        plant_id_data = validated_data.pop('plant_id')
        plant_id, created = models.UtilityPlantId.objects.get_or_create(plant_id=plant_id_data['plant_id'])
        validated_data['plant_id'] = plant_id
        return models.UtilityMonthlyExpense.objects.create(**validated_data)


class UtilityDailyProductionSerializer(BaseModelSerializer):
    """Serializer for UtilityDailyProduction."""
    plant_id = serializers.CharField(source='plant_id.plant_id')
    user = serializers.StringRelatedField()

    class Meta:
        model = models.UtilityDailyProduction
        fields = [
            'id', 'plant_id', 'power_production_kwh', 'production_date',
            'rd', 'status', 'user', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        plant_id_data = validated_data.pop('plant_id')
        plant_id, created = models.UtilityPlantId.objects.get_or_create(plant_id=plant_id_data['plant_id'])
        validated_data['plant_id'] = plant_id
        return models.UtilityDailyProduction.objects.create(**validated_data)


""""
Serializer for mail notification.
"""
class MailNotificationeSerializer(BaseModelSerializer):
    class Meta:
        model = models.MailNotificatione
        fields = '__all__'
