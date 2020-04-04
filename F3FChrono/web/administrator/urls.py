from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login_f3f_admin', views.login_f3f_admin, name='login_f3f_admin'),
    path('logout_f3f_admin', views.logout_f3f_admin, name='logout_f3f_admin'),
    path('sign_in', views.sign_in, name='sign_in')
]
