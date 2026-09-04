from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .models import SupportTicket, TicketMessage
from .forms import SupportTicketForm, TicketMessageForm
from apps.audit.models import AuditLog

class SupportTicketListView(LoginRequiredMixin, ListView):
    model = SupportTicket
    template_name = 'support/support_list.html'
    context_object_name = 'tickets'
    paginate_by = 20

    def get_queryset(self):
        qs = SupportTicket.objects.select_related('player', 'assigned_agent').all()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        if q:
            qs = qs.filter(subject__icontains=q) | qs.filter(ticket_id__icontains=q)
        if status:
            qs = qs.filter(status=status)
        return qs

class SupportTicketDetailView(LoginRequiredMixin, DetailView):
    model = SupportTicket
    template_name = 'support/support_detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        t = self.get_object()
        ctx['ticket_messages'] = t.messages.all()
        ctx['reply_form'] = TicketMessageForm()
        return ctx

class SupportTicketCreateView(LoginRequiredMixin, CreateView):
    model = SupportTicket
    form_class = SupportTicketForm
    template_name = 'support/support_form.html'
    success_url = reverse_lazy('support:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        AuditLog.log_activity(user=self.request.user, action='CREATE_TICKET', module='support', description=f"Created support ticket {self.object.ticket_id}")
        messages.success(self.request, f"Ticket {self.object.ticket_id} opened.")
        return response

@login_required
def add_ticket_reply(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    if request.method == 'POST':
        form = TicketMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.ticket = ticket
            msg.author = request.user
            msg.is_staff = True
            msg.save()
            ticket.status = 'WAITING'
            ticket.save()
            messages.success(request, "Reply sent to player.")
    return redirect('support:detail', pk=ticket.pk)
