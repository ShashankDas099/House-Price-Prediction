# 🏠 AI-Powered Bangalore House Price Prediction System

> **An AI-powered Full Stack Real Estate Valuation Platform with Voice Assistant, Interactive Maps, Investment Analytics, Market Trends, and Machine Learning Price Prediction.**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-success)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript)
![Render](https://img.shields.io/badge/Backend-Render-blue)
![Vercel](https://img.shields.io/badge/Frontend-Vercel-black)

---

# 🚀 Live Demo

### 🌐 Frontend
https://house-price-prediction-model-xi.vercel.app/

### ⚡ Backend API
https://house-price-prediction-model-1-ybt0.onrender.com

---

# 📌 Project Overview

The AI-Powered Bangalore House Price Prediction System is an intelligent real estate valuation platform that predicts residential property prices using Machine Learning while providing a modern AI-driven user experience.

Unlike traditional price prediction websites, this platform combines:

- 🤖 Machine Learning Prediction
- 🎙 Voice Based Property Search
- 🗺 Interactive Property Map
- 📈 Market Trend Analysis
- 💰 Investment Insights
- 📄 PDF Report Generation
- 📊 Property Analytics Dashboard

The system is designed as a complete real-estate intelligence platform rather than a simple ML prediction model.

---

# ✨ Features

## 🤖 AI Price Prediction

Predicts property prices using trained Machine Learning models based on:

- Area (Sqft)
- BHK
- Bathrooms
- Location
- Furnishing
- Amenities
- Nearby Facilities

---

## 🎙 Voice AI Assistant

Users can simply speak:

> "Show me a fully furnished 3 BHK apartment in Indira Nagar with gym and parking."

The system automatically extracts:

- Location
- Area
- BHK
- Furnishing
- Amenities

using Natural Language Processing.

---

## 📍 Interactive Property Map

- Leaflet.js Maps
- Location Marker
- Nearby Area Visualization
- Topographical View

---

## 📈 Market Trend Analytics

Visualizes historical property trends using Chart.js.

Provides:

- Price Growth
- Historical Trends
- Investment Direction

---

## 💰 Investment Analytics

Calculates

- Estimated Rental Yield
- Monthly Rental Income
- Investment Rating

Examples

- Excellent Investment
- Highly Undervalued
- Overpriced

---

## 📄 PDF Report Generator

Generate a complete AI valuation report with one click.

The report includes:

- Property Details
- Estimated Price
- Market Trends
- Investment Analysis

---

## 🎨 Premium Modern UI

- Dark Theme
- Animated Dashboard
- Interactive Charts
- Responsive Design
- Glassmorphism Effects
- Futuristic AI Interface

---

# 🧠 Machine Learning

The prediction engine uses a trained regression model based on Bangalore Housing Dataset.

### Features Used

- Total Sqft
- BHK
- Bathrooms
- Location Encoding
- Furnishing Type
- Amenities
- Nearby Distance Metrics

The backend also performs additional intelligent adjustments using business rules for amenities and furnishing.

---

# 🛠 Tech Stack

## Frontend

- HTML5
- CSS3
- JavaScript
- jQuery
- Chart.js
- Leaflet.js
- HTML2PDF
- Font Awesome

---

## Backend

- Python
- Flask
- Flask-CORS
- REST APIs

---

## Machine Learning

- Scikit-Learn
- NumPy
- Pandas
- Pickle
- XGBoost (Support)

---

## Deployment

Frontend

- Vercel

Backend

- Render

---

# 📂 Project Structure

```
House-Price-prediction-model
│
├── client
│   ├── index.html
│   ├── dashboard.html
│   ├── standalone.html
│   ├── app.js
│   └── styles.css
│
├── server
│   ├── server.py
│   ├── util.py
│   ├── requirements.txt
│   └── artifacts
│
├── model
│   ├── banglore_home_prices_model.pickle
│   ├── columns.json
│   ├── bengaluru_house_prices.csv
│   └── train_model.py
│
└── README.md
```

---

# 🔌 API Endpoints

### Get Locations

```
GET /api/locations
```

---

### Predict Property Price

```
POST /api/predict
```

Parameters

```
location
sqft
bhk
bath
amenities
furnishing
distance metrics
```

---

### Market Trends

```
GET /api/market_trends
```

---

### NLP Voice Parsing

```
POST /api/nlp_parse
```

---

# ⚙ Installation

Clone repository

```bash
git clone https://github.com/Sumit692/House-Price-prediction-model.git
```

Go into project

```bash
cd House-Price-prediction-model
```

Install dependencies

```bash
pip install -r server/requirements.txt
```

Run

```bash
cd server
python server.py
```

Open

```
http://localhost:5000
```

---

# 📊 Future Improvements

- Live Bangalore Property API
- Google Maps Integration
- Satellite View
- Authentication System
- AI Chatbot for Buyers
- Mortgage Calculator
- Property Recommendation Engine
- Price Forecast using Time Series
- Multi-city Support
- Image-based Property Analysis

---

# 📸 Screenshots

Add screenshots here.

<img width="1366" height="697" alt="Screenshot (1)" src="https://github.com/user-attachments/assets/44327746-9950-4c0c-a2c9-840af56a6ccf" />

<img width="1366" height="690" alt="Screenshot (2)" src="https://github.com/user-attachments/assets/07563ceb-268e-49bf-8652-96189680911e" />

<img width="1366" height="688" alt="Screenshot (3)" src="https://github.com/user-attachments/assets/a5965cb5-773c-4809-9e11-6d5fd35e6ad9" />

---

# 🎯 Learning Outcomes

This project demonstrates practical implementation of:

- Machine Learning
- Full Stack Development
- REST APIs
- Data Visualization
- NLP
- Deployment
- Responsive UI Design
- AI Integration

---

# 👨‍💻 Author

## Sumit Kumar Singh

AI Developer | Software Engineer | Machine Learning Enthusiast


---

# ⭐ If you like this project

Give this repository a ⭐ on GitHub!

```
