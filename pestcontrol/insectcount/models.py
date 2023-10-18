
from django.db import models

class InsectCount(models.Model):
    acquisition_date = models.DateTimeField()
    insect_quantity = models.IntegerField()
    insect_area = models.FloatField(max_length=255)
    field_name = models.CharField(max_length=255)
    trap_id = models.IntegerField()