# Job Tracker CRM

A comprehensive full-stack web application for tracking job applications with role-based authentication, email integration, and analytics.

<img width="2048" height="1152" alt="1" src="https://github.com/user-attachments/assets/69d98ddf-f916-43cd-8db8-9ac229d69283" />

<img width="2048" height="1152" alt="2" src="https://github.com/user-attachments/assets/fe97af42-49f9-427a-8e42-94bb849181c9" />


<img width="2048" height="1152" alt="3" src="https://github.com/user-attachments/assets/dd3801fb-229d-4110-b173-7a4d54b99c60" />


<img width="2048" height="1152" alt="4" src="https://github.com/user-attachments/assets/f1a028e9-97ff-43d8-b474-97ca478cbc89" />

<img width="2048" height="1152" alt="5" src="https://github.com/user-attachments/assets/276d9525-021a-4165-aa27-a13b9b5639b8" />



## 🚀 Features

### 🔐 Authentication & User Management
- User registration with email verification
- JWT-based authentication (access + refresh tokens)
- Password reset via email
- Role-based access control (user vs admin)
- Protected routes for different user roles

### 👤 User Dashboard
- Full CRUD operations for job applications
- Advanced filtering by status and company
- Activity timeline view
- Resume URL tracking

### 📬 Email Integration
- Email verification on signup
- Password reset emails
- Interview reminders (24 hours prior)
- Weekly summary emails

### 🧑‍💼 Admin Dashboard
- User management (view, deactivate, delete)
- Global job application analytics
- System-wide broadcast notifications
- Comprehensive statistics

### 📊 Analytics
- Status distribution charts
- Company application trends
- Monthly/weekly activity graphs
- Interactive data visualization

## 🛠️ Tech Stack

### Frontend
- **React.js** - Modern UI framework
- **Tailwind CSS** - Utility-first CSS framework
- **Recharts** - Data visualization library
- **Axios** - HTTP client
- **React Router** - Client-side routing

### Backend
- **Python** - Programming language
- **Django** - Web framework
- **Django REST Framework** - API framework
- **PostgreSQL** - Database
- **Celery** - Task queue for email scheduling
- **Django Cron** - Cron job management

### Authentication & Security
- **JWT** - JSON Web Tokens
- **DRF SimpleJWT** - JWT implementation
- **CORS** - Cross-origin resource sharing
- **Environment variables** - Secure configuration

## 📁 Project Structure

```
job-tracker-crm/
├── frontend/                 # React.js application
│   ├── public/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── hooks/          # Custom React hooks
│   │   ├── utils/          # Utility functions
│   │   └── styles/         # CSS styles
│   ├── package.json
│   └── tailwind.config.js
├── backend/                 # Django application
│   ├── job_tracker/        # Main Django project
│   ├── apps/
│   │   ├── auth/           # Custom authentication
│   │   ├── jobs/           # Job application models
│   │   ├── users/          # User management
│   │   └── analytics/      # Analytics and reporting
│   ├── api/                # API endpoints
│   ├── requirements.txt
│   └── manage.py
├── seed_data/              # Sample data and fixtures
├── .env.example            # Environment variables template
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- PostgreSQL
- Redis (for Celery tasks)

### Backend Setup

1. **Clone and navigate to backend:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp ../.env.example .env
# Edit .env with your database and email credentials
```

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Create superuser:**
```bash
python manage.py createsuperuser
```

7. **Load sample data:**
```bash
python manage.py loaddata ../seed_data/sample_data.json
```

8. **Start the server:**
```bash
python manage.py runserver
```

### Frontend Setup

1. **Navigate to frontend:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Set up environment variables:**
```bash
cp ../.env.example .env
# Edit .env with your backend API URL
```

4. **Start the development server:**
```bash
npm start
```

## 📧 Email Configuration

Configure your email settings in the `.env` file:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🗄️ Database Schema

### Users
- `id` - Primary key
- `email` - Unique email address
- `first_name` - User's first name
- `last_name` - User's last name
- `is_active` - Account status
- `is_staff` - Admin privileges
- `date_joined` - Registration date

### Job Applications
- `id` - Primary key
- `user` - Foreign key to User
- `company_name` - Company name
- `job_title` - Job position title
- `application_date` - Date applied
- `status` - Application status (Applied, Interviewing, Offer, Rejected)
- `notes` - Additional notes
- `resume_url` - Resume link
- `created_at` - Record creation date
- `updated_at` - Last update date

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token
- `POST /api/auth/verify-email/` - Email verification
- `POST /api/auth/reset-password/` - Password reset

### Job Applications
- `GET /api/jobs/` - List user's job applications
- `POST /api/jobs/` - Create new job application
- `GET /api/jobs/{id}/` - Get specific job application
- `PUT /api/jobs/{id}/` - Update job application
- `DELETE /api/jobs/{id}/` - Delete job application

### Admin Endpoints
- `GET /api/admin/users/` - List all users
- `GET /api/admin/analytics/` - Get analytics data
- `POST /api/admin/broadcast/` - Send broadcast notification

## 🚀 Deployment

### Heroku Deployment

1. **Backend deployment:**
```bash
# Add Heroku PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-database-url
heroku config:set EMAIL_HOST=smtp.gmail.com
heroku config:set EMAIL_HOST_USER=your-email
heroku config:set EMAIL_HOST_PASSWORD=your-password

# Deploy
git push heroku main
```

2. **Frontend deployment:**
```bash
# Build the React app
npm run build

# Deploy to Heroku or Netlify
```

### AWS Deployment

1. **EC2 Setup:**
   - Launch Ubuntu instance
   - Install Python, Node.js, PostgreSQL, Nginx
   - Configure security groups

2. **RDS Setup:**
   - Create PostgreSQL instance
   - Configure VPC and security groups

3. **Deploy using Docker:**
```bash
docker-compose up -d
```

## 📊 Sample Data

The application includes sample data with:
- 3 test users (1 admin, 2 regular users)
- 15+ sample job applications
- Various application statuses and companies

## 🔧 Development

### Running Tests
```bash
# Backend tests
python manage.py test

# Frontend tests
npm test
```

### Code Quality
```bash
# Backend linting
flake8 backend/
black backend/

# Frontend linting
npm run lint
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For support and questions, please open an issue in the repository. 
