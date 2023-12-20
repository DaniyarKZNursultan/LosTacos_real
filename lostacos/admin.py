# admin.py
from django.contrib import admin
from .models import Dish, Category
from .forms import DishForm

class DishAdmin(admin.ModelAdmin):
    form = DishForm
    list_display = ('name', 'price', 'category')  # Отображение в списке
    search_fields = ('name',)  # Поиск по имени

admin.site.register(Category)
admin.site.register(Dish, DishAdmin)
