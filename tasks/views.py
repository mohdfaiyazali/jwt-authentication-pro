from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUserRole, IsOwnerOrAdmin

from .models import Task
from .serializers import TaskSerializer

from .permissions import IsAdminUserRole


class TaskListCreateView(generics.ListCreateAPIView):

    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)


class AdminTaskListView(generics.ListAPIView):

    queryset = Task.objects.all()

    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated, IsAdminUserRole]


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Task.objects.all()

    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]