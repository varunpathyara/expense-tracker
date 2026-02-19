"""
Main Flask application for Expense Tracker
Handles all routes and web interface
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import config
from database_sqlite import init_database, test_connection
from models import Expense
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from auth_models import User
from database_auth import init_auth_database

# Create Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

# Predefined expense categories
CATEGORIES = [
    'Food & Dining',
    'Transportation',
    'Shopping',
    'Entertainment',
    'Healthcare',
    'Utilities',
    'Rent',
    'Education',
    'Travel',
    'Other'
]

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.get_by_email(email)
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))
        
        if User.get_by_email(email):
            flash('Email already registered', 'error')
            return redirect(url_for('signup'))
        
        user = User.create_user(username, email, password)
        
        if user:
            login_user(user)
            flash(f'Account created successfully! Welcome, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Error creating account. Please try again.', 'error')
            return redirect(url_for('signup'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Home page - displays all expenses"""
    try:
        expenses = Expense.get_all(user_id=current_user.id)
        total_expenses = len(expenses)
        total_amount = sum(float(exp['amount']) for exp in expenses)
        
        return render_template('index.html', 
                             expenses=expenses,
                             total_expenses=total_expenses,
                             total_amount=total_amount,
                             categories=CATEGORIES)
    except Exception as e:
        flash(f'Error loading expenses: {str(e)}', 'error')
        return render_template('index.html', 
                             expenses=[],
                             total_expenses=0,
                             total_amount=0,
                             categories=CATEGORIES)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Add new expense"""
    if request.method == 'POST':
        try:
            amount = request.form.get('amount')
            category = request.form.get('category')
            date = request.form.get('date')
            description = request.form.get('description', '')
            
            if not all([amount, category, date]):
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('add_expense'))
            
            expense = Expense(amount, category, date, description)
            expense.save()
            
            flash('Expense added successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error adding expense: {str(e)}', 'error')
            return redirect(url_for('add_expense'))
    
    return render_template('add_expense.html', categories=CATEGORIES)

@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    """Edit existing expense"""
    if request.method == 'POST':
        try:
            amount = request.form.get('amount')
            category = request.form.get('category')
            date = request.form.get('date')
            description = request.form.get('description', '')
            
            if not all([amount, category, date]):
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('edit_expense', expense_id=expense_id))
            
            expense = Expense(amount, category, date, description, expense_id)
            expense.save()
            
            flash('Expense updated successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error updating expense: {str(e)}', 'error')
            return redirect(url_for('edit_expense', expense_id=expense_id))
    
    expense = Expense.get_by_id(expense_id)
    
    if not expense:
        flash('Expense not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('edit_expense.html', expense=expense, categories=CATEGORIES)

@app.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete expense"""
    try:
        if Expense.delete(expense_id):
            flash('Expense deleted successfully!', 'success')
        else:
            flash('Expense not found', 'error')
    except Exception as e:
        flash(f'Error deleting expense: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/analytics')
@login_required
def analytics():
    """Analytics page - displays spending analysis and charts"""
    try:
        expenses = Expense.get_all(user_id=current_user.id)
        analytics_data = calculate_analytics(expenses)
        
        return render_template('analytics.html', 
                             analytics=analytics_data,
                             expenses=expenses)
    except Exception as e:
        flash(f'Error loading analytics: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/expenses')
@login_required
def api_expenses():
    """API endpoint to get expenses as JSON"""
    try:
        expenses = Expense.get_all(user_id=current_user.id)
        return jsonify(expenses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics')
@login_required
def api_analytics():
    """API endpoint to get analytics data as JSON"""
    try:
        expenses = Expense.get_all(user_id=current_user.id)
        analytics_data = calculate_analytics(expenses)
        return jsonify(analytics_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_analytics(expenses):
    """Calculate analytics from expenses data"""
    if not expenses:
        return {
            'total_spending': 0,
            'expense_count': 0,
            'category_totals': {},
            'monthly_totals': {},
            'average_expense': 0
        }
    
    total_spending = sum(float(exp['amount']) for exp in expenses)
    expense_count = len(expenses)
    average_expense = total_spending / expense_count if expense_count > 0 else 0
    
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        amount = float(expense['amount'])
        category_totals[category] = category_totals.get(category, 0) + amount
    
    monthly_totals = {}
    for expense in expenses:
        date_str = expense['date']
        month = date_str[:7]
        amount = float(expense['amount'])
        monthly_totals[month] = monthly_totals.get(month, 0) + amount
    
    return {
        'total_spending': round(total_spending, 2),
        'expense_count': expense_count,
        'category_totals': {k: round(v, 2) for k, v in category_totals.items()},
        'monthly_totals': {k: round(v, 2) for k, v in sorted(monthly_totals.items())},
        'average_expense': round(average_expense, 2)
    }

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        if test_connection():
            return jsonify({'status': 'healthy', 'database': 'connected'}), 200
        else:
            return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 503
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🚀 Starting Expense Tracker...")
    
    # Initialize database
    with app.app_context():
        try:
            init_auth_database()
            print("✅ Database initialized successfully!")
        except Exception as e:
            print(f"❌ Database init error: {e}")
    
    # Start server
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Server running on http://localhost:{port}")
    print("📝 Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=port, debug=True)