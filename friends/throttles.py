from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle


class FriendRequestThrottle(UserRateThrottle):
    scope = 'friend_request'
