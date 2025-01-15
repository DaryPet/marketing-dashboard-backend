# Marketing Dashboard Backend

This is the backend for the Marketing Dashboard application. It provides a REST API for managing marketing campaigns and advertising channels.

---

## Features

- View all marketing campaigns.
- Create new campaigns.
- Edit existing campaigns.
- Delete campaigns.
- Manage advertising channels.
- Input validation for budgets, dates, and campaign uniqueness.

---

## Technologies Used

- **Framework**: Django (Python)
- **Database**: Supabase (PostgreSQL)
- **API Documentation**: Swagger (via `drf-yasg`)

---

## Setup Instructions

### Prerequisites

1. Python 3.10+
2. PostgreSQL database (Supabase-compatible)
3. Git

---

### 1. Clone the repository

```bash
git clone https://github.com/your-repo/marketing-dashboard-backend.git
cd marketing-dashboard-backend
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure the database

Update the `DATABASES` section in `backend/settings.py` with your Supabase credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<your-database-name>',
        'USER': '<your-database-user>',
        'PASSWORD': '<your-database-password>',
        'HOST': '<your-database-host>',
        'PORT': '6543',
    }
}
```

---

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Start the development server

```bash
python manage.py runserver
```

The server will start at:

```
http://127.0.0.1:8000/
```

---

## API Documentation

The Swagger UI for testing the API is available at:

```
http://127.0.0.1:8000/swagger/
```

---

## Running Tests

### Unit Tests

The project includes several unit tests for the API endpoints:

- **Test Campaign Creation**: Validates that a new campaign can be successfully created through the API.
- **Test Campaign Deletion**: Verifies that an existing campaign can be deleted successfully.
- **Test Campaign Retrieval**: Ensures that campaigns can be retrieved correctly, including validation for non-existent campaigns.
- **Test Campaign Update**: Ensures that an existing campaign's details can be updated.

To run the automated tests, use the following command:

```bash
python manage.py test backend.campaigns.tests.test_campaign_serializer --keepdb --verbosity=2 or python manage.py test backend.campaigns.tests.unit_tests --keepdb --verbosity=2
```

### Authentication Tests

These tests validate the JWT authentication mechanism and protected API access:

- **Test Obtaining JWT Token**: Verifies that a user can obtain a JWT token by providing valid credentials (username and password).
- **Test Accessing a Protected View with Token**: Simulates accessing a protected endpoint using a valid JWT token and ensures that access is granted.
- **Test Accessing a Protected View without Token**: Simulates accessing a protected endpoint without a token and ensures that the response returns a 401 Unauthorized status, indicating that authentication is required.

To run the automated auth tests, use the following command:

```bash
python manage.py test backend.campaigns.tests.test_auth --keepdb --verbosity=2
```

### End-to-End Tests

These tests simulate the full flow of API requests to ensure all operations work together as expected:

- **Test Creating a Campaign**: Simulates creating a new campaign and verifies the response and database state.
- **Test Deleting a Campaign**: Simulates deleting a campaign and ensures it is correctly removed.
- **Test Retrieving the Campaign List**: Simulates retrieving all campaigns and verifies the returned data.
- **Test Updating a Campaign**: Simulates updating a campaign and checks if the changes are reflected.

To run the automated end-2-end tests, use the following command:

```bash
python manage.py test backend.campaigns.tests.test_end_to_end --keepdb --verbosity=2
```

---

## Project Structure

```
marketing-dashboard-backend/
│
├── backend/
│   ├── campaigns/
│   │   ├── migrations/
│   │   ├── models.py            # Database models
│   │   ├── serializers.py       # API serializers
│   │   ├── views.py             # API views
│   │   ├── test_auth.py         # Auth tests
│   │   ├── test_end_to_end.py   # End-to-End tests
│   └── urls.py                  # Project-level URL configuration
│
├── venv/                        # Virtual environment
├── manage.py                    # Django management script
├── requirements.txt             # Dependencies
└── README.md                    # Project documentation
```

---

## Endpoints

### Campaigns

| Method | Endpoint               | Description                 |
| ------ | ---------------------- | --------------------------- |
| GET    | `/api/campaigns/`      | View all campaigns          |
| POST   | `/api/campaigns/`      | Create a new campaign       |
| PUT    | `/api/campaigns/<id>/` | Update an existing campaign |
| DELETE | `/api/campaigns/<id>/` | Delete a campaign           |

### Channels

| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| GET    | `/api/channels/` | View all channels    |
| POST   | `/api/channels/` | Create a new channel |

---
