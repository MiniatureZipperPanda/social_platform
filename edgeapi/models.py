from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pic", null=True)
    date_of_birth = models.DateField(null=True)
    bio = models.CharField(max_length=240, null=True)
    phone = models.CharField(max_length=15)


class Posts(models.Model):
    title = models.CharField(max_length=120)
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    post_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="posts", null=True)
    liked_by = models.ManyToManyField(User)

    def __str__(self):
        return self.title
