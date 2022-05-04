from django import forms
from django.contrib import admin
from django.forms import ModelChoiceField
from django.utils.safestring import mark_safe

from .models import *

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductAdminForm(forms.ModelForm):
    """Редактор форма"""
    specifications = forms.CharField(label="Характеристики", widget=CKEditorUploadingWidget())
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


class ImageGalleryInline(admin.TabularInline):
    """Галерея изображений для вывода в товарах"""
    model = ImageGallery
    extra = 3
    readonly_fields = ('get_image',)

    def get_image(self, obj):  # вывод изображения
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="auto" height="120px"')

    get_image.short_description = ""


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Товары"""
    list_display = ('name', 'get_image', 'price', 'qty', 'get_time_update', 'main_page', 'draft', 'in_stock')
    inlines = [ImageGalleryInline]
    readonly_fields = ("get_image", 'get_time_update', 'product_parent_category')
    form = ProductAdminForm
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
    list_editable = ('price', 'qty', 'main_page', 'draft', 'in_stock')
    search_fields = ('name', 'description', 'specifications')
    list_filter = ('category',)
    fields = (
        'get_time_update',
        'product_parent_category',
        'category',
        'name',
        'slug',
        'specifications',
        'description',
        ('price', 'qty'),
        ('main_page', 'draft', 'in_stock'),
        ('poster', 'get_image'),
    )


    def get_time_update(self, obj):
        return obj.time_update.strftime('%d-%m-%Y')

    get_time_update.short_description = "Время"

    def get_image(self, obj):  # вывод изображения
        if obj.poster:
            return mark_safe(f'<img src={obj.poster.url} width="auto" height="100px"')

    get_image.short_description = ""

    # def formfield_for_foreignkey(self, db_field, request,
    #                              **kwargs):  # переопределяем поле формы по умолчанию
    #     if db_field.name == 'subcategory':
    #         return ModelChoiceField(Category.objects.exclude(parent_category=None))
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категориии"""
    list_display = ('name', 'parent_category', 'count_prod_id' )
    prepopulated_fields = {"slug": ("name",)}
    ordering = ['-parent_category','name']
    readonly_fields = ('count_prod_id',)



    def formfield_for_foreignkey(self, db_field, request, **kwargs):  # переопределяем поле формы по умолчанию
        if db_field.name == 'parent_category':
            kwargs["queryset"] = Category.objects.filter(parent_category=None)
            # return ModelChoiceField(Category.objects.filter(parent_category=None))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




admin.site.register(ImageGallery)

admin.site.site_title = 'Админ панель Valery Store'
admin.site.site_header = 'Админ панель Valery Store'
