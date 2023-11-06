from django.db import models

# Create your models here.
class Ems(models.Model):
    voltage_R = models.IntegerField()
    voltage_S = models.IntegerField()
    voltage_T = models.IntegerField()
    current_R = models.IntegerField()
    current_S = models.IntegerField()
    current_T = models.IntegerField()
    active_power = models.IntegerField()
    frequency = models.IntegerField()
    accumulate_energy = models.DecimalField(max_digits=20, decimal_places=2)
    save_date = models.DateTimeField()
    
    
class Battery(models.Model):
    DCvoltage_R = models.IntegerField()
    DCvoltage_S = models.IntegerField()
    DCvoltage_T = models.IntegerField()
    DCcurrent_R = models.IntegerField()
    DCcurrent_S = models.IntegerField()
    DCcurrent_T = models.IntegerField()
    active_power = models.IntegerField()
    SOC = models.IntegerField() # State of Charge
    SOH = models.IntegerField() # State of Health
    save_date = models.DateTimeField(auto_now=True)
    
class Photovoltaics(models.Model):
    active_power = models.IntegerField()
    save_date = models.DateTimeField(auto_now=True)