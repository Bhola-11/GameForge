from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AuditLog

class AuditLogListView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = 'audit/audit_list.html'
    context_object_name = 'logs'
    paginate_by = 25

    def get_queryset(self):
        qs = AuditLog.objects.select_related('user').all()
        q = self.request.GET.get('q')
        module = self.request.GET.get('module')
        if q:
            qs = qs.filter(description__icontains=q) | qs.filter(action__icontains=q)
        if module:
            qs = qs.filter(module=module)
        return qs
