from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    UserSearchSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSearchListAPIView(ListAPIView):
    queryset = User.objects.filter(user_type="user").order_by("first_name")
    serializer_class = UserSearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get("query", None)
        if query:
            self.queryset = self.queryset.filter(
                Q(email__icontains=query) | Q(name__icontains=query)
            )
        return self.queryset.exclude(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserView(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            usr_obj = User.objects.filter(email=email).first()
            if usr_obj:
                raise ValidationError({"error": "Email already registered"})
            serializer.save()
            return Response("User Created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)


class LoginView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
