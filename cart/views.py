from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product

from .cart import Cart


@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart})


@login_required
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1
    quantity = min(max(quantity, 1), product.stock)
    if quantity > 0:
        cart.add(product=product, quantity=quantity)
    return redirect("catalog:product_list")


@login_required
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")
