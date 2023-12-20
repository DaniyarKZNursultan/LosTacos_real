from django.urls import path, include
from . import views
from .views import profile_view, signup, category_menu, add_to_cart, view_cart, clear_cart, reviews, edit_review, \
    delete_review

urlpatterns = [
    path('', views.index, name='main'),
    path('about', views.about, name='about'),
    path('menu', views.menu, name='menu'),
    path('add_to_cart/<int:dish_id>/', add_to_cart, name='add_to_cart'),
    path('category/<int:category_id>/', category_menu, name='category_menu'),
    path('view_cart/', view_cart, name='view_cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('reviews/', reviews, name='reviews'),
    path('edit_review/<int:review_id>/', edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('profile', profile_view, name='profile'),
    path('login', views.login, name='login'),
    path('register', signup, name='register'),
]
