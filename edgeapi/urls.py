from django.urls import path
from edgeapi import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register("posts", views.PostViewSetView, basename="posts"),
urlpatterns = [
                  path('users/account/sign-up', views.UserCreationView.as_view()),
                  path('users/account/sign-in', views.SignInView.as_view()),
                  path('users/account/profile', views.UserProfileView.as_view()),
                  path('accounts/token', obtain_auth_token)
              ] + router.urls
