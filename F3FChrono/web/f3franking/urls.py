from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('event_view', views.event_view, name='event_view')
]

