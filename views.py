
# tasks/views.py
from django.shortcuts import render, redirect
from .models import Task
import csv
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import json
from .forms import TaskForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
def task_list(request):
    tasks = Task.objects.all()
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'form': form})

def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('/')
def update_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    task.complete = not task.complete
    task.save()
    return redirect('/')
# tasks/views.py

def edit_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'tasks/edit_task.html', {'form': form})
def register_user(request):
    if request.user.is_authenticated:
        return redirect('task_list')

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')

    return render(request, 'tasks/register.html', {'form': form})
@login_required
def task_list(request):
    tasks = Task.objects.all()
    
    ...
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)  # ✅ Filter by user
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # ✅ Set the current user
            task.save()
            return redirect('/')
            
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'form': form})
@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.delete()
    return redirect('/')
@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    ...
@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    ...

@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        task.complete = not task.complete
        task.save()
        return redirect('/')  # ✅ return something!
@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    # ✅ Add return statement for GET request
    return render(request, 'tasks/edit_task.html', {'form': form})
@login_required
def task_list(request):
    query = request.GET.get('search')  # 🆕 Get search keyword

    if query:
        tasks = Task.objects.filter(user=request.user, title__icontains=query)
    else:
        tasks = Task.objects.filter(user=request.user)

    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('/')

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'form': form})
# Create your views here.
@login_required
def task_list(request):
    query = request.GET.get('search')

    if query:
        tasks = Task.objects.filter(user=request.user, title__icontains=query)
    else:
        tasks = Task.objects.filter(user=request.user)

    # 🧮 Task Stats
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(complete=True).count()
    pending_tasks = total_tasks - completed_tasks

    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('/')

    context = {
        'tasks': tasks,
        'form': form,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
    }

    return render(request, 'tasks/task_list.html', context)
@login_required
def export_tasks_csv(request):
    # Filter tasks for the logged-in user
    tasks = Task.objects.filter(user=request.user)

    # Create HTTP response with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=tasks.csv'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Complete', 'Due Date', 'Priority'])

    for task in tasks:
        writer.writerow([
            task.title,
            'Yes' if task.complete else 'No',
            task.due_date or '',
            task.priority
        ])

    return response
@login_required
def calendar_view(request):
    return render(request, 'tasks/calendar.html')

@login_required
def get_tasks_json(request):
    tasks = Task.objects.filter(user=request.user, due_date__isnull=False)
    data = []

    for task in tasks:
        data.append({
            'title': task.title,
            'start': str(task.due_date),
            'color': '#28a745' if task.complete else '#dc3545',
        })

    return JsonResponse(data, safe=False, encoder=DjangoJSONEncoder)
def export_tasks_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Completed'])

    tasks = Task.objects.all()
    for task in tasks:
        writer.writerow([task.title, task.complete])

    return response

