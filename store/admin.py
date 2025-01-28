from django.contrib import admin
from .models import User, Product, Category, Cart, CartItem

# Inline برای نمایش آیتم‌های داخل سبد خرید
class CartItemInline(admin.TabularInline):  # یا StackedInline برای فرم‌های استک شده
    model = CartItem
    extra = 1  # تعداد فرم‌های اضافی برای افزودن آیتم‌ها
    fields = ('product', 'quantity')  # فیلدهای مورد نظر برای نمایش

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_paid')  # نمایش مجموع قیمت و دیگر فیلدها
    inlines = [CartItemInline]  # نمایش CartItem به‌صورت inline در Cart
    


# ثبت مدل‌ها در پنل ادمین
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart, CartAdmin)
#admin.site.register(CartItem)



