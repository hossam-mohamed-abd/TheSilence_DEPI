# MediSearch Web Application

## Overview

The MediSearch Web Application is the frontend client of the MediSearch platform.

It provides an intuitive and responsive interface that allows users, pharmacies, and administrators to interact with the system.

The application is built using modern Angular technologies and follows a scalable, component-based architecture.

---

# Live Demo

Production URL:

https://medi-search-eight.vercel.app/

Hosting Platform:

Vercel

---

# Source Code

GitHub Repository:

https://github.com/hossam-mohamed-abd/MediSearch

---

# Technology Stack

## Framework

- Angular

## Language

- TypeScript

## Styling

- CSS3
- Responsive Design
- Flexbox
- CSS Grid

## State Management

- RxJS
- Angular Signals (when applicable)

## Routing

- Angular Router

## Forms

- Reactive Forms
- Template Driven Forms

## HTTP Communication

- Angular HttpClient
- REST APIs

## Authentication

- JWT Authentication
- Cookie Authentication

## Deployment

- Vercel

---

# Main Features

- Drug Search
- Price Comparison
- Availability Tracking
- Drug Alternatives
- User Authentication
- Favorites
- Notifications
- Pharmacy Dashboard
- Admin Dashboard
- AI Recommendations

---

# Project Structure

```text
src
│
├── app
│   ├── core
│   ├── shared
│   ├── features
│   ├── layouts
│   ├── pages
│   ├── services
│   ├── guards
│   ├── interceptors
│   └── models
│
├── assets
│
├── environments
│
└── styles
```

---

# High Level Architecture

```text
Angular Frontend
        ↓
REST APIs
        ↓
Backend Services
        ↓
Database Layer
        ↓
Analytics & AI
```

---

# Development Workflow

```text
Requirement
      ↓
UI/UX Design
      ↓
Component Design
      ↓
Development
      ↓
API Integration
      ↓
Testing
      ↓
Deployment
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/hossam-mohamed-abd/MediSearch.git
```

Go to the project:

```bash
cd MediSearch
```

Install dependencies:

```bash
npm install
```

---

# Run Development Server

```bash
ng serve
```

or

```bash
npm start
```

The application will run on:

```text
http://localhost:4200
```

---

# Build Production Version

```bash
ng build --configuration production
```

---

# Generate Components

```bash
ng generate component component-name
```

or

```bash
ng g c component-name
```

---

# Environment Variables

Example:

```typescript
export const environment = {
  production: false,
  apiUrl: '',
  aiApiUrl: '',
};
```

---

# API Communication

The frontend communicates with:

- Authentication Service
- User Service
- Drug Service
- Pharmacy Service
- Recommendation Service
- Notification Service

---

# Responsive Design

Supported Devices:

- Desktop
- Laptop
- Tablet
- Mobile

---

# Best Practices

✅ Use standalone components when possible.

✅ Create reusable components.

✅ Use lazy loading.

✅ Keep business logic inside services.

✅ Use TypeScript interfaces.

✅ Use environment files.

✅ Keep components small and maintainable.

---

# Coding Standards

- Follow Angular Style Guide.
- Use meaningful component names.
- Use feature-based architecture.
- Keep services reusable.
- Avoid duplicated code.

---

# Dependencies

Install Angular CLI globally:

```bash
npm install -g @angular/cli
```

Check Angular version:

```bash
ng version
```

---

# Documentation

UI/UX Design:

https://www.figma.com/board/qygMtKJHuPAP0KwOt1JauR/MediSearch

Frontend Repository:

https://github.com/hossam-mohamed-abd/MediSearch

Backend API:

https://medi-search-backend.vercel.app/

Backend Repository:

https://github.com/hossam-mohamed-abd/MediSearch_backend.git

---

# Responsibilities

The Web Application is responsible for:

- User Interface
- User Experience
- Client-side Validation
- API Communication
- Authentication Flow
- State Management
- Responsive Rendering

The Web Application is NOT responsible for:

- Database Operations
- Data Cleaning
- ETL Pipelines
- Analytics Processing
- Machine Learning Training

These responsibilities belong to the Backend and Data Engineering layers.

---

# Status

```text
Current Stage:
MVP Development
```

```text
Frontend Framework:
Angular
```

```text
Deployment:
Production Available
```
