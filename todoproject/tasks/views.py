from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task, EmailVerification
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from .forms import CustomUserCreationForm
from .utils import send_verification_email, send_welcome_email, send_password_reset_email


from django.http import JsonResponse
import resend
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta

# ---------------- AUTH VIEWS ---------------- #

def verify_email_view(request, token):
    try:
        verification = EmailVerification.objects.get(token=token)

        if verification.is_verified:
            messages.info(request, 'Your email is already verified!')
        elif verification.is_expired():
            messages.error(request, 'This verification link has expired. Please request a new one.')
        else:
            verification.is_verified = True
            verification.verified_at = timezone.now()
            verification.save()

            # Send welcome email after verification
            send_welcome_email(verification.user)

            messages.success(request, '✅ Email verified successfully! Welcome to To-Do App!')

        return redirect('dashboard')
    except EmailVerification.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('home')


# Resend Verification Email
@login_required
def resend_verification_view(request):
    try:
        verification = request.user.email_verification

        if verification.is_verified:
            messages.info(request, 'Your email is already verified!')
        else:
            send_verification_email(request.user, verification.token)
            messages.success(request, 'Verification email sent! Please check your inbox.')
    except EmailVerification.DoesNotExist:
        verification = EmailVerification.objects.create(user=request.user)
        send_verification_email(request.user, verification.token)
        messages.success(request, 'Verification email sent! Please check your inbox.')

    return redirect('dashboard')
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            verification = EmailVerification.objects.create(user=user)

            send_verification_email(user, verification.token)

            login(request, user)
            messages.success(request, f'Account created successfully! Please check your email ({user.email}) to verify your account.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'tasks/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcom eback,{user.user.name}!')
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
    tasks = Task.objects.filter(user=request.user)

    # Check if email is verified
    is_email_verified = False
    try:
        is_email_verified = request.user.email_verification.is_verified
    except EmailVerification.DoesNotExist:
        pass

    context = {
        'tasks': tasks,
        'is_email_verified': is_email_verified,
    }
    return render(request, 'tasks/dashboard.html', context)


# Add Task
@login_required
def add_task_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'medium')
        category = request.POST.get('category', 'other')
        due_date = request.POST.get('due_date', '')

        if title:
            task_data = {
                'user': request.user,
                'title': title,
                'description': description,
                'priority': priority,
                'category': category,
            }

            # Add due_date if provided
            if due_date:
                from django.utils.dateparse import parse_datetime
                parsed_date = parse_datetime(due_date)
                if parsed_date:
                    task_data['due_date'] = parsed_date

            Task.objects.create(**task_data)
            messages.success(request, 'Task added successfully!')
            return redirect('dashboard')

        # Pass choices to template
    context = {
        'priority_choices': Task.PRIORITY_CHOICES,
        'category_choices': Task.CATEGORY_CHOICES,
    }
    return render(request, 'tasks/add_task.html', context)


# Edit Task
@login_required
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description', '')
        task.priority = request.POST.get('priority', 'medium')
        task.category = request.POST.get('category', 'other')
        due_date = request.POST.get('due_date', '')

        # Update due_date
        if due_date:
            from django.utils.dateparse import parse_datetime
            parsed_date = parse_datetime(due_date)
            if parsed_date:
                task.due_date = parsed_date
        else:
            task.due_date = None

        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('dashboard')

        # Pass choices and task to template
    context = {
        'task': task,
        'priority_choices': Task.PRIORITY_CHOICES,
        'category_choices': Task.CATEGORY_CHOICES,
    }
    return render(request, 'tasks/edit_task.html', context)

# Delete Task
@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('dashboard')


# Toggle Task Completion
@login_required
def toggle_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('dashboard')


# Password Reset Request View
def password_reset_request_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create reset URL
            reset_url = f"{settings.SITE_URL}/password-reset/{uid}/{token}/"

            # Send email
            send_password_reset_email(user, reset_url)

            messages.success(request, 'Password reset email sent! Please check your inbox.')
            return redirect('login')
        except User.DoesNotExist:
            # Don't reveal if email exists or not (security)
            messages.success(request, 'If that email exists, a password reset link has been sent.')
            return redirect('login')

    return render(request, 'tasks/password_reset_request.html')


# Password Reset Confirm View
def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, 'Password reset successful! You can now login.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match!')

        return render(request, 'tasks/password_reset_confirm.html', {'validlink': True})
    else:
        messages.error(request, 'Password reset link is invalid or has expired.')
        return redirect('password_reset_request')


def test_email_view(request):
    """Test if Resend works on production"""
    try:
        # Check if API key exists
        api_key = getattr(settings, 'RESEND_API_KEY', None)
        if not api_key:
            return JsonResponse({
                'status': 'error',
                'message': 'RESEND_API_KEY not found in settings'
            })

        # Try to send test email
        resend.api_key = api_key

        params = {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": ["your-email@gmail.com"],  # Replace with YOUR email
            "subject": "Test from Production",
            "html": "<p>This is a test email from production server</p>"
        }

        response = resend.Emails.send(params)

        return JsonResponse({
            'status': 'success',
            'message': 'Email sent!',
            'response': str(response)
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'type': type(e).__name__
        })


@login_required
def statistics_view(request):
    """Show detailed statistics and charts"""
    user_tasks = Task.objects.filter(user=request.user)

    # Overall stats
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    overdue_tasks = user_tasks.filter(
        due_date__lt=timezone.now(),
        completed=False
    ).count()

    # Completion rate
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Tasks by priority
    priority_stats = {
        'low': user_tasks.filter(priority='low').count(),
        'medium': user_tasks.filter(priority='medium').count(),
        'high': user_tasks.filter(priority='high').count(),
        'urgent': user_tasks.filter(priority='urgent').count(),
    }

    # Tasks by category
    category_stats = {}
    for value, label in Task.CATEGORY_CHOICES:
        category_stats[label] = user_tasks.filter(category=value).count()

    # Tasks completed in last 7 days
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_completions = user_tasks.filter(
        completed=True,
        updated_at__gte=seven_days_ago
    ).annotate(
        date=TruncDate('updated_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    # Prepare data for chart (last 7 days)
    daily_completions = {}
    for i in range(7):
        date = (timezone.now() - timedelta(days=i)).date()
        daily_completions[date.strftime('%Y-%m-%d')] = 0

    for item in recent_completions:
        date_str = item['date'].strftime('%Y-%m-%d')
        if date_str in daily_completions:
            daily_completions[date_str] = item['count']

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'completion_rate': round(completion_rate, 1),
        'priority_stats': priority_stats,
        'category_stats': category_stats,
        'daily_completions': daily_completions,
    }

    return render(request, 'tasks/statistics.html', context)