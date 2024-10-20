from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)


# Load the CSV file
restaurants_df = pd.read_csv('DineSmart/restaurants.csv')

# Clean the 'name' column
restaurants_df['name'] = restaurants_df['name'].str.strip()  # Remove leading and trailing spaces

# Convert the 'rating' column to numeric, forcing errors to NaN
restaurants_df['rating'] = pd.to_numeric(restaurants_df['rating'], errors='coerce')

# If necessary, handle NaN values (for example, replacing with a default value or dropping them)
restaurants_df['rating'].fillna(0, inplace=True)  # Replace NaN ratings with 0
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/project')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    city = data.get('city').lower()
    state = data.get('state').lower()
    cuisine = data.get('cuisine')

    # Filter restaurants based on city and state
    filtered_restaurants = restaurants_df[
        (restaurants_df['city'].str.lower() == city) & 
        (restaurants_df['state'].str.lower() == state)

    ]
    if cuisine:
        filtered_restaurants = filtered_restaurants[
            filtered_restaurants['cuisine'].str.lower() == cuisine.lower()
        ]

    if filtered_restaurants.empty:
        return jsonify({'message': 'No restaurants found'})
    
 # Format the price column to include the dollar sign
    filtered_restaurants['price'] = '$' + filtered_restaurants['price'].astype(str)

    recommendations = filtered_restaurants.to_dict(orient='records')
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
