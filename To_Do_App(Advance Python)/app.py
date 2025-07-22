from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)  #object creation for app running

app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get current user information
    current_user = User.query.get(session['user_id'])
    todos = Todo.query.filter_by(user_id=session['user_id']).all()
    return render_template('todo.html', todos=todos, current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
        
        new_user = User(username=username, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/add', methods=['POST'])
def add_todo():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    task = request.form['task'].strip()  # Remove leading/trailing whitespace
    
    # Check if task is empty
    if not task:
        flash('Task cannot be empty!', 'error')
        return redirect(url_for('index'))
    
    # Check for duplicate tasks (case-insensitive)
    existing_task = Todo.query.filter_by(user_id=session['user_id']).filter(
        db.func.lower(Todo.task) == task.lower()
    ).first()
    
    if existing_task:
        flash('Already exists!', 'error')
        return redirect(url_for('index'))
    
    # Create new task if no duplicate found
    new_todo = Todo(task=task, user_id=session['user_id'])
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != session['user_id']:
        return redirect(url_for('index'))
    
    new_task = request.form['task'].strip()  # Remove leading/trailing whitespace
    
    # Check if task is empty
    if not new_task:
        flash('Task cannot be empty!', 'error')
        return redirect(url_for('index'))
    
    # Check for duplicate tasks (excluding current task)
    existing_task = Todo.query.filter_by(user_id=session['user_id']).filter(
        db.func.lower(Todo.task) == new_task.lower(),
        Todo.id != todo_id
    ).first()
    
    if existing_task:
        flash('Already exists!', 'error')
        return redirect(url_for('index'))
    
    # Update task if no duplicate found
    todo.task = new_task
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id == session['user_id']:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id == session['user_id']:
        todo.completed = not todo.completed
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/clear_all_completed')
def clear_all_completed():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Delete all completed todos for the current user
    completed_todos = Todo.query.filter_by(user_id=session['user_id'], completed=True).all()
    for todo in completed_todos:
        db.session.delete(todo)
    
    db.session.commit()
    flash(f'Cleared {len(completed_todos)} completed tasks!')
    return redirect(url_for('index'))

@app.route('/remove_duplicates')
def remove_duplicates():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Find and remove duplicate tasks for the current user
    user_todos = Todo.query.filter_by(user_id=session['user_id']).order_by(Todo.id).all()
    seen_tasks = {}
    duplicates_removed = 0
    
    for todo in user_todos:
        task_lower = todo.task.lower().strip()
        
        if task_lower in seen_tasks:
            # This is a duplicate, remove it
            db.session.delete(todo)
            duplicates_removed += 1
        else:
            seen_tasks[task_lower] = todo
    
    db.session.commit()
    
    if duplicates_removed > 0:
        flash(f'Removed {duplicates_removed} duplicate tasks!')
    else:
        flash('No duplicate tasks found!')
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)