# Rural Opportunity Connect - Setup & Launch Guide

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Windows/Mac/Linux
- Python 3.8+ installed
- Git (optional)

### Step-by-Step Installation

**Step 1: Navigate to Project**
```bash
cd "d:\Design thinking\rural_opportunity_connect"
```

**Step 2: Activate Virtual Environment (Windows)**
```bash
# Using Python directly (bypasses execution policy issues)
.\venv\Scripts\python.exe -m pip list
```

**Step 3: Run Django Server**
```bash
.\venv\Scripts\python.exe manage.py runserver 8000
```

**Step 4: Start Flask API (New Terminal)**
```bash
cd recommendation_api
..\venv\Scripts\python.exe app.py
```

**Step 5: Visit the Application**
Open browser: `http://localhost:8000`

---

## 📋 Complete Directory Structure

```
d:\Design thinking\rural_opportunity_connect/
│
├── manage.py                          # Django management command
├── db.sqlite3                         # SQLite database (ready to use)
├── requirements.txt                   # Python dependencies
├── README.md                          # Project overview
├── TEMPLATE_GUIDE.md                  # Template development guide
├── SETUP_GUIDE.md                     # This file
│
├── config/                            # Django configuration
│   ├── __init__.py
│   ├── settings.py                    # Settings: apps, DB, auth, CORS, templates
│   ├── urls.py                        # Main URL router
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                          # User authentication & profiles
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py                       # Admin configuration for UserProfile
│   ├── apps.py
│   ├── models.py                      # UserProfile model (10 fields)
│   ├── views.py                       # Auth, dashboard, profile, saved items
│   ├── urls.py                        # Auth routes
│   └── tests.py
│
├── opportunities/                     # Jobs
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py                       # JobAdmin configuration
│   ├── apps.py
│   ├── models.py                      # Job, SavedOpportunity models
│   ├── views.py                       # job_list, job_detail views
│   ├── urls.py                        # Jobs routes
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── populate_data.py       # Seeds 10 demo jobs
│   └── tests.py
│
├── scholarships/                      # Scholarships
│   ├── migrations/
│   ├── admin.py
│   ├── models.py                      # Scholarship model (14 fields)
│   ├── views.py                       # scholarship_list, scholarship_detail
│   ├── urls.py
│   └── apps.py
│
├── government_schemes/                # Government Schemes
│   ├── migrations/
│   ├── admin.py
│   ├── models.py                      # GovernmentScheme (10 fields)
│   ├── views.py                       # scheme_list, scheme_detail
│   ├── urls.py
│   └── apps.py
│
├── skills/                            # Skill Development
│   ├── migrations/
│   ├── admin.py
│   ├── models.py                      # SkillProgram (11 fields)
│   ├── views.py                       # skill_list, skill_detail
│   ├── urls.py
│   └── apps.py
│
├── business/                          # Business Opportunities
│   ├── migrations/
│   ├── admin.py
│   ├── models.py                      # BusinessOpportunity (9 fields)
│   ├── views.py                       # business_list, business_detail
│   ├── urls.py
│   └── apps.py
│
├── applications/                      # Application tracking
│   ├── migrations/
│   ├── admin.py
│   ├── models.py                      # Application, DocumentChecklist
│   ├── views.py                       # apply_opportunity view
│   ├── urls.py
│   └── apps.py
│
├── templates/                         # All HTML templates
│   ├── base.html                      # Master template
│   ├── landing.html                   # Homepage
│   ├── login.html                     # Login form
│   ├── register.html                  # Registration form
│   ├── profile_setup.html             # Initial profile setup
│   ├── dashboard.html                 # User dashboard with recommendations
│   ├── jobs_list.html                 # Job listings with filters
│   ├── scholarships_list.html         # Scholarship listings
│   ├── schemes_list.html              # Government schemes
│   ├── skills_list.html               # Skill programs
│   ├── business_list.html             # Business opportunities
│   ├── about.html                     # About & Design Thinking
│   │
│   ├── [REMAINING - SEE TEMPLATE_GUIDE.md]
│   ├── job_detail.html                # [Create]
│   ├── scholarship_detail.html        # [Create]
│   ├── scheme_detail.html             # [Create]
│   ├── skill_detail.html              # [Create]
│   ├── business_detail.html           # [Create]
│   ├── profile.html                   # [Create]
│   ├── saved_opportunities.html       # [Create]
│   ├── application_tracker.html       # [Create]
│   └── document_checklist.html        # [Create]
│
├── static/                            # Static files (CSS, JS, images)
│   └── css/
│       └── style.css
│
├── recommendation_api/                # Flask Recommendation Engine
│   ├── __init__.py
│   ├── app.py                         # Flask app with /api/recommendations endpoint
│   ├── requirements.txt               # Flask dependencies
│   └── README.md
│
└── venv/                              # Python virtual environment
    ├── Scripts/
    ├── Lib/
    └── pyvenv.cfg
```

