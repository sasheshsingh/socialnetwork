from rest_framework import serializers
from friends.models import FriendRequest, Friendship
from users.api.serializers import UserSerializer


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ["id", "to_user", "status", "created_at"]


class FriendsSerializer(serializers.ModelSerializer):
    friend = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ["id", "friend", "created_at"]


class FriendRequestROSerializer(serializers.ModelSerializer):
    to_user = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ["id", "to_user", "status", "created_at"]


class FriendRequestReceivedSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ["id", "from_user", "status", "created_at"]
