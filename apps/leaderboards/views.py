from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Leaderboard, LeaderboardEntry
from .forms import LeaderboardForm
from apps.audit.models import AuditLog

class LeaderboardListView(LoginRequiredMixin, ListView):
    model = Leaderboard
    template_name = 'leaderboards/leaderboard_list.html'
    context_object_name = 'leaderboards'

    def get_queryset(self):
        return Leaderboard.objects.select_related('game').all()

class LeaderboardDetailView(LoginRequiredMixin, DetailView):
    model = Leaderboard
    template_name = 'leaderboards/leaderboard_detail.html'
    context_object_name = 'leaderboard'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lb = self.get_object()
        ctx['entries'] = lb.entries.select_related('player').all()[:50]
        return ctx

class LeaderboardCreateView(LoginRequiredMixin, CreateView):
    model = Leaderboard
    form_class = LeaderboardForm
    template_name = 'leaderboards/leaderboard_form.html'
    success_url = reverse_lazy('leaderboards:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        AuditLog.log_activity(user=self.request.user, action='CREATE_LEADERBOARD', module='leaderboards', description=f"Created leaderboard '{self.object.name}'")
        messages.success(self.request, f"Leaderboard '{self.object.name}' created.")
        return response

class LeaderboardUpdateView(LoginRequiredMixin, UpdateView):
    model = Leaderboard
    form_class = LeaderboardForm
    template_name = 'leaderboards/leaderboard_form.html'
    success_url = reverse_lazy('leaderboards:list')
