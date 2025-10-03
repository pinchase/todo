from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task


# ---------------- AUTH VIEWS ---------------- #

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'tasks/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')


# ---------------- MAIN VIEWS ---------------- #

def home_view(request):
    return render(request, 'tasks/home.html')


@login_required
def dashboard_view(request):
    tasks = Task.objects.filter(user=request.user)  # ✅ correct field
    return render(request, 'tasks/dashboard.html', {'tasks': tasks})


@login_required
def add_task_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if title:
            Task.objects.create(user=request.user, title=title, description=description)
            messages.success(request, 'Task added successfully')
            return redirect('dashboard')

    return render(request, 'tasks/add_task.html')


@login_required
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # ✅ correct field
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description', '')
        task.save()
        messages.success(request, 'Task updated successfully')
        return redirect('dashboard')

    return render(request, 'tasks/edit_task.html', {'task': task})


@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # ✅ correct field
    task.delete()
    messages.success(request, 'Task deleted successfully')
    return redirect('dashboard')


@login_required
def toggle_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # ✅ correct field
    task.completed = not task.completed
    task.save()
    return redirect('dashboard')
