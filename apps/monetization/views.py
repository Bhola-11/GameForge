from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import InGameItem, Transaction
from .forms import InGameItemForm
from apps.audit.models import AuditLog

def monetization_dashboard_view(request):
    transactions = Transaction.objects.select_related('player', 'game', 'item').all()[:20]
    items = InGameItem.objects.select_related('game').all()
    
    total_sales = sum(t.amount for t in Transaction.objects.filter(status='COMPLETED'))
    refund_count = Transaction.objects.filter(status='REFUNDED').count()
    completed_count = Transaction.objects.filter(status='COMPLETED').count()

    return render(request, 'monetization/dashboard.html', {
        'transactions': transactions,
        'items': items,
        'total_sales': total_sales,
        'refund_count': refund_count,
        'completed_count': completed_count,
    })

class InGameItemCreateView(LoginRequiredMixin, CreateView):
    model = InGameItem
    form_class = InGameItemForm
    template_name = 'monetization/item_form.html'
    success_url = reverse_lazy('monetization:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        AuditLog.log_activity(user=self.request.user, action='CREATE_ITEM', module='monetization', description=f"Created store item '{self.object.name}' (${self.object.price})")
        messages.success(self.request, f"Item '{self.object.name}' created.")
        return response
