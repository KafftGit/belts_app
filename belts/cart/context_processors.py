from belts.cart.models import Cart


def cart_items_count(request):
    if not request.user.is_authenticated:
        return {"cart_items_count": 0}

    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return {"cart_items_count": 0}

    return {"cart_items_count": cart.items.count()}
