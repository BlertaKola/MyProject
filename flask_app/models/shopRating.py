from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash

class ShopRating:
    db_name = 'last'
    def __init__(self,data):
        self.id = data['id'],
        self.content = data['content'],
        self.user_id = data['user_id']
    
    @classmethod
    def addRating(cls,data):
        query = 'INSERT INTO shopRatings (content, user_id) VALUES ( %(content)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)
    

    @classmethod
    def getAllRatings(cls):
        query = 'SELECT * FROM shopRatings LEFT JOIN users ON shopRatings.user_id = users.id;'
        ratings = []
        results = connectToMySQL(cls.db_name).query_db(query)
        if results:
            for row in results:
                ratings.append(row)
            return ratings
        return False

    @staticmethod
    def validateRating(rating):
        is_valid = True
        if len(rating['content'] )< 1:
            flash("You cant submit an empty rating", 'content')
            is_valid = False
        return is_valid