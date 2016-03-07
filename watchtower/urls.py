'''
Created on Mar 6, 2016

@author: slaugms
'''
from django.conf.urls import url
from . import views
from watchtower.views import WatchtowerView

urlpatterns = [
              # url(r'^watchtower/', views.index, name='index'),
               url(r'^$', WatchtowerView.as_view()),
]
