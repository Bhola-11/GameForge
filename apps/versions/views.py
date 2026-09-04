from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import GameVersion
from .forms import GameVersionForm
from apps.audit.models import AuditLog

class VersionListView(LoginRequiredMixin, ListView):
    model = GameVersion
    template_name = 'versions/version_list.html'
    context_object_name = 'versions'
    paginate_by = 20

    def get_queryset(self):
        qs = GameVersion.objects.select_related('game').all()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        if q:
            qs = qs.filter(version_number__icontains=q) | qs.filter(game__title__icontains=q)
        if status:
            qs = qs.filter(status=status)
        return qs

class VersionDetailView(LoginRequiredMixin, DetailView):
    model = GameVersion
    template_name = 'versions/version_detail.html'
    context_object_name = 'version'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        v = self.get_object()
        ctx['builds'] = v.builds.all()
        ctx['releases'] = v.releases.all()
        return ctx

class VersionCreateView(LoginRequiredMixin, CreateView):
    model = GameVersion
    form_class = GameVersionForm
    template_name = 'versions/version_form.html'
    success_url = reverse_lazy('versions:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        AuditLog.log_activity(user=self.request.user, action='CREATE_VERSION', module='versions', description=f"Created version {self.object.version_number} for {self.object.game.title}")
        messages.success(self.request, f"Version {self.object.version_number} created.")
        return response

class VersionUpdateView(LoginRequiredMixin, UpdateView):
    model = GameVersion
    form_class = GameVersionForm
    template_name = 'versions/version_form.html'
    success_url = reverse_lazy('versions:list')
