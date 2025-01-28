from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

# مدل کاربر سفارشی
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)
    
    USER_ROLES = (('admin', 'Admin'), ('customer', 'Customer'))
    role = models.CharField(max_length=10, choices=USER_ROLES, default='customer')

    def __str__(self):
        return self.username
    

# مدل دسته‌بندی محصولات
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# مدل محصولات
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # هر کاربر چندین سبد خرید دارد
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # زمان ایجاد سبد خرید
    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total_price(self):
        # اطمینان از اینکه تمام آیتم‌ها به‌درستی جمع می‌شوند
        return sum(item.get_total_price() for item in self.cart_items.all())

    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product.price

