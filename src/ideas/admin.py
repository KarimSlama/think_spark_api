from django.contrib import admin

from ideas.models import Idea, IdeaDescription, IdeaRequirement

# Register your models here.

admin.site.register(Idea)
admin.site.register(IdeaDescription)
admin.site.register(IdeaRequirement)