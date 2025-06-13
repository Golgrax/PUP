# admin_app/admin_web_server.py
from flask import Flask, request, redirect, url_for
from dominate import document
from dominate.tags import *
from shared.database import get_all_products, add_product, update_product, delete_product
import os

app = Flask(__name__, static_folder=os.path.join('..', 'assets'), static_url_path='/static')

def create_admin_page(products):
    doc = document(title="PUP Shop - Admin Panel")
    with doc.head:
        meta(charset="UTF-8")
        link(href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css", rel="stylesheet")

    with doc.body(cls="bg-gray-200 p-8"):
        img(src="/static/images/pup_logo.png", cls="mx-auto h-16 w-16 mb-4")
        h1("INVENTORY MANAGEMENT", cls="text-3xl font-bold text-center text-[#722F37] mb-6 border-b-2 border-[#722F37] pb-2")
        
        # Form for CRUD operations
        with form(action="/add", method="POST", cls="bg-white p-6 rounded-lg shadow-md mb-8"):
            with div(cls="grid grid-cols-1 md:grid-cols-2 gap-4"):
                div(label("ITEM ID (for Update/Delete):", _for="item_id", cls="font-bold"), input_(type="text", name="item_id", id="item_id", cls="p-2 border rounded w-full"))
                div(label("ITEM NAME:", _for="item_name", cls="font-bold"), input_(type="text", name="item_name", id="item_name", required=True, cls="p-2 border rounded w-full"))
                div(label("QUANTITY:", _for="quantity", cls="font-bold"), input_(type="number", name="quantity", id="quantity", required=True, cls="p-2 border rounded w-full"))
                div(label("PRICE:", _for="price", cls="font-bold"), input_(type="text", name="price", id="price", required=True, cls="p-2 border rounded w-full"))
            
            with div(cls="flex justify-center space-x-4 mt-6"):
                button("Add Item", type="submit", formaction="/add", formmethod="post", cls="bg-green-600 text-white px-6 py-2 rounded-lg")
                button("Update Item", type="submit", formaction="/update", formmethod="post", cls="bg-blue-600 text-white px-6 py-2 rounded-lg")
                button("Delete Item", type="submit", formaction="/delete", formmethod="post", cls="bg-red-600 text-white px-6 py-2 rounded-lg")

        # Table of existing inventory
        with table(cls="w-full bg-white rounded-lg shadow-md"):
            with thead(cls="bg-[#722F37] text-white"):
                with tr():
                    th("ID", cls="p-3")
                    th("NAME", cls="p-3")
                    th("QUANTITY", cls="p-3")
                    th("PRICE", cls="p-3")
            with tbody():
                for p in products:
                    with tr(cls="border-b hover:bg-gray-100"):
                        td(p['id'], cls="p-3")
                        td(p['name'], cls="p-3")
                        td(p['stock'], cls="p-3")
                        td(f"₱{p['price']:.2f}", cls="p-3")
    return doc.render()

@app.route("/")
def admin_home():
    products = get_all_products()
    return create_admin_page(products)

@app.route("/add", methods=["POST"])
def admin_add():
    add_product(request.form['item_name'], request.form['quantity'], request.form['price'])
    return redirect(url_for('admin_home'))

@app.route("/update", methods=["POST"])
def admin_update():
    update_product(request.form['item_id'], request.form['item_name'], request.form['quantity'], request.form['price'])
    return redirect(url_for('admin_home'))

@app.route("/delete", methods=["POST"])
def admin_delete():
    delete_product(request.form['item_id'])
    return redirect(url_for('admin_home'))

def run_admin_server():
    # Use a different port for the admin app
    app.run(host='127.0.0.1', port=5001, debug=False)