from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    skills = models.TextField(blank=True)
    github_username = models.CharField(max_length=200, blank=True)
    availability = models.CharField(max_length=64, blank=True)  # Show if free/busy etc.

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_projects")
    created_at = models.DateTimeField(auto_now_add=True)
    is_ai_suggested = models.BooleanField(default=False)
    repo_url = models.URLField(blank=True, null=True)

class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestone')
    title = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)



