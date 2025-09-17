from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, UserProfile, Project, Milestone, Task, ProgressReport

class UserSerializer(serializers.ModelSerializer):
    model = User
    fileds = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fileds = ['user', 'skills', 'github_username', 'availability']

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ['id', 'title', 'due_date', 'order']

class TaskSerializer(serializers.ModelSerializer):
    milestone = MilestoneSerializer(read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'project', 'milestone', 'title', 'description', 'assignee', 
                  'status', 'story_points', 'created_at']

class ProjectSerializer(serializers.ModelSerializer):
    milestone = MilestoneSerializer(many=True, read_only=True)
    task = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'owner', 'is_ai_suggested', 'repo_url,'
        'created_at', 'milestones', 'tasks']
        read_only_fields = ['owner', 'created_at', 'milestones', 'tasks']

class ProgressReportSerializer(serializers.ModelSerializer):
    ai_feedback = serializers.JSONField(read_only=True)
    class Meta:
        model = ProgressReport
        fields = ['id', 'task', 'author', 'notes', 'created_at', 'ai_feedback']
        read_only_fields = ['author', 'created_at', 'ai_feedback']
