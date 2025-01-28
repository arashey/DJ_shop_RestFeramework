1. Prerequisites
Before getting started, make sure the following software is installed on your system:

Python 3.x (recommended version 3.7 or higher)
Pip (Python package manager)
Django 3.x or higher
Django REST Framework
djangorestframework-simplejwt (for JWT token management)
Requests (for making HTTP requests from the client to the API)
2. Installation
2.1. Cloning the Project
If you received this project from GitHub, clone it first and navigate to the project directory:

bash
Copy
Edit
git clone <URL_OF_YOUR_REPOSITORY>
cd <project_directory>
2.2. Creating and Activating a Virtual Environment
To avoid package conflicts with the system, create a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
2.3. Installing Dependencies
After activating the virtual environment, install the required dependencies from the requirements.txt file:

bash
Copy
Edit
pip install -r requirements.txt
If you don't have a requirements.txt, you can install the necessary packages manually:

bash
Copy
Edit
pip install django djangorestframework djangorestframework-simplejwt requests
3. Project Configuration
3.1. Database Setup
If you're using SQLite, no special setup is required. However, if you're using PostgreSQL or another database, you must configure the database connection in the settings.py file.

By default, SQLite is used:

python
Copy
Edit
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}
3.2. Media Configuration
If you are using media files (e.g., product images), ensure the following settings are in place in settings.py:

python
Copy
Edit
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
3.3. Database Migrations
Run the migrations to create the necessary database tables:

bash
Copy
Edit
python manage.py migrate
3.4. Creating a Superuser
To access the Django admin panel, create a superuser:

bash
Copy
Edit
python manage.py createsuperuser
4. Running the Development Server
After completing the steps above, the project is ready to run. To start the Django development server, use the following command:

bash
Copy
Edit
python manage.py runserver
This will run the server at http://127.0.0.1:8000/.

5. How the Project Works
5.1. User Registration and Login
Registration: Users can create a new account using the registration page. In the backend, this is handled by the RegisterView.
Login: After registering, users can log in and receive a JWT token, which is required for accessing the protected APIs.
5.2. Admin Features
The admin interface provides the following functionalities:

User Role Management: The admin can assign roles to users, such as regular user or admin, by setting the is_staff and is_superuser flags.
View and Edit User Accounts: The admin can view user details and edit them, including updating passwords or assigning roles.
Shopping Cart Management: Admin can check the carts of all users, see products in their carts, and remove them as necessary.
5.3. Product Management
Users can view products and check details of each product.
Only authenticated users can add products to their cart.
5.4. Categories Management
The admin can manage product categories. You can create categories and assign products to those categories to better organize the store.
5.5. Shopping Cart
Users can add products to their cart.
Products can be removed from the cart.
After adding products, users can complete the checkout process.
The payment gateway redirects users to complete the payment process.
5.6. Payment
After payment, the cart status is updated to "paid," and product stock is reduced accordingly.
6. Testing the APIs Using Postman
In this section, we’ll guide you on how to test the various APIs of the project using Postman.

6.1. User Registration
Method: POST
URL: http://127.0.0.1:8000/api/register/
Request Body:
json
Copy
Edit
{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "password123"
}
You will receive a response with the user details after successful registration.

6.2. Login and Get Token
Method: POST
URL: http://127.0.0.1:8000/api/login/
Request Body:
json
Copy
Edit
{
    "username": "testuser",
    "password": "password123"
}
In the response, you'll receive access_token and refresh_token which are required to access the protected APIs.

6.3. Get Product List
Method: GET
URL: http://127.0.0.1:8000/api/products/
Request Header:
Authorization: Bearer <access_token>
This will return a list of all products.

6.4. Add Product to Cart
Method: POST
URL: http://127.0.0.1:8000/api/cart/add/
Request Body:
json
Copy
Edit
{
    "product_id": 1,
    "quantity": 2
}
This will add the product with product_id 1 to the cart with a quantity of 2.

6.5. Remove Product from Cart
Method: DELETE
URL: http://127.0.0.1:8000/api/cart/remove/<product_id>/
Request Header:
Authorization: Bearer <access_token>
This request will remove the product from the cart.

6.6. Complete Checkout Process
Method: POST
URL: http://127.0.0.1:8000/api/cart/complete_payment/
Request Header:
Authorization: Bearer <access_token>
This request will complete the checkout process for the cart.

7. Common Issues and Troubleshooting
JWT Errors: If you encounter JWT token errors (e.g., token expired), use the endpoint http://127.0.0.1:8000/api/token/refresh/ to get a new token.

API Access Issues: Ensure that the request you're making includes a valid token in the Authorization header.

8. Conclusion
This project is an e-commerce platform that allows user registration, login, product viewing, adding products to the cart, and completing the payment process. The APIs are developed using Django REST Framework, and you can test them with Postman or any other similar tool.

Admin Capabilities:

Admin can manage users, including assigning roles (regular user or admin).
Admin can check and manage the shopping carts of users.
Admin can create and manage product categories.
Feel free to reach out if you have any questions or need assistance with the setup!

This should now include the extra details for the admin functionalities. Let me know if you need further modifications!
