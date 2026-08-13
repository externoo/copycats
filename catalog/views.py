from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect

from cart.cart import Cart

from .models import Category, Product


def register(request):
    if request.user.is_authenticated:
        return redirect("catalog:product_list")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("catalog:product_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def product_list(request, category_slug=None):
    products = Product.objects.select_related("category").all()

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    sort = request.GET.get("sort")
    sort_fields = {
        "price_asc": "price",
        "price_desc": "-price",
        "name_asc": "name",
        "name_desc": "-name",
    }
    if sort in sort_fields:
        products = products.order_by(sort_fields[sort])

    context = {
        "category": category,
        "products": products,
        "sort": sort,
    }
    return render(request, "catalog/product_list.html", context)


@login_required
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    in_cart_quantity = 0
    for item in Cart(request):
        if item["product"].id == product.id:
            in_cart_quantity = item["quantity"]
            break
    remaining_stock = max(product.stock - in_cart_quantity, 0)
    return render(
        request,
        "catalog/product_detail.html",
        {"product": product, "remaining_stock": remaining_stock},
    )
