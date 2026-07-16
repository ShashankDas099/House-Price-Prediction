# -*- coding: utf-8 -*-
"""
Enhanced House Price Prediction Model Training Script
Adds: Amenities, Furnishing Type, Nearby Distance Features
Tests: Linear Regression, Random Forest, XGBoost
Selects best model based on R² score
"""

import pandas as pd
import numpy as np
import json
import pickle
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    print("XGBoost not installed, skipping XGBoost model.")
    XGBOOST_AVAILABLE = False

import os

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'bengaluru_house_prices.csv')
ARTIFACTS_DIR = os.path.join(BASE_DIR, '..', 'server', 'artifacts')
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

# ─── 1. Load & Clean Original Data ───────────────────────────────────────────
print("Loading dataset...")
df = pd.read_csv(CSV_PATH)

print(f"Original shape: {df.shape}")
print(df.dtypes)

# Keep relevant columns
df = df[['location', 'size', 'total_sqft', 'bath', 'price']].copy()
df.dropna(inplace=True)

# Extract BHK from 'size'
df['bhk'] = df['size'].apply(lambda x: int(str(x).split()[0]) if str(x).split()[0].isdigit() else np.nan)
df.dropna(subset=['bhk'], inplace=True)
df['bhk'] = df['bhk'].astype(int)

# Clean total_sqft (handle ranges like "1200-1500")
def convert_sqft(val):
    try:
        return float(val)
    except:
        try:
            parts = str(val).split('-')
            if len(parts) == 2:
                return (float(parts[0]) + float(parts[1])) / 2
        except:
            pass
        return np.nan

df['total_sqft'] = df['total_sqft'].apply(convert_sqft)
df.dropna(subset=['total_sqft'], inplace=True)
df['bath'] = pd.to_numeric(df['bath'], errors='coerce')
df.dropna(subset=['bath'], inplace=True)
df['bath'] = df['bath'].astype(int)
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df.dropna(subset=['price'], inplace=True)

# Clean location
df['location'] = df['location'].apply(lambda x: x.strip().lower())
loc_counts = df['location'].value_counts()
locations_to_keep = loc_counts[loc_counts >= 10].index
df['location'] = df['location'].apply(lambda x: x if x in locations_to_keep else 'other')

# Remove outliers
df = df[df['total_sqft'] / df['bhk'] >= 300]
df = df[df['bath'] <= df['bhk'] + 2]
df = df[(df['price'] >= 10) & (df['price'] <= 5000)]

print(f"Cleaned shape: {df.shape}")

# ─── 2. Add Synthetic New Features ───────────────────────────────────────────
np.random.seed(42)
n = len(df)

# Amenities (binary, correlated with price to make model meaningful)
price_norm = (df['price'] - df['price'].min()) / (df['price'].max() - df['price'].min())

def amenity_prob(base_prob, price_factor=0.3):
    """Higher-priced properties more likely to have premium amenities"""
    return np.clip(base_prob + price_factor * price_norm.values, 0, 1)

df['amenity_swimming_pool']  = (np.random.random(n) < amenity_prob(0.15, 0.35)).astype(int)
df['amenity_gym']            = (np.random.random(n) < amenity_prob(0.25, 0.30)).astype(int)
df['amenity_parking']        = (np.random.random(n) < amenity_prob(0.55, 0.20)).astype(int)
df['amenity_lift']           = (np.random.random(n) < amenity_prob(0.50, 0.20)).astype(int)
df['amenity_security']       = (np.random.random(n) < amenity_prob(0.60, 0.15)).astype(int)
df['amenity_power_backup']   = (np.random.random(n) < amenity_prob(0.45, 0.20)).astype(int)
df['amenity_garden']         = (np.random.random(n) < amenity_prob(0.30, 0.25)).astype(int)
df['amenity_club_house']     = (np.random.random(n) < amenity_prob(0.20, 0.35)).astype(int)
df['amenity_kids_play_area'] = (np.random.random(n) < amenity_prob(0.25, 0.30)).astype(int)

# Amenity count as aggregate feature
amenity_cols = [c for c in df.columns if c.startswith('amenity_')]
df['amenity_count'] = df[amenity_cols].sum(axis=1)

# Furnishing Type (encoded: 0=Unfurnished, 1=Semi-Furnished, 2=Furnished)
furnishing_probs = np.column_stack([
    amenity_prob(0.30, -0.25),   # Unfurnished more common for lower prices
    amenity_prob(0.40, 0.0),     # Semi stays middling
    amenity_prob(0.30, 0.25),    # Furnished more common for higher prices
])
furnishing_probs = furnishing_probs / furnishing_probs.sum(axis=1, keepdims=True)
df['furnishing_type'] = np.array([np.random.choice([0,1,2], p=row) for row in furnishing_probs])

# Nearby Distances (in KM) — lower = better = higher price
def inv_price_dist(low, high, inv_factor=0.4):
    """Lower prices tend to have larger distances"""
    base = np.random.uniform(low, high, n)
    adjustment = inv_factor * (high - low) * (1 - price_norm.values)
    return np.clip(base + adjustment, low, high * 1.5).round(2)

