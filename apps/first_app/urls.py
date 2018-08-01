from django.conf.urls import url
from . import views  
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login$', views.login, name="login"),
    url(r'^register$', views.register, name="register"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^add_job$', views.add_job, name='add_job'),
    url(r'^show_add_job$', views.show_add_job, name='show_add_job'),
    url(r'^(?P<id>\d+)/join_job$', views.join_job, name='join_job'),
    url(r'^(?P<id>\d+)/show_edit_job$', views.show_edit_job, name='show_edit_job'),
    url(r'^(?P<id>\d+)/edit_job$', views.edit_job, name='edit_job'),
    url(r'^(?P<id>\d+)/view_job$', views.view_job, name='view_job'),
    url(r'^(?P<id>\d+)/cancel_job$', views.cancel_job, name='cancel_job'),
    url(r'^(?P<id>\d+)/complete_job$', views.complete_job, name='complete_job'),
]                            
