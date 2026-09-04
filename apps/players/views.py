from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Player
from .forms import PlayerForm

class PlayerListView(LoginRequiredMixin, ListView):
    model = Player
    template_name = 'players/player_list.html'
    context_object_name = 'players'
    paginate_by = 25

    def get_queryset(self):
        qs = Player.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(username__icontains=q) | qs.filter(email__icontains=q)
        return qs

class PlayerDetailView(LoginRequiredMixin, DetailView):
    model = Player
    template_name = 'players/player_detail.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        p = self.get_object()
        ctx['achievements'] = p.unlocked_achievements.select_related('achievement').all()[:10]
        ctx['leaderboard_scores'] = p.leaderboard_scores.select_related('leaderboard').all()[:10]
        ctx['transactions'] = p.transactions.all()[:10]
        return ctx

class PlayerCreateView(LoginRequiredMixin, CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'players/player_form.html'
    success_url = reverse_lazy('players:list')

class PlayerUpdateView(LoginRequiredMixin, UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'players/player_form.html'
    success_url = reverse_lazy('players:list')
