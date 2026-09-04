from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Task, TaskComment, TaskTimeLog
from .forms import TaskForm, TaskCommentForm, TaskTimeLogForm
from apps.notifications.models import Notification
from apps.audit.models import AuditLog

@login_required
def task_board_view(request):
    tasks = Task.objects.select_related('project', 'assigned_to').all()
    
    project_id = request.GET.get('project')
    if project_id:
        tasks = tasks.filter(project_id=project_id)
        
    todo_tasks = tasks.filter(status='TODO')
    in_progress_tasks = tasks.filter(status='IN_PROGRESS')
    review_tasks = tasks.filter(status='REVIEW')
    testing_tasks = tasks.filter(status='TESTING')
    completed_tasks = tasks.filter(status='COMPLETED')

    return render(request, 'tasks/task_board.html', {
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'review_tasks': review_tasks,
        'testing_tasks': testing_tasks,
        'completed_tasks': completed_tasks,
    })

@login_required
def update_task_status_ajax(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Task.Status.choices):
            old_status = task.status
            task.status = new_status
            task.save()
            AuditLog.log_activity(user=request.user, action='UPDATE_TASK_STATUS', module='tasks', description=f"Task #{task.id} '{task.title}' moved from {old_status} to {new_status}")
            return JsonResponse({'success': True, 'new_status': new_status})
    return JsonResponse({'success': False}, status=400)

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20

    def get_queryset(self):
        qs = Task.objects.select_related('project', 'assigned_to').all()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        if q:
            qs = qs.filter(title__icontains=q)
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)
        return qs

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        task = self.get_object()
        ctx['comments'] = task.comments.select_related('author').all()
        ctx['comment_form'] = TaskCommentForm()
        ctx['time_logs'] = task.time_logs.select_related('user').all()
        ctx['timelog_form'] = TaskTimeLogForm()
        return ctx

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:board')

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        response = super().form_valid(form)
        if self.object.assigned_to and self.object.assigned_to != self.request.user:
            Notification.objects.create(
                recipient=self.object.assigned_to,
                sender=self.request.user,
                title=f"New Task Assigned: {self.object.title}",
                message=f"You have been assigned to task #{self.object.id} in {self.object.project.title}.",
                notification_type='TASK_ASSIGNED',
                link=f"/tasks/{self.object.id}/"
            )
        AuditLog.log_activity(user=self.request.user, action='CREATE_TASK', module='tasks', description=f"Created task #{self.object.id} '{self.object.title}'")
        messages.success(self.request, f"Task '{self.object.title}' created.")
        return response

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:board')

@login_required
def add_task_comment(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.task = task
            c.author = request.user
            c.save()
            messages.success(request, "Comment posted.")
    return redirect('tasks:detail', pk=task.pk)

@login_required
def log_task_time(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskTimeLogForm(request.POST)
        if form.is_valid():
            tl = form.save(commit=False)
            tl.task = task
            tl.user = request.user
            tl.save()
            task.actual_hours += tl.hours
            task.save()
            messages.success(request, f"Logged {tl.hours} hours.")
    return redirect('tasks:detail', pk=task.pk)
