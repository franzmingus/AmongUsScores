from django.db import models
from datetime import datetime as dt

# Create your models here.


class CompetitionModel(models.Model):

    title = models.CharField(max_length=100)
    end_date = models.DateTimeField()
    json_raw_data = models.TextField(max_length=10000)
    json_results = models.TextField(max_length=10000, blank=True)
    new_player = models.CharField(max_length=100, blank=True)
    players = models.TextField(max_length=10000)

    def __str__(self):
        return str(self.title)