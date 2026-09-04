from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Organization, Department, OrgMember, OrgInvitation
from .forms import OrganizationForm, DepartmentForm, OrgInvitationForm
from apps.audit.models import AuditLog

class OrgListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = 'organizations/org_list.html'
    context_object_name = 'organizations'

    def get_queryset(self):
        return Organization.objects.filter(is_active=True).order_by('-created_at')

class OrgDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = 'organizations/org_detail.html'
    context_object_name = 'org'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        org = self.get_object()
        ctx['members'] = org.memberships.select_related('user', 'department')
        ctx['departments'] = org.departments.all()
        ctx['projects_count'] = org.projects.count() if hasattr(org, 'projects') else 0
        ctx['games_count'] = org.games.count() if hasattr(org, 'games') else 0
        return ctx

class OrgCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organizations/org_form.html'
    success_url = reverse_lazy('organizations:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        OrgMember.objects.create(
            organization=self.object,
            user=self.request.user,
            role=OrgMember.Role.OWNER
        )
        AuditLog.log_activity(user=self.request.user, action='CREATE_ORG', module='organizations', description=f"Created organization {self.object.name}")
        messages.success(self.request, f"Organization {self.object.name} created successfully!")
        return response

class OrgUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organizations/org_form.html'
    success_url = reverse_lazy('organizations:list')

@login_required
def invite_member_view(request, pk):
    org = get_object_or_404(Organization, pk=pk)
    if request.method == 'POST':
        form = OrgInvitationForm(request.POST)
        if form.is_valid():
            inv = form.save(commit=False)
            inv.organization = org
            inv.invited_by = request.user
            inv.save()
            messages.success(request, f"Invitation sent to {inv.email}.")
            return redirect('organizations:detail', pk=org.pk)
    else:
        form = OrgInvitationForm()
    return render(request, 'organizations/invite_form.html', {'form': form, 'org': org})
