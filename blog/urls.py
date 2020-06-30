from django.urls import path
from . import views
from .views import AboutView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView


urlpatterns = [
    path('', views.home, name='home-blog'),
    path('about/', views.about, name='about-blog'),
    path('create/', views.create, name='create'),
    path('post/<int:post_id>/', views.detail, name='detail'),
    path('post/<int:post_id>/update/', views.update, name='update'),
    path('post/<int:post_id>/delete/', views.delete, name='delete'),
    
         

    # url patterns for CBV >>>>>>>>>>>>>>>

    path('user/<str:username>', UserPostListView.as_view(), name="author_posts"),
    # path('about/', AboutView.as_view(), name="about-blog"),
    # path('', PostListView.as_view(), name="home-blog"),
    # path("post/<int:pk>/", PostDetailView.as_view(), name="detail"),
    # path("post/create", PostCreateView.as_view(), name="create"),
    # path("post/<int:pk>/update/", PostUpdateView.as_view(), name="update"),
    # path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="delete"),
]


