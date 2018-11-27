from django.contrib import admin
from .models import Piece, PieceSet, Player
# Register your models here.

admin.site.register(Piece)
admin.site.register(PieceSet)
admin.site.register(Player)