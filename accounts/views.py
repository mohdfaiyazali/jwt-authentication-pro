from rest_framework import generics
from .models import User
from .serializers import (
    RegisterSerializer,
    LogoutSerializer,
    CustomTokenObtainPairSerializer
)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer


class LogoutView(generics.GenericAPIView):

    serializer_class = LogoutSerializer

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_205_RESET_CONTENT
        )


class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer