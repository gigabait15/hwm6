from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogUpdateView, BlogListView, BlogDetailView, BlogCreateView

app_name = BlogConfig.name


urlpatterns = [
    path('', BlogListView.as_view(), name='blog'),
    path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog_view/<int:pk>/', BlogDetailView.as_view(), name='blog_view'),
]