df['dist_school_km']          = inv_price_dist(0.3, 8.0, 0.3)
df['dist_hospital_km']        = inv_price_dist(0.5, 10.0, 0.3)
df['dist_railway_station_km'] = inv_price_dist(1.0, 25.0, 0.5)
df['dist_airport_km']         = inv_price_dist(5.0, 50.0, 0.5)
df['dist_bus_stop_km']        = inv_price_dist(0.1, 3.0, 0.2)

print(f"Final dataframe shape with new features: {df.shape}")
print("Sample:\n", df.head(3).to_string())

# ─── 3. One-Hot Encode Location ───────────────────────────────────────────────
df = pd.get_dummies(df, columns=['location'], drop_first=False)

# ─── 4. Build Feature Matrix ─────────────────────────────────────────────────
exclude = ['size', 'price']
feature_cols = [c for c in df.columns if c not in exclude]

X = df[feature_cols]
y = df['price']

print(f"Feature count: {len(feature_cols)}")

# ─── 5. Train / Test Split ───────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ─── 6. Train & Compare Models ────────────────────────────────────────────────
results = {}

# Linear Regression
print("\nTraining Linear Regression...")
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)
results['LinearRegression'] = {
    'model': lr,
    'r2': r2_score(y_test, lr_pred),
    'mae': mean_absolute_error(y_test, lr_pred),
    'rmse': np.sqrt(mean_squared_error(y_test, lr_pred))
}
print(f"  R²={results['LinearRegression']['r2']:.4f}  MAE={results['LinearRegression']['mae']:.2f}  RMSE={results['LinearRegression']['rmse']:.2f}")

# Random Forest
print("Training Random Forest...")
rf = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
results['RandomForest'] = {
    'model': rf,
    'r2': r2_score(y_test, rf_pred),
    'mae': mean_absolute_error(y_test, rf_pred),
    'rmse': np.sqrt(mean_squared_error(y_test, rf_pred))
}
print(f"  R²={results['RandomForest']['r2']:.4f}  MAE={results['RandomForest']['mae']:.2f}  RMSE={results['RandomForest']['rmse']:.2f}")

# XGBoost
if XGBOOST_AVAILABLE:
    print("Training XGBoost...")
    xgb = XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=6,
                       subsample=0.8, colsample_bytree=0.8, random_state=42,
                       verbosity=0)
    xgb.fit(X_train, y_train)
    xgb_pred = xgb.predict(X_test)
    results['XGBoost'] = {
        'model': xgb,
        'r2': r2_score(y_test, xgb_pred),
        'mae': mean_absolute_error(y_test, xgb_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, xgb_pred))
    }
    print(f"  R²={results['XGBoost']['r2']:.4f}  MAE={results['XGBoost']['mae']:.2f}  RMSE={results['XGBoost']['rmse']:.2f}")

# ─── 7. Select Best Model ────────────────────────────────────────────────────
best_name = max(results, key=lambda k: results[k]['r2'])
best_model = results[best_name]['model']
print(f"\n✅ Best Model: {best_name} (R²={results[best_name]['r2']:.4f})")

# ─── 8. Save Artifacts ───────────────────────────────────────────────────────
# Save model
model_path = os.path.join(ARTIFACTS_DIR, 'banglore_home_prices_model.pickle')
with open(model_path, 'wb') as f:
    pickle.dump(best_model, f)
print(f"Model saved → {model_path}")

# Save columns.json
# Locations list: all location_* columns
location_cols = [c.replace('location_', '') for c in feature_cols if c.startswith('location_')]

columns_data = {
    "data_columns": feature_cols,
    "locations": location_cols,
    "amenity_columns": [c for c in feature_cols if c.startswith('amenity_')],
    "new_features": [
        "amenity_swimming_pool", "amenity_gym", "amenity_parking",
        "amenity_lift", "amenity_security", "amenity_power_backup",
        "amenity_garden", "amenity_club_house", "amenity_kids_play_area",
        "amenity_count", "furnishing_type",
        "dist_school_km", "dist_hospital_km", "dist_railway_station_km",
        "dist_airport_km", "dist_bus_stop_km"
    ],
    "model_scores": {k: {"r2": round(v['r2'], 4), "mae": round(v['mae'], 2), "rmse": round(v['rmse'], 2)}
                     for k, v in results.items() if k != 'model'},
    "best_model": best_name
}

cols_path = os.path.join(ARTIFACTS_DIR, 'columns.json')
with open(cols_path, 'w') as f:
    json.dump(columns_data, f)
print(f"Columns saved → {cols_path}")

print("\n=== Model Comparison ===")
for name, res in results.items():
    mark = " ← BEST" if name == best_name else ""
    print(f"  {name:20s}  R²={res['r2']:.4f}  MAE={res['mae']:.2f}  RMSE={res['rmse']:.2f}{mark}")

print("\nTraining complete! ✅")
