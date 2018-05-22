from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^register', views.register),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^home$', views.home),
    url(r'^home/remove/(?P<num>\d+)$', views.remove),
    url(r'^home/delete/(?P<num>\d+)$', views.delete),
    url(r'^home/join/(?P<num>\d+)$', views.join),
    url(r'^home/add$', views.add),
    url(r'^home/add/new$', views.new),
    url(r'^home/item/(?P<num>\d+)$', views.item),
    url(r'^home/back$', views.back),
    url(r'^logout/', views.logout),

]                       
