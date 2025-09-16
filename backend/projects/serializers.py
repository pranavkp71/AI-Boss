from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, UserProfile, Project, Milestone, Task, ProgressReport

class UserSerializers(serializers.ModelSerializer):
    model = User
    fileds = ['id', 'username', 'email']