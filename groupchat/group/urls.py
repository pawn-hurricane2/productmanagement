from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("homepage/<int:user_id>/", views.HomePageView.as_view(), name="homepage"),
    path("create-group-view/<int:user_id>/", views.CreateGroupView.as_view(), name="create_group_view"),
    path("group-display-view/<int:group_id>/", views.GroupDisplayView.as_view(), name="group_display_view"),
    path("group-add-user/<int:group_id>/<int:user_id_to_be_added>/", views.GroupAddUser.as_view(), name="group_add_user"),
    path("group-remove-user/<int:group_id>/<int:user_id_to_be_removed>/", views.GroupRemoveUser.as_view(), name="group_remove_user"),
    path("group-exit-user/<int:group_id>/<int:user_id_to_be_exited>/", views.ExitUser.as_view(), name="group_exit_user"),
    path("group-add-message/<int:group_id>/<int:user_id>/", views.GroupAddMessageView.as_view(), name="group_add_message"),
]
