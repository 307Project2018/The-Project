
from django.shortcuts import render, redirect
from .models import PieceSet, Player, PieceInstance, BoardInstance, Cell
from django.http import Http404
from django.views.generic.edit import CreateView
from django.views.generic import View
from .forms import UserForm, PieceSetForm, PieceInstanceForm, BoardForm, SecondPlayerForm, MoveForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
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
            front = piece.front
            PieceInstance.objects.create(name=name, order=order, piece=piece, piece_set=piece_set, front=front)

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
    return redirect('TeraChess/collection')


def displayGames(request):
    context = {}
    if request.user.is_authenticated:
        player = request.user.profile
        games_player1 = BoardInstance.objects.filter(player1=player.username)
        games_player2 = BoardInstance.objects.filter(player2=player.username)

        context = {
            'games_player1': games_player1,
            'games_player2': games_player2
        }

    return render(request, 'TeraChess/html/my_games.html', context)


# I am so very sorry for having disgusting hard-coded garbage like this
def gametime(request, game_id):
    context = {}
    is_front = False
    if request.user.is_authenticated:
        game = BoardInstance.objects.get(game_id=game_id)
        white_player = Player.objects.get(username=game.white_player)
        black_player = Player.objects.get(username=game.black_player)
        white_player_set = PieceSet.objects.get(player=white_player, main=True).pieceinstance_set
        black_player_set = PieceSet.objects.get(player=black_player, main=True).pieceinstance_set
        for i in range(0, 8):
            for j in range(0, 2):
                if j == 0:
                    is_front = False
                if j == 1:
                    is_front = True
                cell_piece = white_player_set.get(order=i, front=is_front)
                cell_piece.picture = cell_piece.piece.picture_white
                cell_piece.save()
                cell = Cell.objects.get(x_coord=i, y_coord=j, board=game)
                cell.piece = cell_piece
                cell.is_null = False
                cell.save()
        for i in range(0, 8):
            for j in range(2,6):
                cell = Cell.objects.get(x_coord=i, y_coord=j, board=game)
                cell.is_null = True
                cell.save()
        for i in range(0, 8):
            for j in range(6, 8):
                if j == 6:
                    is_front = True
                if j == 7:
                    is_front = False
                cell_piece = black_player_set.get(order=i, front=is_front)
                cell_piece.picture = cell_piece.piece.picture_black
                cell_piece.save()
                cell = Cell.objects.get(x_coord=i, y_coord=j, board=game)
                cell.piece = cell_piece
                cell.is_null = False
                cell.save()
        cell_00 = Cell.objects.get(x_coord=0, y_coord=0, board=game)
        cell_01 = Cell.objects.get(x_coord=0, y_coord=1, board=game)
        cell_02 = Cell.objects.get(x_coord=0, y_coord=2, board=game)
        cell_03 = Cell.objects.get(x_coord=0, y_coord=3, board=game)
        cell_04 = Cell.objects.get(x_coord=0, y_coord=4, board=game)
        cell_05 = Cell.objects.get(x_coord=0, y_coord=5, board=game)
        cell_06 = Cell.objects.get(x_coord=0, y_coord=6, board=game)
        cell_07 = Cell.objects.get(x_coord=0, y_coord=7, board=game)

        cell_10 = Cell.objects.get(x_coord=1, y_coord=0, board=game)
        cell_11 = Cell.objects.get(x_coord=1, y_coord=1, board=game)
        cell_12 = Cell.objects.get(x_coord=1, y_coord=2, board=game)
        cell_13 = Cell.objects.get(x_coord=1, y_coord=3, board=game)
        cell_14 = Cell.objects.get(x_coord=1, y_coord=4, board=game)
        cell_15 = Cell.objects.get(x_coord=1, y_coord=5, board=game)
        cell_16 = Cell.objects.get(x_coord=1, y_coord=6, board=game)
        cell_17 = Cell.objects.get(x_coord=1, y_coord=7, board=game)

        cell_20 = Cell.objects.get(x_coord=2, y_coord=0, board=game)
        cell_21 = Cell.objects.get(x_coord=2, y_coord=1, board=game)
        cell_22 = Cell.objects.get(x_coord=2, y_coord=2, board=game)
        cell_23 = Cell.objects.get(x_coord=2, y_coord=3, board=game)
        cell_24 = Cell.objects.get(x_coord=2, y_coord=4, board=game)
        cell_25 = Cell.objects.get(x_coord=2, y_coord=5, board=game)
        cell_26 = Cell.objects.get(x_coord=2, y_coord=6, board=game)
        cell_27 = Cell.objects.get(x_coord=2, y_coord=7, board=game)

        cell_30 = Cell.objects.get(x_coord=3, y_coord=0, board=game)
        cell_31 = Cell.objects.get(x_coord=3, y_coord=1, board=game)
        cell_32 = Cell.objects.get(x_coord=3, y_coord=2, board=game)
        cell_33 = Cell.objects.get(x_coord=3, y_coord=3, board=game)
        cell_34 = Cell.objects.get(x_coord=3, y_coord=4, board=game)
        cell_35 = Cell.objects.get(x_coord=3, y_coord=5, board=game)
        cell_36 = Cell.objects.get(x_coord=3, y_coord=6, board=game)
        cell_37 = Cell.objects.get(x_coord=3, y_coord=7, board=game)

        cell_40 = Cell.objects.get(x_coord=4, y_coord=0, board=game)
        cell_41 = Cell.objects.get(x_coord=4, y_coord=1, board=game)
        cell_42 = Cell.objects.get(x_coord=4, y_coord=2, board=game)
        cell_43 = Cell.objects.get(x_coord=4, y_coord=3, board=game)
        cell_44 = Cell.objects.get(x_coord=4, y_coord=4, board=game)
        cell_45 = Cell.objects.get(x_coord=4, y_coord=5, board=game)
        cell_46 = Cell.objects.get(x_coord=4, y_coord=6, board=game)
        cell_47 = Cell.objects.get(x_coord=4, y_coord=7, board=game)

        cell_50 = Cell.objects.get(x_coord=5, y_coord=0, board=game)
        cell_51 = Cell.objects.get(x_coord=5, y_coord=1, board=game)
        cell_52 = Cell.objects.get(x_coord=5, y_coord=2, board=game)
        cell_53 = Cell.objects.get(x_coord=5, y_coord=3, board=game)
        cell_54 = Cell.objects.get(x_coord=5, y_coord=4, board=game)
        cell_55 = Cell.objects.get(x_coord=5, y_coord=5, board=game)
        cell_56 = Cell.objects.get(x_coord=5, y_coord=6, board=game)
        cell_57 = Cell.objects.get(x_coord=5, y_coord=7, board=game)

        cell_60 = Cell.objects.get(x_coord=6, y_coord=0, board=game)
        cell_61 = Cell.objects.get(x_coord=6, y_coord=1, board=game)
        cell_62 = Cell.objects.get(x_coord=6, y_coord=2, board=game)
        cell_63 = Cell.objects.get(x_coord=6, y_coord=3, board=game)
        cell_64 = Cell.objects.get(x_coord=6, y_coord=4, board=game)
        cell_65 = Cell.objects.get(x_coord=6, y_coord=5, board=game)
        cell_66 = Cell.objects.get(x_coord=6, y_coord=6, board=game)
        cell_67 = Cell.objects.get(x_coord=6, y_coord=7, board=game)

        cell_70 = Cell.objects.get(x_coord=7, y_coord=0, board=game)
        cell_71 = Cell.objects.get(x_coord=7, y_coord=1, board=game)
        cell_72 = Cell.objects.get(x_coord=7, y_coord=2, board=game)
        cell_73 = Cell.objects.get(x_coord=7, y_coord=3, board=game)
        cell_74 = Cell.objects.get(x_coord=7, y_coord=4, board=game)
        cell_75 = Cell.objects.get(x_coord=7, y_coord=5, board=game)
        cell_76 = Cell.objects.get(x_coord=7, y_coord=6, board=game)
        cell_77 = Cell.objects.get(x_coord=7, y_coord=7, board=game)

        context = {
            'game_id': game_id,
            'white_player_set': white_player_set,
            'black_player_set': black_player_set,
            'player1': game.player1,
            'player2': game.player2,
            'cells': game.cell_set,

            'cell_00': cell_00,
            'cell_01': cell_01,
            'cell_02': cell_02,
            'cell_03': cell_03,
            'cell_04': cell_04,
            'cell_05': cell_05,
            'cell_06': cell_06,
            'cell_07': cell_07,

            'cell_10': cell_10,
            'cell_11': cell_11,
            'cell_12': cell_12,
            'cell_13': cell_13,
            'cell_14': cell_14,
            'cell_15': cell_15,
            'cell_16': cell_16,
            'cell_17': cell_17,

            'cell_20': cell_20,
            'cell_21': cell_21,
            'cell_22': cell_22,
            'cell_23': cell_23,
            'cell_24': cell_24,
            'cell_25': cell_25,
            'cell_26': cell_26,
            'cell_27': cell_27,

            'cell_30': cell_30,
            'cell_31': cell_31,
            'cell_32': cell_32,
            'cell_33': cell_33,
            'cell_34': cell_34,
            'cell_35': cell_35,
            'cell_36': cell_36,
            'cell_37': cell_37,

            'cell_40': cell_40,
            'cell_41': cell_41,
            'cell_42': cell_42,
            'cell_43': cell_43,
            'cell_44': cell_44,
            'cell_45': cell_45,
            'cell_46': cell_46,
            'cell_47': cell_47,

            'cell_50': cell_50,
            'cell_51': cell_51,
            'cell_52': cell_52,
            'cell_53': cell_53,
            'cell_54': cell_54,
            'cell_55': cell_55,
            'cell_56': cell_56,
            'cell_57': cell_57,

            'cell_60': cell_60,
            'cell_61': cell_61,
            'cell_62': cell_62,
            'cell_63': cell_63,
            'cell_64': cell_64,
            'cell_65': cell_65,
            'cell_66': cell_66,
            'cell_67': cell_67,

            'cell_70': cell_70,
            'cell_71': cell_71,
            'cell_72': cell_72,
            'cell_73': cell_73,
            'cell_74': cell_74,
            'cell_75': cell_75,
            'cell_76': cell_76,
            'cell_77': cell_77,

        }
    return render(request, 'TeraChess/html/gameUI.html', context)


