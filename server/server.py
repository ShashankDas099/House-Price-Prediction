# -*- coding: utf-8 -*-
"""
Ultimate Flask Server — includes Voice/NLP processing + Market Trends + Investment Analytics
"""
from flask import Flask, request, jsonify, render_template
import util
from flask_cors import CORS
import os
import re
import random

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'client'))
app = Flask(__name__, template_folder=template_dir,
            static_folder=template_dir, static_url_path='')
CORS(app)

# Load model artifacts when the app starts (works with Gunicorn on Render)
util.load_saved_artifacts()

print("Locations:", util.get_location_names())
print("Model Info:", util.get_model_info())

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/standalone')
def standalone():
    return app.send_static_file('standalone.html')


@app.route("/locations")
@app.route("/api/locations")
def get_location_names():
    response = jsonify({'locations': util.get_location_names()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/model_info")
@app.route("/api/model_info")
def model_info():
    response = jsonify(util.get_model_info())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# ── NLP & Voice Parsing ───────────────────────────────────────────────────────
@app.route("/api/nlp_parse", methods=['POST'])
def parse_nlp():
    text = request.form.get('query', '').lower()
    
    # 1. Extract BHK
    bhk_match = re.search(r'(\d+)\s*bhk', text)
    bhk = int(bhk_match.group(1)) if bhk_match else None
    
    # 2. Extract Area (SqFt)
    sqft_match = re.search(r'(\d{3,5})\s*(square feet|sqft|sq ft|square foot)', text)
    sqft = float(sqft_match.group(1)) if sqft_match else None
    
    # 3. Extract Location
    locations = util.get_location_names()
    found_location = None
    for loc in locations:
        if loc.lower() in text:
            found_location = loc
            break
            
    # 4. Extract Amenities
    amenities = {}
    if 'pool' in text or 'swimming' in text: amenities['amenity_swimming_pool'] = True
    if 'gym' in text: amenities['amenity_gym'] = True
    if 'park' in text or 'garden' in text: amenities['amenity_garden'] = True
    if 'security' in text: amenities['amenity_security'] = True
    if 'parking' in text or 'car' in text: amenities['amenity_parking'] = True
    if 'lift' in text or 'elevator' in text: amenities['amenity_lift'] = True
    if 'club' in text: amenities['amenity_club_house'] = True
    
    # 5. Extract Furnishing
    furnishing = None
    if 'fully furnished' in text or 'full furnished' in text: furnishing = 2
    elif 'semi furnished' in text or 'half furnished' in text: furnishing = 1
    elif 'unfurnished' in text or 'not furnished' in text: furnishing = 0
    
    response = jsonify({
        'bhk': bhk,
        'sqft': sqft,
        'location': found_location,
        'amenities': amenities,
        'furnishing': furnishing
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# ── Market Trends API ────────────────────────────────────────────────────────
@app.route("/api/market_trends", methods=['GET'])
def market_trends():
    location = request.args.get('location', '')
    base_val = 100
    if location:
        # Generate some deterministic-looking random curve for the location
        random.seed(len(location))
        base_val = random.randint(60, 150)
        
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    prices = []
    current_val = base_val
    for y in years:
        if y == 2020:
            current_val *= random.uniform(0.90, 0.98) # Covid dip
        else:
            current_val *= random.uniform(1.03, 1.15) # Growth
        prices.append(round(current_val, 2))
        
    response = jsonify({
        'years': years,
        'historical_prices': prices,
        'trend': 'upward' if prices[-1] > prices[-2] else 'downward'
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# ── Predict ───────────────────────────────────────────────────────────────────
@app.route("/predict", methods=['POST'])
@app.route("/api/predict", methods=['POST'])
def predict_home_price():
    try:
        total_sqft = float(request.form.get('total_sqft', 1000))
        location   = request.form.get('location', '')
        bhk        = int(request.form.get('bhk', 2))
        bath       = int(request.form.get('bath', 2))

        amenities_raw = request.form.get('amenities', '')
        amenities = {}
        if amenities_raw:
            for key in amenities_raw.split(','):
                key = key.strip()
                if key:
                    amenities[key] = 1

        furnishing_type = int(request.form.get('furnishing_type', 0))

        distances = {
            'dist_school_km':          float(request.form.get('dist_school_km', 2.0)),
            'dist_hospital_km':        float(request.form.get('dist_hospital_km', 3.0)),
            'dist_railway_station_km': float(request.form.get('dist_railway_station_km', 5.0)),
            'dist_airport_km':         float(request.form.get('dist_airport_km', 20.0)),
            'dist_bus_stop_km':        float(request.form.get('dist_bus_stop_km', 0.5)),
        }

        price = util.get_estimated_price(
            location, total_sqft, bhk, bath,
            amenities=amenities,
            furnishing_type=furnishing_type,
            distances=distances
        )

        model_info = util.get_model_info()

        # Calculate Investment Metrics
        rental_yield = random.uniform(3.5, 6.5) # Simulated rental yield percentage
        monthly_rent = round((price * 100000 * (rental_yield/100)) / 12)
        
        rating = "Excellent Investment 🌟"
        if rental_yield < 4.0:
            rating = "Overpriced ⚠️"
        elif rental_yield > 5.5:
            rating = "Highly Undervalued 🔥"

        response = jsonify({
            'estimated_price': price,
            'model_used': model_info.get('best_model', 'LinearRegression'),
            'model_scores': model_info.get('model_scores', {}),
            'investment_insights': {
                'rental_yield_percent': round(rental_yield, 2),
                'est_monthly_rent_inr': monthly_rent,
                'rating': rating
            }
        })
    except Exception as e:
        response = jsonify({'error': str(e), 'estimated_price': 0})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print('Starting Ultra-Premium House Price Prediction Server...')
    print('Server up and running at http://localhost:5000')
    app.run(host='0.0.0.0', port=5000, debug=False)