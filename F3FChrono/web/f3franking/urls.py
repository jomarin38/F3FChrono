from django.urls import path

from . import views, administrator_views

urlpatterns = [
    path('', views.index, name='index'),
    path('event_view', views.event_view, name='event_view'),
    path('round_view', views.round_view, name='round_view'),
    path('is_alive', views.is_alive, name='is_alive')
]

