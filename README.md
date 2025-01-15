# Project Documentation

## Overview
This project provides an API-based solution for scheduling interviews, managing user availability, and handling user authentication using JWT. The project supports three user roles:

1. **Candidate**
2. **Interviewer**
3. **Admin**

Admins can oversee the system, while candidates and interviewers can register and provide their availability for scheduling interviews.

---

## Table of Contents
1. [Project Setup](#project-setup)
2. [Running the Project](#running-the-project)
3. [API Documentation](#api-documentation)
4. [User Creation](#user-creation)
5. [Testing](#testing)

---

## Project Setup

### Prerequisites
1. Python 3.8+
2. PostgreSQL
3. Git
4. pip (Python package installer)

### Steps to Set Up
1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate   # For Windows
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser (Admin):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server:**
   ```bash
   python manage.py runserver
   ```

---

## Running the Project

### Local Development
Start the development server by running:
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## API Documentation

### Base URL
- All API endpoints are prefixed with `http://127.0.0.1:8000/`.

### Authentication
JWT-based authentication is used. Include the token in the `Authorization` header:
```
Authorization: Bearer <your_token>
```

---

### Authentication APIs

#### 1. **Login**
**Endpoint:** `/api/token/`

**Method:** POST

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```

#### 2. **Refresh Token**
**Endpoint:** `/api/token/refresh/`

**Method:** POST

**Request Body:**
```json
{
  "refresh": "<refresh_token>"
}
```

**Response:**
```json
{
  "access": "<new_access_token>"
}
```

---

### User Management APIs

#### 1. **Register User**
**Endpoint:** `/api/register/`

**Method:** POST

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "role": 1
}
```

**Response:**
```json
{
  "message": "User registered successfully"
}
```

#### 2. **Get Current User**
**Endpoint:** `/api/user/`

**Method:** GET

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": 1
}
```

---

### Availability Management APIs

#### 1. **Register Availability**
**Endpoint:** `/api/availability/`

**Method:** POST

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "date": "2025-01-15",
  "start_time": "09:00:00",
  "end_time": "12:00:00"
}
```

**Response:**
```json
{
  "message": "Availability registered successfully"
}
```

---

#### 2. **Get Schedule Slots**
**Endpoint:** `/api/schedule/`

**Method:** POST

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "candidate_id": 2,
  "interviewer_id": 3
}
```

**Response:**
```json
{
  "available_slots": [
    ["10:00:00", "11:00:00"],
            "12:00:00"
    ["11:00:00", "12:00:00"]
  ]
}
```

---

## User Creation

### Create Users of Each Type

1. **Admin:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin user.

2. **Candidate and Interviewer:**
   Use the `/api/register/` API to create users with `role: 1` (Candidate) or `role: 2` (Interviewer).

---


### Notes
- Ensure that the JWT tokens are refreshed periodically for long-running sessions.
- Ensure that time slots are provided in hourly increments as required.
