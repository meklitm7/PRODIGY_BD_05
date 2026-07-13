# 🏨 Hotel Booking API

A production-ready **Hotel Booking REST API** built with **Django REST Framework** that allows customers to search, book, and manage hotel reservations while enabling hosts to manage hotel rooms through a secure role-based system.

This project was developed as part of the **Prodigy InfoTech Backend Development Internship – Task 05**.

---

# 🚀 Live Demo

### 🌐 API

https://prodigy-bd-05.onrender.com/api/

### 📖 Swagger Documentation

https://prodigy-bd-05.onrender.com/api/docs/

---

# ✨ Features

### 👤 Authentication

* JWT Authentication
* User Registration
* Secure Login
* User Profile
* Role-Based Authorization

# 👥 User Roles & Workflow

The application implements **Role-Based Access Control (RBAC)** with three different user roles.

### 👤 Customer

Customers can:

* Register an account
* Log in using JWT Authentication
* Browse available hotel rooms
* Search rooms using AI Natural Language Search
* Create hotel bookings
* View their own bookings
* Cancel their own bookings
* Manage their own profile

---

### 🏨 Host

Hosts can:

* Create hotel room listings
* Update their own rooms
* Delete their own rooms
* View rooms they have listed

---

### 👑 Admin

Administrators can:

* Create Host accounts
* Manage all users
* Update user roles
* Activate or deactivate user accounts

---

# 🔄 Application Workflow

```text
Admin
   │
   ├── Creates Host Accounts
   │
   ▼
Host
   │
   ├── Creates Hotel Rooms
   ├── Updates Hotel Rooms
   └── Deletes Hotel Rooms
   │
   ▼
Customer
   │
   ├── Registers
   ├── Logs in
   ├── Browses Available Rooms
   ├── Uses AI Natural Language Search
   ├── Creates Bookings
   ├── Views Bookings
   └── Cancels Bookings
```

### 🏨 Hotel Rooms

* Create Hotel Rooms
* Update Hotel Rooms
* Delete Hotel Rooms
* Retrieve Hotel Rooms
* Pagination
* Filtering
* Searching
* Ordering

### 📅 Booking System

* Create Booking
* View My Bookings
* Retrieve Booking
* Cancel Booking

### 🤖 AI Natural Language Search

Search hotel rooms using natural language.

Examples:

* Luxury suite tomorrow
* Cheap room under 3000
* Family room in Bahir Dar
* Double room for 2 guests
* Suite this weekend

---

# 🛠 Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* MySQL (Development)
* JWT Authentication
* WhiteNoise
* Gunicorn
* drf-spectacular (Swagger)
* django-filter
* Render

---

# 📚 API Documentation

Interactive Swagger Documentation

https://prodigy-bd-05.onrender.com/api/docs/

---

# 📂 Project Structure

```text
hotel_booking/
│
├── users/
├── hotels/
├── bookings/
├── ai_search/
├── hotel_booking/
├── manage.py
├── requirements.txt
└── README.md
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/meklitm7/PRODIGY_BD_05.git
```

Move into the project

```bash
cd PRODIGY_BD_05
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Start the development server

```bash
python manage.py runserver
```

---

# 🧪 Running Tests

Run all automated tests

```bash
python manage.py test
```

✅ Current Status

* 25 Automated Tests Passing

---

# 📖 Skills Demonstrated

* REST API Development
* Django REST Framework
* JWT Authentication
* Role-Based Access Control
* PostgreSQL Integration
* AI Natural Language Search
* Filtering & Pagination
* API Documentation
* Production Deployment
* Automated Testing
* Clean Backend Architecture

---

# 👩‍💻 Author

**Meklit Mulugeta**

Software Engineering Student

Backend Developer

LinkedIn

(https://www.linkedin.com/in/meklit-mulugeta-408816324/)

---

 