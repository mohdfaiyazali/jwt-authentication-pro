from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password


class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):

    uid = serializers.IntegerField()

    token = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )

    password2 = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        if attrs["password"] != attrs["password2"]:

            raise serializers.ValidationError(
                "Passwords do not match."
            )

        validate_password(attrs["password"])

        return attrs

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )

        return user


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def validate(self, attrs):

        self.token = attrs['refresh']

        return attrs

    def save(self, **kwargs):

        try:

            token = RefreshToken(self.token)

            token.blacklist()

        except Exception:
            self.fail('bad_token')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        if not user.is_verified:
            raise serializers.ValidationError(
                "Email not verified."
            )

        token = super().get_token(user)

        # Custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role

        return token