---

## 🗄️ Database Information

**Database:** SQLite (d:\Design thinking\rural_opportunity_connect\db.sqlite3)

**Pre-Loaded Data:**
- 10 Jobs
- 5 Scholarships
- 5 Government Schemes
- 8 Skill Programs
- 8 Business Opportunities
- **TOTAL: 36 Demo Records**

**Admin Credentials:**
- Username: `admin`
- Password: `admin123`

**Access Admin Panel:**
Visit `http://localhost:8000/admin/`

---

## 👤 User Registration & Testing

### Test User 1: Complete Profile
1. Go to http://localhost:8000/
2. Click "Get Started" → Register
3. Fill registration form:
   - First Name: Raj
   - Last Name: Kumar
   - Email: raj@example.com
   - Username: rajkumar
   - Password: TestPass123
4. Complete profile setup with all 9 fields
5. View personalized dashboard with recommendations

### Test User 2: Admin Account
1. Username: `admin`
2. Password: `admin123`
3. Access admin dashboard: http://localhost:8000/admin/

### Test User 3: Quick Test (No Registration)
Just browse landing page and job listings without logging in

---

## 🔌 API Endpoints

### Django Routes

| Method | URL | Purpose | Auth |
|--------|-----|---------|------|
| GET | `/` | Landing page | None |
| POST | `/register/` | User registration | None |
| POST | `/login/` | User login | None |
| GET | `/logout/` | User logout | Required |
| GET | `/dashboard/` | Dashboard with recommendations | Required |
| GET | `/jobs/` | Job listings | None |
| GET | `/jobs/<id>/` | Job details | None |
| GET | `/scholarships/` | Scholarship listings | None |
| GET | `/scholarships/<id>/` | Scholarship details | None |
| GET | `/schemes/` | Government schemes | None |
| GET | `/schemes/<id>/` | Scheme details | None |
| GET | `/skills/` | Skill listings | None |
| GET | `/skills/<id>/` | Skill details | None |
| GET | `/business/` | Business opportunities | None |
| GET | `/business/<id>/` | Business details | None |
| GET | `/profile/` | User profile | Required |
| GET | `/saved-opportunities/` | Saved items | Required |
| GET | `/applications/` | Application tracker | Required |
| GET | `/documents/` | Document checklist | Required |
| POST | `/save-opportunity/` | Save opportunity (AJAX) | Required |
| POST | `/applications/apply/` | Apply for opportunity (AJAX) | Required |

### Flask Recommendation API

**URL:** `http://localhost:5000/api/recommendations`

**Method:** GET

**Query Parameters:**
```
education=bachelor
skills=MS Office, Agriculture
location=Tamil Nadu
income=< 2 Lakhs
interests=Jobs, Education
```

**Response:**
```json
{
  "jobs": [
    {"id": 1, "title": "...", "organization": "..."},
    ...
  ],
  "scholarships": [...],
  "schemes": [...],
  "skills": [...],
  "business": [...]
}
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution:**
```bash
cd "d:\Design thinking\rural_opportunity_connect"
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Issue: "Port 8000 is already in use"
**Solution:**
```bash
# Use different port
.\venv\Scripts\python.exe manage.py runserver 8001
# Then visit http://localhost:8001
```

### Issue: "ExecutionPolicy" error on Windows
**Solution:** Use full Python path instead:
```bash
.\venv\Scripts\python.exe manage.py runserver
```

### Issue: Database appears empty
**Solution:** Populate demo data:
```bash
.\venv\Scripts\python.exe manage.py populate_data
```

### Issue: CSS not loading (styling looks broken)
**Solution:** This is normal in development. Tailwind CSS is loaded via CDN in templates.

### Issue: Flask API not connecting
**Solution:** Ensure Flask server is running in separate terminal:
```bash
cd recommendation_api
..\venv\Scripts\python.exe app.py
```

---

## 📊 Admin Panel Features

Access admin at `http://localhost:8000/admin/`

