from django.db import models
import re
class UserManager(models.Manager):
    def create_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 5:
            errors['first_name'] = "Name should be at least 5 characters."
        if len(postData['last_name']) < 5:
            errors['last_name'] = "Name should be at least 5 characters."
        if len(postData['email']) < 8:
            errors['email'] = "Email needs to be longer."
        if len(postData['password']) <8:
            errors['password'] = "Password must be at least be atleast 8 characters."
        if postData['password'] != postData['confirm_pw']:
            errors['password_conf'] = "Password and confirm password need to match."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email address."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = 255)
    updated_at = models.DateTimeField(auto_now_add = 255)
    objects = UserManager()

class Veggie(models.Model):
    kind = models.CharField(max_length = 255)
    user_uploader = models.ForeignKey(User, related_name = 'user_veggie', on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = 'user_likes')
    created_at = models.DateTimeField(auto_now_add = 255)
    updated_at = models.DateTimeField(auto_now_add = 255)