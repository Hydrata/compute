from django.db import models


class Compute(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
