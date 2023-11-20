from django.contrib import admin
# import all models
from . import models
# from .models import Tag


# Register your models here.
admin.site.register(models.Vendor)
admin.site.register(models.ProductCategory)
# admin.site.register(models.Product)

class CustomerAdmin(admin.ModelAdmin):
    list_display=['get_username','mobile']
    def get_username(self,obj):
        return obj.user.username

admin.site.register(models.Customer,CustomerAdmin)

admin.site.register(models.Order)
admin.site.register(models.OrderItems)

admin.site.register(models.CustomerAddress)

admin.site.register(models.ProductRating)

# product image
admin.site.register(models.ProductImage)

class ProductImagesInline(admin.StackedInline):
    model = models.ProductImage  # Use 'model' instead of 'models'

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImagesInline,]

admin.site.register(models.Product, ProductAdmin)

# admin.site.register(Tag)


