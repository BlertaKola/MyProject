from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash


class Order:
    db_name = 'last'
    def __init__(self,data):
        self.id = data['id'],
        self.user_id = data['user_id']
    

    @classmethod
    def makeOrder(cls,data):
        query = "INSERT INTO orders ( user_id ) VALUES ( %(user_id)s );"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        query2 = "SELECT id FROM orders ORDER BY id DESC LIMIT 1;"
        result2 = connectToMySQL(cls.db_name).query_db(query2)
        idja = result2[0]['id']
        query3 = "INSERT INTO orderItems (order_id, product_id) SELECT " + str(idja) + " , product_id FROM carts WHERE user_id = %(user_id)s;"
        result3 = connectToMySQL(cls.db_name).query_db(query3,data)
        
        query4 = "SELECT * from carts WHERE user_id = %(user_id)s;"
        result4 = connectToMySQL(cls.db_name).query_db(query4, data)
        productsInCart = []
        for product in result4:
            productsInCart.append(product['product_id'])
        return productsInCart

    # @classmethod
    # def getOrderByID(cls,data):
    #     query = 'SELECT id FROM orders WHERE orders.user_id = %(user_id)s;'
    #     result = connectToMySQL(cls.db_name).query_db(query,data)
    #     if result:
    #         return result[0]
    #     return False

    # @classmethod
    # def getAllOrders(cls):
    #     query = 'SELECT users.username,orders.id, users.address, orders.created_at,products.description, products.name, products.price FROM orders LEFT JOIN users ON orders.user_id = users.id LEFT JOIN orderItems ON orderItems.order_id = orders.id LEFT JOIN products ON orderitems.product_id = products.id group by orders.id;'
    #     results = connectToMySQL(cls.db_name).query_db(query)
    #     orders = []
    #     if results:
    #         for row in results:
    #             orders.append(row)
    #         return orders
    #     return False
    
    @classmethod
    def getAllOrdersWithItems(cls):
        query = 'SELECT *, SUM(products.price) AS sumTotal FROM orders LEFT JOIN users ON orders.user_id = users.id LEFT JOIN orderItems ON orderItems.order_id = orders.id LEFT JOIN products ON orderitems.product_id = products.id group by orders.id;'
        results = connectToMySQL(cls.db_name).query_db(query)
        orders = []
        if results:
            for row in results:
                ordersItems = []
                idja = str(row['id'])
                query2 = 'SELECT * FROM orderItems LEFT JOIN products on orderItems.product_id = products.id WHERE order_id =' + idja
                results2 = connectToMySQL(cls.db_name).query_db(query2)
                if results2:
                    for row2 in results2:
                        ordersItems.append(row2)
                row['orderItems']= ordersItems
                orders.append(row)
            return orders
        return False
    
