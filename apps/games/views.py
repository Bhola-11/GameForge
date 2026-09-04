from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Game, GameMilestone
from .forms import GameForm
from apps.audit.models import AuditLog

class GameListView(LoginRequiredMixin, ListView):
    model = Game
    template_name = 'games/game_list.html'
    context_object_name = 'games'
    paginate_by = 12

    def get_queryset(self):
        qs = Game.objects.select_related('organization').all()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(genre__icontains=q)
        if status:
            qs = qs.filter(status=status)
        return qs

class GameDetailView(LoginRequiredMixin, DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        game = self.get_object()
        ctx['projects'] = game.projects.all()
        ctx['versions'] = game.versions.all()
        ctx['builds'] = game.builds.order_by('-build_date')[:6]
        ctx['bugs_count'] = game.bugs.filter(status__in=['OPEN', 'CONFIRMED', 'IN_PROGRESS']).count()
        ctx['milestones'] = game.milestones.all()
        return ctx

class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = 'games/game_form.html'
    success_url = reverse_lazy('games:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        AuditLog.log_activity(user=self.request.user, action='CREATE_GAME', module='games', description=f"Registered new game title: {self.object.title}")
        messages.success(self.request, f"Game title '{self.object.title}' added to catalog.")
        return response

class GameUpdateView(LoginRequiredMixin, UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'games/game_form.html'
    success_url = reverse_lazy('games:list')
