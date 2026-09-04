from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('accounts:dashboard') if request.user.is_authenticated else redirect('accounts:login'), name='root'),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('organizations/', include('apps.organizations.urls', namespace='organizations')),
    path('teams/', include('apps.teams.urls', namespace='teams')),
    path('games/', include('apps.games.urls', namespace='games')),
    path('projects/', include('apps.projects.urls', namespace='projects')),
    path('tasks/', include('apps.tasks.urls', namespace='tasks')),
    path('bugs/', include('apps.bugs.urls', namespace='bugs')),
    path('builds/', include('apps.builds.urls', namespace='builds')),
    path('assets/', include('apps.assets.urls', namespace='assets')),
    path('versions/', include('apps.versions.urls', namespace='versions')),
    path('releases/', include('apps.releases.urls', namespace='releases')),
    path('store/', include('apps.store.urls', namespace='store')),
    path('players/', include('apps.players.urls', namespace='players')),
    path('achievements/', include('apps.achievements.urls', namespace='achievements')),
    path('leaderboards/', include('apps.leaderboards.urls', namespace='leaderboards')),
    path('analytics/', include('apps.analytics.urls', namespace='analytics')),
    path('monetization/', include('apps.monetization.urls', namespace='monetization')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
    path('support/', include('apps.support.urls', namespace='support')),
    path('reports/', include('apps.reports.urls', namespace='reports')),
    path('permissions/', include('apps.permissions.urls', namespace='permissions')),
    path('audit/', include('apps.audit.urls', namespace='audit')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
