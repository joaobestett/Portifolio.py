from pymongo import MongoClient
import os

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_URI"))
        self.db = self.client.Users
        self.collection_users = self.db.Users
        self.collection_products = self.db.Products

    def add_user(self, user):
        try:
            return self.collection_users.insert_one(user)
        except Exception as e:
            raise Exception(f"Error adding user: {e}")

    def get_users(self):
        return list(self.collection_users.find())

    def get_user_by_email(self, email):
        return self.collection_users.find_one({"email": email})

    def update_user(self, email, updates):
        return self.collection_users.update_one({"email": email}, {"$set": updates})

    def delete_user(self, email):
        return self.collection_users.delete_one({"email": email})

    def add_product(self, product):
        try:
            return self.collection_products.insert_one(product)
        except Exception as e:
            raise Exception(f"Error adding product: {e}")

    def get_products(self):
        return list(self.collection_products.find())

    def get_product_by_name(self, name):
        return self.collection_products.find_one({"nome": name})

    def update_product(self, name, updates):
        return self.collection_products.update_one({"nome": name}, {"$set": updates})

    def delete_product(self, name):
        return self.collection_products.delete_one({"nome": name})
