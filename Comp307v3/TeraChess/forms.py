from django.contrib.auth.models import User
from django import forms
from .models import PieceSet, Piece, Player, PieceInstance, BoardInstance, Cell, Move


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields =['username', 'email', 'password']


class PieceSetForm(forms.ModelForm):

    class Meta:
        model = PieceSet
        fields = ['name']


class PieceInstanceForm(forms.ModelForm):

    class Meta:
        model = PieceInstance
        fields = ['piece', 'piece_set', 'order', 'name']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PieceInstanceForm, self).__init__(*args, **kwargs)
        self.fields['piece_set'].queryset = PieceSet.objects.filter(player=user.profile)


class BoardForm(forms.ModelForm):

    class Meta:
        model = BoardInstance
        fields = ['game_id']


class SecondPlayerForm(forms.ModelForm):

    class Meta:
        model = BoardInstance
        fields = ['game_id']


class MoveForm(forms.ModelForm):

    class Meta:
        model = Move
        fields = ['x_coord_old', 'y_coord_old', 'x_coord_new', 'y_coord_new', 'game_id']
