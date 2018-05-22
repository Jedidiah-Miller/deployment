from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from datetime import datetime


class UserManager(models.Manager):
    def registration_verify(self, postData):
        response = {
            'status' : False,
            'errors' : []
        }
        now = str(datetime.now())
        if len(postData['first_name'])   < 2:
            response['errors'].append("first name should be at least 3 characters")
        if len(postData['last_name'])    < 1:
            response['errors'].append("last name should be at least 2 characters")
        if len(postData['email'])        < 1:
            response['errors'].append("username is too short")
        if len(postData['password'])     < 8:
            response['errors'].append("password too short")
        if postData['confirm_password'] != postData['password']:
            response['errors'].append("passwords do not match")

        # DATE VALIDATION FOR NOT A PAST DATE
        if postData['date_hired']        > now:
            response['errors'].append("this is a future date, you cannot time travel yet")

        if len(postData['date_hired'])   < 8:
            response['errors'].append("please choose a start date")
        if len(postData['email'])   < 3:
            response['errors'].append("username should be at least 3 characters")

        # username not being used
        if len(User.objects.filter(email=postData['email'])):
            response['errors'].append( "this username has already been registered")
            return response

        if len(response['errors']) == 0:
            response['status']  = True
            response['user_id'] = User.objects.create(
            first_name          = postData['first_name'],
            last_name           = postData['last_name'],
            email               = postData['email'],
            date_hired          = postData['date_hired'],
            password            = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())).id
        return response

        # password validation below
    def login_verify(self, postData):

        response = {
            'status' : False,
            'errors' : []
        }
        existing_users = (User.objects.filter(email = postData['email']))
        if len(existing_users) == 0:
            response['errors'].append('invalid username change ')
        else:
            if bcrypt.checkpw(postData['password'].encode(), existing_users[0].password.encode()):
                response['status']  = True
                response['user_id'] = existing_users[0].id
            else:
                response['errors'].append('invalid password')
        return response

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    email      = models.CharField(max_length=255)
    password   = models.CharField(max_length=255)
    date_hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    objects    = UserManager()

class TripManager(models.Manager):
    def item_add(self, postData, user_id):
        response = {
            'status' : False,
            'errors' : []
        }
        now = str(datetime.now())
        if len(postData['destination']) < 3:
            response['errors'].append("item should be at least 3 characters")
        if len(response['errors']) == 0:
            response['status']    = True
            response['curr_trip'] = Trip.objects.create (
            destination           = postData['destination'],
            trip_plan             = User.objects.get(id= user_id)
            )
        return response

    def item_join(self, postData, user_id, num):
        this_user = User.objects.get(id= user_id)
        this_item = Trip.objects.get(id = num)
        this_item.users.add(this_user)

    def item_del(self, postData, user_id, num):
        item    = Trip.objects.get(id= num)
        item.delete()

    def item_rem(self, postData, user_id, num):
        this_user = User.objects.get(id= user_id)
        this_item = Trip.objects.get(id = num)
        this_item.users.remove(this_user)

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    trip_plan   = models.ForeignKey(User, related_name = "trips_planned")
    users       = models.ManyToManyField(User, related_name = "destinations")
    created_at  = models.DateTimeField(auto_now_add = True)
    objects     = TripManager()
