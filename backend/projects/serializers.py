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