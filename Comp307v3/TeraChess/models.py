from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class Player(models.Model):
    username = models.CharField(max_length=100, default="Enter Username Here")
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="", related_name='profile')

    def __str__(self):
        return self.username


class PieceSet(models.Model):
    name = models.CharField(max_length=100, default="", unique=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True )
    main = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('collection')

    def __str__(self):
        return self.name


class Piece(models.Model):
    name = models.CharField(max_length=100, default="")
    front = models.BooleanField(default=True)
    picture_white = models.CharField(max_length=1000, default="")
    picture_black = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name


class PieceInstance(models.Model):
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, null=True)
    piece_set = models.ForeignKey(PieceSet, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, default="")
    order = models.IntegerField(default=0)
    front = models.BooleanField(default=True)
    picture = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pieces_details', kwargs={'piece_id': self.pk})


class BoardInstance(models.Model):
    player1 = models.CharField(max_length=100, default="")
    player2 = models.CharField(max_length=100, default="")
    white_player = models.CharField(max_length=100, default="")
    black_player = models.CharField(max_length=100, default="")
    game_id = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.game_id


class Cell(models.Model):
    piece = models.ForeignKey(PieceInstance, on_delete=models.CASCADE, blank=True, null=True)
    x_coord = models.IntegerField(default=0)
    y_coord = models.IntegerField(default=0)
    board = models.ForeignKey(BoardInstance, on_delete=models.CASCADE, null=True)
    is_null = models.BooleanField(default=True)

    def __str__(self):
        return str(self.x_coord) + ", " + str(self.y_coord)


class Move(models.Model):
    x_coord_old = models.IntegerField(default=0)
    y_coord_old = models.IntegerField(default=0)
    x_coord_new = models.IntegerField(default=0)
    y_coord_new = models.IntegerField(default=0)
    game_id = models.CharField(max_length=100, default="")

    def __str__(self):
        return "(" + str(self.x_coord_old) + ", " + str(self.y_coord_old) + ") -> (" + str(self.x_coord_new) + ", " + str(self.y_coord_new) + ")"