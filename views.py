
from django.shortcuts import render, redirect
from .models import PieceSet, Piece, Player
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def account(request):
    return render(request, 'TeraChess/html/account.html')


def build(request):
    return render(request, 'TeraChess/html/build.html')


def collection(request):
    return render(request, 'TeraChess/html/collection.html')


def gameUI(request):
    return render(request, 'TeraChess/html/gameUI.html')


def index(request):
    return render(request, 'TeraChess/html/index.html')


def learn(request):
    return render(request, 'TeraChess/html/learn.html')


def loginSignUp(request):
    all_pieces = PieceSet.objects.all()
    context = {
        'all_pieces': all_pieces
    }
    return render(request, 'TeraChess/html/loginSignUp.html', context)


def pieces(request, piece_set_id):
    try:
        current_set = PieceSet.objects.get(pk=piece_set_id)
        my_pieces = current_set.piece_set.all()
    except PieceSet.DoesNotExist:
        raise Http404("PieceSet does not exist")
    return render(request, 'TeraChess/html/pieces.html', {'pieces': my_pieces})


def piece_details(request, piece_id):
        current_piece = Piece.objects.get(pk=piece_id)
        return render(request, 'TeraChess/html/piece_details.html', {'piece': current_piece})


def play(request):
    return render(request, 'TeraChess/html/play.html')


def template(request):
    return render(request, 'TeraChess/html/template.html')


class PieceSetCreate(CreateView):
    model = PieceSet
    fields = ['name']



