from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import PieceSet, Piece, Player, PieceInstance, User
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core import serializers
from django.views.generic import View
from .forms import UserForm, PieceSetForm, PieceInstanceForm
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth import logout
from django.views.generic.edit import FormView


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



