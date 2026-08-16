# 📸 Professional Online Photography Booking Platform

A feature-rich, enterprise-structured full-stack web application designed to streamline photography service bookings. Initiated in **September 2025**. Built with a robust **Python/Django** backend, this platform implements strict **Role-Based Access Control (RBAC)** to deliver targeted dashboards and isolated workflows for Administrators, Clients, and Photographers.

🌐 **Live Architecture Demo:** [View Live App](https://zaid1dev.pythonanywhere.com/)

---

### 🚀 Key Technical & Operational Features

* **🔐 Advanced Role-Based Access Control (RBAC):** Custom authentication framework using Django `User` + `UserProfile` linkage to securely segregate workflows for Admin, Photographers, and Clients.
* **📅 Calendar Availability Lock Engine:** Prevents double-booking by dynamically locking occupied dates for photographers and preventing selection of past dates.
* **🔍 Photographer Search & Filter System:** Real-time multi-criteria filtering by name/keyword, city location, and photography specialty (Wedding, Portrait, Cinematic, etc.).
* **📞 Client Contact Details Ledger:** Captures client full name, mobile number (with click-to-call), and email address during booking requests so photographers can communicate instantly.
* **✏️ Photographer Self-Service Profile Management:** Enables approved photographers to update their profile picture (DP), specialty, city location, and contact numbers.
* **✨ Glassmorphic UI & 5-Second Auto-Dismiss Alerts:** Responsive dark slate and gold UI featuring backdrop blur cards and auto-dismissing 5-second toast notification alerts.
* **📱 Mobile Responsive Architecture:** Optimised layouts for mobile screens, including responsive headers, compact cards, and drawer menus.

---

### 🗄️ System Architecture & File Structure

```text
photography/ (Project Root)
├── booking/                      # Main Core Application
│   ├── models.py                 # Relational Database Schema (UserProfile, PhotographerProfile, Booking, Notification)
│   ├── views.py                  # Controllers & Search/Booking/Filter Business Logic
│   ├── forms.py                  # Form Validation Engines & Custom Cleaners
│   └── urls.py                   # App-level Endpoint Routing
├── templates/                    # Server-Side Rendered (SSR) Glassmorphic UI Templates
│   └── booking/
│       ├── base.html             # Global Glassmorphic Layout & Navigation
│       ├── home.html             # Hero Video & Portfolio Showcase
│       ├── photographer_list.html# Search & Filter Photographers Grid
│       ├── book_photographer.html# Booking Form & Dynamic Calendar Lock
│       ├── dashboard.html        # Photographer & Client Management Dashboards
│       └── edit_photographer_profile.html # Profile Update Panel
├── static/                       # Static CSS, JS, Brand Logos & Gallery Media
├── media/photographers/          # Isolated User Profile Image Pipeline
├── .gitignore                    # Production Git Ignore Rules
├── requirements.txt              # Project Dependencies
└── LICENSE                       # Official MIT Open Source License
```

---

### 📊 Core Relational Data Models

1. **`UserProfile`:** Extends Django's core Auth module; encapsulates structural role definition (`client` / `photographer`) and an administrative `is_approved` verification pipeline.
2. **`PhotographerProfile`:** Maps professional profiles to users with attributes like full name, phone, specialty, location, and secure image upload pipelines (`profile_pic`).
3. **`Booking`:** Relational bridge connecting Clients, Photographers, schedules (`date`, `time`), client contact info (`client_name`, `client_phone`, `client_email`), event parameters (`venue`, `guest_count`, `message`), and operational states (`status`: pending, accepted, confirmed, rejected, cancelled).
4. **`Notification`:** Relational message ledger managing state-based communication queues with `is_read` boolean flags.

---

### 🔄 End-to-End Application Flow

```text
[User Signup] ──> [Role Selection: Client / Photographer]
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
  [Client Role]             [Photographer Role]
         │                           │
         ▼                           ▼
[Search & Filter Photographers] [Await Admin Approval]
         │                           │
         ▼                           ▼
[Fill Contact & Event Booking]  [Create/Edit Studio Profile]
         │                           │
         ▼                           ▼
[Real-Time Status & Alerts] <──> [Accept / Reject Requests]
```

---

### 🛠️ Technology Stack & Dependencies

* **Backend Framework:** Python 3.x, Django 5.x (MVT Architecture), Django ORM
* **Frontend Engine:** HTML5, CSS3 (Vanilla Glassmorphism), JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons, AOS (Animate On Scroll)
* **Database Engine:** SQLite3 (Development & Production Ready)
* **Media & Asset Isolation:** Django Media Pipeline (`ImageField` / `Pillow`)
* **Version Control & Hosting:** Git, GitHub, PythonAnywhere

---

### 💻 Local Deployment & Setup Guide

To spin up the development environment locally:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/zaid-444/photography.git
   cd photography
   ```

2. **Initialize Isolated Virtual Environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Requirements & Run Database Migrations:**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   ```

4. **Start Development Server:**
   ```bash
   python manage.py runserver
   ```
   Access the local web app at `http://127.0.0.1:8000/`.

---

### 📜 License
This project is open-source and licensed under the [MIT License](LICENSE).

Copyright (c) **2025-2026 Shaikh Zaid Gaffar**. All rights reserved.

---

### 📬 Contact & Collaboration
**Shaikh Zaid Gaffar** — 📧 [zaid.dev8@gmail.com](mailto:zaid.dev8@gmail.com) | [GitHub Profile](https://github.com/zaid-444)
