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
    path('profile/profile_edit/', core_views.edit_user_profile, name='edit_profile'),
    path('profile/<slug:username>/', core_views.get_profile, name='profile'),
    path('delete_interest/<int:interest_id>', core_views.delete_interest, name='delete_interest'),
    path('notifications/', include('notifications.urls')),
    path('follow/<int:user_id>', core_views.follow, name='follow'),
    path('posts/', include('posts.urls')),
    path('feed/<int:index_page>/', posts_views.get_feed, name='feed'),
    path('admin/', admin.site.urls),
    path('search/', core_views.search, name='search'),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handle404 = 'core.views.handle_404'
handle500 = 'core.views.handle_500'
