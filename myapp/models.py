from django.db import models

# Класс (Class)
# Класс (Class)
class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_number = models.IntegerField()  # Номер класса (например, 1, 2, 3 и т.д.)
    class_letter = models.CharField(max_length=1)  # Буква класса (А, Б, В и т.д.)
    student_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['class_number', 'class_letter']  # Сортировка классов

    def __str__(self):
        return f"{self.class_number}{self.class_letter}"



# Предмет (Subject)
class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Кабинет (Office)
class Office(models.Model):
    office_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=10)  # Номер кабинета
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Room {self.room_number}"


# Учень (Student)
class Student(models.Model):
    student_id = models.CharField(max_length=20, primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Вчитель (Teacher)
class Teacher(models.Model):
    teacher_id = models.CharField(max_length=20, primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    certification_category = models.CharField(max_length=50)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Захід (Event)
class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    event_date = models.DateTimeField()
    organizer = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    participants = models.ManyToManyField(Student)

    def __str__(self):
        return self.name


# Розклад (Schedule)
class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    schedule_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    datetime = models.DateTimeField()

    def __str__(self):
        return f"Class {self.schedule_class} - {self.subject}"


# Адміністратор (Administrator)
class Administrator(models.Model):
    administrator_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"Admin {self.administrator_id}"


# Журнал дій (Action Log)
class ActionLog(models.Model):
    action_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    administrator = models.ForeignKey(Administrator, on_delete=models.SET_NULL, null=True, blank=True)
    action_date = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(
        max_length=50,
        choices=[('Added', 'Added'), ('Deleted', 'Deleted'), ('Updated', 'Updated')],
    )

    def __str__(self):
        return f"{self.action_type} on {self.action_date}"





