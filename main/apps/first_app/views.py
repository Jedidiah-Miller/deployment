from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Q

def register(request):
    context = {
        'now'       : datetime.now()
    }
    request.session.flush()
    return render(request,'first_app/index.html', context)

def create(request):
    result = User.objects.registration_verify(request.POST)
    if result['status']:
        request.session['user_id'] = result['user_id']
        return redirect('/home')
    else:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/register')

def login(request):
    result = User.objects.login_verify(request.POST)
    if result['status']:
        request.session['user_id'] = result['user_id']
        return redirect('/home')
    else:
        for error in result['errors']:
            messages.error(request, error)
    return redirect('/register')

def home(request):
    if 'user_id' in request.session:
        context = {
        'curr_user' : User.objects.get(id = request.session['user_id']),
        'now'       : datetime.now(),
        'item'      : Trip.objects.filter(trip_plan_id = request.session['user_id']),
        'joined'    : Trip.objects.filter(users = request.session['user_id']),
        'add_item'  : Trip.objects.exclude(trip_plan_id = request.session['user_id']) & Trip.objects.exclude(users = request.session['user_id'])
    }
        return render(request,'first_app/newindex.html', context)
    else:
        return redirect('/register')

def join(request, num):
    Trip.objects.item_join(request.POST, request.session['user_id'], num)
    return redirect('/home')

def logout(request):
    request.session.flush()
    return redirect('/register')

def remove(request, num):
    Trip.objects.item_rem(request.POST, request.session['user_id'], num)
    return redirect('/home')

def delete(request, num):
    Trip.objects.item_del(request.POST, request.session['user_id'], num)
    return redirect('/home')

def add(request):
    if 'user_id' in request.session:
        context = {
            'curr_user' : User.objects.get(id = request.session['user_id']),
        }
        return render(request, 'first_app/add.html', context)
    else:
        return redirect('/register')

def new(request):
    result = Trip.objects.item_add(request.POST, request.session['user_id'])
    if result['status']:
        return redirect('/home')
    else:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/home/add')

def item(request, num):
    if 'user_id' in request.session:
        trip    = Trip.objects.get(id= num)
        context = {
        'trip'         : trip,
        'users'        : trip.users.all(),
        'curr_user'    : User.objects.get(id = request.session['user_id']),
        'item'         : Trip.objects.get(id = num ),
        }
        return render(request, 'first_app/item.html', context)
    else:
        return redirect('/register')

def back(request):
    return redirect('/home')
