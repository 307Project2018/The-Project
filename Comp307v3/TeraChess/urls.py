from django.conf.urls import url
from . import views
from django.views.generic import RedirectView
from django.urls import path
#app_name = 'TeraChess'
from django.urls import path, include # new



urlpatterns = [
    url(r'index$', views.index, name='index'),
    url(r'^account$', views.account, name='account'),
    url(r'^build$', views.build, name='build'),
    url(r'^collection$', views.collection, name='collection'),
    url(r'^gameUI$', views.gameUI, name='gameUI'),
    url(r'^learn$', views.learn, name='learn'),
    url(r'^loginSignUp', views.loginSignUp, name='loginSignUp'), #/(?P<my_user_id>[0-9]+)$', views.loginSignUp, name='loginSignUp'),
    url(r'^register$', views.UserFormView.as_view(), name='register'),
    url(r'^DeletePieceSet$', views.deletePieceSet, name='deletePieceSet'),
    url(r'^play$', views.BoardFormView.as_view(), name='play'),
    url(r'^play/second', views.SecondPlayer.as_view(), name='secondplayer'),
    url(r'^template$', views.template, name='template'),
    url(r'^PieceSet/(?P<piece_set_id>[0-9]+)/$', views.pieces, name='pieces'),
    url(r'^Piece/(?P<piece_id>[0-9]+)/$', views.piece_details, name='pieces_details'),
    url(r'^PieceSet/add/$', views.PieceSetFormView.as_view(), name='PieceSetAdd'),
    url(r'PieceSet/delete/(?P<piece_set_id>[0-9]+)$', views.PieceSetDelete, name='PieceSetDelete'),
    url(r'^Piece/add/$', views.PieceInstanceFormView.as_view(), name='PieceInstanceAdd'),
    url(r'^logout$', views.logoutview, name='logout'),
    url(r'^login$', views.loginview, name='login'),
    url(r'^update/(?P<piece_set_id>[0-9]+)$', views.piecesetupdate, name='update'),
    url(r'^mygames$', views.displayGames, name='mygames'),
    url(r'^GameTime/(?P<game_id>[a-zA-Z0-9_]+)$', views.gametime, name='gametime'),
    url(r'^nextmove$', views.NextMoveFormView.as_view(), name='next'),
    url(r'^ViewGame/(?P<game_id>[a-zA-Z0-9_]+)$', views.viewgame, name='viewgame')
]

# request.user.pieceset_set.get(name=


