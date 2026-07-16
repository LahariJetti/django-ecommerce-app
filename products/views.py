from django.shortcuts import render,get_object_or_404,redirect
from .models import Product

def home(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, "products/home.html", {
        "products": products,
        "query": query
    })
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, "products/detail.html", {
        "product": product
    })
def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id not in cart:
        cart.append(product_id)

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', [])

    products = Product.objects.filter(id__in=cart)

    total = sum(product.price for product in products)

    return render(request, 'products/cart.html', {
        'products': products,
        'total': total
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id in cart:
        cart.remove(product_id)

    request.session['cart'] = cart

    return redirect('cart')