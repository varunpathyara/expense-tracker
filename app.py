"""
Main Flask application for Expense Tracker
Handles all routes and web interface
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import config
from database_sqlite import init_database, test_connection
from models import Expense
import os

# Create Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

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

@app.route('/')
def index():
    """Home page - displays all expenses"""
    try:
        expenses = Expense.get_all()
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
def add_expense():
    """Add new expense"""
    if request.method == 'POST':
        try:
            # Get form data
            amount = request.form.get('amount')
            category = request.form.get('category')
            date = request.form.get('date')
            description = request.form.get('description', '')
            
            # Validate data
            if not all([amount, category, date]):
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('add_expense'))
            
            # Create and save expense
            expense = Expense(amount, category, date, description)
            expense.save()
            
            flash('Expense added successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error adding expense: {str(e)}', 'error')
            return redirect(url_for('add_expense'))
    
    return render_template('add_expense.html', categories=CATEGORIES)

@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    """Edit existing expense"""
    if request.method == 'POST':
        try:
            # Get form data
            amount = request.form.get('amount')
            category = request.form.get('category')
            date = request.form.get('date')
            description = request.form.get('description', '')
            
            # Validate data
            if not all([amount, category, date]):
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('edit_expense', expense_id=expense_id))
            
            # Update expense
            expense = Expense(amount, category, date, description, expense_id)
            expense.save()
            
            flash('Expense updated successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error updating expense: {str(e)}', 'error')
            return redirect(url_for('edit_expense', expense_id=expense_id))
    
    # GET request - show edit form
    expense = Expense.get_by_id(expense_id)
    
    if not expense:
        flash('Expense not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('edit_expense.html', expense=expense, categories=CATEGORIES)

@app.route('/delete/<int:expense_id>', methods=['POST'])
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
def analytics():
    """Analytics page - displays spending analysis and charts"""
    try:
        expenses = Expense.get_all()
        
        # Calculate analytics data
        analytics_data = calculate_analytics(expenses)
        
        return render_template('analytics.html', 
                             analytics=analytics_data,
                             expenses=expenses)
    except Exception as e:
        flash(f'Error loading analytics: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/expenses')
def api_expenses():
    """API endpoint to get expenses as JSON"""
    try:
        expenses = Expense.get_all()
        return jsonify(expenses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics')
def api_analytics():
    """API endpoint to get analytics data as JSON"""
    try:
        expenses = Expense.get_all()
        analytics_data = calculate_analytics(expenses)
        return jsonify(analytics_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_analytics(expenses):
    """
    Calculate analytics from expenses data
    
    Args:
        expenses (list): List of expense dictionaries
        
    Returns:
        dict: Analytics data
    """
    if not expenses:
        return {
            'total_spending': 0,
            'expense_count': 0,
            'category_totals': {},
            'monthly_totals': {},
            'average_expense': 0
        }
    
    # Total spending
    total_spending = sum(float(exp['amount']) for exp in expenses)
    expense_count = len(expenses)
    average_expense = total_spending / expense_count if expense_count > 0 else 0
    
    # Category-wise totals
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        amount = float(expense['amount'])
        category_totals[category] = category_totals.get(category, 0) + amount
    
    # Monthly totals (simplified - just using month from date)
    monthly_totals = {}
    for expense in expenses:
        date_str = expense['date']
        month = date_str[:7]  # Get YYYY-MM
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
        # Test database connection
        if test_connection():
            return jsonify({
                'status': 'healthy',
                'database': 'connected'
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected'
            }), 503
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    # Initialize database on first run
    try:
        print("Checking database connection...")
        init_database()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")
        print("Make sure MySQL is running and credentials are correct in .env file")
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
