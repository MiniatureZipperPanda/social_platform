from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from edgeapi.models import Posts, UserProfile, User
from rest_framework import authentication, permissions
from edgeapi.serializers import SignUpSerializer, LogInSerializer, PostSerializers, UserProfileSerializer


class UserCreationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            uname = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = authenticate(request, username=uname, password=password)
            if user:
                login(request, user)
                return Response({"msg": "Success"})
            else:
                return Response({"msg": "Invalid User"})


class PostViewSetView(ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model = Posts
    serializer_class = PostSerializers
    queryset = Posts.objects.all()

    def get_queryset(self):
        return Posts.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = PostSerializers(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UserProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_data = User.objects.get(id=request.user.id)
        user_profile_data = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile_data)
        udata = SignUpSerializer(user_data)
        a = serializer.data
        return Response(a)

    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
