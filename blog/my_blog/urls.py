from django.urls import path

from .views import BlogLoginView, BlogRegisterView, HomePageView, BlogCreateView, \
    BlogEditView, AdminView, AllBlogsRegisteredUser, LikedBlogView, LogoutView

urlpatterns = [
    path('login/', BlogLoginView.as_view(), name="login"),
    path('register/', BlogRegisterView.as_view(), name="register"),
    path('home/<int:id>/', HomePageView.as_view(), name="home"),
    path('create-blog/<int:id>/', BlogCreateView.as_view(), name="blog-create"),
    path('edit/<int:blog_id>/<int:user_id>/', BlogEditView.as_view(), name="blog-edit"),
    path('admin/<int:id>/',AdminView.as_view(), name="admin"),
    path('all-blogs/<int:user_id>/', AllBlogsRegisteredUser.as_view(), name="blog-list-reg-user"),
    path('liked-blogs/<int:user_id>/<int:blog_id>/', LikedBlogView.as_view(), name="likedBlog"),
    path('logout/', LogoutView.as_view(), name="logout"),
]