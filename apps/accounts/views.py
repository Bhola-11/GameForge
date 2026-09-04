from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, UserPreference
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, UserPreferenceForm
from apps.games.models import Game
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.bugs.models import Bug
from apps.builds.models import Build
from apps.releases.models import Release
from apps.players.models import Player
from apps.monetization.models import Transaction
from apps.support.models import SupportTicket
from apps.audit.models import AuditLog

@login_required
def dashboard_view(request):
    user = request.user
    
    total_games = Game.objects.count()
    active_projects = Project.objects.filter(status__in=['IN_PROGRESS', 'PLANNING']).count()
    open_bugs = Bug.objects.filter(status__in=['OPEN', 'CONFIRMED', 'IN_PROGRESS']).count()
    pending_tasks = Task.objects.filter(status__in=['TODO', 'IN_PROGRESS', 'REVIEW']).count()
    upcoming_releases = Release.objects.filter(status__in=['PLANNED', 'PREPARING', 'QA']).count()
    total_players = Player.objects.count()
    total_revenue = sum(t.amount for t in Transaction.objects.filter(status='COMPLETED'))
    support_tickets = SupportTicket.objects.filter(status__in=['OPEN', 'IN_PROGRESS']).count()

    my_tasks = Task.objects.filter(assigned_to=user).exclude(status='COMPLETED')[:6]
    my_bugs = Bug.objects.filter(assigned_to=user).exclude(status='CLOSED')[:6]
    recent_activities = AuditLog.objects.select_related('user')[:10]
    recent_builds = Build.objects.select_related('game', 'version')[:5]
    recent_games = Game.objects.all()[:4]

    context = {
        'total_games': total_games,
        'active_projects': active_projects,
        'open_bugs': open_bugs,
        'pending_tasks': pending_tasks,
        'upcoming_releases': upcoming_releases,
        'total_players': total_players,
        'total_revenue': total_revenue,
        'support_tickets': support_tickets,
        'my_tasks': my_tasks,
        'my_bugs': my_bugs,
        'recent_activities': recent_activities,
        'recent_builds': recent_builds,
        'recent_games': recent_games,
    }
    return render(request, 'accounts/dashboard.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            AuditLog.log_activity(user=user, action='LOGIN', module='accounts', description=f"User {user.username} signed in.")
            messages.success(request, f"Welcome back, {user.display_name}!")
            return redirect('accounts:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserPreference.objects.create(user=user)
            login(request, user)
            AuditLog.log_activity(user=user, action='REGISTER', module='accounts', description=f"New user registered: {user.username}")
            messages.success(request, "Account created successfully! Welcome to GameForge.")
            return redirect('accounts:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        AuditLog.log_activity(user=request.user, action='LOGOUT', module='accounts', description=f"User {request.user.username} signed out.")
        logout(request)
        messages.info(request, "You have been successfully logged out.")
    return redirect('accounts:login')

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            AuditLog.log_activity(user=user, action='UPDATE_PROFILE', module='accounts', description="Profile details updated.")
            messages.success(request, "Your profile has been updated.")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'accounts/profile.html', {'form': form, 'user_obj': user})

@login_required
def settings_view(request):
    user = request.user
    pref, _ = UserPreference.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=pref)
        if form.is_valid():
            form.save()
            messages.success(request, "Preferences saved.")
            return redirect('accounts:settings')
    else:
        form = UserPreferenceForm(instance=pref)
    return render(request, 'accounts/settings.html', {'form': form, 'pref': pref})

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 15

    def get_queryset(self):
        qs = User.objects.all().order_by('-date_joined')
        q = self.request.GET.get('q')
        role = self.request.GET.get('role')
        if q:
            qs = qs.filter(username__icontains=q) | qs.filter(first_name__icontains=q) | qs.filter(email__icontains=q)
        if role:
            qs = qs.filter(role=role)
        return qs

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'profile_user'
