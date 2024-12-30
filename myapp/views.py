from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student, Teacher, Administrator, Class
from .forms import StudentForm, TeacherForm, AdministratorForm
from .models import Subject

# Главная страница
def main_page(request):
    return render(request, 'main_page.html')


# Страница логина
def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        # Проверка для Student
        student = Student.objects.filter(student_id=user_id).first()
        if student and password == student.password:
            request.session['user_id'] = student.student_id  # Сохраняем ID в сессии
            request.session['user_type'] = 'student'
            return redirect('student_menu')

        # Проверка для Teacher
        teacher = Teacher.objects.filter(teacher_id=user_id).first()
        if teacher and password == teacher.password:
            request.session['user_id'] = teacher.teacher_id  # Сохраняем ID в сессии
            request.session['user_type'] = 'teacher'
            return redirect('teacher_menu')

        # Проверка для Administrator
        administrator = Administrator.objects.filter(administrator_id=user_id).first()
        if administrator and password == administrator.password:
            request.session['user_id'] = administrator.administrator_id  # Сохраняем ID в сессии
            request.session['user_type'] = 'admin'
            return redirect('admin_menu')

        messages.error(request, "Неверный ID или пароль.")
        return redirect('login')

    return render(request, 'login_page.html')


# Страница профиля
def profile(request):
    user = None
    user_type = None

    # Определяем пользователя по ID (для примера, здесь это session или GET-параметры)
    user_id = request.session.get('user_id')  # ID пользователя берётся из сессии

    if not user_id:
        messages.error(request, "Вы не авторизованы. Пожалуйста, войдите в систему.")
        return redirect('login')

    # Определяем роль пользователя
    try:
        if Student.objects.filter(student_id=user_id).exists():
            user = Student.objects.get(student_id=user_id)
            user_type = 'student'
        elif Teacher.objects.filter(teacher_id=user_id).exists():
            user = Teacher.objects.get(teacher_id=user_id)
            user_type = 'teacher'
        elif Administrator.objects.filter(administrator_id=user_id).exists():
            user = Administrator.objects.get(administrator_id=user_id)
            user_type = 'admin'
    except Exception as e:
        messages.error(request, "Ошибка при загрузке данных профиля.")
        return render(request, 'profile.html', {'user': None, 'user_type': None})

    # Обработка смены пароля
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            # Проверяем старый пароль
            if old_password == user.password:
                user.password = new_password  # Прямое обновление пароля
                user.save()
                messages.success(request, "Пароль успешно изменен.")
            else:
                messages.error(request, "Старый пароль неверен.")
        else:
            messages.error(request, "Новый пароль и подтверждение не совпадают.")

    return render(request, 'profile.html', {
        'user': user,
        'user_type': user_type,
    })


# Страница пользователей
def users_page(request):
    teachers = Teacher.objects.all()
    students = Student.objects.all()
    administrators = Administrator.objects.all()
    return render(request, 'admin/users_page.html', {
        'teachers': teachers,
        'students': students,
        'administrators': administrators,
    })


# Добавить ученика
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ученик добавлен!")
            return redirect('users_page')
    else:
        form = StudentForm()
    return render(request, 'admin/add_user.html', {'form': form, 'user_type': 'student'})


# Добавить учителя
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Учитель добавлен!")
            return redirect('users_page')
    else:
        form = TeacherForm()
    return render(request, 'admin/add_user.html', {'form': form, 'user_type': 'teacher'})


# Добавить администратора
def add_administrator(request):
    if request.method == 'POST':
        form = AdministratorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Администратор добавлен!")
            return redirect('users_page')
    else:
        form = AdministratorForm()
    return render(request, 'admin/add_user.html', {'form': form, 'user_type': 'administrator'})


# Редактировать ученика
def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные ученика обновлены!")
            return redirect('users_page')
    else:
        form = StudentForm(instance=student)
    return render(request, 'admin/edit_user.html', {'form': form, 'user_type': 'student'})


# Редактировать учителя
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные учителя обновлены!")
            return redirect('users_page')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'admin/edit_user.html', {'form': form, 'user_type': 'teacher'})


# Редактировать администратора
def edit_administrator(request, administrator_id):
    administrator = get_object_or_404(Administrator, administrator_id=administrator_id)
    if request.method == 'POST':
        form = AdministratorForm(request.POST, instance=administrator)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные администратора обновлены!")
            return redirect('users_page')
    else:
        form = AdministratorForm(instance=administrator)
    return render(request, 'admin/edit_user.html', {'form': form, 'user_type': 'administrator'})


