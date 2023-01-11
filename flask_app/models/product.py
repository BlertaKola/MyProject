from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Product:
    db_name = 'last'
    def __init__(self,data):
        self.id = data['id'],
        self.name = data['name'],
        self.description = data['description'],
        self.price = data['price'],
        self.quantity = data['quantity'],
        self.imageProduct = data['imageProduct'],
        self.user_id = data['user_id'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    @classmethod
    def addProduct(cls,data):
        query = 'INSERT INTO products ( name, description, price, quantity, user_id, imageProduct ) VALUES ( %(name)s, %(description)s, %(price)s, %(quantity)s, %(user_id)s, %(imageProduct)s ) ;'
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def editProducts(cls,data):
        query = 'UPDATE products SET name = %(name)s, description = %(description)s, price = %(price)s, imageProduct = %(imageProduct)s, quantity = %(quantity)s WHERE id = %(product_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def decreaseQuantity(cls,data):
        query = 'UPDATE products SET quantity = quantity-1 WHERE id = %(product_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)



    
    @classmethod
    def getProductByID(cls,data):
        query = 'SELECT * FROM products WHERE products.id = %(product_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results[0]

    @classmethod
    def deleteProducts(cls,data):
        query = 'DELETE FROM products WHERE id = %(product_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)
    


    @classmethod
    def getAllProducts(cls):
        query = 'SELECT * FROM products LEFT JOIN users ON products.user_id = users.id;'
        products = []
        results = connectToMySQL(cls.db_name).query_db(query)
        if results:
            for row in results:
                products.append(row)
            return products
        return False
    

    @classmethod
    def addToWishlist(cls,data):
        query = 'INSERT INTO wishlists ( user_id, product_id ) VALUES ( %(user_id)s, %(product_id)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)
    

    @classmethod
    def deleteFromWishlist(cls,data):
        query = 'DELETE FROM wishlists WHERE product_id = %(product_id)s AND user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)
    


    @classmethod
    def deleteAllWishlists(cls, data):
        query= 'DELETE FROM wishlists WHERE wishlists.product_id = %(product_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)



    @classmethod
    def deleteAllCarts(cls, data):
        query= 'DELETE FROM carts WHERE carts.product_id = %(product_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)



    @classmethod
    def deleteAllReviews(cls,data):
        query = 'DELETE FROM productReviews WHERE productReviews.product_id = %(product_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)





    @classmethod
    def wishlist(cls,data):
        query = 'SELECT products.id as ID FROM products LEFT JOIN wishlists ON wishlists.product_id = products.id LEFT JOIN users ON wishlists.user_id = users.id WHERE wishlists.user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        wishlists = []
        if results:
            for row in results:
                wishlists.append(row['ID'])
            return wishlists
        return results  


    @classmethod
    def reviews(cls,data):
        query = 'SELECT * FROM productReviews LEFT JOIN users on productReviews.user_id = users.id WHERE product_id = %(product_id)s;'
        revs = []
        results = connectToMySQL(cls.db_name).query_db(query,data)
    
        for row in results:
            revs.append(row)
        return revs
        


    @classmethod
    def addProductReview(cls,data):
        query = 'INSERT INTO productReviews (content, product_id, user_id) VALUES ( %(content)s, %(product_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)




    @classmethod
    def deleteProducts(cls,data):
        query = 'DELETE FROM products WHERE products.id = %(product_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def carts(cls,data):
        query = 'SELECT products.id as ID FROM products LEFT JOIN carts ON carts.product_id = products.id LEFT JOIN users ON carts.user_id = users.id WHERE carts.user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        carts = []
        for row in results:
            carts.append(row['ID'])
        return carts


    @classmethod
    def addToCart(cls,data):
        query = 'INSERT INTO carts ( user_id, product_id ) VALUES ( %(user_id)s, %(product_id)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def deleteFromCart(cls,data):
        query = 'DELETE FROM carts WHERE product_id = %(product_id)s AND user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def deleteAllFromCart(cls,data):
        query = 'DELETE FROM carts WHERE user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)



    @classmethod
    def uploadPhoto(cls,data):
        query = 'UPDATE products SET image = %(image)s WHERE id = %(product_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def deleteProductFromOrders(cls,data):
        query = 'DELETE FROM orderItems WHERE product_id = %(product_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)




    @staticmethod
    def validateProduct(product):
        is_valid = True
        if len(product['name']) < 3:
            flash("The name of the product must be at least 3 characterts long", 'name')
            is_valid = False
        if len(product['description']) < 10:
            flash("The products description must be at least 10 characters long", 'description')
            is_valid = False
        if product['price'] == '':
            flash("The product must have a price", 'price')
            is_valid = False
        if product['quantity'] == '':
            flash("The product must have quantity", 'quantity')
            is_valid = False
        return is_valid
