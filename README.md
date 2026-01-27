# Chemical Equipment Parameter Visualizer  
(Hybrid Web + Desktop Application)

---

## 📌 Project Overview

The **Chemical Equipment Parameter Visualizer** is a hybrid application that runs both as a **Web Application** and a **Desktop Application**.  
It allows users to upload CSV files containing chemical equipment data, performs analytical processing on the backend, and presents insights through tables, charts, and downloadable PDF reports.

Both the Web and Desktop applications consume the **same Django REST API**, ensuring consistency and reusability of backend logic.

This project was developed as part of the **FOSSEE Semester Internship Screening Task (2026)**.

---

## 🧪 Problem Statement

Chemical plants and laboratories generate large amounts of equipment data (flow rate, pressure, temperature, etc.).  
Analyzing such data manually is inefficient and error-prone.

This project provides:
- Automated data ingestion (CSV)
- Analytical summaries
- Visual insights
- Report generation
- Multi-platform access (Web + Desktop)

---

## 🏗️ System Architecture
┌───────────────────────────┐
│        React Web App       │
│  (Axios, Chart.js, React)  │
└─────────────▲─────────────┘
              │ REST API (JSON)
              │
┌─────────────┴─────────────┐
│      Django Backend        │
│ (Django REST Framework)   │
│        + Pandas            │
└───────▲───────────▲───────┘
        │           │
        │ ORM       │ REST API
        │           │
┌───────┴───────┐   └────────────────────┐
│ SQLite DB     │                        │
│ (Datasets,   │                        │
│ Stats, Time) │                        │
└──────────────┘                        │
                                        │
                          ┌─────────────▼─────────────┐
                          │     PyQt5 Desktop App      │
                          │  (Matplotlib + Requests)  │
                          └───────────────────────────┘


## 🧰 Tech Stack

### Backend
- **Python**
- **Django**
- **Django REST Framework**
- **Pandas** (CSV parsing & analytics)
- **ReportLab** (PDF generation)
- **SQLite** (Database)

### Web Frontend
- **React.js**
- **Axios** (API calls)
- **Chart.js** & **react-chartjs-2**

### Desktop Application
- **PyQt5**
- **Matplotlib**
- **Requests**

### Tools
- Git & GitHub
- Postman (API testing)
- VS Code

---

## 📂 Project Structure

chemical-equipment-visualizer/
│
├── backend/
│ ├── api/
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ ├── urls.py
│ │ └── pdf_utils.py
│ ├── backend/
│ ├── manage.py
│ └── db.sqlite3
│
├── web-frontend/
│ ├── src/
│ │ ├── components/
│ │ │ ├── HistoryTable.js
│ │ │ └── Charts.js
│ │ ├── api.js
│ │ └── App.js
│ └── package.json
│
├── desktop_app.py
├── sample_equipment_data.csv
└── README.md


---

## 📊 CSV File Format

The uploaded CSV file must contain the following columns:

| Column Name | Description |
|------------|-------------|
| Equipment Name | Name of the equipment |
| Type | Equipment category (Pump, Valve, etc.) |
| Flowrate | Flow rate value |
| Pressure | Pressure value |
| Temperature | Temperature value |

A sample file `sample_equipment_data.csv` is included for testing.

---

## ⚙️ Features Implemented

### ✅ Backend Features
- CSV upload via REST API
- Data validation and parsing using Pandas
- Calculation of:
  - Total equipment count
  - Average flowrate
  - Average pressure
  - Average temperature
  - Equipment type distribution
- Storage of last 5 uploaded datasets
- Token-based authentication
- Dynamic PDF report generation

### ✅ Web Application Features
- Dataset history table
- Data visualization using charts
- Secure API access using tokens
- Automatic data refresh

### ✅ Desktop Application Features
- Uses same Django API as web app
- Displays dataset in table format
- Visualizes equipment distribution using Matplotlib
- Fully standalone desktop window

---

## 🔐 Authentication

The backend uses **Token Authentication** provided by Django REST Framework.

- Protected endpoints:
  - `/api/history/`
  - `/api/pdf/<id>/`
- Token must be sent in request headers:
Generated token 841f7b990a37ab1487ba5d003cdd9961c48c5078 for user rishi


---

## 📡 API Endpoints

| Method | Endpoint | Description |
|------|----------|-------------|
| POST | `/api/upload/` | Upload CSV and return analytics |
| GET | `/api/history/` | Fetch last 5 datasets (token required) |
| GET | `/api/pdf/<id>/` | Download dataset PDF report |

---

## 🧾 PDF Report

For each uploaded dataset, a downloadable PDF report is generated containing:
- Filename
- Total equipment
- Average metrics
- Equipment type distribution

The PDF is dynamically generated using **ReportLab**.

---

## 🛠️ Setup Instructions

### 1️⃣ Backend Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

###  2️⃣ Web Frontend Setup
cd web-frontend
npm install
npm start

###   3️⃣ Desktop Application
Ensure backend server is running, then:
python desktop_app.py


### Author
Tushit Tiwari 
For FOSSEE(2026)