# 🚀 Expense Tracker - Complete Setup Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Detailed Setup](#detailed-setup)
4. [Running the Application](#running-the-application)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **MySQL 8.0+** - [Download](https://dev.mysql.com/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **Docker** (Optional) - [Download](https://www.docker.com/products/docker-desktop)

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, or Ubuntu 20.04+
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB free space

---

## Quick Start

### Using Docker (Easiest Method)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker

# 2. Start the application
docker-compose up -d

# 3. Access the application
# Open browser: http://localhost:5000

# 4. Stop the application
docker-compose down
```

That's it! The application is running with MySQL database.

---

## Detailed Setup

### Step 1: Install MySQL

#### On Windows:
1. Download MySQL Installer from official website
2. Run installer and select "Developer Default"
3. Set root password (remember this!)
4. Complete installation

#### On macOS:
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

#### On Ubuntu:
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

### Step 2: Configure MySQL

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE expense_tracker;

# Create user (optional but recommended)
CREATE USER 'expenseuser'@'localhost' IDENTIFIED BY 'expensepass';
GRANT ALL PRIVILEGES ON expense_tracker.* TO 'expenseuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 3: Clone and Setup Project

```bash
# Clone repository
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
# On Windows: notepad .env
# On macOS/Linux: nano .env
```

**Edit .env file:**
```env
MYSQL_HOST=localhost
MYSQL_USER=expenseuser
MYSQL_PASSWORD=expensepass
MYSQL_DB=expense_tracker

FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-here

PORT=5000
```

### Step 5: Initialize Database

```bash
# Run database initialization script
python database.py

# You should see:
# "Database initialized successfully!"
# "Database connection test successful!"
```

---

## Running the Application

### Method 1: Development Mode (Local)

```bash
# Make sure virtual environment is activated
python app.py

# Output:
# * Running on http://0.0.0.0:5000
# * Debug mode: on
```

Open browser: `http://localhost:5000`

### Method 2: Production Mode (Gunicorn)

```bash
gunicorn --bind 0.0.0.0:5000 --workers 2 app:app
```

### Method 3: Docker (Recommended)

```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

---

## Testing

### Manual Testing Checklist

✅ **Homepage**
- [ ] Can view expenses list
- [ ] Statistics display correctly
- [ ] Empty state shows when no expenses

✅ **Add Expense**
- [ ] Can add new expense
- [ ] Form validation works
- [ ] Success message appears
- [ ] Redirects to homepage

✅ **Edit Expense**
- [ ] Can edit existing expense
- [ ] Form pre-fills with existing data
- [ ] Updates save correctly

✅ **Delete Expense**
- [ ] Confirmation dialog appears
- [ ] Expense deletes successfully

✅ **Analytics**
- [ ] Category breakdown displays
- [ ] Monthly trends show
- [ ] Statistics calculate correctly

### Automated Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=. tests/

# Run specific test file
pytest tests/test_models.py -v
```

---

## Deployment

### Deploy to AWS EC2

#### Step 1: Launch EC2 Instance
1. Choose Ubuntu 22.04 AMI
2. Instance type: t2.micro (free tier)
3. Configure security group:
   - SSH (22): Your IP
   - HTTP (80): 0.0.0.0/0
   - HTTPS (443): 0.0.0.0/0
   - Custom (5000): 0.0.0.0/0

#### Step 2: Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv git mysql-server docker.io docker-compose

# Clone repository
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker

# Setup MySQL
sudo mysql
CREATE DATABASE expense_tracker;
CREATE USER 'expenseuser'@'localhost' IDENTIFIED BY 'strongpassword';
GRANT ALL PRIVILEGES ON expense_tracker.* TO 'expenseuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Configure environment
cp .env.example .env
nano .env  # Update with production values

# Run with Docker
sudo docker-compose up -d
```

#### Step 3: Configure Nginx (Optional)

```bash
# Install Nginx
sudo apt install nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/expense-tracker

# Add configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/expense-tracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Deploy to Azure

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login

# Create resource group
az group create --name expense-tracker-rg --location eastus

# Create App Service plan
az appservice plan create --name expense-tracker-plan --resource-group expense-tracker-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group expense-tracker-rg --plan expense-tracker-plan --name your-app-name --runtime "PYTHON:3.9"

# Deploy
az webapp deployment source config --name your-app-name --resource-group expense-tracker-rg --repo-url https://github.com/yourusername/expense-tracker --branch main --manual-integration
```

### Deploy to Heroku

```bash
# Install Heroku CLI
# Visit: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create expense-tracker-yourname

# Add MySQL addon
heroku addons:create jawsdb:kitefin

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Open app
heroku open
```

---

## Troubleshooting

### Common Issues

#### Issue: MySQL Connection Error

**Symptoms:**
```
Error connecting to MySQL: Can't connect to MySQL server
```

**Solutions:**
1. Check MySQL is running:
   ```bash
   # Windows
   services.msc  # Find MySQL service
   
   # macOS
   brew services list
   
   # Linux
   sudo systemctl status mysql
   ```

2. Verify credentials in `.env` file
3. Check MySQL port (default: 3306)

#### Issue: Port Already in Use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**
1. Change port in `.env`:
   ```env
   PORT=8000
   ```

2. Or kill process using port 5000:
   ```bash
   # On macOS/Linux
   lsof -ti:5000 | xargs kill -9
   
   # On Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

#### Issue: Module Not Found

**Symptoms:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solutions:**
1. Activate virtual environment:
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Issue: Database Tables Not Created

**Symptoms:**
```
Table 'expense_tracker.expenses' doesn't exist
```

**Solutions:**
1. Run database initialization:
   ```bash
   python database.py
   ```

2. Verify database exists:
   ```bash
   mysql -u root -p
   SHOW DATABASES;
   USE expense_tracker;
   SHOW TABLES;
   ```

#### Issue: Docker Container Won't Start

**Symptoms:**
```
Container keeps restarting
```

**Solutions:**
1. Check logs:
   ```bash
   docker-compose logs web
   docker-compose logs db
   ```

2. Rebuild containers:
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```

3. Remove volumes and restart:
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

### Getting Help

If you encounter issues:

1. **Check logs**: Look for error messages in console output
2. **Search issues**: GitHub repository issues section
3. **Ask for help**: Create new issue with:
   - Error message
   - Steps to reproduce
   - Your environment (OS, Python version, etc.)

---

## Performance Tips

### Database Optimization
```sql
-- Add indexes for better query performance
CREATE INDEX idx_date ON expenses(date);
CREATE INDEX idx_category ON expenses(category);
```

### Application Optimization
- Use Gunicorn with multiple workers in production
- Enable database connection pooling
- Implement caching for analytics data
- Compress static files

### Docker Optimization
- Use multi-stage builds
- Minimize image size
- Use volume mounts for development

---

## Next Steps

Now that you have the application running:

1. ✅ **Customize**: Modify categories, colors, and branding
2. ✅ **Add Data**: Input your expenses
3. ✅ **Explore Analytics**: View spending patterns
4. ✅ **Extend Features**: Add authentication, budgets, etc.
5. ✅ **Deploy**: Put it on the cloud for remote access

---

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Docker Documentation](https://docs.docker.com/)
- [Python Documentation](https://docs.python.org/3/)

---

**Happy Expense Tracking! 💰**
