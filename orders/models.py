from django.db import models
from django.utils.html import format_html
from goods.models import Products

from users.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)





class OrderitemQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Пользователь", default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    requires_delivery = models.BooleanField(default=False, verbose_name="Требуется доставка")
    delivery_address = models.TextField(null=True, blank=True, verbose_name="Адрес доставки")
    payment_on_get = models.BooleanField(default=False, verbose_name="Оплата при получении")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(max_length=50, default='В обработке', verbose_name="Статус заказа")                                   

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("id",)
        
        
        

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, verbose_name="Продукт", default=None)
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")
    
    # Убрали поле return_date, так как будем вычислять его динамически

    class Meta:
        db_table = "order_item"
        verbose_name = "Арендуемый товар"
        verbose_name_plural = "Арендуемые товары"
        ordering = ("id",)

    objects = OrderitemQueryset.as_manager()

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"
    
    def products_price(self):
        # Проверяем, нужно ли применять скидку
        if self.quantity > 30 and self.product.discount:
            return round(self.product.sell_price() * self.quantity, 2)
    
        # Если количество товара 30 или меньше, возвращаем обычную цену
        return round(self.product.price * self.quantity, 2)
    
    @property
    def return_date(self):
        """Дата возврата: дата заказа + 30 дней × количество"""
        return self.order.created_timestamp + timedelta(days=1 + self.quantity)
    
    @property
    def is_overdue(self):
        """Проверка просрочки (текущая дата > даты возврата)"""
        return timezone.now() > self.return_date
    

