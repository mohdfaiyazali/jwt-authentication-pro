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
from .utils import send_verification_email
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .utils import email_verification_token
from .models import User

class VerifyEmailView(APIView):

    def get(self, request, user_id, token):

        user = get_object_or_404(
            User,
            id=user_id
        )

        if email_verification_token.check_token(
            user,
            token
        ):

            user.is_verified = True
            user.save()

            return Response(
                {"message": "Email verified successfully"}
            )

        return Response(
            {"message": "Invalid or expired token"},
            status=400
        )

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        send_verification_email(user)

        return Response(
            {
                "message": "Registration successful. Check your email for verification."
            },
            status=status.HTTP_201_CREATED
        )


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