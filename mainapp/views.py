# mainapp/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem
from django.core.paginator import Paginator

def index(request):
    return render(request, 'mainapp/index.html')

def about(request):
    return render(request, 'mainapp/about.html')

def contact(request):
    return render(request, 'mainapp/contact.html')

CATEGORY_SLUGS = {
    'pampers': 'pampers',
    'soap': 'soap',
    'stroller': 'stroller',
    'bottle': 'bottle',
    'boys-fashion': 'boys',
    'boys_fashions': 'boys',
    'boys': 'boys', 
    'girls_fashions': 'girls',
    'offers': 'offers',
    'offer': 'offers'
}

def product_list(request, category):
    
    category_key = CATEGORY_SLUGS.get(category.lower())
    if not category_key:
        products = Product.objects.none()
    else:
        products = Product.objects.filter(category=category_key)


    price_range = request.GET.get('price')
    free_shipping = request.GET.get('free_shipping')
    discounts = request.GET.get('discounts')

    if price_range:
        if price_range == "100-1000":
            products = products.filter(price__gte=100, price__lte=1000)
        elif price_range == "1000-1500":
            products = products.filter(price__gte=1000, price__lte=1500)
        elif price_range == "1500-2000":
            products = products.filter(price__gte=1500, price__lte=2000)

    if free_shipping == '1':
        products = products.filter(free_shipping=True)

    if discounts == '1':
        products = products.filter(discount__gt=0)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'category': category.title(),
        'page_obj': page_obj,
        'range_five': range(5),
        'filters': {
            'price': price_range,
            'free_shipping': free_shipping,
            'discounts': discounts,
        }
    }
    return render(request, 'mainapp/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all()

    context = {
        'product': product,
        'images': images,
    }
    return render(request, 'mainapp/product_detail.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

# -------------------
# Utility functions
# -------------------
def get_cart(request):
    """Get cart from session or create new one"""
    return request.session.get('cart', {})

def save_cart(request, cart):
    """Save updated cart in session"""
    request.session['cart'] = cart
    request.session.modified = True

def get_cart_count(cart):
    """Total quantity of items in cart"""
    return sum(cart.values())

def get_cart_items(cart):
    """Return list of cart items with product and quantity"""
    items = []
    for product_id, qty in cart.items():
        product = get_object_or_404(Product, id=product_id)
        items.append({
            'product': product,
            'quantity': qty
        })
    return items

def get_cart_subtotal(cart):
    subtotal = 0
    for product_id, qty in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal += float(product.price) * qty
    return subtotal

# -------------------
# Views
# -------------------
def cart_view(request):
    cart = get_cart(request)
    cart_items = get_cart_items(cart)
    subtotal = get_cart_subtotal(cart)
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'cart_count': get_cart_count(cart)
    }
    return render(request, 'mainapp/cart.html', context)

def add_to_cart(request, product_id):
    cart = get_cart(request)
    qty = int(request.POST.get('quantity', 1))
    pid = str(product_id)

    # Merge instead of overwrite
    cart[pid] = cart.get(pid, 0) + qty

    save_cart(request, cart)
    return redirect('cart')

def buy_now(request, product_id):
    """
    If you want buy now to also merge:
    """
    cart = get_cart(request)
    qty = int(request.POST.get('quantity', 1))
    pid = str(product_id)

    cart[pid] = cart.get(pid, 0) + qty

    save_cart(request, cart)
    return redirect('cart')

def update_cart(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)

    if request.method == 'POST':
        qty = request.POST.get('quantity')
        action = request.POST.get('action')

        if qty is not None:
            try:
                qty = int(qty)
                if qty < 1:
                    qty = 1
                cart[pid] = qty
            except ValueError:
                pass
        else:
            if pid in cart:
                if action == 'increase':
                    cart[pid] += 1
                elif action == 'decrease':
                    cart[pid] = max(1, cart[pid] - 1)

    save_cart(request, cart)
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)

    if pid in cart:
        del cart[pid]

    save_cart(request, cart)
    return redirect('cart')

# -------------------
# Context processor
# -------------------
def cart_count_processor(request):
    cart = get_cart(request)
    return {'cart_count': get_cart_count(cart)}

def checkout_page(request):
    # Clear cart from session
    request.session['cart'] = {}
    request.session.modified = True
    return render(request, 'mainapp/checkout.html')
