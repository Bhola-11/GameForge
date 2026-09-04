from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import StoreListing
from .forms import StoreListingForm
from apps.audit.models import AuditLog

class StoreListView(LoginRequiredMixin, ListView):
    model = StoreListing
    template_name = 'store/store_list.html'
    context_object_name = 'listings'
    paginate_by = 15

    def get_queryset(self):
        qs = StoreListing.objects.select_related('game').all()
        q = self.request.GET.get('q')
        store = self.request.GET.get('store')
        if q:
            qs = qs.filter(game__title__icontains=q) | qs.filter(headline__icontains=q)
        if store:
            qs = qs.filter(store=store)
        return qs

class StoreDetailView(LoginRequiredMixin, DetailView):
    model = StoreListing
    template_name = 'store/store_detail.html'
    context_object_name = 'listing'

class StoreCreateView(LoginRequiredMixin, CreateView):
    model = StoreListing
    form_class = StoreListingForm
    template_name = 'store/store_form.html'
    success_url = reverse_lazy('store:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        AuditLog.log_activity(user=self.request.user, action='CREATE_STORE_LISTING', module='store', description=f"Created store listing for {self.object.game.title} on {self.object.get_store_display()}")
        messages.success(self.request, f"Store listing created.")
        return response

class StoreUpdateView(LoginRequiredMixin, UpdateView):
    model = StoreListing
    form_class = StoreListingForm
    template_name = 'store/store_form.html'
    success_url = reverse_lazy('store:list')
