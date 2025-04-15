# 🛒 E-Commerce Web Application

A fully functional, secure, and responsive **E-Commerce Web Application** built using **Django**. This platform enables seamless user experiences from browsing products to secure checkout, complete with admin controls and role-based access.

## 🚀 Features

- 🔐 **User Authentication**: Signup, login, and role-based access control using Django's built-in auth system.
- 🛍️ **Product Catalog**: Browse and search for products with category-wise filtering.
- 🛒 **Shopping Cart**: Add/remove items, adjust quantity, and view cart summaries.
- 💳 **Secure Payments**: Integrated Razorpay for a fast and reliable checkout process.
- 🧑‍💼 **Admin Dashboard**: Admin panel for managing users, orders, and products.
- 📱 **Responsive UI**: Designed using Django templating engine with clean HTML/CSS.
- ⚡ **Optimized ORM**: Efficient database interaction and migration handling with Django ORM.

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (can be upgraded to PostgreSQL/MySQL)
- **Payment Integration**: Razorpay
- **Frontend**: HTML, CSS (Bootstrap optional)

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ecommerce-django-app.git

# Navigate into the project directory
cd ecommerce-django-app

# Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser

# Start the development server
python manage.py runserver