### Manage:
- ✅ User Profiles - View/edit user information
- ✅ Jobs - Create, edit, delete job listings
- ✅ Scholarships - Manage scholarship database
- ✅ Government Schemes - Manage scheme data
- ✅ Skill Programs - Add/remove courses
- ✅ Business Opportunities - Manage business ideas
- ✅ Applications - Track user applications
- ✅ Saved Opportunities - Monitor saved items
- ✅ Document Checklists - View document status

---

## 🎯 Feature Checklist

### ✅ Completed Features
- [x] User authentication (Login/Register)
- [x] User profiles with 9 fields
- [x] Profile completion tracking
- [x] Job search & filtering
- [x] Scholarship discovery
- [x] Government schemes browser
- [x] Skill programs listing
- [x] Business opportunities
- [x] Personalized recommendations (Flask API)
- [x] Save/favorite opportunities
- [x] Application tracking model
- [x] Document checklist model
- [x] Admin panel management
- [x] Responsive design (Tailwind CSS)
- [x] Landing page with hero section
- [x] About page with Design Thinking process

### 🔄 In Progress / Needed
- [ ] Job detail page
- [ ] Scholarship detail page
- [ ] Scheme detail page
- [ ] Skill detail page
- [ ] Business detail page
- [ ] Profile edit page
- [ ] Saved opportunities page
- [ ] Application tracker page
- [ ] Document checklist UI
- [ ] Apply functionality (backend complete)
- [ ] Email notifications
- [ ] SMS alerts

See TEMPLATE_GUIDE.md for creating remaining templates

---

## 🚀 Deployment

### Option 1: Heroku (Free Cloud Hosting)
1. Install Heroku CLI
2. Create Procfile: `web: gunicorn config.wsgi`
3. Add gunicorn: `pip install gunicorn`
4. Deploy: `heroku create && git push heroku main`

### Option 2: PythonAnywhere (Beginner-Friendly)
1. Upload code to pythonanywhere.com
2. Configure virtual env
3. Set WSGI configuration
4. Visit your pythonanywhere URL

### Option 3: AWS/DigitalOcean (Advanced)
Use docker and configure properly for production

**For any deployment:**
1. Set DEBUG = False in settings.py
2. Configure ALLOWED_HOSTS
3. Use PostgreSQL instead of SQLite
4. Set SECRET_KEY in environment variable
5. Enable HTTPS
6. Collect static files: `python manage.py collectstatic`

---

## 📚 Learning Resources

**Django Documentation:**
- https://docs.djangoproject.com/

**Tailwind CSS:**
- https://tailwindcss.com/docs

**Flask:**
- https://flask.palletsprojects.com/

**SQLite:**
- https://www.sqlite.org/docs.html

---

## 🔑 Important Files & Their Purpose

| File | Purpose |
|------|---------|
| `config/settings.py` | Database, apps, auth config |
| `config/urls.py` | Main URL routing |
| `accounts/views.py` | Authentication & recommendations logic |
| `recommendations_api/app.py` | Personalization engine |
| `templates/base.html` | Master template with styling |
| `db.sqlite3` | Database with all records |

---

## 💡 Tips for Success

1. **Always use `./venv/Scripts/python.exe`** on Windows to avoid execution policy issues
2. **Run Flask API in separate terminal** for recommendations to work
3. **Check admin panel** to verify data is loaded
4. **Use browser DevTools** to debug CSS/JavaScript issues
5. **Review Django logs** in terminal for backend errors
6. **Test with multiple users** to verify user isolation

---

## 📞 Support

**Still having issues?**
1. Check terminal output for error messages
2. Verify all files from README exist
3. Ensure Python 3.8+ is installed
4. Try recreating virtual environment
5. Check TEMPLATE_GUIDE.md for template-specific issues

---

**Ready to launch?** 🚀

```bash
# Terminal 1: Django Server
cd "d:\Design thinking\rural_opportunity_connect"
.\venv\Scripts\python.exe manage.py runserver

# Terminal 2: Flask API
cd "d:\Design thinking\rural_opportunity_connect\recommendation_api"
..\..\venv\Scripts\python.exe app.py

# Then open: http://localhost:8000
```

---

**Happy building! 🌱**

This prototype demonstrates:
✨ Full-stack web development
✨ Design Thinking methodology
✨ Professional UI/UX with Tailwind CSS
✨ Real-world problem solving
✨ SDG-aligned impact design