class NextMoveFormView(View):
    form_class = MoveForm
    template_name = 'TeraChess/gameUI_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            x_old = form.cleaned_data['x_coord_old']
            y_old = form.cleaned_data['y_coord_old']
            x_new = form.cleaned_data['x_coord_new']
            y_new = form.cleaned_data['y_coord_new']
            game_id = form.cleaned_data['game_id']

            game = BoardInstance.objects.get(game_id=game_id)
            old_cell = game.cell_set.get(x_coord=x_old, y_coord=y_old)
            new_cell = game.cell_set.get(x_coord=x_new, y_coord=y_new)

            def is_valid_move(prev_cell, next_cell):
                return True

            if is_valid_move(old_cell, new_cell):
                new_cell.piece = old_cell.piece
                new_cell.is_null = False
                new_cell.save()

                old_cell.is_null = True
                old_cell.save()
        if request.user.is_authenticated:
            next_page = 'ViewGame/' + str(game_id)
            return redirect(next_page)

        return render(request, self.template_name, {'form': form})


def viewgame(request, game_id):
    context = {}
    game = BoardInstance.objects.get(game_id=game_id)
    if request.user.is_authenticated:
        cell_00 = Cell.objects.get(x_coord=0, y_coord=0, board=game)
        cell_01 = Cell.objects.get(x_coord=0, y_coord=1, board=game)
        cell_02 = Cell.objects.get(x_coord=0, y_coord=2, board=game)
        cell_03 = Cell.objects.get(x_coord=0, y_coord=3, board=game)
        cell_04 = Cell.objects.get(x_coord=0, y_coord=4, board=game)
        cell_05 = Cell.objects.get(x_coord=0, y_coord=5, board=game)
        cell_06 = Cell.objects.get(x_coord=0, y_coord=6, board=game)
        cell_07 = Cell.objects.get(x_coord=0, y_coord=7, board=game)

        cell_10 = Cell.objects.get(x_coord=1, y_coord=0, board=game)
        cell_11 = Cell.objects.get(x_coord=1, y_coord=1, board=game)
        cell_12 = Cell.objects.get(x_coord=1, y_coord=2, board=game)
        cell_13 = Cell.objects.get(x_coord=1, y_coord=3, board=game)
        cell_14 = Cell.objects.get(x_coord=1, y_coord=4, board=game)
        cell_15 = Cell.objects.get(x_coord=1, y_coord=5, board=game)
        cell_16 = Cell.objects.get(x_coord=1, y_coord=6, board=game)
        cell_17 = Cell.objects.get(x_coord=1, y_coord=7, board=game)

        cell_20 = Cell.objects.get(x_coord=2, y_coord=0, board=game)
        cell_21 = Cell.objects.get(x_coord=2, y_coord=1, board=game)
        cell_22 = Cell.objects.get(x_coord=2, y_coord=2, board=game)
        cell_23 = Cell.objects.get(x_coord=2, y_coord=3, board=game)
        cell_24 = Cell.objects.get(x_coord=2, y_coord=4, board=game)
        cell_25 = Cell.objects.get(x_coord=2, y_coord=5, board=game)
        cell_26 = Cell.objects.get(x_coord=2, y_coord=6, board=game)
        cell_27 = Cell.objects.get(x_coord=2, y_coord=7, board=game)

        cell_30 = Cell.objects.get(x_coord=3, y_coord=0, board=game)
        cell_31 = Cell.objects.get(x_coord=3, y_coord=1, board=game)
        cell_32 = Cell.objects.get(x_coord=3, y_coord=2, board=game)
        cell_33 = Cell.objects.get(x_coord=3, y_coord=3, board=game)
        cell_34 = Cell.objects.get(x_coord=3, y_coord=4, board=game)
        cell_35 = Cell.objects.get(x_coord=3, y_coord=5, board=game)
        cell_36 = Cell.objects.get(x_coord=3, y_coord=6, board=game)
        cell_37 = Cell.objects.get(x_coord=3, y_coord=7, board=game)

        cell_40 = Cell.objects.get(x_coord=4, y_coord=0, board=game)
        cell_41 = Cell.objects.get(x_coord=4, y_coord=1, board=game)
        cell_42 = Cell.objects.get(x_coord=4, y_coord=2, board=game)
        cell_43 = Cell.objects.get(x_coord=4, y_coord=3, board=game)
        cell_44 = Cell.objects.get(x_coord=4, y_coord=4, board=game)
        cell_45 = Cell.objects.get(x_coord=4, y_coord=5, board=game)
        cell_46 = Cell.objects.get(x_coord=4, y_coord=6, board=game)
        cell_47 = Cell.objects.get(x_coord=4, y_coord=7, board=game)

        cell_50 = Cell.objects.get(x_coord=5, y_coord=0, board=game)
        cell_51 = Cell.objects.get(x_coord=5, y_coord=1, board=game)
        cell_52 = Cell.objects.get(x_coord=5, y_coord=2, board=game)
        cell_53 = Cell.objects.get(x_coord=5, y_coord=3, board=game)
        cell_54 = Cell.objects.get(x_coord=5, y_coord=4, board=game)
        cell_55 = Cell.objects.get(x_coord=5, y_coord=5, board=game)
        cell_56 = Cell.objects.get(x_coord=5, y_coord=6, board=game)
        cell_57 = Cell.objects.get(x_coord=5, y_coord=7, board=game)

        cell_60 = Cell.objects.get(x_coord=6, y_coord=0, board=game)
        cell_61 = Cell.objects.get(x_coord=6, y_coord=1, board=game)
        cell_62 = Cell.objects.get(x_coord=6, y_coord=2, board=game)
        cell_63 = Cell.objects.get(x_coord=6, y_coord=3, board=game)
        cell_64 = Cell.objects.get(x_coord=6, y_coord=4, board=game)
        cell_65 = Cell.objects.get(x_coord=6, y_coord=5, board=game)
        cell_66 = Cell.objects.get(x_coord=6, y_coord=6, board=game)
        cell_67 = Cell.objects.get(x_coord=6, y_coord=7, board=game)

        cell_70 = Cell.objects.get(x_coord=7, y_coord=0, board=game)
        cell_71 = Cell.objects.get(x_coord=7, y_coord=1, board=game)
        cell_72 = Cell.objects.get(x_coord=7, y_coord=2, board=game)
        cell_73 = Cell.objects.get(x_coord=7, y_coord=3, board=game)
        cell_74 = Cell.objects.get(x_coord=7, y_coord=4, board=game)
        cell_75 = Cell.objects.get(x_coord=7, y_coord=5, board=game)
        cell_76 = Cell.objects.get(x_coord=7, y_coord=6, board=game)
        cell_77 = Cell.objects.get(x_coord=7, y_coord=7, board=game)
        context = {
            'game_id': game_id,

            'cell_00': cell_00,
            'cell_01': cell_01,
            'cell_02': cell_02,
            'cell_03': cell_03,
            'cell_04': cell_04,
            'cell_05': cell_05,
            'cell_06': cell_06,
            'cell_07': cell_07,

            'cell_10': cell_10,
            'cell_11': cell_11,
            'cell_12': cell_12,
            'cell_13': cell_13,
            'cell_14': cell_14,
            'cell_15': cell_15,
            'cell_16': cell_16,
            'cell_17': cell_17,

            'cell_20': cell_20,
            'cell_21': cell_21,
            'cell_22': cell_22,
            'cell_23': cell_23,
            'cell_24': cell_24,
            'cell_25': cell_25,
            'cell_26': cell_26,
            'cell_27': cell_27,

            'cell_30': cell_30,
            'cell_31': cell_31,
            'cell_32': cell_32,
            'cell_33': cell_33,
            'cell_34': cell_34,
            'cell_35': cell_35,
            'cell_36': cell_36,
            'cell_37': cell_37,

            'cell_40': cell_40,
            'cell_41': cell_41,
            'cell_42': cell_42,
            'cell_43': cell_43,
            'cell_44': cell_44,
            'cell_45': cell_45,
            'cell_46': cell_46,
            'cell_47': cell_47,

            'cell_50': cell_50,
            'cell_51': cell_51,
            'cell_52': cell_52,
            'cell_53': cell_53,
            'cell_54': cell_54,
            'cell_55': cell_55,
            'cell_56': cell_56,
            'cell_57': cell_57,

            'cell_60': cell_60,
            'cell_61': cell_61,
            'cell_62': cell_62,
            'cell_63': cell_63,
            'cell_64': cell_64,
            'cell_65': cell_65,
            'cell_66': cell_66,
            'cell_67': cell_67,

            'cell_70': cell_70,
            'cell_71': cell_71,
            'cell_72': cell_72,
            'cell_73': cell_73,
            'cell_74': cell_74,
            'cell_75': cell_75,
            'cell_76': cell_76,
            'cell_77': cell_77,

        }
    next_page = 'TeraChess/ '
    return render(request, 'TeraChess/html/gameUI.html', context)