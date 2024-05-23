from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "is_active", "is_staff", "is_superuser", "id"]


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "is_active", "is_staff", "is_superuser"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = ["password", "email", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
            email=validated_data["email"],
            username=validated_data["email"],
            user_type="user",
            name=validated_data["first_name"] + " " + validated_data["last_name"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get("email")
        password = data.get("password")

        if username and password:
            user = authenticate(email=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is disabled.")
                refresh = RefreshToken.for_user(user)
                return {
                    "username": user.username,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            else:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError('Must include "email" and "password".')
