# 📸 Professional Online Photography Booking Platform

A feature-rich, enterprise-structured full-stack web application designed to streamline photography service bookings. Built with a robust **Python/Django** backend, this platform implements strict **Role-Based Access Control (RBAC)** to deliver targeted dashboards and isolated workflows for Administrators, Clients, and Photographers.

🌐 **Live Architecture Demo:** [View Live App](https://zaid1dev.pythonanywhere.com/)

---

### 🚀 Key Technical Highlights

* **Advanced Role-Based Access Control (RBAC):** Custom authentication framework using Django User + `UserProfile` linkage to securely segregate workflows for Admin, Photographers, and Clients.
* **Modern UI Architecture:** Responsive frontend designed with elegant **Glass-morphism UI effects**, custom dark gradients, **AOS (Animate On Scroll)** animation systems, and a dynamic floating WhatsApp integration.
* **Smart Booking & Scheduling Ledger:** Multi-state workflow engine tracking event parameters (`event_type`, `guest_count`, `date/time slots`) with automated operational states (`pending`, `confirmed`, `cancelled`).
* **Real-time Event Notification Subsystem:** Keeps clients instantly informed via automated alerts whenever an assignment status is updated by a photographer.

---

### 🗄️ System Architecture & Database Schema

The platform utilizes an optimized relational schema engineered to handle multi-user interactions seamlessly:

```text
vikas_photography/ (Project Root)
├── booking/                      # Main Core Application
│   ├── models.py                 # Relational Database Schema
│   ├── views.py                  # Functional Controllers & Authentication
│   ├── forms.py                  # Form Validation Engines
│   └── urls.py                   # App-level Endpoint Routing
├── templates/                    # Server-Side Rendered (SSR) Glassmorphic UI
└── media/photographers/          # Isolated Media Upload Pipeline
📊 Core Relational Data Models:
UserProfile: Extends Django's core Auth module; encapsulates structural role definition ('client' / 'photographer') and an administrative is_approved verification pipeline.

PhotographerProfile: Maps professional profiles to users with target attributes like specialty, location, and secure image-upload pipelines (profile_pic).

Booking: The relational bridge connecting Clients, Photographers, schedules, and structural states (status).

Notification: Relational message ledger managing state-based communication queues with is_read boolean flags.

🔄 End-to-End Application Flow
Plaintext
[User Signup] ──> [Role Assignment]
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
  [Client Role]             [Photographer Role]
         │                           │
         ▼                           ▼
[Browse Profiles]           [Await Admin Approval]
         │                           │
         ▼                           ▼
[Submit Booking]            [Build Studio Profile]
         │                           │
         ▼                           ▼
[Await Confirmation] <──>  [Accept / Reject Requests]
Onboarding: Multi-role signup initializes isolated dashboards based on user intent. Photographers enter a verification queue.

Discovery & Booking: Clients access a server-rendered grid of authorized photographers, select availability matrices, and fire a request.

State Resolution: Photographers manipulate incoming requests from their dedicated dashboard panels, dispatching notification queries back to clients.

🛠️ Technology Stack & Dependencies
Backend Framework: Python, Django (MVT Architecture), Django ORM

Frontend Engine: HTML5, CSS3, JavaScript, Bootstrap 5, AOS Library

Database Management: SQLite (Development / Testing Ready)

Storage & Uploads: Django Media Pipeline for automated file isolation

Environment & Deployment: Git, GitHub, PythonAnywhere, WSGI/ASGI Production Layers

💻 Local Deployment & Configuration
To spin up the development environment locally:

Clone the Source Ledger:

Bash
git clone [https://github.com/zaid-444/photography.git](https://github.com/zaid-444/photography.git)
cd photography
Initialize Isolated Virtual Environment:

Bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
Install Requirements & Fire Migrations:

Bash
pip install -r requirements.txt
python manage.py migrate
Boot Up Development Server:

Bash
python manage.py runserver
Access the local ecosystem via http://127.0.0.1:8000/.

📬 Contact & Collaboration
Shaikh Zaid Gaffar - LinkedIn | 📧 zaidx0444@gmail.com
