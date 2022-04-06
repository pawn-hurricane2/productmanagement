from collections import OrderedDict

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView, ListView

from group.forms import RegistrationForm, LoginForm
from group.models import Group, GroupUsers, RegisteredUsers, Message


class IndexView(TemplateView):
    template_name = "group/indexpage.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('homepage', kwargs={"user_id": self.request.user.id}))
        return super(IndexView, self).get(request, *args, **kwargs)


class RegistrationFormView(FormView):
    form_class = RegistrationForm
    template_name = "group/register.html"
    success_url = "/group/login/"

    def form_valid(self, form):
        form.save()
        return super(RegistrationFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = LoginForm
    template_name = "group/login.html"

    def form_valid(self, form):
        user = form.get_authenticated_user()
        login(self.request, user)
        return redirect(reverse('homepage', kwargs={"user_id": user.id}))


class LoginView(LoginFormView):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('homepage', kwargs={"user_id": self.request.user.id}))
        return super(LoginView, self).get(request, *args, **kwargs)


class RegistrationView(RegistrationFormView):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('homepage', kwargs={"user_id": self.request.user.id}))
        return super(RegistrationView, self).get(request, *args, **kwargs)


class HomePageView(LoginRequiredMixin, ListView):
    permission_denied_message = "You must be an authenticated user."
    template_name = "group/homepage.html"
    context_object_name = "group_lists"

    def get_queryset(self):
        group_ids_of_this_user = GroupUsers.objects.filter(user_id=self.kwargs.get("user_id")).values_list("group_id")
        groups_of_this_user = Group.objects.filter(id__in=group_ids_of_this_user)
        return groups_of_this_user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({"user_id": self.kwargs.get("user_id")})
        return context


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse("index"))


class CreateGroupView(LoginRequiredMixin, View):
    template_name = "group/create-group.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"user_id": kwargs.get("user_id")})

    def post(self, request, *args, **kwargs):
        post_data = request.POST.copy()
        if not post_data.get("title") or not post_data.get("description"):
            return render(request, self.template_name, {"user_id": kwargs.get("user_id")})
        else:
            data = {}
            data.update({"title": post_data["title"], "description": post_data["description"],
                         "admin_user_id": kwargs.get("user_id")})
            group = Group.objects.create(**data)
            GroupUsers.objects.create(group_id=group.id, user_id=kwargs.get("user_id"))
            return redirect(reverse('homepage', kwargs={"user_id": kwargs.get("user_id")}))


class GroupDisplayView(LoginRequiredMixin, View):
    permission_denied_message = "You must be an authenticated user."
    template_name = "group/group-display.html"

    def get(self, request, *args, **kwargs):
        group = Group.objects.get(id=kwargs.get("group_id"))
        user_ids_in_this_group = GroupUsers.objects.filter(group_id=kwargs.get("group_id")).values_list("user_id")
        users_in_this_group = RegisteredUsers.objects.filter(id__in=user_ids_in_this_group)
        users_not_in_this_group = RegisteredUsers.objects.exclude(id__in=user_ids_in_this_group)

        messages = Message.objects.filter(group_id=kwargs.get("group_id")).order_by("creation_date")

        messages_dict = OrderedDict()

        for message in messages:
            user = RegisteredUsers.objects.get(id=message.user_id)
            if user not in messages_dict:
                messages_dict[user] = [message]
            else:
                messages_dict.update({user: messages_dict[user] + [message]})

        return render(request, self.template_name, {"group": group, "users_to_be_added": users_not_in_this_group, "users_present": users_in_this_group, "user_loggedin": self.request.user, "messages": messages_dict})


class GroupAddUser(LoginRequiredMixin, View):
    permission_denied_message = "You must be an authenticated user."

    def get(self, request, *args, **kwargs):
        GroupUsers.objects.create(group_id=kwargs.get("group_id"), user_id=kwargs.get("user_id_to_be_added"))
        return redirect(reverse('group_display_view', kwargs={"group_id": kwargs.get("group_id")}))


class GroupRemoveUser(LoginRequiredMixin, View):
    permission_denied_message = "You must be an authenticated user."

    def get(self, request, *args, **kwargs):
        group = Group.objects.get(id=kwargs.get("group_id"))
        if self.request.user.id != group.admin_user_id:
            return HttpResponse("Only admin user can remove a user!!!")
        else:
            group_user_object = GroupUsers.objects.get(group_id=kwargs.get("group_id"), user_id=kwargs.get("user_id_to_be_removed"))
            group_user_object.delete()
            return redirect(reverse('group_display_view', kwargs={"group_id": kwargs.get("group_id")}))


class ExitUser(LoginRequiredMixin, View):
    permission_denied_message = "You must be an authenticated user."

    def get(self, request, *args, **kwargs):
        if self.request.user.id != kwargs.get("user_id_to_be_exited"):
            return HttpResponse("You cannot exit another user!!!")
        else:
            group_user_object = GroupUsers.objects.get(group_id=kwargs.get("group_id"),
                                                       user_id=kwargs.get("user_id_to_be_exited"))
            group_user_object.delete()
            return redirect(reverse('homepage', kwargs={"user_id": kwargs.get("user_id_to_be_exited")}))


class GroupAddMessageView(LoginRequiredMixin, View):
    permission_denied_message = "You must be an authenticated user."

    def post(self, request, *args, **kwargs):
        if self.request.user.id != kwargs.get("user_id"):
            return HttpResponse("You cannot message as another user")
        else:
            data_dict = {}
            post_data = request.POST
            data_dict["content"] = post_data.get("content")
            data_dict["user_id"] = kwargs.get("user_id")
            data_dict["group_id"] = kwargs.get("group_id")

            Message.objects.create(**data_dict)
            return redirect(reverse('group_display_view', kwargs={"group_id": kwargs.get("group_id")}))

