from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login_f3f_admin', views.login_f3f_admin, name='login_f3f_admin'),
    path('logout_f3f_admin', views.logout_f3f_admin, name='logout_f3f_admin'),
    path('create_new_event', views.create_new_event, name='create_new_event'),
    path('load_from_f3x_vault', views.load_from_f3x_vault, name='load_from_f3x_vault'),
    path('load_from_scratch', views.load_from_scratch, name='load_from_scratch'),
    path('manage_event', views.manage_event, name='manage_event'),
    path('set_competitor_presence', views.set_competitor_presence, name='set_competitor_presence'),
    path('remove_competitor', views.remove_competitor, name='remove_competitor'),
    path('new_pilot_input', views.new_pilot_input, name='new_pilot_input'),
    path('register_new_pilot', views.register_new_pilot, name='register_new_pilot'),
    path('cancel_round', views.cancel_round, name='cancel_round'),
    path('delete_event', views.delete_event, name='delete_event'),
    path('do_delete_event', views.do_delete_event, name='do_delete_event'),
    path('manage_round', views.manage_round, name='manage_round'),
    path('give_refly', views.give_refly, name='give_refly'),
    path('give_penalty', views.give_penalty, name='give_penalty'),
    path('give_zero', views.give_zero, name='give_zero'),
    path('export_round_f3x_vault', views.export_round_f3x_vault, name='export_round_f3x_vault'),
    path('login_to_export_round_f3x_vault', views.login_to_export_round_f3x_vault,
         name='login_to_export_round_f3x_vault'),
    path('export_event_f3x_vault', views.export_event_f3x_vault, name='export_event_f3x_vault'),
    path('login_to_export_event_f3x_vault', views.login_to_export_event_f3x_vault,
         name='login_to_export_event_f3x_vault'),
    path('sign_in', views.sign_in, name='sign_in')
]
