from os import environ as env

from django.conf.urls import url

from .views import (TattletrailStatusCheckView, TattletrailStatusCheckUpdateView,
                    duplicate_check)

urlpatterns = [

    url(r'^tattletrail/create/',
        view=TattletrailStatusCheckView.as_view(),
        name='create-tattletrail-check'),

    url(r'^tattletrail/update/(?P<pk>\d+)/',
        view=TattletrailStatusCheckUpdateView.as_view(),
        name='update-tattletrail-check'),

    url(r'^tattletrail/duplicate/(?P<pk>\d+)/',
        view=duplicate_check,
        name='duplicate-tattletrail-check')
]