from django.db import models
from goods.models import Products

from users.models import User


class CartQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'cart'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        ordering = ("id",)

    objects = CartQueryset().as_manager()

    def products_price(self):
        # Проверяем, нужно ли применять скидку
        if self.quantity > 30 and self.product.discount:
            return round(self.product.sell_price() * self.quantity, 2)
    
        # Если количество товара 30 или меньше, возвращаем обычную цену
        return round(self.product.price * self.quantity, 2)
    
    
    
    
    
    
    def increase_quantity(self, amount=30):
        self.quantity += amount
        self.save()

    def decrease_quantity(self, amount=30):
        if self.quantity >= amount:
            self.quantity -= amount
        else:
            self.quantity = 0  # Устанавливаем в 0, если количество меньше 30
        self.save()



    def __str__(self):
        if self.user:
            return f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}'
            
        return f'Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}'



