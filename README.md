# PRICEPILOT | AI-Powered Dynamic Pricing & Demand Forecasting

<p align="center">
  <strong>An intelligent retail analytics platform for demand forecasting, pricing analysis, and scenario-based price optimization.</strong>
</p>

<p align="center">
  <a href="https://pricepilot-dashboard.onrender.com">
    <img src="https://img.shields.io/badge/🚀_LIVE_DEMO-Open_PRICEPILOT-00BFA6?style=for-the-badge" alt="Live Demo">
  </a>
  <a href="https://github.com/LipsitaTripathy/PRICEPILOT">
    <img src="https://img.shields.io/badge/GitHub-View_Repository-181717?style=for-the-badge&logo=github" alt="GitHub Repository">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/XGBoost-Machine_Learning-orange" alt="XGBoost">
  <img src="https://img.shields.io/badge/LightGBM-Machine_Learning-green" alt="LightGBM">
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker" alt="Docker">
</p>

---

## 🚀 Live Application

**Explore PRICEPILOT:**  
### https://pricepilot-dashboard.onrender.com

PRICEPILOT is publicly deployed using Render. Open the live application to explore its interactive dashboard and pricing analysis features.

*Note: The free hosting service may take a little time to wake up after a period of inactivity.*

## 📌 Project Overview

PRICEPILOT is a machine-learning-powered retail analytics application designed to analyze product demand, explore pricing patterns, and simulate alternative pricing strategies.

The platform combines demand forecasting models, pricing analysis, and an interactive dashboard to help users understand how different pricing scenarios may influence estimated demand, revenue, and profit.

Built using Python, XGBoost, LightGBM, FastAPI, Streamlit, and Docker, PRICEPILOT brings machine learning and retail analytics together in one application.

## ✨ Key Features

- **Demand Forecasting:** Predicts product demand using trained machine learning models.
- **Dynamic Pricing Simulation:** Evaluates alternative product prices through scenario-based calculations.
- **Pricing Analysis:** Explores product pricing patterns and demand relationships.
- **Revenue & Profit Estimation:** Compares estimated business outcomes across pricing scenarios.
- **Interactive Dashboard:** Presents analytical insights through visualizations and dashboard components.
- **REST API Integration:** Uses FastAPI to serve backend functionality and model predictions.
- **Containerized Architecture:** Runs the dashboard and API in separate Docker containers.
- **Cloud Deployment:** Publicly accessible dashboard and backend hosted on Render.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python 3.11 |
| Frontend & Dashboard | Streamlit |
| Backend | FastAPI, Uvicorn |
| Machine Learning | XGBoost, LightGBM, Scikit-learn |
| Data Processing | Pandas, NumPy |
| Data Visualization | Plotly |
| Model Persistence | Joblib, Pickle |
| Containerization | Docker, Docker Compose |
| Cloud Hosting | Render |
| Development Tools | VS Code, Git, GitHub |

## 🧠 Machine Learning Approach

### 1. Demand Forecasting — XGBoost

A trained XGBoost model processes historical retail data and engineered features to estimate product demand.

### 2. Pricing Analysis — LightGBM

A LightGBM-based pricing model supports analysis of pricing-related patterns and demand relationships.

### 3. Scenario-Based Price Optimization

The application evaluates alternative price points using estimated demand, assumed price elasticity, and business constraints.

Scenario outputs are estimates based on model predictions and assumptions. They are not guaranteed business outcomes or proof of causal price elasticity.

## 🏗️ System Architecture

```text
             RETAIL INVENTORY DATA
                       |
                       v
              DATA PREPROCESSING
                       |
                       v
              FEATURE ENGINEERING
                       |
              +--------+--------+
              |                 |
              v                 v
        XGBOOST MODEL      LIGHTGBM MODEL
        DEMAND FORECAST    PRICING ANALYSIS
              |                 |
              +--------+--------+
                       |
                       v
                 FASTAPI BACKEND
                       |
                       v
               STREAMLIT DASHBOARD
                       |
                       v
             FORECASTS & PRICING
                  SCENARIOS
                       |
                       v
               RENDER DEPLOYMENT
```

## 📂 Project Structure

```text
PRICEPILOT/
│
├── api/
│   ├── __init__.py
│   └── main.py
│
├── assets/
│   └── style.css
│
├── data/
│   └── retail_inventory.csv
│
├── models/
│   ├── lightgbm_model.pkl
│   ├── pricing_demand_model.pkl
│   ├── xgboost_model.pkl
│   └── analysis_results.csv
│
├── utils/
│   ├── features.py
│   ├── preprocessing.py
│   ├── pricing_optimizer.py
│   ├── train_models.py
│   └── ...
│
├── app.py
├── Dockerfile
├── Dockerfile.api
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
└── .gitignore
```

## ⚙️ Run Locally

### Prerequisites

- Python 3.11
- Git
- Docker Desktop (optional)

### 1. Clone the Repository

```bash
git clone https://github.com/LipsitaTripathy/PRICEPILOT.git
cd PRICEPILOT
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI Backend

```bash
python -m uvicorn api.main:app --reload --port 8000
```

API documentation:

http://127.0.0.1:8000/docs

### 5. Start the Streamlit Dashboard

Open another terminal:

```bash
streamlit run app.py
```

Dashboard:

http://localhost:8501

## 🐳 Run Using Docker

Build the Docker images:

```bash
docker compose build
```

Start both services:

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

Stop the containers:

```bash
docker compose down
```

## ☁️ Deployment

PRICEPILOT is deployed on **Render** using two separate services:

| Service | Technology | Status |
|---|---|---|
| Dashboard | Streamlit + Docker | Deployed |
| Backend API | FastAPI + Docker | Deployed |

**Public URLs:**

- Live Dashboard: https://pricepilot-dashboard.onrender.com
- Backend API: https://pricepilot-04jv.onrender.com
- API Documentation: https://pricepilot-04jv.onrender.com/docs
- API Health Check: https://pricepilot-04jv.onrender.com/health

## 🔮 Future Enhancements

- Integration with real-time retail and competitor pricing data.
- Improved demand forecasting and model evaluation.
- Automated model retraining and monitoring.
- Advanced pricing recommendations with additional business constraints.
- Enhanced cloud infrastructure and deployment monitoring.

## 👩‍💻 Author

**Lipsita Tripathy**  
B.Tech — Computer Science and Engineering (AI & ML)

- **GitHub:** https://github.com/LipsitaTripathy
- **LinkedIn:** https://www.linkedin.com/in/lipsita-tripathy-b2b19728a/

---

<p align="center">
  <strong>PRICEPILOT</strong><br>
  Turning retail data into informed pricing decisions.
</p>
