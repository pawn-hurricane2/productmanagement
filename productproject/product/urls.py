from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.CategoriesListingView.as_view(), name="categories_list"),
    path("sub-category-listing/<int:category_id>/", views.SubCategoryListing.as_view(), name="sub_categories_list"),
    path("product-listing/<int:sub_category_id>/", views.ProductListing.as_view(), name="products_list"),
    path("product-listing-category/<int:category_id>/", views.ProductListingCategory.as_view(), name="product_list_category"),
    path("all-listing/", views.ProductAllListing.as_view(), name="all_listing"),
    path("add-product/", views.AddProduct.as_view(), name="add_product")
]
