from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Bug, BugComment
from .forms import BugForm, BugCommentForm
from apps.notifications.models import Notification
from apps.audit.models import AuditLog

class BugListView(LoginRequiredMixin, ListView):
    model = Bug
    template_name = 'bugs/bug_list.html'
    context_object_name = 'bugs'
    paginate_by = 20

    def get_queryset(self):
        qs = Bug.objects.select_related('game', 'assigned_to', 'reporter').all()
        q = self.request.GET.get('q')
        severity = self.request.GET.get('severity')
        status = self.request.GET.get('status')
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(bug_id__icontains=q)
        if severity:
            qs = qs.filter(severity=severity)
        if status:
            qs = qs.filter(status=status)
        return qs

class BugDetailView(LoginRequiredMixin, DetailView):
    model = Bug
    template_name = 'bugs/bug_detail.html'
    context_object_name = 'bug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        bug = self.get_object()
        ctx['comments'] = bug.comments.select_related('author').all()
        ctx['comment_form'] = BugCommentForm()
        return ctx

class BugCreateView(LoginRequiredMixin, CreateView):
    model = Bug
    form_class = BugForm
    template_name = 'bugs/bug_form.html'
    success_url = reverse_lazy('bugs:list')

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        response = super().form_valid(form)
        if self.object.assigned_to and self.object.assigned_to != self.request.user:
            Notification.objects.create(
                recipient=self.object.assigned_to,
                sender=self.request.user,
                title=f"Bug Assigned: {self.object.bug_id}",
                message=f"Defect {self.object.title} [{self.object.get_severity_display()}] assigned to you.",
                notification_type='BUG_FILED',
                link=f"/bugs/{self.object.id}/"
            )
        AuditLog.log_activity(user=self.request.user, action='REPORT_BUG', module='bugs', description=f"Filed bug {self.object.bug_id}: {self.object.title}")
        messages.success(self.request, f"Bug {self.object.bug_id} filed successfully.")
        return response

class BugUpdateView(LoginRequiredMixin, UpdateView):
    model = Bug
    form_class = BugForm
    template_name = 'bugs/bug_form.html'
    success_url = reverse_lazy('bugs:list')

@login_required
def add_bug_comment(request, pk):
    bug = get_object_or_404(Bug, pk=pk)
    if request.method == 'POST':
        form = BugCommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.bug = bug
            c.author = request.user
            c.save()
            messages.success(request, "QA note posted.")
    return redirect('bugs:detail', pk=bug.pk)
