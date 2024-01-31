from django.contrib import admin
from .models import Category, CategoryItem

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id' , 'title', 'total_vote']
    prepopulated_fields = {'slug' : ('title',) }

admin.site.register(Category, CategoryAdmin)

class CategoryItemAdmin(admin.ModelAdmin):
    list_display = ['id' , 'title', 'category']

admin.site.register(CategoryItem, CategoryItemAdmin)


