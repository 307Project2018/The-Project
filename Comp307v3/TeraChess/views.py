from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import PieceSet, Piece, Player, PieceInstance, User, BoardInstance, Cell
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core import serializers
from django.views.generic import View
from .forms import UserForm, PieceSetForm, PieceInstanceForm, BoardForm, SecondPlayerForm
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth import logout
from django.views.generic.edit import FormView
import random


def account(request):
    return render(request, 'TeraChess/html/account.html')


def build(request):
    return render(request, 'TeraChess/html/build.html')


def collection(request):
    context = {}
    if request.user.is_authenticated:

        profile = request.user.profile
        all_pieces = PieceSet.objects.filter(player=profile)
        context = {
            'profile': profile,
            'all_pieces': all_pieces
        }
    return render(request, 'TeraChess/html/collection.html', context)


def gameUI(request):
    return render(request, 'TeraChess/html/gameUI.html')


def index(request):
    return render(request, 'TeraChess/html/index.html')


def learn(request):
    return render(request, 'TeraChess/html/learn.html')


def loginSignUp(request):
    context = {}
    if request.user.is_authenticated:

        profile = request.user.profile
        all_pieces = PieceSet.objects.filter(player=profile)
        context = {
            'profile': profile,
            'all_pieces': all_pieces
        }
    return render(request, 'TeraChess/html/loginSignUp.html', context)


def pieces(request, piece_set_id):
    try:
        current_set = PieceSet.objects.get(pk=piece_set_id)
        my_pieces = current_set.pieceinstance_set.all()
    except PieceSet.DoesNotExist:
        raise Http404("PieceSet does not exist")
    return render(request, 'TeraChess/html/pieces.html', {'pieces': my_pieces})


def piecesetupdate(request, piece_set_id):
    current_set = PieceSet.objects.get(pk=piece_set_id)
    all_sets = PieceSet.objects.filter(player=request.user.profile)
    for set in all_sets:
        set.main = False
        set.save()
    current_set.main = True
    current_set.save()
    return render(request, 'TeraChess/html/index.html')


def piece_details(request, piece_id):
        current_piece = PieceInstance.objects.get(pk=piece_id)
        return render(request, 'TeraChess/html/piece_details.html', {'piece_instance': current_piece})


def play(request):
    return render(request, 'TeraChess/html/play.html')


def template(request):
    return render(request, 'TeraChess/html/template.html')


class PieceSetCreate(CreateView):
    model = PieceSet
    fields = ['name', 'player']


def PieceSetDelete(request, piece_set_id):
    piece_set = PieceSet.objects.get(pk=piece_set_id)
    piece_set.delete()
    return render(request, 'TeraChess/html/pieceset_confirm_delete.html', {'piece_set':piece_set})


def deletePieceSet(request):
    context = {}
    if request.user.is_authenticated:

        profile = request.user.profile
        all_pieces = PieceSet.objects.filter(player=profile)
        context = {
            'profile': profile,
            'all_pieces': all_pieces
        }
    return render(request, 'TeraChess/html/delete_pieceset.html', context)


class PieceInstanceCreate(CreateView):
    model = PieceInstance
    fields = ['name', 'order', 'piece', 'piece_set']


