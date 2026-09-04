from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Project, ProjectMember, ProjectRisk
from .forms import ProjectForm
from apps.audit.models import AuditLog

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 15

    def get_queryset(self):
        qs = Project.objects.select_related('game', 'organization', 'lead').all()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(game__title__icontains=q)
        if status:
            qs = qs.filter(status=status)
        return qs

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        p = self.get_object()
        ctx['tasks'] = p.tasks.select_related('assigned_to').all()[:10]
        ctx['members'] = p.memberships.select_related('user').all()
        ctx['risks'] = p.risks.all()
        return ctx

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        AuditLog.log_activity(user=self.request.user, action='CREATE_PROJECT', module='projects', description=f"Initiated project '{self.object.title}'")
        messages.success(self.request, f"Project '{self.object.title}' created.")
        return response

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:list')
