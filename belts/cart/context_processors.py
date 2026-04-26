from belts.cart.models import Cart


def cart_items_count(request):
    if not request.user.is_authenticated:
        return {"cart_items_count": 0}

    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return {"cart_items_count": 0}

    total_quantity = sum(item.quantity for item in cart.items.all())

    return {"cart_items_count": total_quantity}