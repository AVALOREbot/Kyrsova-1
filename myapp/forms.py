from django import forms
from .models import Student, Teacher, Administrator, Class, Subject, Office

# Форма для добавления и редактирования ученика
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'date_of_birth', 'address', 'student_class', 'password']

# Форма для добавления и редактирования учителя
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'first_name', 'last_name', 'subject', 'certification_category', 'office', 'password']

# Форма для добавления и редактирования администратора
class AdministratorForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ['administrator_id', 'password']
