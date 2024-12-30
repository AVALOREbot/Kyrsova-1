from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('login/', views.login_view, name='login'),
    path('student_menu/', views.student_menu, name='student_menu'),
    path('teacher_menu/', views.teacher_menu, name='teacher_menu'),
    path('admin_menu/', views.admin_menu, name='admin_menu'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('users/', views.users_page, name='users_page'),
    path('teachers/', views.teachers_list, name='teachers_list'),
    path('students/', views.students_list, name='students_list'),
    path('administrators/', views.administrators_list, name='administrators_list'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('edit_teacher/<str:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('add_student/', views.add_student, name='add_student'),
    path('edit_student/<str:student_id>/', views.edit_student, name='edit_student'),
    path('add_administrator/', views.add_administrator, name='add_administrator'),
    path('edit_administrator/<str:administrator_id>/', views.edit_administrator, name='edit_administrator'),
    path('delete_user/<str:user_type>/<str:user_id>/', views.delete_user, name='delete_user'),  # Удалить пользователя
    path('offices/', views.offices_list, name='offices_list'),
    path('offices/add/', views.add_office, name='add_office'),
    path('offices/edit/<int:office_id>/', views.edit_office, name='edit_office'),
    path('offices/delete/<int:office_id>/', views.delete_office, name='delete_office'),
    path('class/<int:class_id>/', views.class_details, name='class_details'),
    path('classes/', views.classes_list, name='classes_list'),
    path('classes/add/', views.add_class, name='add_class'),
    path('classes/delete/<int:class_id>/', views.delete_class, name='delete_class'),
    path('subjects/', views.subjects_list, name='subjects_list'),
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('subjects/delete/<int:subject_id>/', views.delete_subject, name='delete_subject'),
]
