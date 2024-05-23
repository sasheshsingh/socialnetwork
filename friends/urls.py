from django.urls import path
from .api.views import (
    FriendRequestListCreateView,
    AcceptFriendRequestView,
    RejectFriendRequestView,
    FriendListAPIView,
    FriendRequestReceivedListAPIView,
)

urlpatterns = [
    path(
        "friend-requests", FriendRequestListCreateView.as_view(), name="friend-requests"
    ),
    path(
        "friend-requests/<int:pk>/accept",
        AcceptFriendRequestView.as_view(),
        name="accept-friend-request",
    ),
    path(
        "friend-requests/<int:pk>/reject",
        RejectFriendRequestView.as_view(),
        name="reject-friend-request",
    ),
    path("friend-list", FriendListAPIView.as_view(), name="friend-list"),
    path(
        "friend-requests-received",
        FriendRequestReceivedListAPIView.as_view(),
        name="friend-requests-received",
    ),
]
