from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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

        token = super().get_token(user)

        # Custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role

        return token