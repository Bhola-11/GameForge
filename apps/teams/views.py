from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Team, TeamMember, TeamWorkload
from .forms import TeamForm, TeamMemberForm
from apps.audit.models import AuditLog

class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'

    def get_queryset(self):
        return Team.objects.select_related('organization', 'lead').prefetch_related('memberships').all()

class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        team = self.get_object()
        ctx['members'] = team.memberships.select_related('user').all()
        ctx['workloads'] = team.workload_logs.all()[:6]
        return ctx

class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_url = reverse_lazy('teams:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        AuditLog.log_activity(user=self.request.user, action='CREATE_TEAM', module='teams', description=f"Created team {self.object.name}")
        messages.success(self.request, f"Team '{self.object.name}' created.")
        return response

class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_url = reverse_lazy('teams:list')

@login_required
def add_team_member_view(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.team = team
            member.save()
            messages.success(request, f"{member.user.display_name} added to {team.name}.")
            return redirect('teams:detail', pk=team.pk)
    else:
        form = TeamMemberForm()
    return render(request, 'teams/add_member.html', {'form': form, 'team': team})
