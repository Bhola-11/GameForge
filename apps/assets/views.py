from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Asset
from .forms import AssetForm
from apps.audit.models import AuditLog

class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = 'assets/asset_list.html'
    context_object_name = 'assets'
    paginate_by = 16

    def get_queryset(self):
        qs = Asset.objects.select_related('game', 'owner').all()
        q = self.request.GET.get('q')
        cat = self.request.GET.get('category')
        if q:
            qs = qs.filter(title__icontains=q)
        if cat:
            qs = qs.filter(category=cat)
        return qs

class AssetDetailView(LoginRequiredMixin, DetailView):
    model = Asset
    template_name = 'assets/asset_detail.html'
    context_object_name = 'asset'

class AssetCreateView(LoginRequiredMixin, CreateView):
    model = Asset
    form_class = AssetForm
    template_name = 'assets/asset_form.html'
    success_url = reverse_lazy('assets:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        AuditLog.log_activity(user=self.request.user, action='UPLOAD_ASSET', module='assets', description=f"Uploaded asset '{self.object.title}' ({self.object.get_category_display()})")
        messages.success(self.request, f"Asset '{self.object.title}' added to studio vault.")
        return response

class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = 'assets/asset_form.html'
    success_url = reverse_lazy('assets:list')
