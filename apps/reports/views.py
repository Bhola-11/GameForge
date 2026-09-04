from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.games.models import Game
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.bugs.models import Bug
from apps.builds.models import Build
from apps.monetization.models import Transaction
from .models import ReportTemplate

@login_required
def report_list_view(request):
    reports = ReportTemplate.objects.all()
    return render(request, 'reports/report_list.html', {'reports': reports})

@login_required
def report_detail_view(request, pk):
    report = get_object_or_404(ReportTemplate, pk=pk)
    
    total_games = Game.objects.count()
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='COMPLETED').count()
    total_bugs = Bug.objects.count()
    resolved_bugs = Bug.objects.filter(status='CLOSED').count()
    total_builds = Build.objects.count()
    total_revenue = sum(t.amount for t in Transaction.objects.filter(status='COMPLETED'))

    return render(request, 'reports/report_detail.html', {
        'report': report,
        'total_games': total_games,
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'total_bugs': total_bugs,
        'resolved_bugs': resolved_bugs,
        'total_builds': total_builds,
        'total_revenue': total_revenue,
    })
