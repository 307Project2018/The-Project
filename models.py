from django.db import models
from django.urls import reverse
# Create your models here.


class Player(models.Model):
    username = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.username


class PieceSet(models.Model):
    name = models.CharField(max_length=100, default="")
    user = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('loginSignUp')

    def __str__(self):
        return self.name


class Piece(models.Model):
    name = models.CharField(max_length=100, default="")
    picture = models.CharField(max_length=1000, default="")
    front = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PieceInstance(models.Model):
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, null=True)
    piece_set = models.ForeignKey(PieceSet, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, default="")
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pieces_details', kwargs={'piece_id': self.pk})