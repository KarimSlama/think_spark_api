from django.db import models
from preferences.models import Preferences
from django.contrib.auth.models import User

class Idea(models.Model):
    title = models.CharField(max_length=100)
    categories = models.ManyToManyField(Preferences, related_name='categories')
    location = models.CharField(max_length=50)
  
    description = models.OneToOneField('IdeaDescription', on_delete=models.CASCADE, null=True, blank=True)
    requirements = models.OneToOneField('IdeaRequirement', on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    idea_images = models.ImageField(upload_to='idea_photos/', null=True, blank=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ideas')
    
    def __str__(self):
        return self.title[:40]

class IdeaDescription(models.Model):
    problems = models.CharField(max_length=700)
    solutions = models.CharField(max_length=700)
    why_it_works = models.CharField(max_length=700)
    benifits = models.CharField(max_length=700)

    def __str__(self):
        return self.problems[:50]


class IdeaRequirement(models.Model):
    technical = models.CharField(max_length=400)
    operational = models.CharField(max_length=400)
    team = models.CharField(max_length=400)
    expected_duration = models.CharField(max_length=50)

    def __str__(self):
        return self.technical[:50]