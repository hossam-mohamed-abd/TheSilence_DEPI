# Medical & Pharmacy Intelligence System

## Project Structure Documentation

This document explains the purpose and contents of each folder in the repository.

---

## 📁 docs/

Contains all project documentation.

### docs/srs/

* SRS (Software Requirements Specification)
* Includes:

  * Introduction
  * System Overview
  * Functional Requirements
  * Non-functional Requirements
  * Use Cases

### docs/architecture/

* System design diagrams
* High-level architecture (how components interact)

### docs/diagrams/

* ERD (Entity Relationship Diagram)
* Data Flow Diagrams
* Any visual representation of the system

### docs/presentation/

* Final presentation slides (PPT or PDF)
* Demo explanation

---

## 📁 data/

Stores all datasets in different stages.

### data/raw/

* Original data as collected
* No processing applied
* Sources: APIs, scraping, datasets

### data/staging/

* Cleaned and partially processed data
* Ready for transformation

### data/warehouse/

* Final structured data
* Ready for analysis and querying

---

## 📁 pipelines/

Contains ETL (Extract, Transform, Load) pipelines.

### pipelines/ingestion/

* Scripts for collecting data
* API calls / scraping scripts

### pipelines/processing/

* Data cleaning
* Data transformation

### pipelines/loading/

* Load data into database or warehouse

---

## 📁 database/

Responsible for database structure and management.

### database/schema/

* SQL schema files
* Table definitions

### database/migrations/

* Database version control
* Changes to schema over time

### database/seeds/

* Initial data for testing

---

## 📁 analytics/

Handles data analysis and insights.

### analytics/notebooks/

* Jupyter notebooks
* Exploration and experiments

### analytics/reports/

* Final charts and insights
* Images or PDFs

### analytics/models/

* Machine learning models (if used)
* Prediction logic (e.g., demand forecasting)

---

## 📁 web_app/

Main application (frontend + backend).

### web_app/backend/

* API (Flask / FastAPI)
* Handles requests from frontend

Contents may include:

* routes/
* controllers/
* models/

### web_app/frontend/

* User interface
* React / HTML / CSS / JS

### web_app/services/

* Business logic
* Examples:

  * drug_search
  * price_comparison
  * recommendation system

### web_app/utils/

* Helper functions
* Common utilities

---

## 📁 dashboard/

* Visualization tools
* Power BI / Streamlit dashboards
* Connected to processed data

---

## 📁 tests/

* Unit tests
* Integration tests

---

## 📄 Root Files

### README.md

* Project overview
* Setup instructions
* How to run the project

### requirements.txt

* Python dependencies

### .env.example

* Example environment variables

### docker-compose.yml (optional)

* Container setup for services

### .gitignore

* Files to ignore in Git

---

## ✅ Notes

* Each folder should contain a small README.md explaining its purpose.
* Follow consistent naming conventions.
* Keep code modular and organized.

---
