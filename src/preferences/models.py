from django.db import models

class Preferences(models.Model):

    TYPE_CHOICES = (
        ('category', 'Category'),
        ('filter', 'Filter'),
        ('location', 'Location'),
    )

    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    def __str__(self):
        return self.name
