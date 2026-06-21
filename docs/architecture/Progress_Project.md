# Data Engineering Progress

## Status Summary

| #  | Task                                   | الوصف                                             | Status         | Owner | Notes                            |
| -- | -------------------------------------- | ------------------------------------------------- | -------------- | ----- | -------------------------------- |
| 1  | Problem Definition                     | تحديد المشكلة التي يحلها المشروع وأهميتها         | ✅ Done         |       | -                                |
| 2  | Business Understanding                 | فهم المجال الطبي والصيدليات ومتطلبات السوق        | ✅ Done         |       | -                                |
| 3  | Stakeholders Analysis                  | تحديد جميع الأطراف المستفيدة والمتعاملة مع النظام | ✅ Done         |       | Stakeholders Identified          |
| 4  | System Scope Definition                | تحديد حدود المشروع وما سيتم تنفيذه                | ✅ Done         |       | Scope Finalized                  |
| 5  | SRS                                    | توثيق جميع المتطلبات الوظيفية وغير الوظيفية       | ✅ Done         |       | -                                |
| 6  | High Level Architecture                | تصميم المعمارية العامة للنظام                     | ✅ Done         |       | High Level Architecture          |
| 7  | Data Sources Documentation             | توثيق جميع مصادر البيانات المستخدمة               | 🟡 In Progress |       | APIs, Datasets, Scraping Sources |
| 8  | Web Scraping Research                  | دراسة المواقع المستهدفة وآلية جمع البيانات        | 🟡 In Progress |       | Pharmacy Data Sources            |
| 9  | Web Scraping Architecture              | تصميم نظام الـ Scraping والـ Crawlers             | 🟡 In Progress |       | Pharmacy Data Collection         |
| 10 | Data Collection                        | جمع البيانات الأولية                              | ✅ Done         |       | Initial Dataset Collected        |
| 11 | Data Cleaning                          | تنظيف البيانات وإزالة التكرار والأخطاء            | ✅ Done         |       | Initial Dataset Prepared         |
| 12 | Data Validation Strategy               | وضع قواعد التحقق من صحة البيانات                  | ⏳ Next         |       | Validation Rules                 |
| 13 | Data Quality Strategy                  | معالجة Missing Values وDuplicates وIntegrity      | ⏳ Next         |       | Data Quality Rules               |
| 14 | Data Staging Design                    | تصميم طبقة تجهيز البيانات قبل المعالجة            | ✅ Done         |       | Staging Layer Defined            |
| 15 | Data Modeling                          | تصميم النموذج المنطقي للبيانات                    | ✅ Done         |       | Initial Model Completed          |
| 16 | Main Database Design (OLTP)            | تصميم قاعدة البيانات التشغيلية للموقع             | 🟡 In Progress |       | ERD Under Review                 |
| 17 | Main Database Implementation           | تنفيذ قاعدة البيانات وإنشاء الجداول               | 🟡 In Progress |       | Database Creation                |
| 18 | Data Dictionary                        | توثيق جميع الجداول والأعمدة والعلاقات             | ⏳ Next         |       | Tables & Columns Documentation   |
| 19 | Data Warehouse Requirements            | تحديد البيانات المطلوبة داخل الـ Warehouse        | ⏳ Next         |       | Fact & Dimension Requirements    |
| 20 | Data Warehouse Design (OLAP)           | تصميم الـ Warehouse والـ Fact Tables              | 🟡 In Progress |       | Fact & Dimension Modeling        |
| 21 | Warehouse Loading Strategy             | تصميم آلية تحميل البيانات للـ Warehouse           | ⏳ Next         |       | Incremental Loading Design       |
| 22 | ETL Pipeline Design                    | تصميم Analytics Pipeline                          | 🟡 In Progress |       | Extract, Transform, Load         |
| 23 | AI Pipeline Design                     | تصميم Pipeline الخاصة بالتوصيات والذكاء الاصطناعي | ⏳ Next         |       | Recommendation Processing        |
| 24 | Real-Time Sync Design                  | تصميم مزامنة الأسعار والمخزون لحظيًا              | ⏳ Next         |       | Inventory & Price Updates        |
| 25 | Monitoring & Logging Strategy          | تصميم نظام متابعة الأخطاء والـ Pipelines          | ⏳ Next         |       | Pipelines Monitoring             |
| 26 | Analytics Layer Design                 | تصميم طبقة التحليلات والتقارير                    | ⏳ Next         |       | KPIs & Business Metrics          |
| 27 | KPI Definition                         | تحديد مؤشرات الأداء الرئيسية                      | ⏳ Next         |       | Business KPIs                    |
| 28 | Security & Governance                  | تصميم الصلاحيات وسياسات الأمان                    | ⏳ Next         |       | Roles & Access Control           |
| 29 | Data Governance Policy                 | وضع سياسات إدارة البيانات وجودتها                 | ⏳ Next         |       | Data Ownership & Standards       |
| 30 | Backup & Recovery Strategy             | تصميم النسخ الاحتياطي واستعادة البيانات           | ⏳ Next         |       | Disaster Recovery                |
| 31 | Recommendation Engine Design           | تصميم محرك التوصيات                               | ⏳ Next         |       | AI Recommendation Logic          |
| 32 | AI Feature Engineering                 | تجهيز Features المستخدمة في الذكاء الاصطناعي      | ⏳ Next         |       | TF-IDF, Similarity Features      |
| 33 | Model Training Strategy                | تحديد طريقة وجدولة تدريب المودلز                  | ⏳ Next         |       | Training Schedule                |
| 34 | Model Evaluation Strategy              | تقييم جودة المودلز ودقتها                         | ⏳ Next         |       | Accuracy & Validation            |
| 35 | Model Versioning & Experiment Tracking | إدارة نسخ المودلز وتتبع التجارب                   | ⏳ Next         |       | ML Lifecycle                     |
| 36 | Backend Architecture Design            | تصميم هيكل الباك إند والخدمات                     | ⏳ Next         |       | APIs & Services                  |
| 37 | API Design                             | تصميم جميع الـ APIs الخاصة بالنظام                | ⏳ Next         |       | API Contracts                    |
| 38 | Authentication & Authorization         | تصميم نظام تسجيل الدخول والصلاحيات                | ⏳ Next         |       | JWT & Roles                      |
| 39 | Backend Development                    | تطوير الباك إند وتنفيذ الـ APIs                   | ⏳ Next         |       | Core APIs                        |
| 40 | Frontend Architecture Design           | تصميم هيكل مشروع Angular                          | ⏳ Next         |       | Angular Structure                |
| 41 | UI/UX Design                           | تصميم الشاشات وتجربة المستخدم                     | ✅ Done           |       | Wireframes & Screens             |
| 42 | Frontend Development                   | تنفيذ واجهات المستخدم                             | ⏳ Next         |       | User Platform                    |
| 43 | Search System Development              | تطوير نظام البحث الذكي عن الأدوية                 | ⏳ Next         |       | Drug Search Engine               |
| 44 | Recommendation System Development      | تطوير نظام التوصيات وربطه بالذكاء الاصطناعي       | ⏳ Next         |       | AI Recommendations               |
| 45 | Price Comparison Module                | تطوير مقارنة الأسعار بين الصيدليات                | ⏳ Next         |       | Multi Pharmacy Comparison        |
| 46 | Availability Tracking Module           | تطوير متابعة التوفر والمخزون                      | ⏳ Next         |       | Inventory Visibility             |
| 47 | Pharmacy Dashboard Development         | تطوير لوحة تحكم الصيدليات                         | ⏳ Next         |       | Pharmacy Management              |
| 48 | Admin Dashboard Development            | تطوير لوحة تحكم الإدارة                           | ⏳ Next         |       | System Management                |
| 49 | Notifications Module                   | تطوير الإشعارات والتنبيهات                        | ⏳ Next         |       | Alerts & Updates                 |
| 50 | AI Integration                         | ربط المودلز بالنظام الفعلي                        | ⏳ Next         |       | AI Integration                   |
| 51 | Data Warehouse Integration             | ربط الـ Warehouse بالنظام                         | ⏳ Next         |       | Warehouse Integration            |
| 52 | End-to-End Integration                 | ربط جميع أجزاء المشروع معًا                       | ⏳ Next         |       | Full System Integration          |
| 53 | Unit Testing                           | اختبار كل جزء بشكل منفصل                          | ⏳ Next         |       | Unit Tests                       |
| 54 | Integration Testing                    | اختبار تكامل جميع المكونات                        | ⏳ Next         |       | Full System Testing              |
| 55 | Performance Testing                    | اختبار الأداء والتحميل                            | ⏳ Next         |       | Load & Stress Testing            |
| 56 | Security Testing                       | اختبار الحماية والصلاحيات                         | ⏳ Next         |       | Security Validation              |
| 57 | Deployment Architecture                | تصميم بيئة النشر النهائية                         | ⏳ Next         |       | Azure Infrastructure             |
| 58 | CI/CD Setup                            | إعداد النشر التلقائي                              | ⏳ Next         |       | Automated Deployment             |
| 59 | Production Deployment                  | رفع النظام على البيئة النهائية                    | ⏳ Next         |       | Production Release               |
| 60 | Technical Documentation                | توثيق الجانب التقني بالكامل                       | ⏳ Next         |       | Technical Docs                   |
| 61 | User Documentation                     | توثيق طريقة استخدام النظام                        | ⏳ Next         |       | User Guide                       |
| 62 | Final Project Documentation            | تجميع جميع ملفات المشروع النهائية                 | ⏳ Next         |       | Final Documentation              |
| 63 | Project Roadmap                        | توضيح مراحل التطوير المستقبلية                    | ⏳ Next         |       | V1, V2, Future Features          |
| 64 | Demo Preparation                       | تجهيز سيناريو العرض العملي                        | ⏳ Next         |       | Demo Scenario                    |
| 65 | PowerPoint Preparation                 | إعداد عرض المشروع للمناقشة                        | ⏳ Next         |       | Presentation Slides              |
| 66 | Final Presentation                     | عرض المشروع أمام اللجنة                           | ⏳ Next         |       | Graduation Project Defense       |
| 67 | Graduation Project Submission          | تسليم المشروع النهائي                             | ⏳ Next         |       | Final Submission                 |


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
