from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add/', views.add_task_view, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task_view, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task_view, name='delete_task'),
    path('toggle/<int:task_id>/', views.toggle_task_view, name='toggle_task'),

]