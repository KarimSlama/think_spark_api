from django.db import models
from preferences.models import Preferences

class Idea(models.Model):
    title = models.CharField(max_length=100)
    categories = models.ManyToManyField(Preferences, related_name='categories')
    publisher = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    problems = models.CharField(max_length=400)
    solutions = models.CharField(max_length=400)
    why_it_works = models.CharField(max_length=700)
    benifits = models.CharField(max_length=400)
    image = models.ImageField(upload_to='idea_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    
