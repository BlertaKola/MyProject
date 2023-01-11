from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash

class User:
    db_name = 'last'
    def __init__(self,data):
        self.id = data['id'],
        self.first_name = data['first_name'],
        self.last_name = data['last_name'],
        self.address = data['address'],
        self.email = data['email'],
        self.password = data['password'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    
    @classmethod
    def addUser(cls,data):
        query = 'INSERT INTO users ( username, email, password, address , role) VALUES ( %(username)s, %(email)s, %(password)s, %(address)s, %(role)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def uploadUserPhoto(cls,data):
        query = 'UPDATE users SET image = %(image)s WHERE id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)
    

    # @classmethod
    # def updateUserInfo(cls,data)


    @classmethod
    def getUserByID(cls,data):
        query = 'SELECT * FROM users WHERE id = %(user_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return result[0]

    
    @classmethod
    def getUserByEmail(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if result:
            return result[0]
        return False

    

    @classmethod
    def usersWishlist(cls,data):
        query = 'SELECT * FROM products LEFT JOIN wishlists ON wishlists.product_id = products.id LEFT JOIN users ON wishlists.user_id = users.id WHERE wishlists.user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        wishlists = []
        if results:
            for row in results:
                wishlists.append(row)
            return wishlists
        return results


    @classmethod
    def usersCart(cls,data):
        query = 'SELECT * FROM products LEFT JOIN carts ON carts.product_id = products.id LEFT JOIN users ON carts.user_id = users.id WHERE carts.user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        carts = []
        if results:
            for row in results:
                carts.append(row)
            return carts
        return results
    


    @classmethod
    def sumTotalCart(cls,data):
        query = 'SELECT SUM(products.price) AS sumTotal FROM products LEFT JOIN carts ON carts.product_id = products.id LEFT JOIN users ON carts.user_id = users.id WHERE users.id = %(user_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if result:
            return result[0]
        return False

    # select sum(products.price) as sumTotal FROM orders LEFT JOIN orderItems on orderItems.order_id = orders.id LEFT JOIN products on orderItems.product_id = products.id GROUP BY orders.id; 




    @classmethod
    def usersOrders(cls,data):
        query = ''
        results = connectToMySQL(cls.db_name).query_db(query,data)
        carts = []
        if results:
            for row in results:
                carts.append(row)
            return carts
        return results


    @staticmethod
    def validateUser(user):
        is_valid = True
        if len(user['username']) < 1:
            flash("Username is required to register!", 'username')
            is_valid = False
        if 'address' not in user:
            flash("Please add your address", 'address')
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailRegister')
            is_valid = False 
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long!", 'passwordRegister')
            is_valid = False
        if user['password'] != user['confirmPassword']:
            flash("Password do not match, try again!", 'passwordConfirm')
            is_valid = False
        return is_valid