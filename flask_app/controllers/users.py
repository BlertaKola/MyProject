from flask_app import app
from flask import render_template, request, redirect, session, flash, jsonify
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
from flask import send_from_directory
import urllib.request
import os
from werkzeug.utils import secure_filename
from flask_app.models.user import User
from flask_app.models.product import Product
from flask_app.models.shopRating import ShopRating
from flask_app.models.order import Order
import uuid as uuid
import paypalrestsdk






paypalrestsdk.configure({
    "mode": "sandbox", # sandbox or live
    "client_id": "CLIENT_ID",
    "client_secret": "CLIENT_SECRET" })


# this is the paypal stuff
@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "500.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "500.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})



# it ends here




UPLOAD_FOLDER = 'flask_app/static/img/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/')
def welcome():
    if 'user' in session:
        return redirect('/adminDashboard')
    return render_template("Welcome.html")

@app.route('/loginPage')
def loginPage():
    if 'user' in session:
        return redirect('/adminDashboard')
    return render_template("loginPage.html")
    

@app.route('/loginUser', methods = ['POST'])
def loginUser():
    data = {
        'email' : request.form['email'],
        'password': request.form['password']
    }
    if len(request.form['email'])< 1:
        flash("Please enter the email", 'emailLogin')
        return redirect(request.referrer)
    if not User.getUserByEmail(data):
        flash("This email doesn't exit, try again", 'emailLogin')
        return redirect(request.referrer)
    user = User.getUserByEmail(data)
    
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Incorrect password", 'passwordLogin')
        return redirect(request.referrer)
    session['user'] = user['id']
    return redirect('/adminDashboard')


@app.route('/adminDashboard')
def adminDashboard():
    if 'user' not in session :
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    loggedUser = User.getUserByID(data)
    if loggedUser['role'] == 'Administrator':
        products = Product.getAllProducts()
        return render_template("adminDashboard.html", loggedUser = loggedUser, products = products)
    return redirect('/dashboard')
    
    
    






@app.route('/account')
def viewAccount():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    loggedUser = User.getUserByID(data)
    ratings = ShopRating.getAllRatings()
    return render_template("account.html", loggedUser = loggedUser, ratings = ratings)




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')






@app.route('/uploadPhoto', methods = ['POST'])
def uploadPhotoUser():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image = str(uuid.uuid1()) + "_" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], image))
        data['image'] = image
    else:
        flash("Allowed image types are .png, .jpg, .jpeg", 'allowedError')
        return redirect(request.referrer)

    User.uploadUserPhoto(data)
    return redirect(request.referrer)






@app.route('/dashboard')
def dashboard():
    if 'user' in session :
        data = {
        'user_id': session['user']
        }
        loggedUser = User.getUserByID(data)
        products = Product.getAllProducts()
        wishlists = Product.wishlist(data)
        carts = Product.carts(data)
        return render_template("dashboard.html", loggedUser = loggedUser, products = products, wishlists = wishlists, carts = carts)
    return redirect('/logout')






@app.route('/myWishlist')
def renderWishlist():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    loggedUser = User.getUserByID(data)
    carts = Product.carts(data)
    wishlists = User.usersWishlist(data)
    return render_template("myWishlist.html", wishlists = wishlists, loggedUser = loggedUser, carts = carts)





@app.route('/orders')
def ordersTemplate():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    orders = Order.getAllOrdersWithItems()
    loggedUser = User.getUserByID(data)
    return render_template("orders.html", loggedUser = loggedUser, orders = orders)




    
@app.route('/myCart')
def renderCart():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    loggedUser = User.getUserByID(data)
    carts = User.usersCart(data)
    sumTotal = User.sumTotalCart(data)
    print(carts)
    return render_template("myCart.html", carts = carts, loggedUser = loggedUser, sumTotal = sumTotal)



@app.route('/registerPage')
def registerPage():
    if 'user' in session:
        return redirect('/adminDashboard')
    return render_template("registerPage.html")
    




@app.route('/registerUser', methods = ['POST'])
def registerUser():
    if not User.validateUser(request.form):
        flash("Something is wrong, check the errors", 'signUpError')
        return redirect(request.referrer)
    if User.getUserByEmail(request.form):
        flash("This email already exists, try another one", 'emailRegister')
        return redirect(request.referrer)
    data = {
        'username': request.form['username'],
        'email' : request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'address': request.form['address'],
        'role': 'Customer'
    }
    User.addUser(data)
    flash("You can now login", 'signUpSuccess')
    return redirect(request.referrer)






@app.route('/ratings')
def rating():
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user']
    }
    loggedUser = User.getUserByID(data)
    ratings = ShopRating.getAllRatings()
    return render_template("shopRatings.html", loggedUser = loggedUser, ratings = ratings)





@app.route('/leaveReview', methods = ['POST'])
def review():
    if 'user' not in session:
        return redirect('/logout')
    if not ShopRating.validateRating(request.form):
        flash("Something is wrong", 'error')
        return redirect(request.referrer)
    data = {
        'user_id': session['user'],
        'content': request.form['content']
    }
    ShopRating.addRating(data)
    print('blerta')
    return redirect(request.referrer)



