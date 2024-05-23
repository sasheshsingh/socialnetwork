from django.db.models import Q
from rest_framework import generics, permissions, serializers
from rest_framework.views import APIView
from friends.models import FriendRequest, Friendship
from .serializers import (
    FriendsSerializer,
    FriendRequestROSerializer,
    FriendRequestReceivedSerializer,
    FriendRequestSerializer,
)
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status

from ..throttles import FriendRequestThrottle

User = get_user_model()


class FriendRequestReceivedListAPIView(generics.ListAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestReceivedSerializer

    def get_queryset(self):
        return self.queryset.filter(Q(to_user=self.request.user) & Q(status="pending"))


class FriendListAPIView(generics.ListAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendsSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)



class FriendRequestListCreateView(generics.ListCreateAPIView):
    queryset = FriendRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FriendRequestROSerializer
        return FriendRequestSerializer

    def get_throttles(self):
        if self.request.method == "POST":
            return [FriendRequestThrottle()]
        return []

    def perform_create(self, serializer):
        to_user = serializer.validated_data.get("to_user")
        if to_user == self.request.user:
            raise serializers.ValidationError(
                {"error": "Friend Request cannot be created with self."}
            )
        request_exists = (
            self.queryset.filter(to_user=to_user)
            .filter(from_user=self.request.user)
            .first()
        )
        if request_exists:
            raise serializers.ValidationError(
                {"error": "Friend Request already exists."}
            )
        serializer.save(from_user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(
            Q(from_user=self.request.user) & Q(status="pending")
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class AcceptFriendRequestView(APIView):
    def post(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk)
        except FriendRequest.DoesNotExist:
            return Response(
                {"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if friend_request.to_user == request.user:
            friend_request.status = "accepted"
            Friendship.objects.create(
                user=request.user, friend=friend_request.from_user
            )
            Friendship.objects.create(
                user=friend_request.from_user, friend=request.user
            )
            friend_request.save()
            return Response({"status": "accepted"})
        return Response(
            {"error": "You are not authorized to accept this friend request"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class RejectFriendRequestView(APIView):
    def post(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk)
        except FriendRequest.DoesNotExist:
            return Response(
                {"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if friend_request.to_user == request.user:
            friend_request.delete()
            return Response({"status": "rejected"})
        return Response(
            {"error": "You are not authorized to reject this friend request"},
            status=status.HTTP_400_BAD_REQUEST,
        )
