# -*- coding: utf-8 -*-
"""
Enhanced util.py — supports new features:
  - Amenities (binary flags + count)
  - Furnishing type (0/1/2)
  - Nearby distances (km)
  - Multi-model support (LR, RF, XGBoost)
"""

import json
import pickle
import numpy as np
import os

__locations = None
__data_columns = None
__model = None
__model_scores = None
__best_model_name = None
__new_features = None

AMENITY_PREMIUM = {
    'amenity_swimming_pool':  8.0,
    'amenity_gym':            4.0,
    'amenity_parking':        3.0,
    'amenity_lift':           2.5,
    'amenity_security':       2.0,
    'amenity_power_backup':   1.5,
    'amenity_garden':         3.5,
    'amenity_club_house':     5.0,
    'amenity_kids_play_area': 2.0,
}

FURNISHING_PREMIUM = {0: 0.0, 1: 5.0, 2: 12.0}   # Unfurnished / Semi / Furnished

DISTANCE_PENALTY = {
    'dist_school_km':          -1.2,
    'dist_hospital_km':        -0.8,
    'dist_railway_station_km': -0.5,
    'dist_airport_km':         -0.3,
    'dist_bus_stop_km':        -1.5,
}


def get_estimated_price(location, sqft, bhk, bath,
                        amenities=None, furnishing_type=0, distances=None):
    """
    Predict price using the loaded model.
    Falls back to rule-based adjustment if model columns don't include new features.
    """
    amenities = amenities or {}
    distances = distances or {}

    # Build feature vector
    x = np.zeros(len(__data_columns))

    def _idx(col):
        try:
            return __data_columns.index(col)
        except ValueError:
            return -1

    # Core features
    sqft_i = _idx('total_sqft')
    if sqft_i >= 0: x[sqft_i] = sqft
    bath_i = _idx('bath')
    if bath_i >= 0: x[bath_i] = bath
    bhk_i = _idx('bhk')
    if bhk_i >= 0: x[bhk_i] = bhk

    # Location one-hot
    loc_key = f"location_{location.lower().strip()}"
    loc_i = _idx(loc_key)
    if loc_i >= 0:
        x[loc_i] = 1

    # Amenities
    amenity_count = 0
    for key, val in amenities.items():
        i = _idx(key)
        if i >= 0:
            x[i] = int(bool(val))
        if val:
            amenity_count += 1
    ac_i = _idx('amenity_count')
    if ac_i >= 0: x[ac_i] = amenity_count

    # Furnishing type
    ft_i = _idx('furnishing_type')
    if ft_i >= 0: x[ft_i] = furnishing_type

    # Distances
    for key, val in distances.items():
        i = _idx(key)
        if i >= 0:
            x[i] = float(val)

    # Model prediction
    base_price = float(__model.predict([x])[0])

    # If model was trained WITHOUT new features (old model), add rule-based premium
    model_has_new_features = any(_idx(f) >= 0 for f in [
        'amenity_swimming_pool', 'furnishing_type', 'dist_school_km'
    ])

    if not model_has_new_features:
        # Apply manual premiums on top of old model
        for key, val in amenities.items():
            if val:
                base_price += AMENITY_PREMIUM.get(key, 0)
        base_price += FURNISHING_PREMIUM.get(furnishing_type, 0)
        for key, val in distances.items():
            base_price += DISTANCE_PENALTY.get(key, 0) * float(val)

    return round(max(base_price, 5.0), 2)


def get_location_names():
    return __locations


def get_model_info():
    return {
        'model_scores': __model_scores or {},
        'best_model': __best_model_name or 'LinearRegression'
    }


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns, __locations, __model
    global __model_scores, __best_model_name, __new_features

    # Try server/artifacts first, then model/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidate_dirs = [
        os.path.join(script_dir, 'artifacts'),
        os.path.join(script_dir, '..', 'model'),
        os.path.join(script_dir, '..', 'server', 'artifacts'),
        './artifacts',
    ]

    cols_path = None
    model_path = None
    for d in candidate_dirs:
        cp = os.path.join(d, 'columns.json')
        mp = os.path.join(d, 'banglore_home_prices_model.pickle')
        if os.path.exists(cp) and cols_path is None:
            cols_path = cp
        if os.path.exists(mp) and model_path is None:
            model_path = mp

    if cols_path is None or model_path is None:
        raise FileNotFoundError(
            f"Could not find artifacts. Searched: {candidate_dirs}"
        )

    print(f"  columns.json → {cols_path}")
    print(f"  model.pickle → {model_path}")

    with open(cols_path, 'r') as f:
        data = json.load(f)

    # Support both old format (list) and new format (dict)
    if isinstance(data, list):
        __data_columns = data
        __locations = [c.replace('location_', '') for c in data if c.startswith('location_')]
        if not __locations:
            __locations = data[3:]   # fallback: old columns.json format
    else:
        __data_columns = data['data_columns']
        __locations = data.get('locations', [
            c.replace('location_', '') for c in __data_columns if c.startswith('location_')
        ])
        if not __locations:
            __locations = __data_columns[3:]
        __model_scores = data.get('model_scores', {})
        __best_model_name = data.get('best_model', 'LinearRegression')
        __new_features = data.get('new_features', [])

    with open(model_path, 'rb') as f:
        __model = pickle.load(f)

    print(f"  Columns: {len(__data_columns)}, Locations: {len(__locations)}")
    print(f"  Best model: {__best_model_name}")
    print("loading saved artifacts...done")


if __name__ == '__main__':
    load_saved_artifacts()
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Indira Nagar', 1500, 3, 3,
                              amenities={'amenity_swimming_pool': 1, 'amenity_gym': 1},
                              furnishing_type=2,
                              distances={'dist_school_km': 0.5, 'dist_hospital_km': 1.2}))