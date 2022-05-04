from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, post_delete
from django.urls import reverse
from .utils import upload_function, upload_function_poster, new_image_field


class ProductManager(models.Manager):
    """Менеджер товаров"""

    def get_queryset(self):
        return super().get_queryset().filter(draft=False).only(
            'name', 'poster', 'specifications', 'price', 'specifications', 'in_stock',
            'category', 'slug', 'product_parent_category').select_related('category').order_by('-time_update')


class Category(models.Model):
    """Категории"""

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(max_length=50, unique=True)
    parent_category = models.ForeignKey(
        'self', verbose_name='Главная категория', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children')
    count_prod_id = models.IntegerField(verbose_name='Количество товара', null=True, blank=True)

    def __str__(self):
        if self.parent_category:
            return f'{self.parent_category.name}:{self.name}'
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Product(models.Model):
    """Товар"""

    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    product_parent_category = models.CharField(verbose_name='Родительская категория', max_length=150, null=True,
                                               blank=True,
                                               db_index=True)
    category = models.ForeignKey(
        Category, verbose_name='Подкатегория', on_delete=models.SET_NULL, null=True, related_name='related_product_cat')
    name = models.CharField(max_length=150, verbose_name='Наименование')
    slug = models.SlugField(max_length=50, unique=True)
    poster = models.ImageField(verbose_name='Постер', upload_to=upload_function_poster)
    specifications = models.TextField(blank=True, null=True, verbose_name='Характеристики')
    description = models.TextField(verbose_name='Описание', default='Описание появится позже')
    price = models.IntegerField(verbose_name='Цена', null=True, blank=True)
    main_page = models.BooleanField(default=False, verbose_name='Главная?')
    draft = models.BooleanField(verbose_name='Черновик?', default=False)
    in_stock = models.BooleanField(verbose_name='В наличии?', default=True)
    qty = models.IntegerField(verbose_name='Количество', default=0, blank=True)

    objects = models.Manager()
    objects_shop = ProductManager()

    def __str__(self):
        # if self.subcategory:
        #     return f'{self.subcategory.name}: {self.name}'
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={
            'category_slug': self.category.slug, 'product_slug': self.slug})

    def save(self, *args, **kwargs):
        self.poster = new_image_field(self.poster, 800, 600)
        self.product_parent_category = self.category.parent_category.slug if self.category.parent_category \
            else self.category.slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-time_update']


class ImageGallery(models.Model):
    """Галерея изображений"""

    image = models.ImageField('Изображение', upload_to=upload_function)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='related_gallery')

    def __str__(self):
        return f'Изображение для {self.product}'

    def save(self, *args, **kwargs):
        self.image = new_image_field(self.image, 1000, 750)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Галерея изображений'
        verbose_name_plural = verbose_name


def update_qty(instance, **kwargs):
    """Изменение кол-ва товара в категориях и подкатегориях (при сохранении и удалении)"""
    if instance.category.parent_category:
        qty_sub = Product.objects.filter(category=instance.category.id, draft=False).count()
        Category.objects.filter(pk=instance.category.id).update(count_prod_id=qty_sub)
    qty_cat = Product.objects.filter(product_parent_category=instance.product_parent_category, draft=False).count()
    Category.objects.filter(slug=instance.product_parent_category).update(count_prod_id=qty_cat)


post_save.connect(update_qty, sender=Product)
post_delete.connect(update_qty, sender=Product)
