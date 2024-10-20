from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV file
restaurants_df = pd.read_csv('/Users/jameskang/Desktop/Desktop - James’s MacBook Pro/VSC/v0/restaurants.csv')

@app.route('/')
def index():
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

    recommendations = filtered_restaurants.to_dict(orient='records')
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
