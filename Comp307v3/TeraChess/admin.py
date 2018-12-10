from django.contrib import admin
from .models import Piece, PieceSet, Player, PieceInstance, Cell, BoardInstance
# Register your models here.

admin.site.register(Piece)
admin.site.register(PieceSet)
admin.site.register(Player)
admin.site.register(PieceInstance)
admin.site.register(Cell)
admin.site.register(BoardInstance)