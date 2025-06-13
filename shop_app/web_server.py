# shop_app/web_server.py
from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from dominate import document
from dominate.tags import *
from shared.database import get_all_products, hash_password, get_db_connection
import os

# Create the Flask application
# The static_folder points to the shared 'assets' directory
app = Flask(__name__, static_folder=os.path.join('..', 'assets'), static_url_path='/static')

def create_page(page_title, active_section_id):
    """
    Generates the base HTML structure for all pages using dominate.
    This function recreates the single-page application feel from your HTML sample.
    """
    doc = document(title=page_title)

    with doc.head:
        meta(charset="UTF-8")
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        # Tailwind CSS and Font Awesome for icons
        link(href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css", rel="stylesheet")
        link(href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css", rel="stylesheet")
        # Link to our custom font stylesheet
        link(href="/static/css/style.css", rel="stylesheet")
        
        style("""
            .section { display: none; }
            .section.active { display: block; }
            .bottom-nav-item.active { color: #FFD700; }
        """)

    # CORRECTED: Changed cls to class_
    with doc.body(class_="bg-gray-100"):
        # Padding bottom for nav bar
        with div(id="app-container", class_="pb-24"): 
            # Header
            with header(class_="bg-[#722F37] text-white p-3 shadow-md flex items-center justify-between sticky top-0 z-40"):
                img(src="/static/images/pup_logo.png", class_="h-10 w-10")
                h1("PUP E-Commerce", class_="text-xl font-bold")
                div(class_="space-x-4", _id="top-nav-icons")

            # Main Content Area
            with main(id="main-content"):
                # All sections are rendered, but only one is 'active'
                _create_login_register_section(active_section_id)
                _create_shopping_cart_section(active_section_id)
                _create_checkout_section(active_section_id)
                _create_profile_section(active_section_id)
                _create_order_history_section(active_section_id)
                _create_contact_us_section(active_section_id)
                # Homepage is special as it's dynamically populated
                _create_homepage_section(active_section_id, get_all_products())

        # Fixed Bottom Navigation Bar
        with nav(class_="fixed bottom-0 left-0 right-0 bg-[#722F37] text-white p-2 shadow-t-lg z-50"):
            with div(class_="flex justify-around"):
                # CORRECTED: Changed cls to class_
                button(i(class_="fas fa-home text-2xl"), span("Home", class_="text-xs block"),
                       class_="text-center bottom-nav-item active" if active_section_id == 'homepage' else "text-center bottom-nav-item opacity-70",
                       onclick="showSection('homepage')")
                button(i(class_="fas fa-shopping-cart text-2xl"), span("Cart", class_="text-xs block"),
                       class_="text-center bottom-nav-item active" if active_section_id == 'cart' else "text-center bottom-nav-item opacity-70",
                       onclick="showSection('cart')")
                button(i(class_="fas fa-user text-2xl"), span("Profile", class_="text-xs block"),
                       class_="text-center bottom-nav-item active" if active_section_id == 'profile' else "text-center bottom-nav-item opacity-70",
                       onclick="showSection('profile')")
        
        # Help button
        button("?", class_="fixed bottom-20 right-4 bg-black text-white w-12 h-12 rounded-full text-2xl shadow-lg z-40", onclick="showSection('contact')")

        # JavaScript for SPA functionality
        _add_spa_javascript()
        
    return doc.render()

# --- Section Creation Functions ---
# All cls="..." instances below have been corrected to class_="..."

def _create_login_register_section(active_id):
    # Registration Page (Image 1)
    with section(id='register', class_='p-5 section active' if active_id == 'register' else 'p-5 section'):
        with div(class_="text-center mb-6"):
            img(src="/static/images/pup_logo.png", class_="mx-auto h-20 w-20 mb-4")
            h2("Mula sayo para sa bayan", class_="text-3xl font-bold text-[#722F37]")
        
        with form(action="/register", method="POST", class_="bg-white p-6 rounded-lg shadow-md"):
            div(label("Name:", _for="reg_name", class_="block mb-2 font-bold"),
                input_(type="text", id="reg_name", name="name", required=True, class_="w-full p-2 border rounded mb-4"),
                class_="mb-4")
            div(label("Email Address:", _for="reg_email", class_="block mb-2 font-bold"),
                input_(type="email", id="reg_email", name="email", required=True, class_="w-full p-2 border rounded mb-4"),
                class_="mb-4")
            div(label("Password:", _for="reg_password", class_="block mb-2 font-bold"),
                input_(type="password", id="reg_password", name="password", required=True, class_="w-full p-2 border rounded mb-4"),
                class_="mb-4")
            div(label("Confirm Password:", _for="reg_confirm_password", class_="block mb-2 font-bold"),
                input_(type="password", id="reg_confirm_password", name="confirm_password", required=True, class_="w-full p-2 border rounded"),
                class_="mb-4")
            
            button("Back to LOGIN", type="button", onclick="showSection('login')", class_="w-full bg-cyan-400 text-white p-3 rounded-lg mb-2 hover:bg-cyan-500")
            button("REGISTER", type="submit", class_="w-full bg-cyan-500 text-white p-3 rounded-lg hover:bg-cyan-600")

    # Login Page (Similar structure)
    with section(id='login', class_='p-5 section active' if active_id == 'login' else 'p-5 section'):
        with div(class_="text-center mb-6"):
             img(src="/static/images/pup_logo.png", class_="mx-auto h-20 w-20 mb-4")
             h2("Welcome Back!", class_="text-3xl font-bold text-[#722F37]")
        
        with form(action="/login", method="POST", class_="bg-white p-6 rounded-lg shadow-md"):
            div(label("Email Address:", _for="login_email", class_="block mb-2 font-bold"),
                input_(type="email", id="login_email", name="email", required=True, class_="w-full p-2 border rounded"),
                class_="mb-4")
            div(label("Password:", _for="login_password", class_="block mb-2 font-bold"),
                input_(type="password", id="login_password", name="password", required=True, class_="w-full p-2 border rounded"),
                class_="mb-4")

            button("LOGIN", type="submit", class_="w-full bg-[#722F37] text-white p-3 rounded-lg mb-2 hover:bg-[#5a252a]")
            a("Forgot Password?", href="#", class_="text-sm text-cyan-600 block text-center mb-4")
            button("Create Account", type="button", onclick="showSection('register')", class_="w-full bg-gray-200 text-gray-700 p-3 rounded-lg")


def _create_homepage_section(active_id, products):
    with section(id='homepage', class_='p-4 section active' if active_id == 'homepage' else 'p-4 section'):
        img(src="/static/images/pup_logo.png", class_="w-full h-40 object-contain rounded-lg mb-4", alt="PUP Main Gate")
        
        h3("Best Sellers", class_="text-2xl font-bold text-[#722F37] mb-4")
        with div(class_="grid grid-cols-2 gap-4"):
            for p in products:
                with div(class_="bg-white rounded-lg shadow-md p-3 text-center"):
                    img(src=p['image_url'], alt=p['name'], class_="h-32 w-full object-contain mb-2")
                    p(p['name'], class_="font-bold text-sm h-10")
                    p(f"₱{p['price']:.2f}", class_="text-red-600 font-bold mb-2")
                    button("Add to Cart", class_="w-full bg-red-500 text-white text-sm py-1 rounded-full",
                           onclick=f"addToCart({p['id']}, '{p['name']}', {p['price']}, '{p['image_url']}')")


def _create_shopping_cart_section(active_id):
    # This is a template. The actual content is built by JavaScript.
    with section(id='cart', class_='p-4 section active' if active_id == 'cart' else 'p-4 section'):
        div(h2("Shopping Cart", class_="text-2xl font-bold text-[#722F37] mb-4"),
            class_="flex justify-between items-center")
        
        with div(class_="flex justify-between items-center mb-4 bg-white p-2 rounded-lg"):
            div(input_(type="checkbox", id="select-all-cart", onchange="toggleSelectAll(this)"), label(" Select All", _for="select-all-cart"), class_="flex items-center space-x-2")
            button("Delete", class_="text-red-500", onclick="deleteSelectedItems()")
            
        div(id="cart-items-container", class_="space-y-3 mb-4") # JS will populate this
        
        with div(id="cart-summary", class_="bg-white p-4 rounded-lg shadow-t-lg fixed bottom-16 left-0 right-0"):
            with div(class_="flex justify-between items-center mb-4"):
                span("Subtotal:", class_="font-bold")
                span("₱0.00", id="cart-subtotal", class_="font-bold")
            button("CHECK OUT", class_="w-full bg-[#722F37] text-white p-3 rounded-lg font-bold", onclick="showSection('checkout')")

def _create_checkout_section(active_id):
    # This is a template. JS will populate the summary.
    with section(id='checkout', class_='p-4 section active' if active_id == 'checkout' else 'p-4 section'):
        h2("STUDY WITH PASSION", class_="text-2xl font-bold text-center text-[#722F37] mb-6")
        
        # Order Summary
        with div(class_="bg-white p-4 rounded-lg shadow-md mb-6"):
             h3("Order Summary", class_="font-bold border-b pb-2 mb-2")
             div(span("Subtotal"), span("₱0.00", id="checkout-subtotal", class_="float-right"), class_="mb-2")
             div(span("Shipping"), span("₱36.00", id="checkout-shipping", class_="float-right"), class_="mb-2")
             hr(class_="my-2")
             div(span("Total", class_="font-bold"), span("₱36.00", id="checkout-total", class_="font-bold float-right"), class_="text-lg")
        
        # Payment Method
        with div(class_="bg-white p-4 rounded-lg shadow-md mb-6"):
            h3("Payment Method", class_="font-bold mb-2")
            div(input_(type="radio", name="payment", id="cod", checked=True), label(" Cash on delivery", _for="cod"), class_="flex items-center")
        
        button("CHECK OUT NOW!", class_="w-full bg-red-600 text-white p-4 rounded-lg font-bold text-lg")


def _create_profile_section(active_id):
    with section(id='profile', class_='p-4 section active' if active_id == 'profile' else 'p-4 section'):
        div(i(class_="fas fa-user-circle text-8xl text-gray-400"), class_="text-center mb-4")
        
        with div(class_="bg-white p-4 rounded-lg shadow-md mb-4"):
            h3("Address 1", class_="font-bold")
            p("Juan Dela Cruz", class_="text-gray-600")
            p("123 Sampaguita St, Sampaloc, Manila", class_="text-gray-600")
            p("0917-123-4567", class_="text-gray-600")
        
        with div(class_="bg-white rounded-lg shadow-md"):
            a(div("Order History", i(class_="fas fa-chevron-right float-right text-gray-400")), href="#", onclick="showSection('order_history')", class_="block p-3 border-b")
            a(div("User Settings", i(class_="fas fa-chevron-right float-right text-gray-400")), href="#", class_="block p-3 border-b")
            a(div("Change Password", i(class_="fas fa-chevron-right float-right text-gray-400")), href="#", class_="block p-3")


def _create_order_history_section(active_id):
    with section(id='order_history', class_='p-4 section active' if active_id == 'order_history' else 'p-4 section'):
        h2("Order History", class_="text-2xl font-bold text-[#722F37] mb-4 text-center p-3 bg-white rounded-lg shadow-md")
        with div(class_="overflow-x-auto"):
            with table(class_="w-full text-left bg-white rounded-lg shadow-md"):
                with thead():
                    with tr(class_="border-b"):
                        th("Ref No.", class_="p-3")
                        th("Status", class_="p-3")
                        th("Items", class_="p-3")
                        th("Payment", class_="p-3")
                with tbody():
                    with tr(class_="border-b"):
                        td("PUPSHP-001", class_="p-3")
                        td("Delivered", class_="p-3 text-green-600")
                        td("2", class_="p-3")
                        td("₱356.00", class_="p-3")
                    with tr():
                        td("PUPSHP-002", class_="p-3")
                        td("Shipped", class_="p-3 text-blue-600")
                        td("1", class_="p-3")
                        td("₱140.00", class_="p-3")

def _create_contact_us_section(active_id):
    with section(id='contact', class_='p-4 section active' if active_id == 'contact' else 'p-4 section'):
        h2("Contact Us", class_="text-2xl font-bold text-center text-[#722F37] mb-6")
        with form(class_="bg-white p-6 rounded-lg shadow-md"):
            div(label("Name:", _for="contact_name", class_="block mb-2 font-bold"),
                input_(type="text", id="contact_name", name="name", class_="w-full p-2 border rounded"), class_="mb-4")
            div(label("Email Address:", _for="contact_email", class_="block mb-2 font-bold"),
                input_(type="email", id="contact_email", name="email", class_="w-full p-2 border rounded"), class_="mb-4")
            div(label("Message", i(class_="fas fa-question-circle text-gray-400 ml-1"), _for="contact_message", class_="block mb-2 font-bold"),
                textarea(id="contact_message", name="message", rows="5", class_="w-full p-2 border rounded"), class_="mb-6")
            button("Submit", type="submit", class_="w-full bg-[#722F37] text-white p-3 rounded-lg font-bold")

def _add_spa_javascript():
    # This function remains unchanged as it contains the correct JavaScript logic
    script(src="https://unpkg.com/localforage@1.10.0/dist/localforage.min.js")
    script(type="text/javascript").add_raw("""
        let cart = [];

        function showSection(sectionId) {
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            const sectionToShow = document.getElementById(sectionId);
            if(sectionToShow) {
                sectionToShow.classList.add('active');
            } else {
                console.error("Section not found:", sectionId);
                document.getElementById('homepage').classList.add('active'); // Fallback
            }

            document.querySelectorAll('.bottom-nav-item').forEach(b => {
                b.classList.add('opacity-70');
                b.classList.remove('active');
            });
            const activeNav = document.querySelector(`button[onclick="showSection('${sectionId}')"]`);
            if(activeNav) {
                activeNav.classList.remove('opacity-70');
                activeNav.classList.add('active');
            }
            if(sectionId === 'cart') updateCartDisplay();
            if(sectionId === 'checkout') updateCheckoutDisplay();
        }

        async function loadCart() {
            const savedCart = await localforage.getItem('pup_cart');
            cart = savedCart || [];
            updateCartDisplay();
        }
        
        async function saveCart() {
            await localforage.setItem('pup_cart', cart);
        }

        function addToCart(id, name, price, image_url) {
            const existingItem = cart.find(item => item.id === id);
            if (existingItem) {
                existingItem.quantity++;
            } else {
                cart.push({ id, name, price, image_url, quantity: 1, selected: true });
            }
            saveCart();
            updateCartDisplay();
            showNotification(`${name} added to cart!`);
        }
        
        function updateQuantity(id, change) {
            const item = cart.find(item => item.id === id);
            if(item) {
                item.quantity += change;
                if(item.quantity <= 0) {
                    cart = cart.filter(i => i.id !== id);
                }
            }
            saveCart();
            updateCartDisplay();
        }

        function toggleItemSelection(id, checkbox) {
            const item = cart.find(item => item.id === id);
            if(item) item.selected = checkbox.checked;
            saveCart();
            updateCartDisplay();
        }

        function toggleSelectAll(checkbox) {
            cart.forEach(item => item.selected = checkbox.checked);
            document.querySelectorAll('.cart-item-checkbox').forEach(cb => cb.checked = checkbox.checked);
            saveCart();
            updateCartDisplay();
        }

        function deleteSelectedItems() {
            cart = cart.filter(item => !item.selected);
            saveCart();
            updateCartDisplay();
        }

        function updateCartDisplay() {
            const container = document.getElementById('cart-items-container');
            const subtotalEl = document.getElementById('cart-subtotal');
            if (!container || !subtotalEl) return;

            if (cart.length === 0) {
                container.innerHTML = `<div class="text-center text-gray-500 py-10"><i class="fas fa-shopping-cart text-4xl mb-2"></i><p>Your cart is empty.</p></div>`;
                subtotalEl.textContent = '₱0.00';
                return;
            }

            container.innerHTML = cart.map(item => `
                <div class="flex items-center bg-white p-2 rounded-lg space-x-3">
                    <input type="checkbox" class="cart-item-checkbox" ${item.selected ? 'checked' : ''} onchange="toggleItemSelection(${item.id}, this)">
                    <img src="${item.image_url}" class="w-16 h-16 object-contain rounded-md">
                    <div class="flex-grow">
                        <p class="font-bold text-sm">${item.name}</p>
                        <p class="text-red-500 font-bold">₱${item.price.toFixed(2)}</p>
                    </div>
                    <div class="flex items-center space-x-2">
                        <button onclick="updateQuantity(${item.id}, -1)" class="w-6 h-6 bg-gray-200 rounded-full">-</button>
                        <span>${item.quantity}</span>
                        <button onclick="updateQuantity(${item.id}, 1)" class="w-6 h-6 bg-gray-200 rounded-full">+</button>
                    </div>
                </div>
            `).join('');

            const subtotal = cart.filter(i => i.selected).reduce((sum, item) => sum + item.price * item.quantity, 0);
            subtotalEl.textContent = `₱${subtotal.toFixed(2)}`;
            
            const allSelected = cart.every(i => i.selected);
            document.getElementById('select-all-cart').checked = allSelected && cart.length > 0;
        }

        function updateCheckoutDisplay() {
            const subtotal = cart.filter(i => i.selected).reduce((sum, item) => sum + item.price * item.quantity, 0);
            const shipping = 36.00;
            const total = subtotal + shipping;

            document.getElementById('checkout-subtotal').textContent = `₱${subtotal.toFixed(2)}`;
            document.getElementById('checkout-shipping').textContent = `₱${shipping.toFixed(2)}`;
            document.getElementById('checkout-total').textContent = `₱${total.toFixed(2)}`;
        }
        
        function showNotification(message) {
            const notif = document.createElement('div');
            // CORRECTED JavaScript to use className
            notif.className = 'fixed top-16 left-1/2 -translate-x-1/2 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
            notif.textContent = message;
            document.body.appendChild(notif);
            setTimeout(() => { notif.remove(); }, 2000);
        }

        // Initial load
        document.addEventListener('DOMContentLoaded', () => {
            const initialSection = window.location.hash.substring(1) || 'homepage';
            showSection(initialSection);
            loadCart();
        });
    """)

# --- Flask Routes ---
@app.route("/")
def index():
    return create_page("PUP Shop - Home", "homepage")

@app.route("/show/<section>")
def show_section(section):
    # This allows direct navigation via URL, e.g., /show/cart
    valid_sections = ['login', 'register', 'cart', 'checkout', 'profile', 'order_history', 'contact', 'homepage']
    if section in valid_sections:
        return create_page(f"PUP Shop - {section.title()}", section)
    return redirect(url_for('index'))

@app.route("/register", methods=["POST"])
def handle_register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return "Passwords do not match!", 400

    password_hash = hash_password(password)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)", (name, email, password_hash))
        conn.commit()
    except mysql.connector.Error as err:
        return f"Error: {err}", 500
    finally:
        cursor.close()
        conn.close()

    # On success, redirect to login page
    return create_page("PUP Shop - Login", "login")

def run_shop_server():
    # Use a different port for the shop app
    app.run(host='127.0.0.1', port=5000, debug=False)