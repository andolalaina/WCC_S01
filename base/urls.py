from django.urls import path
from .views import index, login_view, users, users_request, users_requests, employees, employees_requests, filler, manage_view, logout_view, request_pdf, employees_edit_user, manage_edit_employee

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('users/', users, name='users'),
    path('users/request/', users_request, name='user_make_request'),
    path('users/requests/', users_requests, name='user_requests'),
    path('employees/', employees, name='employees'),
    path('employees/requests/', employees_requests, name='employees_requests'),
    path('employees/requests/<int:request_id>/pdf', request_pdf, name='request_pdf'),
    path('employees/edit/<int:person_id>',employees_edit_user , name='edit_user'),
    path('filler/', filler, name='filler'),
    path('manage/', manage_view, name='manager'),
    path('manage/edit/<int:person_id>', manage_edit_employee, name='edit_employee'),
    path('logout/', logout_view, name='logout'),
]
