from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, post_data):
        email_users = User.objects.filter(email=post_data['email'])
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Email address is not a valid format."
        if User.objects.filter(email = post_data['email']).exists():
            errors['emailexists'] = "Email already exists."
        if len(post_data['password']) < 8:
            errors["password"] = "Password must be at least 8 characters."
        if post_data['password'] != post_data['password_confirm']:
            errors['passwordmatching'] = 'Your passwords do not match'
        return errors
    def login_validator(self, post_data):
        errors = {}
        user_email = post_data['email']
        user = User.objects.filter(email=user_email)
        print(user)
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid login credentials."
        if len(user)<1:
            errors['email'] = "Invalid login credentials."
        if not bcrypt.checkpw(post_data['password'].encode(), user[0].password.encode()):
            errors['password'] = "Invalid login credentials."
        return errors

class User(models.Model):
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
        
    def __str__(self):
        return str(self.id)

class QuoteManager(models.Manager):
    def quote_validator(self, post_data):
        errors = {}
        quotedby = post_data['quotedby']
        if len(post_data['quotedby']) < 2:
            errors['quotelength'] = "Quote must be longer than 2 characters."
        if len(post_data['quotedescription']) < 10:
            errors['descriptionlength'] = "Description must be longer than 10 characters."
        return errors

class Quote(models.Model):
    quotedby = models.CharField(max_length=64)
    quotedescription = models.CharField(max_length=264)
    submitter = models.ForeignKey(User, related_name="quotes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

    def __str__(self):
        return str(self.id)