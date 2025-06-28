from typing import Optional
from django.db import models
from django.db.models.indexes import Index
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Movie(models.Model):
    name: str = models.CharField(max_length=100, null=False)
    description: str = models.CharField(max_length=400, null=False)
    active: bool = models.BooleanField(default=True)
    file_name: str = models.CharField(max_length=255, null=False)
    mpd_file_absolute_path: str = models.CharField(max_length=500)
    class Meta:
        db_table: str = 'movies'
        indexes: Index = [
            models.Index(fields=['name'], name='movie_name_index')
        ]

    def __str__(self):
        return self.name