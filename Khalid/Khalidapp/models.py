from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm']:
            errors["password"] = "Password should match with confirm password"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        return errors
    
   

class tvShowsManager(models.Manager):   
    def basic_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors["title"] = "title should be at least 2 characters"
        if len(postData['network']) < 2:
            errors["network"] = "network should be at least 2 characters"
        if len(postData['desc']) < 3:
            errors["desc"] = "desc should be at least 8 characters"
        if len(postData['date']) == 0:
            errors["date"] = "date shouldnt be null characters"
        return errors  
    
class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
    password = models.CharField(max_length = 255)
    likeCount=models.IntegerField(default=0)
    likeFlag=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class TvShows(models.Model):
    title = models.CharField(max_length = 45)
    network = models.CharField(max_length = 45)
    date = models.DateTimeField()
    desc = models.CharField(max_length = 255)
    likeCount=models.IntegerField(default=0)
    likeFlag=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ManyToManyField(User, related_name="users")
    like = models.ForeignKey(User, related_name="likes", on_delete = models.CASCADE)
    objects = tvShowsManager()

class Likes(models.Model):
    likeCount=models.IntegerField(default=0)
    likeFlag=models.BooleanField(default=False)
    user = models.ManyToManyField(User, related_name="usersLikes")
    tvshow = models.ManyToManyField(TvShows, related_name="shows")

