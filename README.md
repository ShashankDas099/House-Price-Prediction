<h1 align="center">🏠 AI-Powered Bangalore House Price Prediction System</h1>

<p align="center">
  <strong>An AI-powered Full Stack Real Estate Valuation Platform featuring Machine Learning, Voice Search, Investment Analytics, Interactive Maps, and Smart Property Insights.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask"/>
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/>
  <img src="https://img.shields.io/badge/Frontend-Vercel-black?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Backend-Render-blue?style=for-the-badge"/>
</p>

---

# 🌐 Live Demo

### 🚀 Frontend

https://house-price-prediction-model-xi.vercel.app/

### ⚡ Backend API

https://house-price-prediction-model-1-ybt0.onrender.com

---

# 📖 Overview

The **AI-Powered Bangalore House Price Prediction System** is a full-stack real estate intelligence platform that predicts residential property prices using Machine Learning while providing users with a modern, AI-driven experience.

Unlike traditional property valuation websites, this application combines intelligent price prediction with voice-assisted property search, investment analytics, interactive maps, and market trend visualization to help users make informed real estate decisions.

Designed as a comprehensive property intelligence platform, it delivers a seamless experience for home buyers, investors, and real estate enthusiasts.

---

# ✨ Features

- 🏠 AI-powered House Price Prediction
- 🎙 Voice-based Property Search
- 📍 Interactive Property Map
- 📈 Market Trend Visualization
- 💰 Investment Analysis
- 📄 PDF Report Generation
- 📊 Property Analytics Dashboard
- 🌙 Modern Responsive UI
- ⚡ Fast REST API Backend

---

# 🎯 Target Users

- 🏡 Home Buyers
- 💼 Real Estate Investors
- 🏢 Property Consultants
- 📊 Data Science Enthusiasts
- 👨‍💻 Developers exploring ML applications
- 🎓 Students learning Machine Learning and Full Stack Development

---

# 🧠 Machine Learning

The prediction engine is trained using the **Bangalore Housing Dataset** and leverages regression-based Machine Learning algorithms to estimate residential property prices.

### Prediction Parameters

- Total Area (Sqft)
- Number of Bedrooms (BHK)
- Bathrooms
- Property Location
- Furnishing Type
- Available Amenities
- Nearby Distance Metrics

Additional business logic enhances predictions based on furnishing quality and property amenities.

---

# 🛠 Tech Stack

## Frontend

- HTML5
- CSS3
- JavaScript (ES6)
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
- Pandas
- NumPy
- Pickle
- XGBoost (Support)

---

## Deployment

### Frontend

- Vercel

### Backend

- Render

---

# 🏗 System Architecture

```text
                 User
                  │
                  ▼
         Responsive Web Interface
                  │
                  ▼
      Voice Search / Form Input
                  │
                  ▼
          Flask REST API Server
                  │
        ┌─────────┴──────────┐
        ▼                    ▼
 Machine Learning      Market Analytics
 Prediction Model      & Investment Logic
        │                    │
        └─────────┬──────────┘
                  ▼
          Property Prediction
                  │
                  ▼
      Charts • Maps • PDF Report
                  │
                  ▼
                 User
```

---

# 📂 Project Structure

```text
House-Price-Prediction/
│
├── client/
│   ├── index.html
│   ├── dashboard.html
│   ├── standalone.html
│   ├── app.js
│   └── styles.css
│
├── server/
│   ├── server.py
│   ├── util.py
│   ├── requirements.txt
│   └── artifacts/
│
├── model/
│   ├── banglore_home_prices_model.pickle
│   ├── columns.json
│   ├── bengaluru_house_prices.csv
│   └── train_model.py
│
└── README.md
```

---

# 🔌 API Endpoints

## Get Available Locations

```http
GET /api/locations
```

---

## Predict House Price

```http
POST /api/predict
```

### Parameters

- location
- sqft
- bhk
- bath
- amenities
- furnishing
- distance_metrics

---

## Market Trends

```http
GET /api/market_trends
```

---

## Voice NLP Parsing

```http
POST /api/nlp_parse
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/ShashankDas099/House-Price-Prediction.git
```

Move into the project directory

```bash
cd House-Price-Prediction
```

Install the required dependencies

```bash
pip install -r server/requirements.txt
```

Run the backend server

```bash
cd server
python server.py
```

Open your browser and visit

```
http://localhost:5000
```

---

# 🚀 Workflow

1. Enter property details manually or using voice input.
2. The backend processes user inputs.
3. The Machine Learning model predicts the estimated property price.
4. Market trends and investment insights are generated.
5. Interactive charts and maps visualize the results.
6. Users can download a complete PDF valuation report.

---

# 🚀 Future Enhancements

- Google Maps API Integration
- Live Property Data APIs
- Mortgage & EMI Calculator
- AI Chatbot for Property Queries
- Property Recommendation Engine
- Time-Series Price Forecasting
- Satellite View Support
- Multi-city Expansion
- Image-based Property Analysis
- User Authentication & Saved Searches

---

# 🎓 Learning Outcomes

This project demonstrates practical implementation of:

- Machine Learning
- Regression Models
- REST API Development
- Flask Backend Development
- Full Stack Web Development
- Data Visualization
- Natural Language Processing
- Interactive Maps
- Cloud Deployment
- Responsive UI Design

---

# 👥 Development Team

This project was collaboratively developed as part of a Machine Learning and Full Stack Development initiative.

| Team Member | Contribution |
|-------------|--------------|
| **Raj Mishra** | Frontend Development, UI/UX Design, Dashboard & Interactive Visualizations |
| **Sumit Kumar Singh** | Machine Learning Model Development, Backend APIs & Deployment |
| **Shashank Das** | Backend Development, API Integration, Feature Engineering & System Integration |

---

# 📄 License

This project is developed for educational and learning purposes.

---

# 🙏 Acknowledgements

This project utilizes several open-source technologies and frameworks:

- Flask
- Scikit-Learn
- Pandas
- NumPy
- Chart.js
- Leaflet.js
- HTML2PDF
- Vercel
- Render

Special thanks to the open-source community for making these technologies freely available.

---

<h3 align="center">⭐ If you found this project useful, consider giving it a Star!</h3>
