from django.contrib import admin
from django.utils.safestring import mark_safe

from texnomart.models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'image', 'get_image']
    list_display = ['title', 'get_image', 'slug']
    search_fields = ['title']
    readonly_fields = ['get_image']

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='50' height='50'>")

    get_image.short_description = 'Image'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'price', 'discount', 'user_like','category']

admin.site.register(Comments)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']

admin.site.register(AttributeValue)
admin.site.register(AttributeKey)
admin.site.register(Attribute)