class PieceInstanceFormView(View):
    form_class = PieceInstanceForm
    template_name = 'TeraChess/pieceinstance_form.html'

    def get(self, request):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, user=request.user)

        if form.is_valid():
            name = form.cleaned_data['name']
            order = form.cleaned_data['order']
            piece = form.cleaned_data['piece']
            piece_set = form.cleaned_data['piece_set']
            PieceInstance.objects.create(name=name, order=order, piece=piece, piece_set=piece_set)

        if request.user.is_authenticated:
            return redirect('TeraChess/index')
        return render(request, self.template_name, {'form': form})

    def get_form_kwargs(self):
        kwargs = super(PieceInstanceFormView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class PieceSetFormView(View):
    form_class = PieceSetForm
    template_name = 'TeraChess/pieceset_form.html'

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            PieceSet.objects.create(player=request.user.profile, name=name)

        if request.user.is_authenticated:
            return redirect('TeraChess/index')
        return render(request, self.template_name, {'form': form})

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


class BoardFormView(View):
    template_name = 'TeraChess/boardinstance_form.html'
    form_class = BoardForm


    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        my_rand = random.randint(0, 11)
        if form.is_valid():
            game_id = form.cleaned_data['game_id']
            current_player = request.user.profile
            if my_rand <= 4:
                board = BoardInstance.objects.create(player1=current_player, game_id=game_id, white_player=current_player)
            else:
                board = BoardInstance.objects.create(player1=current_player, game_id=game_id, black_player=current_player)
            for i in range(0, 8):
                for j in range(0, 8):
                    board.cell_set.add(Cell.objects.create(x_coord=j, y_coord=i))

        if request.user.is_authenticated:
            return redirect('TeraChess/index')
        return render(request, self.template_name, {'form': form})


class SecondPlayer(View):
    form_class = SecondPlayerForm
    template_name = 'TeraChess/secondplayer_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            game_id = form.cleaned_data['game_id']
            current_player = request.user.profile
            board = BoardInstance.objects.get(game_id=game_id)
            board.player2 = current_player.username
            if board.white_player:
                board.black_player = current_player.username
            else:
                board.white_player = current_player.username
            board.save()

        if request.user.is_authenticated:
            return redirect('TeraChess/index')
        return render(request, self.template_name, {'form': form})


class UserFormView(View):
    form_class = UserForm
    template_name = 'TeraChess/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.username = username
            user.set_password(password)
            user.save()
            Player.objects.create(user=user, username=username)

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('TeraChess/index')

        return render(request, self.template_name, {'form': form})


def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('TeraChess/index')


def loginview(request):
    if request.user.is_authenticated:
        login(request)
    return redirect('TeraChess/index')


def move_piece_checker(request, start, end):
   """ Returns 0 if piece at start cannot move to end,
        1 if it can move, 2 if it can move but the move is an attack """
   boardWidth = 8
   boardHeight = 8
   board = [[None for x in range(boardWidth)] for y in range(boardHeight)]
   if start == end:
       return 0
   piece_to_move = board[start[0]][start[1]]
   # query database about piece info, in particular the move_set
   move_set_example = "(0,4),(4,3),(5,6),(0,3)"
   move_set = Piece.objects.find(name=piece_to_move)
   possible_ends = re.findall(r"\((.,.)\)", move_set)
   possible_ends_tuples = [tuple(int(s) for s in i.split(',')) for i in possible_ends]

   # check if possible to move there
   possible_to_move = 0
   for x in possible_ends_tuples:
       if (x[0] + start[0], x[1] + start[1]) == end:
           print(x)
           possible_to_move = 1

   if possible_to_move == 0:
       return 0

   # check if pieces exist between start and end
   diff = (end[0] - start[0], end[1] - start[1])

   # crest movement
   if diff[0] == 0 or diff[1] == 0:
       min_v = min(diff[0], diff[1])
       max_v = max(diff[0], diff[1])
       if diff[0] == 0:
           for x in range(min_v+1, max_v):
               if board[start[0]][x] is not None:
                   return 0
       else:
           for x in range(min_v+1, max_v):
               if board[x][start[0]] is not None:
                   return 0

       possible_to_move = 1

   # diagonal movement
   if abs(diff[0]) == abs(diff[1]):
       a = (diff[0] * 1/abs(diff[0]), diff[1] * 1/abs(diff[1]))
       y = lambda z: (a[0] * z + start[0], a[1] * z + start[1])
       for x in range(1, abs(diff[1])):
           if board[y(x)[0]][y(x)[1]] is not None:
               return 0
       possible_to_move = 1

   end_location = board[end[0]][end[1]]
   if end_location is not None:
       endPiece = board[end[0]][end[1]]
   # query database about endPiece
   # check if enemy piece belongs to enemy player return 2
   # if piece does not belong to enemy player return 0
   return 2

