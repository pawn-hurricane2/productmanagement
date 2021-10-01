
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView, ListView
from rest_framework.views import APIView
from .models import Users1, Blog1


class IndexView(TemplateView):
    template_name = "my_blog/index_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({"blogs":Blog1.objects.all()})
        return context


class BlogLoginView(APIView):
    template_name = "my_blog/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return render(request, self.template_name)

        user = Users1.objects.filter(email=email).first()

        if user:
            user_password = user.password

            if user_password != user.password:
                return render(request, self.template_name)
            else:

                login(request, user)

                if user.is_admin:
                    return HttpResponseRedirect("/blog/admin/{}".format(user.id))
                else:
                    return HttpResponseRedirect("/blog/home/{}".format(user.id))

        else:
            return render(request, self.template_name)


class BlogRegisterView(APIView):
    template_name = "my_blog/register.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        email = request.POST.get("email")
        cell_phone = request.POST.get("cell_phone")
        password = request.POST.get("password")
        is_admin = request.POST.get("is_admin")

        is_admin = 1 if is_admin == "Yes" else 0

        if name != None and email != None and cell_phone != None and password != None:
            try:
                data_dict = {"name": name, "email": email, "cell_phone": cell_phone, "password": password,
                             "is_admin": is_admin}
                Users1.objects.create(**data_dict)

                return redirect("/blog/login/")
            except Exception as ex:
                return render(request, self.template_name)

        else:
            return render(request, self.template_name)


class HomePageView(LoginRequiredMixin, ListView):
    template_name = "my_blog/home.html"
    context_object_name = "blogs"

    def get_queryset(self):
        # print(self.request, self.request.user, self.request.user.is_authenticated, "\n\n\nthis is debug home page\n\n\n\n")
        all_blogs_of_user = Blog1.objects.filter(user_id=self.kwargs.get("id"))
        return all_blogs_of_user

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data()
        user_id = self.kwargs.get("id")
        context.update({"user_id":user_id})
        return context


class BlogCreateView(APIView):
    template_name = "my_blog/blog-create.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"user_id":kwargs.get("id")})

    def post(self, request, *args, **kwargs):

        text = request.POST.get("text")
        user_id = kwargs.get("id")
        try:
            data_dict = {"text":text, "user_id":user_id}
            Blog1.objects.create(**data_dict)
            return HttpResponseRedirect("/blog/home/{}/".format(user_id))

        except Exception as ex:
            return render(request, self.template_name, {"user_id": kwargs.get("id")})


class BlogEditView(LoginRequiredMixin, APIView):
    template_name = "my_blog/blog-edit.html"

    def get(self, request, *args, **kwargs):

        blog_obj = Blog1.objects.get(id=kwargs.get("blog_id"))
        txt = blog_obj.text
        return render(request, self.template_name, {"blog_id":kwargs.get("blog_id"), "text":txt, "user_id":kwargs.get("user_id")})

    def post(self, request, *args, **kwargs):

        text = request.POST.get("text")
        blog_id = kwargs.get("blog_id")
        user_id = kwargs.get("user_id")
        blog_obj = Blog1.objects.filter(id=blog_id).first()
        if blog_obj:
            blog_obj.text = text
            blog_obj.save()
            return HttpResponseRedirect("/blog/home/{}/".format(user_id))
        else:
            render(request, self.template_name, {"blog_id": kwargs.get("blog_id")})


class AdminView(LoginRequiredMixin, APIView):
    template_name = "my_blog/admin.html"

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user=Users1.objects.get(id=user_id)
        if not user.is_admin:
            return HttpResponseRedirect("/blog/login/")

        queryset = Users1.objects.all()
        return render(request, self.template_name, {"queryset":queryset})


class AllBlogsRegisteredUser(APIView):
    template_name = "my_blog/all-blogs.html"

    def get(self, request, *args, **kwargs):
        context = {"all_blogs": Blog1.objects.all(), "user_id":kwargs.get("user_id")}
        return render(request, self.template_name, context)


class LikedBlogView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = Users1.objects.get(id=user_id)
        if user.liked_blog_id:
            return HttpResponseRedirect("/blog/all-blogs/{}/".format(user_id))
        else:
            blog_id = kwargs.get("blog_id")
            blog_obj = Blog1.objects.get(id=blog_id)
            blog_obj.like += 1
            blog_obj.save()
            user.liked_blog_id = blog_id
            user.save()
            return HttpResponseRedirect("/blog/all-blogs/{}/".format(user_id))


class LogoutView(APIView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("/blog/login/")





