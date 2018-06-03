from django.db import models

PULSE_TYPES =  (
    ('primitive', 'primitive'),
    ('corpse', 'corpse'),
    ('gaussian', 'gaussian'),
    ('cinbb', 'cinbb'),
    ('cinsk', 'cinsk'),
)

# Create your models here.
class Pulse(models.Model):
    name = models.CharField(db_index=True, max_length=255, blank=False)
    maximum_rabi_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    polar_angle = models.DecimalField(max_digits=2, decimal_places=1, blank=False)
    pulse_type = models.CharField(max_length=9, choices=PULSE_TYPES, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    