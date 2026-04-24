# Data Engineering Progress

## Status Summary

| Task                    | Status         | Owner           | Deadline           | Notes |      
| ----------------------- | -------------- | --------------- | ------------------ | ----- |
| Problem Definition      | ✅ Done         | -               | -                  | -     |    
| SRS                     | ✅ Done         | -               | -                  | -     |        
| Data Collection         | ✅ Done         | -               | -                  | -     |       
| Data Cleaning           | ✅ Done         | -               | -                  | -     |   
| Data Modeling           | ✅ Done         | -               | -                  | -     |  
| Data Staging            | ✅ Done         | -               | -                  | -     |  
| Database Implementation | 🟡 In Progress | Hala Mohamed    | 22-04-2026 7:00 PM |Failure to meet the deadline| 
| Data Warehouse          | 🟡 In Progress | Zainab abdelhak | 26-04-2026 3:00 AM |       |       
| Pipeline                | 🟡 In Progress | abram Eisa      | [Date]             |       |   
| Data Validation         | ⏳ Next         | [Name]          | [Date]             |       | 

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
