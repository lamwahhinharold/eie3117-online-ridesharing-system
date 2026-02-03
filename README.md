# EIE3117 Online Ridesharing System

A full-stack web application for an online ridesharing platform. Users can register as riders or drivers, advertise routes, and book rides.

## Features

- User Authentication: Register and login as rider or driver
- Route Advertising: Drivers create routes with date, time, locations, car model, capacity
- Ride Booking: Riders browse and book available routes
- Profile Management: Update nickname and profile image
- Real-time Availability: Shows remaining seats, unavailable when full
- Responsive Design: Mobile-friendly with Bulma CSS

## Tech Stack

### Backend
- Django 5.2 with Django REST Framework
- Djoser for authentication
- SQLite database

### Frontend
- Vue.js 3 with Vue Router and Vuex
- Axios for API calls
- Bulma CSS framework
- Vite build tool

## Prerequisites

- Python 3.8+ for backend
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
   - Or pip: `pip install -r requirements.txt`

3. Set up frontend: `cd frontend && npm install && cd ..`

## Setup

1. Run migrations: `python manage.py migrate`
2. (Optional) Create superuser: `python manage.py createsuperuser`
3. Start backend: `python manage.py runserver` (API at http://localhost:8000)
4. Start frontend: `cd frontend && npm run dev` (App at http://localhost:5173)

## Usage

- Register as rider or driver
- Login to access platform
- Drivers: Advertise routes via "Advertise" page
- Riders: Browse routes on home page, book seats
- Update profile with nickname and image

## API Endpoints

RESTful API for authentication, routes, bookings, profiles.
Base URL: `http://localhost:8000/api/`

## Project Structure

```
eie3117-online-ridesharing-system/
├── backend/          # Django backend
├── core/             # Main app (models, views, etc.)
├── frontend/         # Vue.js frontend
├── media/            # Uploaded files
├── db.sqlite3        # Database
└── environment.yml   # Conda env
```
