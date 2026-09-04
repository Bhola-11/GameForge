from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.models import User
from .models import RolePermission

@login_required
def permissions_matrix_view(request):
    modules = ['games', 'projects', 'tasks', 'bugs', 'builds', 'assets', 'versions', 'releases', 'store', 'players', 'achievements', 'monetization', 'support', 'reports', 'audit']
    roles = User.Role.choices

    permissions = RolePermission.objects.all()
    matrix = {}
    for p in permissions:
        matrix[(p.role, p.module_name)] = p

    return render(request, 'permissions/matrix.html', {
        'modules': modules,
        'roles': roles,
        'matrix': matrix,
    })
