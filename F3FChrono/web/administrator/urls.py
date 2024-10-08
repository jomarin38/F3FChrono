#
# This file is part of the F3FChrono distribution (https://github.com/jomarin38/F3FChrono).
# Copyright (c) 2021 Sylvain DAVIET, Joel MARIN.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from django.urls import path, re_path, include

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
    path('edit_run_time', views.edit_run_time, name='edit_run_time'),
    path('set_time', views.set_time, name='set_time'),
    path('new_pilot_input', views.new_pilot_input, name='new_pilot_input'),
    path('register_new_pilot', views.register_new_pilot, name='register_new_pilot'),
    path('cancel_round', views.cancel_round, name='cancel_round'),
    path('validate_round', views.validate_round, name='validate_round'),
    path('delete_event', views.delete_event, name='delete_event'),
    path('do_delete_event', views.do_delete_event, name='do_delete_event'),
    path('manage_round', views.manage_round, name='manage_round'),
    path('give_refly', views.give_refly, name='give_refly'),
    path('give_penalty', views.give_penalty, name='give_penalty'),
    path('give_zero', views.give_zero, name='give_zero'),
    path('download_csv', views.download_csv, name='download_csv'),
    path('download_pilots_as_csv', views.download_pilots_as_csv, name='download_pilots_as_csv'),
    path('export_round_f3x_vault', views.export_round_f3x_vault, name='export_round_f3x_vault'),
    path('login_to_export_round_f3x_vault', views.login_to_export_round_f3x_vault,
         name='login_to_export_round_f3x_vault'),
    path('auto_export_round_f3x_vault', views.auto_export_round_f3x_vault,
             name='auto_export_round_f3x_vault'),
    path('export_event_f3x_vault', views.export_event_f3x_vault, name='export_event_f3x_vault'),
    path('login_to_export_event_f3x_vault', views.login_to_export_event_f3x_vault,
         name='login_to_export_event_f3x_vault'),
    path('define_bibs', views.define_bibs, name='define_bibs'),
    path('do_define_bibs', views.do_define_bibs, name='define_bibs'),
    path('define_fly_order', views.define_fly_order, name='define_fly_order'),
    path('do_define_fly_order', views.do_define_fly_order, name='define_fly_order'),
    re_path(r'^celery-progress/', include('celery_progress.urls', namespace="celery_progress")),
]
