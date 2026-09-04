from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.games.models import Game
from apps.players.models import Player
from apps.bugs.models import Bug
from apps.monetization.models import Transaction
from .models import DailyMetric, GameAnalyticsEvent

@login_required
def analytics_overview_view(request):
    games = Game.objects.all()
    selected_game_id = request.GET.get('game')
    
    selected_game = None
    if selected_game_id:
        selected_game = Game.objects.filter(id=selected_game_id).first()
    if not selected_game and games.exists():
        selected_game = games.first()

    metrics = DailyMetric.objects.filter(game=selected_game).order_by('metric_date')[:30] if selected_game else []
    recent_events = GameAnalyticsEvent.objects.filter(game=selected_game).select_related('player')[:15] if selected_game else []

    total_players = Player.objects.count()
    total_revenue = sum(t.amount for t in Transaction.objects.filter(status='COMPLETED'))
    open_bugs_count = Bug.objects.filter(status__in=['OPEN', 'CONFIRMED']).count()

    context = {
        'games': games,
        'selected_game': selected_game,
        'metrics': metrics,
        'recent_events': recent_events,
        'total_players': total_players,
        'total_revenue': total_revenue,
        'open_bugs_count': open_bugs_count,
    }
    return render(request, 'analytics/overview.html', context)
