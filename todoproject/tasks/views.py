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
from .forms import CustomUserCreationForm
from .utils import send_verification_email, send_welcome_email, send_password_reset_email


from django.http import JsonResponse
import resend

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

        if title:
            Task.objects.create(user=request.user, title=title, description=description)
            messages.success(request, 'Task added successfully!')
            return redirect('dashboard')
    return render(request, 'tasks/add_task.html')


# Edit Task
@login_required
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description', '')
        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('dashboard')

    return render(request, 'tasks/edit_task.html', {'task': task})


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
