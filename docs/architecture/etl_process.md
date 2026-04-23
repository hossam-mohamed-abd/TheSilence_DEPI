# Data Engineering Progress

This document describes what has been completed and what is currently in progress in the Data Engineering phase of the project.

---

## ✅ Completed Tasks

### 1. Problem Definition

* Defined the main goals of the system:

  * Drug search
  * Price comparison
  * Pharmacy discovery

### 2. SRS (Software Requirements Specification)

* Documented:

  * Functional requirements
  * Non-functional requirements
  * Use cases

### 3. Data Collection

* Collected datasets including:

  * Drugs
  * Pharmacies
  * Prices

### 4. Data Cleaning

* Removed duplicates
* Handled missing values
* Standardized data formats

### 5. Data Modeling (Schema Design)

* Designed database schema (ERD)
* Defined relationships between tables

### 6. Data Staging

* Stored cleaned data in CSV/Excel files
* Organized under data/staging/

---

## 🟡 In Progress Tasks

### 7. Database Implementation (In Progress)

* Creating database and tables
* Applying schema.sql
* Preparing tables for data insertion

---

### 8. Data Warehouse (In Progress)

* Creating a final structured dataset
* Combining data from multiple tables
* Target:

  * final_dataset table or CSV
  * Includes drug, pharmacy, price, and location

---

### 9. Pipeline (In Progress)

* Building ETL pipeline script
* Automating:

  * Reading data
  * Cleaning
  * Loading into database
* Goal:

  * Run everything with one command

---

## ⏳ Next Steps

### 10. Data Validation

* Ensure:

  * No null values
  * No duplicates
  * Correct relationships

---

## 📌 Status Summary

| Task                    | Status         |
| ----------------------- | -------------- |
| Problem Definition      | ✅ Done         |
| SRS                     | ✅ Done         |
| Data Collection         | ✅ Done         |
| Data Cleaning           | ✅ Done         |
| Data Modeling           | ✅ Done         |
| Data Staging            | ✅ Done         |
| Database Implementation | 🟡 In Progress |
| Data Warehouse          | 🟡 In Progress |
| Pipeline                | 🟡 In Progress |
| Data Validation         | ⏳ Next         |

---

