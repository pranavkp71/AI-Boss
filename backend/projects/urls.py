from rest_framework import routers
from .views import ProjectViewSet, TaskViewSet, ProgressReportViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('tasks', TaskViewSet, basename='tast')
router.register('progress', ProgressReportViewSet, basename='progress')

urlpatterns = [
    path('', include(router.urls)),
]