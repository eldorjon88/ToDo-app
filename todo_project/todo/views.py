# todo/views.py
from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrAdmin
from .filters import TaskFilter


class TaskViewSet(viewsets.ModelViewSet):
    """
    Task CRUD API.
    Staff foydalanuvchilar barcha tasklarni ko‘ra oladi,
    odatiy foydalanuvchi faqat o‘z tasklarini ko‘radi.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrAdmin]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "due_date", "priority"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.objects.all().order_by('-created_at')
        return Task.objects.filter(owner=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AdminStatsAPIView(APIView):
    """
    Admin uchun statistik ma'lumotlar API.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        total_tasks = Task.objects.count()
        done = Task.objects.filter(status="done").count()
        not_done = total_tasks - done
        by_status = Task.objects.values("status").annotate(count=Count("id"))

        return Response({
            "total_users": total_users,
            "total_tasks": total_tasks,
            "done_tasks": done,
            "not_done_tasks": not_done,
            "by_status": by_status,
        })
