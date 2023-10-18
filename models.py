from django.db import models

class InsectCount(models.Model):
    acquisition_date = models.DateTimeField()
    insect_number = models.IntegerField()
    insect_area = models.FloatField(max_length=255)