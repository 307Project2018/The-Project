from django.conf.urls import url
from . import views
from django.views.generic import RedirectView
from django.urls import path
#app_name = 'TeraChess'

urlpatterns = [
    url(r'Index$', views.index, name='index'),
    url(r'^account$', views.account, name='account'),
    url(r'^build$', views.build, name='build'),
    url(r'^collection$', views.collection, name='collection'),
    url(r'^gameUI$', views.gameUI, name='gameUI'),
    url(r'^learn$', views.learn, name='learn'),
    url(r'^loginSignUp$', views.loginSignUp, name='loginSignUp'),
    url(r'^play$', views.play, name='play'),
    url(r'^template$', views.template, name='template'),
    url(r'^PieceSet/(?P<piece_set_id>[0-9]+)/$', views.pieces, name='pieces'),
    url(r'^Piece/(?P<piece_id>[0-9]+)/$', views.piece_details, name='pieces_details'),
    url(r'^PieceSet/add/$', views.PieceSetCreate.as_view(), name='PieceSetAdd')
]

