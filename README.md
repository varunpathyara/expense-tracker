# 💰 Expense Tracker - Full Stack Web Application

A modern, cloud-ready expense tracking application built with Flask, MySQL, Docker, and CI/CD pipeline. Track your expenses, analyze spending patterns, and gain financial insights.

## 🚀 Features

- **Expense Management**: Add, edit, delete, and view expenses
- **Category Organization**: Organize expenses into predefined categories
- **Analytics Dashboard**: Visual spending analysis with charts and graphs
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **RESTful API**: JSON endpoints for programmatic access
- **Containerized**: Fully dockerized for easy deployment
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions
- **Cloud-Ready**: Designed for deployment on AWS, Azure, or GCP

## 🛠️ Tech Stack

### Backend
- **Python 3.9+**
- **Flask** - Web framework
- **MySQL** - Database
- **Gunicorn** - WSGI server

### Frontend
- **HTML5/CSS3**
- **JavaScript (Vanilla)**
- **Responsive Design**

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD pipeline
- **Gunicorn** - Production server

### Libraries & Tools
- **Pandas** - Data analysis
- **Matplotlib/Plotly** - Visualization
- **Git** - Version control

## 📋 Prerequisites

- Python 3.9 or higher
- MySQL 8.0 or higher
- Docker & Docker Compose (optional)
- Git

## 🔧 Installation

### Option 1: Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your MySQL credentials
```

5. **Initialize database**
```bash
python database.py
```

6. **Run the application**
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

### Option 2: Docker Setup (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```

2. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

The application will be available at `http://localhost:5000`

To stop the application:
```bash
docker-compose down
```

## 📁 Project Structure

```
expense-tracker/
├── app.py                  # Main Flask application
├── config.py              # Configuration settings
├── database.py            # Database setup and connection
├── models.py              # Data models and business logic
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── .dockerignore        # Docker ignore rules
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── add_expense.html
│   ├── edit_expense.html
│   ├── analytics.html
│   ├── 404.html
│   └── 500.html
├── static/              # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── .github/
│   └── workflows/
│       └── deploy.yml   # CI/CD pipeline
└── tests/               # Test files
```

## 🎯 Usage

### Adding Expenses
1. Click "Add New Expense" button
2. Fill in amount, category, date, and description
3. Click "Save Expense"

### Viewing Analytics
1. Navigate to "Analytics" page
2. View total spending, category breakdown, and monthly trends
3. Analyze spending patterns with visual charts

### API Endpoints

- `GET /api/expenses` - Get all expenses as JSON
- `GET /api/analytics` - Get analytics data as JSON
- `GET /health` - Health check endpoint

Example API usage:
```bash
curl http://localhost:5000/api/expenses
```

## 🚢 Deployment

### Cloud Deployment Options

#### AWS (EC2 + RDS)
1. Create EC2 instance (Ubuntu 22.04)
2. Create RDS MySQL instance
3. SSH into EC2 and clone repository
4. Set up environment variables
5. Run with Docker Compose or Gunicorn

#### Azure (App Service + MySQL)
1. Create Azure App Service (Python)
2. Create Azure Database for MySQL
3. Deploy using Git or Docker
4. Configure connection strings

#### Google Cloud (Cloud Run + Cloud SQL)
1. Build Docker image
2. Push to Google Container Registry
3. Deploy to Cloud Run
4. Connect to Cloud SQL

### CI/CD Pipeline

The project includes a GitHub Actions workflow that:
- Runs tests on every push
- Builds Docker image
- Deploys to production (when configured)

To enable deployment:
1. Add cloud provider credentials to GitHub Secrets
2. Uncomment deployment steps in `.github/workflows/deploy.yml`
3. Push to main branch

## 🧪 Testing

Run tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest --cov=. tests/
```

## 🔒 Security

- Never commit `.env` file
- Use strong passwords for production
- Enable HTTPS in production
- Keep dependencies updated
- Use environment variables for sensitive data

## 📊 Database Schema

```sql
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_date (date),
    INDEX idx_category (category)
);
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Varun Kumar Pathyara**
- Email: varunpathyara@gmail.com
- LinkedIn: [Your LinkedIn Profile]
- GitHub: [Your GitHub Profile]

## 🙏 Acknowledgments

- Flask documentation
- MySQL documentation
- Docker documentation
- GitHub Actions documentation

## 📞 Support

For support, email varunpathyara@gmail.com or create an issue in the repository.

## 🗺️ Roadmap

- [ ] Phase 1: Core Application ✅
- [ ] Phase 2: Advanced Analytics & Charts
- [ ] Phase 3: User Authentication
- [ ] Phase 4: Budget Planning
- [ ] Phase 5: Mobile App (React Native)
- [ ] Phase 6: AI-powered Insights

---

**Built with ❤️ using Flask, MySQL, and Docker**
