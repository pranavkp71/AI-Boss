from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project, Task, ProgressReport
from .serializers import ProgressReportSerializer, TaskSerializer, ProjectSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.id
        title = data.get('title') or 'AI Generated Project'
        description = data.get('description', '')
        is_ai_suggested = data.get('suggest', False)

        project = Project.objects.create(title=title, description=description, owner=request.user, is_ai_suggested=is_ai_suggested)

        # Mock AI
        Task.objects.create(project=project, title="Serup project structure", description="Initialize repo and basic structure")
        Task.objects.create(project=project, title="Create models", description="Implement Project, Task, ProgressReport models")
        Task.objects.create(project=project, title="Integrate AI review", description="Create endpoint for progress review")
        serializer = ProjectSerializer(project, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user) | Task.objects.filter(assignee=self.request.user)
    
    @action(detail=True, methods=['post'])
    def submit_progress(self, request, pk=None):
        task = self.get_object()
        notes = request.data.get('notes', '')
        report = ProgressReport.objects.create(task=task, author=request.author, notes=notes)

        # Mock AI review
        feedback = {
            "status": "partial" if len(notes) < 50 else "passed",
            "comments": "Looks good. Add unit tests."if len(notes) >= 50 else "Please give more details and link code/PR."
        }
        report.ai_feedback = feedback
        report.save()
        serializer = ProgressReportSerializer(report, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
