from django.db.models import Q, Count
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator

from .models import *
from analytics.decorators import counted


@method_decorator(counted, name='dispatch')
class BaseView(ListView):
    """Главная страница"""
    model = Product
    template_name = "base.html"
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        return Product.objects_shop.filter(main_page=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(parent_category=None).prefetch_related('children')
        count_all = Product.objects.filter(draft=False).count()
        context['categories'] = categories
        context['count_all'] = count_all
        context['title'] = 'Главная страница'
        return context


class AllProdView(BaseView):
    """Все товары"""

    def get_queryset(self):
        return Product.objects_shop.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все товары'
        return context


class CategoryView(BaseView):
    """Товары по категориям"""

    allow_empty = False
    template_name = 'category_detail.html'

    def get_queryset(self):
        return Product.objects_shop.filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = context['products'][0].category
        context['title'] = Category.objects.get(slug=self.kwargs['category_slug'])
        return context


class SubCategoryViewAll(BaseView):
    """Товары любой категории в подкатегории Все """

    allow_empty = False
    template_name = 'category_detail.html'

    def get_queryset(self):
        # cat = Category.objects.get(slug=self.kwargs['category_slug'])
        # ids = cat.children.all().values_list('id')
        # return Product.objects_shop.filter(Q(category__id__in=ids) | Q(category=cat))
        return Product.objects_shop.filter(product_parent_category=self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['category_slug'])
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.prefetch_related('related_gallery')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['product']
        return context


class Search(BaseView):
    """Поиск товара"""
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Product.objects_shop.filter(
            Q(name__icontains=query) | Q(specifications__icontains=query) | Q(description__icontains=query) | Q(
                category__name__icontains=query)
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        context['title'] = f'Результаты поиска: {self.request.GET.get("q")}'
        return context
