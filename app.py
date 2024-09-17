from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
import re

app = Flask(__name__)


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  
            user='root',
            password='Vanathi@2003',
            database='retail_store'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_query = data.get('query')

    connection = create_connection()
    if not connection:
        return jsonify({"response": "Database connection failed. Please try again."}), 500
    
    
    response = handle_query(user_query, connection)

    connection.close()
    return jsonify({"response": response})

def handle_query(query, connection):
    cursor = connection.cursor()
    
    
    if re.search(r'(stock|available|in stock|inventory)', query, re.I):
        product, size = extract_product_and_size(query)
        if product:
            cursor.execute("SELECT quantity FROM inventory WHERE product = %s AND size = %s", (product, size))
            result = cursor.fetchone()
            if result:
                return f"Yes, we have {result[0]} {product}s available in size {size}."
            else:
                return f"Sorry, {product} in size {size} is out of stock."
        else:
            return "Sorry, I couldn't understand which product you're asking about."
    
    
    elif re.search(r'(promotion|discount|offer)', query, re.I):
        product_category = extract_product_category(query)
        if product_category:
            cursor.execute("SELECT discount FROM promotions WHERE product_category = %s", (product_category,))
            result = cursor.fetchone()
            if result:
                return f"There is a promotion: {result[0]} off on {product_category}."
            else:
                return f"There are no current promotions for {product_category}."
        else:
            return "Sorry, I couldn't identify which product category you're asking about."
    
    
    else:
        return "I'm not sure how to help with that. Can you ask in a different way?"

def extract_product_and_size(query):
    
    
    products = ['shoe', 'jacket', 'smartphone']
    sizes = ['6', '7', '8', '9', '10', '11', '12'] 

    product = None
    size = None

    
    for p in products:
        if p in query.lower():
            product = p
            break
    
    
    for s in sizes:
        if s in query:
            size = s
            break

    return product, size

def extract_product_category(query):
    
    product_categories = ['shoes', 'jackets', 'smartphones', 'laptops', 'accessories']
    
    for category in product_categories:
        if category in query.lower():
            return category
    
    return None

if __name__ == "__main__":
    app.run(debug=True)
