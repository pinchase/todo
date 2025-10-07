from django.urls import path
from . import views

urlpatterns = [
    # Home & Auth
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Email Verification
    path('verify-email/<uuid:token>/', views.verify_email_view, name='verify_email'),
    path('resend-verification/', views.resend_verification_view, name='resend_verification'),

    # Password Reset
    path('password-reset/', views.password_reset_request_view, name='password_reset_request'),
    path('password-reset/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),

    # Dashboard & Tasks
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add/', views.add_task_view, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task_view, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task_view, name='delete_task'),
    path('toggle/<int:task_id>/', views.toggle_task_view, name='toggle_task'),

     path('test-email/', views.test_email_view, name='test_email'),

    path('statistics/', views.statistics_view, name='statistics'),

# Subtasks
    path('subtask/add/<int:task_id>/', views.add_subtask_view, name='add_subtask'),
    path('subtask/toggle/<int:subtask_id>/', views.toggle_subtask_view, name='toggle_subtask'),
    path('subtask/delete/<int:subtask_id>/', views.delete_subtask_view, name='delete_subtask'),

]