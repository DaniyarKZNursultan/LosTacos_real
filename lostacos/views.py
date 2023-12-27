from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import RegisterForm, ReviewForm, UserForgotPasswordForm, UserSetNewPasswordForm
from .models import Dish, Category, Cart, CartItem, Review


def index(request):
    return render(request, 'lostacos/main.html')

def about(request):
    return render(request, 'lostacos/about.html')

def kaspi_qr(request):
    return render(request, 'lostacos/kaspiqr.html')

def order(request):
    return render(request, 'lostacos/order.html')

@login_required
def menu(request):
    dishes = Dish.objects.all()
    return render(request, 'lostacos/menu.html', {'dishes': dishes})

def category_menu(request, category_id):
    category = Category.objects.get(pk=category_id)
    dishes = Dish.objects.filter(category=category)
    return render(request, 'lostacos/category_menu.html', {'category': category, 'dishes': dishes})

@login_required
def view_cart(request):
    user = request.user
    print('Current user:', user)

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        # Если корзина не существует, создаем ее
        cart = Cart.objects.create(user=user)

    cart = get_object_or_404(Cart, user=user)
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = cart.total_price
    return render(request, 'lostacos/profile.html', {'cart': cart, 'cart_items': cart_items, 'total_price': total_price})


@login_required
def clear_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)

    # Удаляем все элементы корзины
    cart.cartitem_set.all().delete()

    # Обнуляем общую стоимость корзины
    cart.total_price = 0
    cart.save()

    return redirect('lostacos/profile.html')



@login_required
def menu(request):
    dishes = Dish.objects.all()
    return render(request, 'lostacos/menu.html', {'dishes': dishes})

@login_required
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, pk=dish_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, dish=dish)

    if not cart_item_created:
        # Если блюдо уже есть в корзине, увеличиваем количество на 1
        cart_item.quantity += 1
    else:
        # Если блюдо только что добавлено в корзину, устанавливаем количество на 1
        cart_item.quantity = 1

    cart_item.save()

    # Пересчитываем общую стоимость корзины
    cart.total_price = sum(item.dish.price * item.quantity for item in cart.cartitem_set.all())
    cart.save()

    return redirect('view_cart')

@login_required
def reviews(request):
    reviews_list = Review.objects.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews')
    else:
        form = ReviewForm()

    return render(request, 'lostacos/reviews.html', {'reviews_list': reviews_list, 'form': form})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    # Проверяем, является ли текущий пользователь автором отзыва или администратором
    if request.user == review.user or request.user.is_staff:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('reviews')
        else:
            form = ReviewForm(instance=review)

        return render(request, 'lostacos/edit_review.html', {'form': form, 'review': review})
    else:
        # Пользователь не имеет права редактировать этот отзыв
        return redirect('reviews')

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    # Проверяем, является ли текущий пользователь автором отзыва или администратором
    if request.user == review.user or request.user.is_staff:
        review.delete()
    # Если пользователь не имеет права удалять этот отзыв, вы можете добавить другое поведение

    return redirect('reviews')


@login_required
def profile_view(request):
    return render(request, 'lostacos/profile.html')

def login_view(request):
    return render(request, 'registration/login.html')

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/') # на главную страницу сайта


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'registration/user_password_reset.html'
    success_url = reverse_lazy('main')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'registration/password_subject_reset_mail.txt'
    email_template_name = 'registration/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'registration/user_password_set_new.html'
    success_url = reverse_lazy('home')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context
