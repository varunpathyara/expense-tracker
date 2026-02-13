# 🚀 Expense Tracker - Quick Reference Guide

## Essential Commands

### Local Development

```bash
# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings

# Initialize Database
python database.py

# Run Application
python app.py

# Access
http://localhost:5000
```

### Docker Commands

```bash
# Start Application
docker-compose up -d

# View Logs
docker-compose logs -f
docker-compose logs web
docker-compose logs db

# Stop Application
docker-compose down

# Rebuild After Changes
docker-compose up -d --build

# Remove Everything (including data)
docker-compose down -v

# Execute Commands in Container
docker-compose exec web python database.py
docker-compose exec db mysql -u root -p

# Check Container Status
docker-compose ps
```

### Git Commands

```bash
# Initial Setup
git init
git add .
git commit -m "Initial commit: Expense Tracker v1.0"

# Create GitHub Repo
# Go to github.com, create new repository
git remote add origin https://github.com/yourusername/expense-tracker.git
git branch -M main
git push -u origin main

# Regular Workflow
git add .
git commit -m "Add: description of changes"
git push

# View Changes
git status
git diff
git log --oneline
```

### MySQL Commands

```bash
# Login
mysql -u root -p

# Database Operations
SHOW DATABASES;
USE expense_tracker;
SHOW TABLES;
DESCRIBE expenses;

# Query Data
SELECT * FROM expenses;
SELECT * FROM expenses WHERE category = 'Food & Dining';
SELECT category, SUM(amount) FROM expenses GROUP BY category;

# Backup
mysqldump -u root -p expense_tracker > backup.sql

# Restore
mysql -u root -p expense_tracker < backup.sql
```

### Testing

```bash
# Run All Tests
pytest tests/ -v

# Run Specific Test
pytest tests/test_models.py -v

# With Coverage
pytest --cov=. tests/

# Generate HTML Coverage Report
pytest --cov=. --cov-report=html tests/
```

### Deployment

```bash
# AWS EC2
ssh -i key.pem ubuntu@ec2-ip
git clone repo-url
cd expense-tracker
docker-compose up -d

# Heroku
heroku login
heroku create app-name
git push heroku main
heroku open

# Azure
az login
az webapp up --name app-name --resource-group rg-name
```

---

## File Locations

```
Project Files:        /mnt/user-data/outputs/expense-tracker/
Configuration:        .env
Main App:            app.py
Database:            database.py
Models:              models.py
Templates:           templates/
Static Files:        static/
Docker Config:       Dockerfile, docker-compose.yml
CI/CD:               .github/workflows/deploy.yml
```

---

## Common URLs

```
Application:         http://localhost:5000
Add Expense:         http://localhost:5000/add
Analytics:           http://localhost:5000/analytics
API (Expenses):      http://localhost:5000/api/expenses
API (Analytics):     http://localhost:5000/api/analytics
Health Check:        http://localhost:5000/health
```

---

## Environment Variables

```env
# Database
MYSQL_HOST=localhost
MYSQL_USER=expenseuser
MYSQL_PASSWORD=your_password
MYSQL_DB=expense_tracker

# Flask
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key

# App
PORT=5000
```

---

## Troubleshooting Quick Fixes

```bash
# Port Already in Use
# Linux/Mac:
lsof -ti:5000 | xargs kill -9
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Permission Denied (Docker)
sudo usermod -aG docker $USER
newgrp docker

# Module Not Found
pip install -r requirements.txt

# Database Connection Failed
# Check MySQL is running:
sudo systemctl status mysql  # Linux
brew services list           # Mac
services.msc                 # Windows

# Docker Container Won't Start
docker-compose down -v
docker-compose up -d --build

# Clear Python Cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

---

## Database Schema

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

---

## API Examples

```bash
# Get All Expenses
curl http://localhost:5000/api/expenses

# Get Analytics
curl http://localhost:5000/api/analytics

# Health Check
curl http://localhost:5000/health

# Add Expense (via form)
curl -X POST http://localhost:5000/add \
  -d "amount=100&category=Food&date=2025-02-13&description=Lunch"
```

---

## Useful Python Commands

```python
# Database Check
python -c "from database import test_connection; test_connection()"

# Create Sample Data
python -c "
from models import Expense
from datetime import datetime
e = Expense(100.50, 'Food & Dining', datetime.now().strftime('%Y-%m-%d'), 'Lunch')
e.save()
print('Sample expense created!')
"

# Get All Expenses
python -c "
from models import Expense
expenses = Expense.get_all()
print(f'Total expenses: {len(expenses)}')
"
```

---

## Project Statistics

```bash
# Count Lines of Code
find . -name "*.py" | xargs wc -l

# Count Files
find . -type f | wc -l

# Project Size
du -sh .

# Git Stats
git log --oneline | wc -l  # Number of commits
git log --shortstat | grep "files changed" | wc -l
```

---

## Performance Monitoring

```bash
# Check Application Response Time
time curl http://localhost:5000

# Monitor Docker Resources
docker stats

# Check MySQL Performance
mysql -u root -p -e "SHOW PROCESSLIST;"
mysql -u root -p -e "SHOW STATUS LIKE 'Threads_connected';"

# Application Logs
tail -f logs/app.log  # If you add logging
docker-compose logs -f web
```

---

## Security Checklist

```bash
✅ Environment variables used (not hardcoded)
✅ .env file in .gitignore
✅ SQL injection prevention (parameterized queries)
✅ CSRF protection enabled
✅ Strong secret key in production
✅ HTTPS enabled (for production)
✅ Regular dependency updates
✅ Database backups configured
✅ Error handling without info leakage
✅ Input validation on forms
```

---

## Next Steps After Setup

1. ✅ Test all CRUD operations
2. ✅ Add sample data
3. ✅ Check analytics page
4. ✅ Test Docker deployment
5. ✅ Push to GitHub
6. ✅ Set up CI/CD
7. ✅ Deploy to cloud
8. ✅ Share with recruiters

---

## Resources

- **Flask Docs**: https://flask.palletsprojects.com/
- **MySQL Docs**: https://dev.mysql.com/doc/
- **Docker Docs**: https://docs.docker.com/
- **GitHub Actions**: https://docs.github.com/actions

---

**Keep this file handy for quick reference! 📌**
