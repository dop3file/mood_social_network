from django.contrib import admin
from django.urls import path
from core import views


urlpatterns = [
    path('', views.get_main_page, name='index'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('admin/', admin.site.urls),
]
