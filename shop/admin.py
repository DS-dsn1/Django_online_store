from django.contrib import admin
from .models import Category, Manufacturer, Product, Review


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price',
                    'available', 'created', 'guarantee']
    list_filter = ['available', 'category', 'manufacturer', 'created', 'updated']
    search_fields = ('name', 'description')
    list_editable = ['price', 'available']
    raw_id_fields = ('manufacturer', )
    date_hierarchy = 'created'
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('created',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'product', 'created', 'active']
    list_filter = ['active', 'created']
    search_fields = ('name', 'email', 'body', 'product')
