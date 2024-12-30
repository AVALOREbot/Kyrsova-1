from django.contrib import admin
from django.urls import path, include  # Импортируем include для подключения приложений

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # Подключаем маршруты из myapp
]
