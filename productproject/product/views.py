from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from product.models import Category, SubCategory, Product
from product.serializers import AddProductSerializer
from django.contrib import messages

class IndexView(TemplateView):
    template_name = "product/indexpage.html"


class CategoriesListingView(ListView):
    template_name = "product/categories-listing.html"
    context_object_name = "categories_list"

    def get_queryset(self):
        categories_lists = Category.objects.all()
        return categories_lists


class SubCategoryListing(ListView):
    template_name = "product/sub-categories-listing.html"
    context_object_name = "sub_categories_list"

    def get_queryset(self):
        self.category = Category.objects.filter(id=self.kwargs.get("category_id")).first()
        if not self.category:
            return []
        else:
            sub_categories_lists = self.category.subcategory_set.all()
            return sub_categories_lists

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({"cat": self.category})
        return context


class ProductListing(ListView):
    template_name = "product/product-listing.html"
    context_object_name = "product_list"

    def get_queryset(self):
        self.sub_category = SubCategory.objects.filter(id=self.kwargs.get("sub_category_id")).first()
        if not self.sub_category:
            return []
        else:
            product_lists = self.sub_category.product_set.all()
            return product_lists

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({"sub_cat": self.sub_category})
        return context


class ProductListingCategory(TemplateView):
    template_name = "product/product-listing-category.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.filter(id=self.kwargs.get("category_id")).first()
        if category:
            context.update({"category": category})
        return context


class ProductAllListing(TemplateView):
    template_name = "product/product-all-listing.html"

    def get(self, request, *args, **kwargs):
        product_ordering = self.request.GET.get("product_order")
        sub_category_ordering = self.request.GET.get("sub_category_order")
        category_ordering = self.request.GET.get("category_order")

        context = {
            "product_ordering": product_ordering,
            "sub_category_ordering": sub_category_ordering,
            "category_ordering": category_ordering
        }

        if product_ordering:
            if product_ordering == "asc":
                products = Product.objects.all().order_by("name")

            else:
                products = Product.objects.all().order_by("-name")
            context.update({"products": products})

        elif sub_category_ordering:
            if sub_category_ordering == "asc":
                sub_categories = SubCategory.objects.all().order_by("name")

            else:
                sub_categories = SubCategory.objects.all().order_by("-name")
            context.update({"sub_categories": sub_categories})

        elif category_ordering:
            if category_ordering == "asc":
                categories = Category.objects.all().order_by("name")

            else:
                categories = Category.objects.all().order_by("-name")
            context.update({"categories": categories})

        else:
            products = Product.objects.all()
            context.update({"products": products})

        # return context for form data
        all_subcategories = SubCategory.objects.all().values_list("name", flat=True)
        all_categories = Category.objects.all().values_list("name", flat=True)

        context.update({"all_subcategories": all_subcategories, "all_categories":  all_categories})

        return render(request, self.template_name, context)


class AddProduct(CreateAPIView):
    serializer_class = AddProductSerializer

    def post(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)
            return redirect(reverse("all_listing"))
        except Exception as exc:
            messages.error(request, str(exc))
            return redirect(reverse("all_listing"))


