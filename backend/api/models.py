from django.db import models


class Dataset(models.Model):
    filename = models.CharField(max_length=255)
    total_equipment = models.IntegerField()
    average_flowrate = models.FloatField()
    average_pressure = models.FloatField()
    average_temperature = models.FloatField()
    type_distribution = models.JSONField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
