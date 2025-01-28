from django.urls import path
from .views import (RegisterView, LoginView, ProductDetailView, ProductListView,
                    register_view, login_view, product_list_view, product_detail_view, 
                    AddToCartView, CartView, RemoveFromCartView, CompletePaymentView, 
                    cart_view, add_to_cart, remove_from_cart, complete_payment,
                    go_to_payment, payment_callback, complete_payment, payment_gateway, logout_view )


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/complete_payment/', CompletePaymentView.as_view(), name='complete_payment'),


    
    path('account/register/', register_view, name='register_page'),  # ویو صفحه ثبت‌نام
    path('account/login/', login_view, name='login_page'),
    path('account/logout/', logout_view, name='logout'),
    path('account/products/', product_list_view, name='product_list'),
    path('account/products/<int:product_id>/', product_detail_view, name='product_detail'),
    path('account/cart/', cart_view, name='cart'),
    path('account/cart/add/', add_to_cart, name='add_to_cart'),
    path('account/cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('account/cart/complete_payment/', complete_payment, name='complete_payment'),
    path('account/cart/<int:cart_id>/payment/', go_to_payment, name='go_to_payment'),
    path('account/payment_callback/', payment_callback, name='payment_callback'),
    path('account/payment/', complete_payment, name='complete_payment'),
    path('account/payment/gateway/', payment_gateway, name='payment_gateway_url'),



    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)