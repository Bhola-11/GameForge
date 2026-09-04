from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Release, ReleaseChecklist
from .forms import ReleaseForm
from apps.audit.models import AuditLog

class ReleaseListView(LoginRequiredMixin, ListView):
    model = Release
    template_name = 'releases/release_list.html'
    context_object_name = 'releases'
    paginate_by = 15

    def get_queryset(self):
        qs = Release.objects.select_related('game', 'version').all()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(release_code__icontains=q)
        if status:
            qs = qs.filter(status=status)
        return qs

class ReleaseDetailView(LoginRequiredMixin, DetailView):
    model = Release
    template_name = 'releases/release_detail.html'
    context_object_name = 'release'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        r = self.get_object()
        ctx['checklist_items'] = r.checklists.all()
        return ctx

class ReleaseCreateView(LoginRequiredMixin, CreateView):
    model = Release
    form_class = ReleaseForm
    template_name = 'releases/release_form.html'
    success_url = reverse_lazy('releases:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        AuditLog.log_activity(user=self.request.user, action='PLAN_RELEASE', module='releases', description=f"Scheduled release {self.object.release_code} for {self.object.game.title}")
        messages.success(self.request, f"Release '{self.object.title}' scheduled.")
        return response

class ReleaseUpdateView(LoginRequiredMixin, UpdateView):
    model = Release
    form_class = ReleaseForm
    template_name = 'releases/release_form.html'
    success_url = reverse_lazy('releases:list')
