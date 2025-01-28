from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product, CartItem
from .serializers import ProductSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Product
from .serializers import CartSerializer
from rest_framework.exceptions import NotFound
from django.urls import reverse
import requests






User = get_user_model()
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        # اعتبارسنجی کاربر
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # اگر کاربر معتبر بود، توکن را ایجاد و ارسال می‌کنیم
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price']

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]







#for html



def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address', '')  # مقدار پیش‌فرض خالی باشد
        password = request.POST.get('password')

        response = requests.post('http://127.0.0.1:8000/api/register/', data={
            'username': username,
            'email': email,
            'phone_number': phone_number,
            'address': address,  # ارسال آدرس (اگر مقدار نداشت، مقدار خالی می‌رود)
            'password': password
        })

        if response.status_code == status.HTTP_201_CREATED:
            return redirect('product_list')

        else:
            errors = response.json()
            return render(request, 'register.html', {'errors': errors})

    return render(request, 'register.html')







def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ارسال درخواست به API برای دریافت توکن
        response = requests.post('http://127.0.0.1:8000/api/login/', data={
            'username': username,
            'password': password
        })

        if response.status_code == 200:
            tokens = response.json()
            request.session['access_token'] = tokens['access_token']
            request.session['refresh_token'] = tokens['refresh_token']

            # احراز هویت کاربر در سیستم Django
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)  # ثبت لاگین کاربر در Django
                messages.success(request, "شما با موفقیت وارد شدید!")
                return redirect('product_list')  # هدایت به صفحه محصولات
            else:
                messages.error(request, "مشکلی در احراز هویت به‌وجود آمد!")
                return render(request, 'login.html')

        else:
            error_message = response.json().get('detail', 'نام کاربری یا رمز عبور اشتباه است.')
            messages.error(request, error_message)
            return render(request, 'login.html')

    return render(request, 'login.html')



def product_list_view(request):
    api_url = 'http://127.0.0.1:8000/api/products/'

    # دریافت توکن و توکن تازه‌سازی از session
    access_token = request.session.get('access_token')
    refresh_token = request.session.get('refresh_token')

    if not access_token:
        # اگر توکن وجود نداشته باشد، کاربر باید وارد حساب کاربری شود
        return render(request, 'error.html', {'message': 'لطفا وارد حساب کاربری خود شوید'})

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    try:
        # ارسال درخواست GET برای دریافت محصولات
        response = requests.get(api_url, headers=headers)

        # بررسی اینکه آیا توکن منقضی شده است
        if response.status_code == 401:  # اگر توکن منقضی شده باشد
            refresh_url = 'http://127.0.0.1:8000/api/token/refresh/'
            refresh_data = {'refresh': refresh_token}
            
            try:
                # ارسال درخواست برای دریافت توکن جدید
                refresh_response = requests.post(refresh_url, data=refresh_data)
                refresh_response.raise_for_status()  # بررسی وضعیت درخواست

                if refresh_response.status_code == 200:
                    # دریافت توکن جدید و ذخیره آن در session
                    new_tokens = refresh_response.json()
                    request.session['access_token'] = new_tokens['access']
                    access_token = new_tokens['access']  # توکن جدید را استفاده می‌کنیم

                    # تلاش مجدد برای دریافت محصولات با توکن جدید
                    headers = {'Authorization': f'Bearer {access_token}'}
                    response = requests.get(api_url, headers=headers)
                else:
                    return render(request, 'error.html', {'message': 'توکن منقضی شده است. لطفاً دوباره وارد شوید.'})

            except requests.exceptions.RequestException as e:
                return render(request, 'error.html', {'message': 'مشکلی در دریافت توکن جدید پیش آمد. لطفاً دوباره تلاش کنید.'})

        # اگر توکن معتبر است
        response.raise_for_status()  # بررسی وضعیت پاسخ
        products = response.json()  # تبدیل پاسخ به JSON

    except requests.exceptions.RequestException as e:
        products = []  # در صورت بروز خطا، لیست خالی
        print(f"Error fetching products: {e}")

    # ارسال داده‌ها به قالب
    return render(request, 'products.html', {'products': products})



def product_detail_view(request, product_id):
    api_url = f'http://127.0.0.1:8000/api/products/{product_id}/'
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        product = response.json()
    else:
        product = None  # اگر محصولی پیدا نشد، مقدار None برگردان

    return render(request, 'product_detail.html', {'product': product})







class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # بررسی اینکه آیا کاربر سبد خرید دارد یا نه
        try:
            cart = Cart.objects.get(user=self.request.user, is_paid=False)
            return cart
        except Cart.DoesNotExist:
            raise NotFound(detail="سبد خرید برای این کاربر وجود ندارد.")


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]  # اطمینان از اینکه کاربر احراز هویت شده است

    def delete(self, request, product_id):
        try:
            # ابتدا سبد خرید کاربر رو پیدا می‌کنیم
            cart = Cart.objects.get(user=request.user, is_paid=False)

            # پیدا کردن آیتم داخل سبد خرید
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            
            # حذف آیتم از سبد خرید
            cart_item.delete()

            return Response({"message": "محصول از سبد خرید حذف شد!"}, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response({"message": "سبد خرید پیدا نشد!"}, status=status.HTTP_404_NOT_FOUND)

        except CartItem.DoesNotExist:
            return Response({"message": "محصول در سبد خرید موجود نیست!"}, status=status.HTTP_404_NOT_FOUND)


class MarkAsPaidView(APIView):
    def post(self, request, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id)
            cart.is_paid = True  # تغییر وضعیت پرداخت
            cart.save()
            return Response({"message": "وضعیت پرداخت به روز شد."})
        except Cart.DoesNotExist:
            return Response({"message": "سبد خرید پیدا نشد!"}, status=400)
        

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "محصول یافت نشد!"}, status=404)

        # گرفتن آخرین سبد خرید پرداخت نشده، یا ایجاد یک سبد جدید
        cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)

        # بررسی اینکه آیا این محصول قبلاً در سبد خرید وجود دارد
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()

        if cart_item:
            cart_item.quantity += quantity  # افزایش تعداد محصول
            cart_item.save()
        else:
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)  # ایجاد آیتم جدید

        return Response({"message": "محصول به سبد خرید اضافه شد!"})




class CompletePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user, is_paid=False)

            # بررسی اگر سبد خرید قبلاً پرداخت شده باشد
            if cart.is_paid:
                return Response({"message": "سبد خرید قبلاً پرداخت شده است."}, status=400)

            # کاهش موجودی محصولات در سبد خرید
            for cart_item in cart.cart_items.all():
                product = cart_item.product
                if product.stock >= cart_item.quantity:
                    product.stock -= cart_item.quantity  # کاهش موجودی
                    product.save()  # ذخیره تغییرات موجودی در دیتابیس
                else:
                    return Response({"message": f"محصول {product.name} موجودی کافی ندارد."}, status=400)

            # تغییر وضعیت سبد خرید به پرداخت شده
            cart.is_paid = True
            cart.save()

            # حذف اقلام سبد خرید پس از پرداخت
            cart.cart_items.all().delete()

            # بررسی وجود سبد خرید جدید قبل از ایجاد
            if not Cart.objects.filter(user=request.user, is_paid=False).exists():
                Cart.objects.create(user=request.user, is_paid=False)

            return Response({"message": "پرداخت با موفقیت انجام شد. سبد خرید جدید ایجاد شد."}, status=200)

        except Cart.DoesNotExist:
            return Response({"message": "سبد خرید پیدا نشد."}, status=404)




def go_to_payment(request, cart_id):
    # ابتدا سبد خرید را از پایگاه داده پیدا کنید
    cart = Cart.objects.get(id=cart_id, user=request.user, is_paid=False)

    # مجموع قیمت سبد خرید
    total_price = cart.get_total_price()

    # در اینجا باید از API درگاه پرداخت استفاده کنید. فرضاً زرین‌پال
    url = 'https://www.zarinpal.com/pg/StartPay/{payment_request_token}'

    # داده‌های ارسال به درگاه
    payment_data = {
        'amount': total_price,  # مبلغ برای پرداخت
        'callback_url': 'http://your-domain.com/payment_callback/',  # آدرس بازگشتی پس از پرداخت
    }

    response = requests.post('https://api.zarinpal.com/pg/StartPay', data=payment_data)

    if response.status_code == 200:
        payment_url = response.json().get('payment_url')

        # چاپ URL برای بررسی
        print(f'Payment URL: {payment_url}')

        # هدایت به درگاه پرداخت
        return redirect(payment_url)
    else:
        return JsonResponse({'error': 'Payment request failed'}, status=400)

# ویو برای نمایش سبد خرید (HTML)

def cart_view(request):
    """ نمایش سبد خرید برای کاربران لاگین‌شده و لاگین‌نشده """
    cart = None
    cart_items = []
    total_price = 0

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
        cart_items = cart.cart_items.all()
        total_price = cart.get_total_price()

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")  # گرفتن product_id از داده‌های POST
        if not product_id:
            return redirect('cart')  # اگر شناسه محصول ارسال نشده بود، به صفحه سبد خرید هدایت می‌شود.

        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
        else:
            return redirect('login_page')  # اگر کاربر لاگین نکرده است، به صفحه ورود هدایت می‌شود

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart')  # پس از اضافه شدن به سبد خرید، به صفحه سبد خرید هدایت می‌شود

    return redirect('cart')  # اگر متد درخواست درست نباشد، به سبد خرید هدایت می‌شود



def remove_from_cart(request, product_id):
    """ حذف محصول از سبد خرید، فقط برای کاربران لاگین‌شده """
    if not request.user.is_authenticated:
        return redirect('login_page')  # کاربران لاگین‌نشده را به صفحه ورود هدایت کن

    try:
        cart = Cart.objects.get(user=request.user, is_paid=False)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()
    except Cart.DoesNotExist:
        return redirect('cart')  # اگر سبد خرید وجود ندارد، به سبد خرید برگشت می‌شود

    return redirect('cart')  # بعد از حذف، به سبد خرید هدایت می‌شود.



def complete_payment(request):
    if request.method == "POST":
        payment_url = reverse('payment_gateway_url')  # حالا به درستی مقداردهی شده است
        return redirect(payment_url)

    return redirect('cart')


def payment_callback(request):
    # در اینجا شما باید اطلاعات بازگشتی از درگاه پرداخت را بررسی کنید
    # معمولاً باید از کد وضعیت و توکن‌ها استفاده کنید تا مطمئن شوید پرداخت انجام شده است

    payment_status = request.GET.get('Status')
    payment_ref_id = request.GET.get('RefID')

    if payment_status == 'OK':
        # پرداخت موفقیت‌آمیز بود
        # تغییر وضعیت سبد خرید به پرداخت‌شده
        cart = Cart.objects.get(payment_ref_id=payment_ref_id)
        cart.is_paid = True
        cart.save()

        # به کاربر صفحه تایید پرداخت را نمایش دهید
        return render(request, 'payment_success.html', {'cart': cart})

    else:
        # پرداخت ناموفق
        return render(request, 'payment_failed.html', {'error': 'Payment failed'})
    



def payment_gateway(request):
    return redirect("https://www.zarinpal.com/pg/StartPay/xxxxxxxxxxxxxxxx")


def logout_view(request):
    logout(request)
    return redirect('product_list') 

