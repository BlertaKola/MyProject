from flask_app import app
from flask import render_template, request, redirect, session, flash, url_for
from flask import send_from_directory
import urllib.request
import os
from werkzeug.utils import secure_filename
from flask_app.models.user import User
from flask_app.models.product import Product
from flask_app.models.order import Order
import uuid as uuid

UPLOAD_FOLDER = 'flask_app/static/img/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/addProduct')
def addProduct():
    if 'user' not in session:
        return redirect('/logout')
    return render_template('/addingProducts.html')


@app.route('/addProductForm', methods = ['GET','POST'])
def addProductForm():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'price': request.form['price'],
        'quantity': request.form['quantity'],
        'user_id':session['user']
    }
    file = request.files['imageProduct']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        imageProduct = str(uuid.uuid1()) + "_" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], imageProduct))
        data['imageProduct'] = imageProduct
    else:
        flash("Allowed image types are .png, .jpg, .jpeg", 'allowedError')
        return redirect(request.referrer)

    Product.addProduct(data)
    return redirect('/adminDashboard')



@app.route('/viewProduct/<int:id>')
def view(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'product_id': id,
        'user_id': session['user']
    }
    productReviews = Product.reviews(data)
    product = Product.getProductByID(data)
    print(product)
    loggedUser = User.getUserByID(data)
    return render_template("viewProduct.html", loggedUser = loggedUser, product = product, productReviews = productReviews)


@app.route('/leaveProductReview/<int:id>', methods = ['POST'])
def addReview(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'product_id': id,
        'user_id': session['user'],
        'content': request.form['content']
    }
    Product.addProductReview(data)
    return redirect(request.referrer)

@app.route('/addWishlist/<int:id>')
def addWishlist(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'product_id': id,
        'user_id': session['user']
    }
    Product.addToWishlist(data)
    return redirect(request.referrer)



@app.route('/removeFromWishlist/<int:id>')
def removeWishlist(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'product_id': id,
        'user_id': session['user']
    }
    Product.deleteFromWishlist(data)
    return redirect(request.referrer)


@app.route('/addToCart/<int:id>')
def addCart(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'product_id': id,
        'user_id': session['user']
    }
    Product.addToCart(data)
    return redirect(request.referrer)


@app.route('/removeFromCart/<int:id>')
def removeCart(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'product_id': id,
        'user_id': session['user']
    }
    Product.deleteFromCart(data)
    return redirect(request.referrer)


@app.route('/addProduct')
def addProducts():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    loggedUser = User.getUserByID(data)
    return render_template("addingProducts.html", loggedUser = loggedUser)






# @app.route('/deleteProduct/<int:id>')
# def deleteProduct(id):
#     if 'user' not in session:
#         return redirect('/logout')
#     data = {
#         'product_id': id,
#         'user_id': session['user']
#     }
#     product = Product.getProductByID(data)
#     if session['user'] == product['user_id']:
#         Product.deleteAllWishlists(data)
#         Product.deleteAllCarts(data)
#         Product.deleteAllReviews(data)
#         Product.deleteProducts(data)

#     return redirect(request.referrer)

@app.route('/editProduct/<int:id>')
def editProduct(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'product_id': id,
        'user_id': session['user']
    }
    product = Product.getProductByID(data)
    loggedUser = User.getUserByID(data)
    return render_template("editProduct.html", loggedUser = loggedUser, product = product )


@app.route('/editProductForm/<int:id>', methods = ['POST'])
def editForm(id):
    if 'user' not in session:
        return redirect('/logout')
    if not Product.validateProduct(request.form):
        flash("Please fill the fields correctly", 'error')
        return redirect(request.referrer)
    data = {
        'product_id': id,
        'user_id': session['user'],
        'name': request.form['name'],
        'description': request.form['description'],
        'price': request.form['price'],
        'quantity': request.form['quantity']
    }
    file = request.files['imageProduct']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        imageProduct = str(uuid.uuid1()) + "_" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], imageProduct))
        data['imageProduct'] = imageProduct
    else:
        flash("Allowed image types are .png, .jpg, .jpeg", 'allowedError')
        return redirect(request.referrer)

    Product.editProducts(data)
    return redirect('/adminDashboard')

@app.route('/orderProducts')
def makeOrderi():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user'],
    }
    myProducts = Order.makeOrder(data)
    for product in myProducts:
        data2 = {
            'product_id': product
        }
        Product.decreaseQuantity(data2)
    Product.deleteAllFromCart(data)
    return redirect('/dashboard')
