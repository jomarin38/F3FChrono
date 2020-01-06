from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('event_view', views.event_view, name='event_view'),
    path('round_view', views.round_view, name='round_view'),
]

