from rest_framework import serializers
from django.contrib.auth.models import User
from edgeapi.models import Posts, UserProfile
from rest_framework.serializers import ModelSerializer


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class PostSerializers(ModelSerializer):
    user = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Posts
        exclude = ["liked_by"]

    def create(self, validated_data):
        user = self.context.get("user")
        return Posts.objects.create(**validated_data, user=user)


class UserProfileSerializer(ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["user", "profile_pic", "bio", "date_of_birth", "phone"]

    def create(self, validated_data):
        user = self.context.get('user')
        return UserProfile.objects.create(**validated_data, user=user)