# Удалить пользователя
def delete_user(request, user_type, user_id):
    if user_type == 'student':
        user = get_object_or_404(Student, student_id=user_id)
    elif user_type == 'teacher':
        user = get_object_or_404(Teacher, teacher_id=user_id)
    else:
        user = get_object_or_404(Administrator, administrator_id=user_id)

    user.delete()
    messages.success(request, f"{user_type.capitalize()} удален!")
    return redirect('users_page')


# Страница меню ученика
def student_menu(request):
    return render(request, 'student_menu.html')


# Страница меню учителя
def teacher_menu(request):
    return render(request, 'teacher_menu.html')


# Страница меню администратора
def admin_menu(request):
    return render(request, 'admin_menu.html')


# Страница изменения пароля
def change_password(request):
    return render(request, 'change_password.html')


# Страница учителей
def teachers_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'admin/teachers_list.html', {'teachers': teachers})

# Страница учеников по классам
def students_list(request):
    class_filter = request.GET.get('class_filter')  # Получаем ID класса из GET-запроса
    classes = Class.objects.all()  # Загружаем список всех классов

    if class_filter and class_filter.isdigit():
        students = Student.objects.filter(student_class_id=int(class_filter)).select_related('student_class')
    else:
        students = Student.objects.select_related('student_class').all()

    return render(request, 'admin/students_list.html', {
        'students': students,
        'classes': classes,
        'selected_class': class_filter,  # Передаем выбранный класс в шаблон
    })

# Страница администраторов
def administrators_list(request):
    administrators = Administrator.objects.all()
    return render(request, 'admin/administrators_list.html', {'administrators': administrators})


from .models import Office


def is_admin(user):
    return user.is_authenticated and user.is_staff


# Просмотр списка кабинетов
def offices_list(request):
    offices = Office.objects.all()
    user_type = request.session.get('user_type')
    return render(request, 'offices/offices_list.html', {'offices': offices, 'user_type': user_type})


# Добавить кабинет (только для администратора)
def add_office(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        description = request.POST.get('description')
        Office.objects.create(room_number=room_number, description=description)
        messages.success(request, "Кабинет добавлен!")
        return redirect('offices_list')
    return render(request, 'offices/add_office.html')


# Редактировать кабинет (только для администратора)

def edit_office(request, office_id):
    office = get_object_or_404(Office, pk=office_id)
    if request.method == 'POST':
        office.room_number = request.POST.get('room_number')
        office.description = request.POST.get('description')
        office.save()
        messages.success(request, "Кабинет обновлен!")
        return redirect('offices_list')
    return render(request, 'offices/edit_office.html', {'office': office})


# Удалить кабинет (только для администратора)

def delete_office(request, office_id):
    office = get_object_or_404(Office, pk=office_id)
    office.delete()
    messages.success(request, "Кабинет удален!")
    return redirect('offices_list')


def class_details(request, class_id):
    class_obj = get_object_or_404(Class, pk=class_id)
    students = Student.objects.filter(student_class=class_obj)

    return render(request, 'classes/templates/class_details.html', {
        'class_obj': class_obj,
        'students': students,
    })


def classes_list(request):
    classes = Class.objects.all()  # Получаем все классы
    return render(request, 'classes/classes_list.html', {'classes': classes})


def add_class(request):
    if request.method == 'POST':
        class_number = request.POST.get('class_number')
        class_letter = request.POST.get('class_letter')
        student_count = request.POST.get('student_count', 0)

        # Создание нового класса
        Class.objects.create(
            class_number=class_number,
            class_letter=class_letter,
            student_count=student_count
        )
        messages.success(request, "Класс успешно добавлен!")
        return redirect('classes_list')

    return render(request, 'classes/add_class.html')


def delete_class(request, class_id):
    class_obj = get_object_or_404(Class, class_id=class_id)
    class_obj.delete()
    messages.success(request, "Класс успешно удален!")
    return redirect('classes_list')


# Просмотр списка предметов
def subjects_list(request):
    subjects = Subject.objects.all()  # Получаем все предметы
    return render(request, 'subjects/subjects_list.html', {'subjects': subjects})

# Добавить предмет
def add_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Subject.objects.create(name=name)
            messages.success(request, "Предмет успішно додано!")
            return redirect('subjects_list')
        else:
            messages.error(request, "Назва предмету не може бути порожньою.")
    return render(request, 'subjects/add_subject.html')

# Удалить предмет
def delete_subject(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    subject.delete()
    messages.success(request, "Предмет успішно видалено!")
    return redirect('subjects_list')