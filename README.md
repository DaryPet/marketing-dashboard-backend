# marketing-dashboard-backend

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

### 6. Load test data

Load the pre-created test data into the database:

```bash
python manage.py loaddata backend/campaigns/fixtures/initial_data.json
```

---

### 7. Start the development server

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

To run the automated tests, use the following command:

```bash
python manage.py test backend.campaigns --keepdb
```

---

## Project Structure

```
marketing-dashboard-backend/
│
├── backend/
│   ├── campaigns/
│   │   ├── migrations/
│   │   ├── fixtures/            # Test data (initial_data.json)
│   │   ├── models.py            # Database models
│   │   ├── serializers.py       # API serializers
│   │   ├── views.py             # API views
│   │   ├── tests.py             # Unit tests
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
