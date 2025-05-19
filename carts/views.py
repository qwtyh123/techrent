from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from carts.mixins import CartMixin
from carts.models import Cart
from carts.utils import get_user_carts

from goods.models import Products


class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        product = Products.objects.get(id=product_id)
        cart = self.get_cart(request, product=product)

        if cart:
            # Если товар уже есть в корзине
            if cart.quantity == 7:
                # Первое добавление - было 7, добавляем 23 (итого 30)
                cart.quantity += 23
            else:
                # Все последующие добавления - по 30
                cart.quantity += 30
            cart.save()
        else:
            # Если товара нет в корзине - добавляем 7 единиц
            Cart.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else None,
                product=product, 
                quantity=7
            )
        
        response_data = {
            "message": "Товар добавлен в корзину",
            'cart_items_html': self.render_cart(request)
        }
        return JsonResponse(response_data)



from django.http import JsonResponse
from django.views import View

class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        action = request.POST.get("action")  # Получаем действие (increase или decrease)

        # Получаем объект корзины
        cart = self.get_cart(request, cart_id=cart_id)

        if action == "increase":
            if cart.quantity == 0:
                cart.quantity = 7  # Устанавливаем начальное количество на 7
                message = "Количество установлено на 7 днях"
            elif cart.quantity == 7:
                cart.quantity += 23  # Первое добавление после инициализации
                message = "Количество увеличено на 23 дня"
            else:
                cart.quantity += 30  # Все последующие добавления
                message = "Количество увеличено на 30 дней"

        elif action == "decrease":
            if cart.quantity > 30:
                cart.quantity -= 30  # Уменьшаем количество на 30
                message = "Количество уменьшено на 30 дней"
            elif cart.quantity == 30:
                cart.quantity -= 23  # Уменьшаем до 7
                message = "Количество уменьшено до 7 дней"
            else:
                cart.quantity = max(0, cart.quantity - (cart.quantity - 7))  # Не даем уйти ниже нуля
                message = "Вы достигли минимального числа дней аренды"

        cart.save()

        quantity = cart.quantity

        response_data = {
            "message": message,
            "quantity": quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        
        cart = self.get_cart(request, cart_id=cart_id)
        quantity = cart.quantity
        cart.delete()

        response_data = {
            "message": "Товар удален из корзины",
            "quantity_deleted": quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)
