from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Build
from .forms import BuildForm
from apps.audit.models import AuditLog

class BuildListView(LoginRequiredMixin, ListView):
    model = Build
    template_name = 'builds/build_list.html'
    context_object_name = 'builds'
    paginate_by = 20

    def get_queryset(self):
        qs = Build.objects.select_related('game', 'developer').all()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        platform = self.request.GET.get('platform')
        if q:
            qs = qs.filter(game__title__icontains=q) | qs.filter(branch_name__icontains=q)
        if status:
            qs = qs.filter(status=status)
        if platform:
            qs = qs.filter(platform=platform)
        return qs

class BuildDetailView(LoginRequiredMixin, DetailView):
    model = Build
    template_name = 'builds/build_detail.html'
    context_object_name = 'build'

class BuildCreateView(LoginRequiredMixin, CreateView):
    model = Build
    form_class = BuildForm
    template_name = 'builds/build_form.html'
    success_url = reverse_lazy('builds:list')

    def form_valid(self, form):
        form.instance.developer = self.request.user
        response = super().form_valid(form)
        AuditLog.log_activity(user=self.request.user, action='TRIGGER_BUILD', module='builds', description=f"Registered build #{self.object.build_number} for {self.object.game.title}")
        messages.success(self.request, f"Build #{self.object.build_number} registered.")
        return response

class BuildUpdateView(LoginRequiredMixin, UpdateView):
    model = Build
    form_class = BuildForm
    template_name = 'builds/build_form.html'
    success_url = reverse_lazy('builds:list')
