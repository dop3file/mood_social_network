from django.contrib import admin
from django.urls import path
from core import views


urlpatterns = [
    path('', views.get_main_page, name='index'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.get_user_profile, name='profile'),
    path('profile/edit', views.edit_user_profile, name='edit_profile'),
    path('admin/', admin.site.urls),
]
