from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language_code=language,
                                     translations__slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products})

from django.db.models import Q

def search_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    query = request.Get.get("q")
    if query:
        queries = query.split(" ")
    products = Product.objects.filter(available=True)
    for q in queries:
        products = products.filter(
            Q(name__icontains=q) |
            Q(slug__icontains=q)
        ).distinct()

    return render(request,
                  'shop/product/search_list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})