## Storefront – E-Commerce Backend (Django REST Framework)

A backend for an e-commerce application built with Django REST Framework and PostgreSQL.
It provides a complete REST API for managing products, customers, shopping carts, orders, and reviews, optimized for performance and scalability.

## 🚀 Features

E-commerce APIs – products, customers, carts, orders, and reviews.

Relational data models in PostgreSQL with constraints and validations.

Optimized queries using select_related, prefetch_related, and annotations to reduce N+1 queries.

Pagination, filtering, sorting, and search for efficient data retrieval.

Serializer logic with computed fields (e.g., price_with_tax) to separate business rules from models.

## 🛠 Tech Stack

Backend: Django, Django REST Framework

Database: PostgreSQL

Auth: Django built-in authentication (extensible for JWT/OAuth2)

API Tools: DjangoFilter, Pagination, DRF Browsable API

## ⚙️ Installation & Setup
1. Clone the repo
```bash
git clone https://github.com/yourusername/storefront.git
cd storefront
```
2. Create & activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Configure database
Update your PostgreSQL settings in storefront/settings.py:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'storefront',
        'USER': 'postgres',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. Run migrations
```bash
python manage.py migrate
```
