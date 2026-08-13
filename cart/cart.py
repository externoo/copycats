from decimal import Decimal

from catalog.models import Product

CART_SESSION_KEY = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        new_quantity = self.cart[product_id]["quantity"] + quantity
        self.cart[product_id]["quantity"] = min(new_quantity, product.stock)
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        products_by_id = {str(product.id): product for product in products}

        for product_id, item in self.cart.items():
            product = products_by_id.get(product_id)
            if product is None:
                continue
            price = Decimal(item["price"])
            yield {
                "product": product,
                "quantity": item["quantity"],
                "price": price,
                "total_price": price * item["quantity"],
            }

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())
