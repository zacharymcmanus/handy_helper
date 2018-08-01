from __future__ import unicode_literals
from django.db import models
import re
import bcrypt 
from datetime import date, datetime
from time import strptime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def user_val(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = 'You must enter a first name!'
        if len(postData['last_name']) < 2:
            errors["last_name"] = 'You must enter a last name!'
        if len(postData['email']) < 1:
            errors["email"] = 'You must enter an email!'
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = 'You must use proper email syntax!'
        if len(User.objects.filter(email = postData['email'])):
            errors["email"] = 'Email already exists'
        if len(postData['password']) < 8:
            errors["password"] = 'Your password must be at least 8 characters!'
        if postData['password_conf'] != postData['password']:
            errors["password_conf"] = 'Your passwords must match!'
        return errors

    def login_val(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors["first_name"] = 'You must enter an email!'
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = 'You must use proper email syntax!'
        if len(User.objects.filter(email = postData['email'])):
            errors["email"] = 'Email already exists'        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class JobManager(models.Manager):
    def job_val(self, postData):
        errors = {}
        if len(postData['job_name']) < 3:
            errors["job_name"] = 'Job name must be more than 3 characters!'
        if len(postData['job_description']) < 10:
            errors["job_description"] = 'Your job description must be at least 10 characters!'
        if len(postData['job_location']) < 0:
            errors["job_location"] = 'You must enter a job location!'
        return errors

class Job(models.Model):
    job_name = models.CharField(max_length=255)
    job_description = models.CharField(max_length=255)
    job_location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    creator = models.ForeignKey(User, related_name="planner")
    join = models.ManyToManyField(User, related_name="joiner")
    objects = JobManager()



