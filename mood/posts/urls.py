from django.urls import path
from posts import views


urlpatterns = [
    path('post/<int:post_id>/', views.get_post, name='get_post'),
    path('add_post/', views.add_post, name='add_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('all_posts/<slug:username>/<int:index_page>/', views.get_all_posts, name='all_posts'),
    path('saved/', views.get_saved_posts, name='saved_posts')
]
