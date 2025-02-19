from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='Blog-home'),
    path('search-posts/', views.search_posts, name='search-posts'),
    path('post/<int:post_id>/react/<str:reaction_type>/', views.update_reaction, name='update-reaction'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('popular-posts/', views.popular_posts, name='popular-posts'),
    path('about/', views.about, name="Blog-about"),
    path('donate/', views.donate, name='donate'),
    path('feedback/', views.feedback, name='feedback'),
]