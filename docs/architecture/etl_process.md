# Data Engineering Progress

## Status Summary

| Task                           | Status         | Owner           | Deadline           | Notes                               |
| ------------------------------ | -------------- | --------------- | ------------------ | ----------------------------------- |
| Problem Definition             | ✅ Done         | -               | -                  | -                                   |
| SRS                            | ✅ Done         | -               | -                  | -                                   |
| Stakeholders Analysis          | ✅ Done         | -               | -                  | Stakeholders Identified             |
| System Scope Definition        | ✅ Done         | -               | -                  | Scope Finalized                     |
| System Architecture Diagram    | ✅ Done         | -               | -                  | High Level Architecture             |
| Main Database Design (OLTP)    | 🟡 In Progress | Team            | -                  | ERD Under Review                    |
| Data Warehouse Design (OLAP)   | 🟡 In Progress | Zainab Abdelhak | 26-04-2026 3:00 AM | Fact & Dimension Modeling           |
| Data Sources Documentation     | 🟡 In Progress | Team            | -                  | APIs, Datasets, Scraping Sources    |
| Web Scraping Architecture      | 🟡 In Progress | Team            | -                  | Pharmacy Data Collection            |
| Data Collection                | ✅ Done         | -               | -                  | Initial Dataset Collected           |
| Data Cleaning                  | ✅ Done         | -               | -                  | Initial Dataset Prepared            |
| Data Validation Strategy       | ⏳ Next         | -               | -                  | Validation Rules                    |
| Data Quality Strategy          | ⏳ Next         | -               | -                  | Missing Data, Duplicates, Integrity |
| Data Modeling                  | ✅ Done         | -               | -                  | Initial Model Completed             |
| Data Dictionary                | ⏳ Next         | -               | -                  | Tables & Columns Documentation      |
| Data Staging Design            | ✅ Done         | -               | -                  | Staging Layer Defined               |
| Database Implementation        | 🟡 In Progress | Hala Mohamed    | 22-04-2026 7:00 PM | Failure to meet deadline            |
| Warehouse Loading Strategy     | ⏳ Next         | -               | -                  | Incremental Loading Design          |
| ETL Pipeline Design            | 🟡 In Progress | Abram Eisa      | -                  | Analytics Pipeline                  |
| AI Pipeline Design             | ⏳ Next         | -               | -                  | Recommendation Processing           |
| Real-Time Sync Design          | ⏳ Next         | -               | -                  | Inventory & Price Updates           |
| Analytics Layer Design         | ⏳ Next         | -               | -                  | KPIs & Business Metrics             |
| Security & Governance          | ⏳ Next         | -               | -                  | Roles & Access Control              |
| Monitoring & Logging Strategy  | ⏳ Next         | -               | -                  | Pipelines Monitoring                |
| Recommendation Engine Design   | ⏳ Next         | -               | -                  | AI Recommendation Logic             |
| AI Feature Engineering         | ⏳ Next         | -               | -                  | TF-IDF & Similarity Features        |
| Model Training Strategy        | ⏳ Next         | -               | -                  | Training Schedule                   |
| Model Evaluation Strategy      | ⏳ Next         | -               | -                  | Accuracy & Validation               |
| Backend Architecture Design    | ⏳ Next         | -               | -                  | APIs & Services                     |
| Backend Development            | ⏳ Next         | -               | -                  | Core APIs                           |
| Frontend Architecture Design   | ⏳ Next         | -               | -                  | Angular Structure                   |
| UI/UX Design                   | ⏳ Next         | -               | -                  | Wireframes & Screens                |
| Frontend Development           | ⏳ Next         | -               | -                  | User Platform                       |
| Pharmacy Dashboard Development | ⏳ Next         | -               | -                  | Pharmacy Management                 |
| Authentication & Authorization | ⏳ Next         | -               | -                  | JWT & Roles                         |
| Search System Development      | ⏳ Next         | -               | -                  | Drug Search Engine                  |
| Price Comparison Module        | ⏳ Next         | -               | -                  | Multi Pharmacy Comparison           |
| Availability Tracking Module   | ⏳ Next         | -               | -                  | Inventory Visibility                |
| Notifications Module           | ⏳ Next         | -               | -                  | Alerts & Updates                    |
| Integration Testing            | ⏳ Next         | -               | -                  | Full System Testing                 |
| Performance Testing            | ⏳ Next         | -               | -                  | Load & Stress Testing               |
| Deployment Architecture        | ⏳ Next         | -               | -                  | Azure Infrastructure                |
| CI/CD Setup                    | ⏳ Next         | -               | -                  | Automated Deployment                |
| Project Documentation          | ⏳ Next         | -               | -                  | Final Documentation                 |
| Project Roadmap                | ⏳ Next         | -               | -                  | V1, V2, Future Features             |
| Final Presentation             | ⏳ Next         | -               | -                  | Graduation Project Defense          |

---

## Overview

This document describes what has been completed and what is currently in progress in the Data Engineering phase of the project.

---

## Completed Work

### Problem Definition

Defined the main goals of the system:

* Drug search
* Price comparison
* Pharmacy discovery

### SRS (Software Requirements Specification)

Documented:

* Functional requirements
* Non-functional requirements
* Use cases

### Data Collection

Collected datasets including:

* Drugs
* Pharmacies
* Prices

### Data Cleaning

* Removed duplicates
* Handled missing values
* Standardized data formats

### Data Modeling (Schema Design)

* Designed database schema (ERD)
* Defined relationships between tables

### Data Staging

* Stored cleaned data in CSV/Excel files
* Organized under data/staging/

---

## Work In Progress

### Database Implementation

* Creating database and tables
* Applying schema.sql
* Preparing tables for data insertion

### Data Warehouse

* Creating a final structured dataset
* Combining data from multiple tables
* Target output:

  * final_dataset table or CSV
  * Includes drug, pharmacy, price, and location

### Pipeline

* Building ETL pipeline script
* Automating:

  * Reading data
  * Cleaning
  * Loading into database
* Goal:

  * Run everything with one command

---

## Next Step

### Data Validation

* Ensure:

  * No null values
  * No duplicates
  * Correct relationships
