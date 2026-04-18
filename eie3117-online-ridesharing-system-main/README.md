# EIE3117 Online Ridesharing System

A full-stack web application for an online ridesharing platform. Users can register as riders or drivers, advertise routes, and book rides.

## Features

- User Authentication: Register and login as rider or driver with session-based auth
- Route Advertising: Drivers create routes with date, time, locations, car model, capacity
- Ride Booking: Riders browse and book available routes
- Profile Management: Update nickname, email, and profile image
- Seat Availability: Shows remaining seats, unavailable when full or expired
- Responsive Design: Mobile-friendly with Bulma CSS

## Tech Stack

### Backend
- Django 5.2 with Django REST Framework
- Session-based authentication with custom views
- SQLite database

### Frontend
- Vue.js 3 with Vue Router and Vuex
- Axios for API calls
- Bulma CSS framework
- Vite build tool

## Prerequisites

- Python 3.10+ for backend
- Node.js 20+ for frontend
- Conda (optional) for environment management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/eie3117-online-ridesharing-system.git
   cd eie3117-online-ridesharing-system
   ```

2. Set up Python environment:
   - With Conda: `conda env create -f environment.yml`
   - Activate venv: `conda activate eie3117`

3. Set up frontend: `cd frontend && npm install && cd ..`

## Setup

1. Run migrations: `python manage.py migrate`
2. (Optional) Create superuser: `python manage.py createsuperuser`
3. Start backend: `python manage.py runserver` (API at http://localhost:8000)
4. Start frontend: `cd frontend && npm run dev` (App at http://localhost:5173)

## Usage

- Register as rider or driver
- Login to access platform
- Drivers: Advertise routes via "New Route" page
- Riders: Browse routes on home page, book seats
- Update profile with nickname, email, and image

## API Endpoints

Base URL: `http://localhost:8000/api/`

| Endpoint | Method | Description |
|---|---|---|
| `/api/csrf/` | GET | Get CSRF token cookie |
| `/api/register/` | POST | Register a new user |
| `/api/login/` | POST | Login (session-based) |
| `/api/logout/` | POST | Logout (invalidate session) |
| `/api/user/` | GET, PATCH | Get or update current user profile |
| `/api/routes/` | GET, POST | List all routes or create a new route |
| `/api/routes/{id}/` | GET, PUT, PATCH, DELETE | Retrieve, update, or delete a route |
| `/api/routes/{id}/join/` | POST | Reserve a seat on a route (riders only) |
| `/api/routes/my_advertisements/` | GET | List routes created by the logged-in driver |
| `/api/bookings/` | GET | List current user's bookings |
| `/api/bookings/{id}/` | GET, DELETE | Retrieve or cancel a booking |

## Project Structure

```
eie3117-online-ridesharing-system/
├── backend/          # Django project settings and config
├── core/             # Main app (models, views, serializers, tests)
├── frontend/         # Vue.js frontend
├── media/            # Uploaded files (profile images)
├── manage.py         # Django management script
├── db.sqlite3        # SQLite database
└── environment.yml   # Conda environment
```
