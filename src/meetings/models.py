from django.db import models
from django.contrib.auth import get_user_model
from ideas.models import Idea

User = get_user_model()

class Meeting(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='meetings')
    investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scheduled_meetings')
    scheduled_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Meeting with {self.idea.user} by {self.investor} at {self.scheduled_datetime}'
