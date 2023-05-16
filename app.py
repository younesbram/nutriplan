# Required libraries
import openai
import requests
import json
from pymongo import MongoClient


#  To implement QR code scanning in Python,
#  you'd typically use a library like pyzbar for the QR code scanning itself
#  in a mobile app or web app, you'd likely use the device's built-in camera along
#  with a JavaScript library or mobile SDK for the QR code scanning.

# Hypothetical function to scan a QR code
def scan_qr_code():
    # Normally here you would access the device's camera and scan a QR code
    # The QR code would then be decoded to give you a unique identifier (e.g., a product code)
    # For this hypothetical function, let's say the QR code gives us a product code of '123456'
    product_code = '123456'

    return product_code

# Function to lookup a food item in a database using a product code
def lookup_food_item(product_code):
    return None
    client = MongoClient("mongodb://localhost:27017/")
    db = client["database_name"]
    collection = db["ollection_name"]
    food_item = collection.find_one({"product_code": product_code})

    if food_item is not None:
        return food_item["name"]
    else:
        return None
    
# Function to search for a food item in a database using a search query
def search_food_item(query):
    return None
    client = MongoClient("mongodb://localhost:27017/")
    db = client["database_name"]
    collection = db["collection_name"]
    food_item = collection.find_one({"name": {"$regex": query, "$options": "i"}})

    if food_item is not None:
        return food_item["name"]
    else:
        return None


# For the OCR task
def fetch_product_details(product_code):
    url = f'https://api.bazaarvoice.com/data/products.json?passkey=l7o783yf16tmpcr2d9dwkm783&locale=en_CA&allowMissing=true&apiVersion=5.4&filter=id:{product_code}'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        product_details = data['Results'][0]['ProductDescription']
        return product_details
    else:
        return None

# Function to generate meals
def generate_meals(allergies, diet, client_stats, fridgenventory):
    openai.api_key = 'sk-key' # replace this with your OpenAI API key
   
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
                "content": f"You are a highly skilled sports diet assistant from the future (you only respond in JSON files). Your task is to assist your client with his daily meal planning."},
            {"role": "user",
                "content": f"The client is following the {diet} diet. Their stats are {client_stats} Please respond with meal plans and timings, considering the fact that the client is a bodybuilder and needs diet-specific nutrients.. Please also take into account their allergies: {allergies}, and the use only food items currently available: {', '.join(fridgenventory)} REPLY ONLY WITH A JSON FILE OF THE MEALS"},
        ],
        temperature=0.666,
    )

    # Extract the generated text from the response
    generated_text = response['choices'][0]['message']['content']

    # Find the first and last index of the JSON part
    start_index = generated_text.find('{')
    end_index = generated_text.rfind('}') + 1  # +1 to include the last '}'

    # Extract the JSON part
    json_part = generated_text[start_index:end_index]

    #json extracting didnt work  fix it later

    return json_part



# Example usage - get this from the user with a nice front end

allergies = ["peanuts"]
diet = "Intermittent Fasting 16:8"
#add more stats later like lifts, body fat, etc, results from calories with a good formula like  mifflin st jeor
client_stats = {"height": 180, "weight": "205 lbs", "age": 22.4}
#add calorie information to this later and specific macros and weights
fridgenventory = ["greek yogurt", "eggs", "spinach", "carrots","milk", "whey", "quest protein chips" "yogurt"]

#if user presses button to scan qr code
product_code = scan_qr_code()
food_item = lookup_food_item(product_code)

#else if user just searches for food item
query = "searchbar query"
food_item = search_food_item(query)

if food_item is not None:
    fridgenventory.append(food_item)
print(generate_meals(allergies, diet, client_stats, fridgenventory))
