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
        return reverse('pieces', kwargs={'piece_set_id': self.pk})

    def __str__(self):
        return self.name


class Piece(models.Model):
    name = models.CharField(max_length=100, default="")
    picture = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name


class PieceInstance(models.Model):
    piece = models.OneToOneField(Piece, on_delete=models.CASCADE, null=True)
    piece_set = models.ForeignKey(PieceSet, on_delete=models.CASCADE, null=True)