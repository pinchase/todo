from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User


def send_welcome_email(user):
    """Send welcome email after successful signup"""
    subject = 'Welcome to To-Do App! 🎉'

    # Render HTML template
    html_content = render_to_string('tasks/emails/welcome_email.html', {
        'username': user.username,
        'dashboard_url': f"{settings.SITE_URL}/dashboard/",
    })

    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body='Welcome to To-Do App!',  # Plain text fallback
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending welcome email: {e}")
        return False


def send_verification_email(user, token):
    """Send email verification link"""
    subject = 'Verify Your Email Address 🔐'

    verification_url = f"{settings.SITE_URL}/verify-email/{token}/"

    # Render HTML template
    html_content = render_to_string('tasks/emails/verify_email.html', {
        'username': user.username,
        'verification_url': verification_url,
    })

    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=f'Click this link to verify your email: {verification_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return False


def send_password_reset_email(user, reset_url):
    """Send password reset email"""
    subject = 'Reset Your Password 🔑'

    # Render HTML template
    html_content = render_to_string('tasks/emails/password_reset_email.html', {
        'username': user.username,
        'reset_url': reset_url,
    })

    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=f'Click this link to reset your password: {reset_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending password reset email: {e}")
        return False