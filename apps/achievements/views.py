from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Achievement, PlayerAchievement
from .forms import AchievementForm
from apps.audit.models import AuditLog

class AchievementListView(LoginRequiredMixin, ListView):
    model = Achievement
    template_name = 'achievements/achievement_list.html'
    context_object_name = 'achievements'
    paginate_by = 20

    def get_queryset(self):
        qs = Achievement.objects.select_related('game').all()
        q = self.request.GET.get('q')
        game_id = self.request.GET.get('game')
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(description__icontains=q)
        if game_id:
            qs = qs.filter(game_id=game_id)
        return qs

class AchievementDetailView(LoginRequiredMixin, DetailView):
    model = Achievement
    template_name = 'achievements/achievement_detail.html'
    context_object_name = 'achievement'

class AchievementCreateView(LoginRequiredMixin, CreateView):
    model = Achievement
    form_class = AchievementForm
    template_name = 'achievements/achievement_form.html'
    success_url = reverse_lazy('achievements:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        AuditLog.log_activity(user=self.request.user, action='CREATE_ACHIEVEMENT', module='achievements', description=f"Created achievement '{self.object.name}' for {self.object.game.title}")
        messages.success(self.request, f"Achievement '{self.object.name}' registered.")
        return response

class AchievementUpdateView(LoginRequiredMixin, UpdateView):
    model = Achievement
    form_class = AchievementForm
    template_name = 'achievements/achievement_form.html'
    success_url = reverse_lazy('achievements:list')
