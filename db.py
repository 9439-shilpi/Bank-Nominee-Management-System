import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="NewPassword@123",
        database="bank_nominee_db"
    )