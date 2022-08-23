from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from core import views as core_views
from posts import views as posts_views


urlpatterns = [
    path('', core_views.get_main_page, name='index'),
    path('register/', core_views.RegisterUser.as_view(), name='register'),
    path('login/', core_views.LoginUser.as_view(), name='login'),
    path('logout/', core_views.logout_user, name='logout'),
    path('profile/<slug:username>/', core_views.get_profile, name='profile'),
    path('profile/<slug:username>/profile_edit/', core_views.edit_user_profile, name='edit_profile'),
    path('posts/', include('posts.urls')),
    path('admin/', admin.site.urls),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
