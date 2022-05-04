from django.urls import path

from .views import BaseView, CategoryView, ProductDetailView, AllProdView, Search, SubCategoryViewAll

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('all/', AllProdView.as_view(), name='all'),
    path("search/", Search.as_view(), name='search'),
    path('<str:category_slug>/', CategoryView.as_view(), name='category_detail'),
    path('<str:category_slug>/all/', SubCategoryViewAll.as_view(), name='category_detail_all'),
    path('<str:category_slug>/<str:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
]
