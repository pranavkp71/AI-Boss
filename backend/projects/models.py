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

class Task(models.Model):
    STATUS_CHOICES = [('todo', 'To DO'), ('in_progress', 'In Progress'), ('done', 'Done')]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='task')
    milestone = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True, blank=True, related_name='task')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')  #User working on the task
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='todo')
    story_points = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

class ProgressReport(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='progress_report')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_report')
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ai_feedback = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Progress on {self.task.title} by {self.author.username}"



