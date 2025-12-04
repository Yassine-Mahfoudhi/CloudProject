from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Sample product data
PRODUCTS = [
    {
        'id': 1,
        'name': 'Wireless Headphones',
        'price': 79.99,
        'image': 'https://picsum.photos/seed/headphones/400/400',
        'description': 'High-quality wireless headphones with noise cancellation and 30-hour battery life.'
    },
    {
        'id': 2,
        'name': 'Smart Watch',
        'price': 199.99,
        'image': 'https://picsum.photos/seed/watch/400/400',
        'description': 'Feature-rich smartwatch with fitness tracking, heart rate monitor, and smartphone connectivity.'
    },
    {
        'id': 3,
        'name': 'Laptop Stand',
        'price': 49.99,
        'image': 'https://picsum.photos/seed/laptop/400/400',
        'description': 'Ergonomic aluminum laptop stand with adjustable height and ventilation.'
    },
    {
        'id': 4,
        'name': 'Mechanical Keyboard',
        'price': 129.99,
        'image': 'https://picsum.photos/seed/keyboard/400/400',
        'description': 'RGB backlit mechanical keyboard with Cherry MX switches and programmable keys.'
    },
    {
        'id': 5,
        'name': 'USB-C Hub',
        'price': 39.99,
        'image': 'https://picsum.photos/seed/usbhub/400/400',
        'description': 'Multi-port USB-C hub with HDMI, USB 3.0, and SD card reader support.'
    },
    {
        'id': 6,
        'name': 'Wireless Mouse',
        'price': 29.99,
        'image': 'https://picsum.photos/seed/mouse/400/400',
        'description': 'Ergonomic wireless mouse with precision tracking and long battery life.'
    }
]

def get_cart():
    """Get or initialize cart in session"""
    if 'cart' not in session:
        session['cart'] = {}
    return session['cart']

def get_cart_total():
    """Calculate total price of items in cart"""
    cart = get_cart()
    total = 0
    for product_id, quantity in cart.items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            total += product['price'] * quantity
    return round(total, 2)

@app.route('/')
def index():
    """Home page - display all products"""
    return render_template('index.html', products=PRODUCTS)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('index'))
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add product to cart"""
    cart = get_cart()
    quantity = int(request.form.get('quantity', 1))
    
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    
    session['cart'] = cart
    flash('Product added to cart!', 'success')
    return redirect(request.referrer or url_for('index'))

@app.route('/cart')
def cart():
    """Shopping cart page"""
    cart = get_cart()
    cart_items = []
    
    for product_id, quantity in cart.items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': round(product['price'] * quantity, 2)
            })
    
    total = get_cart_total()
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    """Update quantity of item in cart"""
    cart = get_cart()
    quantity = int(request.form.get('quantity', 0))
    
    if quantity <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = quantity
    
    session['cart'] = cart
    flash('Cart updated!', 'success')
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Remove item from cart"""
    cart = get_cart()
    cart.pop(str(product_id), None)
    session['cart'] = cart
    flash('Item removed from cart!', 'success')
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    """Checkout page"""
    cart = get_cart()
    if not cart:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('cart'))
    
    cart_items = []
    for product_id, quantity in cart.items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': round(product['price'] * quantity, 2)
            })
    
    total = get_cart_total()
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/place_order', methods=['POST'])
def place_order():
    """Process order"""
    # In a real application, you would process payment and save order to database
    name = request.form.get('name')
    email = request.form.get('email')
    address = request.form.get('address')
    
    if not all([name, email, address]):
        flash('Please fill in all fields', 'error')
        return redirect(url_for('checkout'))
    
    # Clear cart after order
    session['cart'] = {}
    flash(f'Thank you for your order, {name}! Your order has been placed successfully.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

