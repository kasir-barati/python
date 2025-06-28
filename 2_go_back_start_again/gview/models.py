from django.db import models


# Create your models here.
class Apple(models.Model):
    color: str = models.CharField(max_length=6)
    pub_date = models.DateTimeField()

