"""
Creating the model to store the solar data.
"""
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

"""
Group for the Logger and Plantid
"""


class BaseModel(models.Model):
    status = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    class Meta:
        abstract = True  # This makes the model an abstract base class

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if the object is new
        super().save(*args, **kwargs)  # Save normally first

        if not is_new:  # Only update if the object already existed
            self.__class__.objects.filter(pk=self.pk).update(
                status=models.Case(
                    models.When(created_at=models.F('updated_at'), then=True),
                    default=False,
                    output_field=models.BooleanField()
                )
            )



class LoggerPlantGroup(BaseModel):
    group_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.group_name


"""
Power plan details 
"""
class PowerPlantDetail(BaseModel):
    RESOURCE_CHOICES = [
        ('Solar', 'Solar'),
        ('Biomass', 'Biomass'),
        ('Wind', 'Wind'),
    ]
    system_name = models.CharField(max_length=50)
    system_id = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=100)
    resource = models.CharField(max_length=100, choices=RESOURCE_CHOICES, default='Solar')
    country_name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=15, decimal_places=12)
    longitude = models.DecimalField(max_digits=15, decimal_places=12)
    altitude = models.DecimalField(max_digits=10, decimal_places=4)
    azimuth = models.DecimalField(max_digits=10, decimal_places=4)
    tilt = models.DecimalField(max_digits=10, decimal_places=4)
    capacity_dc = models.DecimalField(max_digits=10, decimal_places=2)
    capacity_ac = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(LoggerPlantGroup, on_delete=models.CASCADE, default=1)
    
    
    class Meta:
        # Define unique constraint based on plant_id, plant_name.
        unique_together = [('system_name', 'system_id','group')]

    def __str__(self):
        return f'{self.system_id} of {self.group}'
    

class GisWeather(BaseModel):
    # ForeignKey referencing the PowerPlantDetail model via its 'id'
    # Ensures that each GIS record is linked to a specific power plant.
    power_plant = models.ForeignKey(PowerPlantDetail, on_delete=models.CASCADE)
    ghi = models.DecimalField(max_digits=8, decimal_places=3)
    gti = models.DecimalField(max_digits=8, decimal_places=3)
    pvout = models.DecimalField(max_digits=8, decimal_places=3)
    date = models.DateField(null=True, blank=True)


    class Meta:
        unique_together = [('power_plant', 'date')]

    def __str__(self):
        return f'GIS data for {self.power_plant.system_id} on {self.date}'



"""
Solar power plan detsils
"""

class LoggerCategory(BaseModel):
    logger_name = models.CharField(max_length=100, unique=True)
    alter_plant_id = models.CharField(max_length=100, null=True, blank=True)
    group = models.ForeignKey(LoggerPlantGroup, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.logger_name


class LoggerPowerGen(BaseModel):
    logger_name = models.ForeignKey(LoggerCategory, on_delete=models.CASCADE)
    power_gen = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField(null=True, blank=True, default=date.today)

    class Meta:
        unique_together = [('logger_name', 'date')]


"""
Utility data Model are created below this
"""
class UtilityPlantId(BaseModel):
    plant_id = models.CharField(max_length=100, unique=True)
    alter_plant_id = models.CharField(max_length=100, null=True, blank=True)
    group = models.ForeignKey(LoggerPlantGroup, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.plant_id



class UtilityMonthlyRevenue(BaseModel):
    plant_id = models.ForeignKey(UtilityPlantId, on_delete=models.CASCADE)
    contract_id = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    power_capacity_kw = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, null=True)
    sales_days = models.IntegerField(blank=True, null=True)
    sales_electricity_kwh = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, null=True)
    sales_amount_jpy = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, null=True)
    tax_jpy = models.DecimalField(max_digits=10, decimal_places=2,
                                  blank=True, null=True)
    average_daily_sales_kwh = models.DecimalField(max_digits=10, decimal_places=2,
                                  blank=True, null=True)
    
    # Store year and month as a string in 'YYYY-MM' format
    rd = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        # Define unique constraint based on plant_id, period_year, and period_month
        unique_together = [('plant_id', 'contract_id', 'rd')]


class UtilityMonthlyExpense(BaseModel):
    plant_id = models.ForeignKey(UtilityPlantId, on_delete=models.CASCADE)
    used_electricity_kwh = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, null=True)
    used_amount_jpy = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, null=True)
    tax_jpy = models.DecimalField(max_digits=10, decimal_places=2,
                                  blank=True, null=True)
    # Store year and month as a string in 'YYYY-MM' format
    rd = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        # Define unique constraint based on plant_id, period_year, and period_month
        unique_together = [('plant_id', 'rd')]


class UtilityDailyProduction(BaseModel):
    plant_id = models.ForeignKey(UtilityPlantId, on_delete=models.CASCADE)
    power_production_kwh = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, null=True)
    production_date = models.DateField(null=True, blank=True)
    # Store year and month as a string in 'YYYY-MM' format
    rd = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        # Define unique constraint based on plant_id, period_year, and period_month
        unique_together = [('plant_id', 'production_date')]


# Curtailment model

class CurtailmentEvent(BaseModel):
    plant_id = models.ForeignKey(UtilityPlantId, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    # Store year and month as a string in 'YYYY-MM' format
    rd = models.CharField(max_length=7, blank=True, null=True)
   

    def __str__(self):
        return f"Curtailment Event for {self.plant_id.plant_id} on {self.date}"
    
    class Meta:
        # Define unique constraint based on plant_id and date
        unique_together = [('plant_id', 'date')]

    def clean(self):
        # Check if end_time is greater than start_time
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError({
                'end_time': _('End time must be later than start time.')
            })


class MailNotificatione(BaseModel):
    FROM_CHOICES = [
        ("Major", "Major"),
        ("Minor", "Minor"),
        ("None", "None"),
    ]

    from_field = models.TextField(verbose_name="From")
    to = models.TextField(verbose_name="To",null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    mail_date_time = models.TextField(verbose_name="Mail Date&Time",null=True, blank=True)
    subject = models.TextField(verbose_name="Subject",null=True, blank=True)
    body = models.TextField(verbose_name="Body",null=True, blank=True)
    impact_category = models.CharField(
        max_length=10, 
        choices=FROM_CHOICES, 
        default="-",
        blank=True, 
        verbose_name="Impact Category"
    )
    memo = models.TextField(verbose_name="Memo", blank=True, null=True)
    
    class Meta:
        unique_together = [( 'mail_date_time', 'body')]

    def __str__(self):
        return f"{self.subject} ({self.date})"
    