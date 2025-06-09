"""
Authentication routes for user sign-in, sign-up, and session management.
"""
from flask import Blueprint, request, jsonify, session
from datetime import datetime, timedelta
import hashlib
import secrets
import json
import os

auth_bp = Blueprint('auth', __name__)

# Simple in-memory user storage (in production, use a proper database)
USERS_FILE = 'users.json'

def load_users():
    """Load users from JSON file."""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    """Save users to JSON file."""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except:
        return False

def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_token():
    """Generate a secure session token."""
    return secrets.token_urlsafe(32)

def validate_email(email):
    """Basic email validation."""
    return '@' in email and '.' in email.split('@')[1]

def validate_password(password):
    """Basic password validation."""
    return len(password) >= 8

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """User registration endpoint."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'firstName', 'lastName', 'company']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'{field} is required'
                }), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        confirm_password = data.get('confirmPassword', '')
        first_name = data['firstName'].strip()
        last_name = data['lastName'].strip()
        company = data['company'].strip()
        
        # Validate email format
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400
        
        # Validate password strength
        if not validate_password(password):
            return jsonify({
                'success': False,
                'message': 'Password must be at least 8 characters long'
            }), 400
        
        # Check password confirmation
        if confirm_password and password != confirm_password:
            return jsonify({
                'success': False,
                'message': 'Passwords do not match'
            }), 400
        
        # Load existing users
        users = load_users()
        
        # Check if user already exists
        if email in users:
            return jsonify({
                'success': False,
                'message': 'User with this email already exists'
            }), 409
        
        # Create new user
        user_data = {
            'email': email,
            'password_hash': hash_password(password),
            'first_name': first_name,
            'last_name': last_name,
            'company': company,
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'is_active': True
        }
        
        users[email] = user_data
        
        # Save users
        if not save_users(users):
            return jsonify({
                'success': False,
                'message': 'Failed to save user data'
            }), 500
        
        # Generate session token
        session_token = generate_session_token()
        session['user_email'] = email
        session['session_token'] = session_token
        
        # Return user data (without password hash)
        user_response = {
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'company': company,
            'createdAt': user_data['created_at']
        }
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'user': user_response,
            'session_token': session_token
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500

@auth_bp.route('/signin', methods=['POST'])
def signin():
    """User login endpoint."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Load users
        users = load_users()
        
        # Check if user exists
        if email not in users:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        user = users[email]
        
        # Check if account is active
        if not user.get('is_active', True):
            return jsonify({
                'success': False,
                'message': 'Account is deactivated'
            }), 401
        
        # Verify password
        if user['password_hash'] != hash_password(password):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Update last login
        user['last_login'] = datetime.now().isoformat()
        users[email] = user
        save_users(users)
        
        # Generate session token
        session_token = generate_session_token()
        session['user_email'] = email
        session['session_token'] = session_token
        
        # Return user data (without password hash)
        user_response = {
            'email': email,
            'firstName': user['first_name'],
            'lastName': user['last_name'],
            'company': user['company'],
            'lastLogin': user['last_login']
        }
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user_response,
            'session_token': session_token
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login failed: {str(e)}'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """User logout endpoint."""
    try:
        # Clear session
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Logout failed: {str(e)}'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get current user profile."""
    try:
        # Check if user is logged in
        user_email = session.get('user_email')
        if not user_email:
            return jsonify({
                'success': False,
                'message': 'Not authenticated'
            }), 401
        
        # Load users
        users = load_users()
        
        # Check if user still exists
        if user_email not in users:
            session.clear()
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        user = users[user_email]
        
        # Return user data (without password hash)
        user_response = {
            'email': user_email,
            'firstName': user['first_name'],
            'lastName': user['last_name'],
            'company': user['company'],
            'createdAt': user['created_at'],
            'lastLogin': user.get('last_login')
        }
        
        return jsonify({
            'success': True,
            'user': user_response
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get profile: {str(e)}'
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
def update_profile():
    """Update user profile."""
    try:
        # Check if user is logged in
        user_email = session.get('user_email')
        if not user_email:
            return jsonify({
                'success': False,
                'message': 'Not authenticated'
            }), 401
        
        data = request.get_json()
        
        # Load users
        users = load_users()
        
        # Check if user still exists
        if user_email not in users:
            session.clear()
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        user = users[user_email]
        
        # Update allowed fields
        if data.get('firstName'):
            user['first_name'] = data['firstName'].strip()
        if data.get('lastName'):
            user['last_name'] = data['lastName'].strip()
        if data.get('company'):
            user['company'] = data['company'].strip()
        
        # Save updated user data
        users[user_email] = user
        if not save_users(users):
            return jsonify({
                'success': False,
                'message': 'Failed to save user data'
            }), 500
        
        # Return updated user data
        user_response = {
            'email': user_email,
            'firstName': user['first_name'],
            'lastName': user['last_name'],
            'company': user['company'],
            'createdAt': user['created_at'],
            'lastLogin': user.get('last_login')
        }
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': user_response
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to update profile: {str(e)}'
        }), 500

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    """Change user password."""
    try:
        # Check if user is logged in
        user_email = session.get('user_email')
        if not user_email:
            return jsonify({
                'success': False,
                'message': 'Not authenticated'
            }), 401
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('currentPassword') or not data.get('newPassword'):
            return jsonify({
                'success': False,
                'message': 'Current password and new password are required'
            }), 400
        
        current_password = data['currentPassword']
        new_password = data['newPassword']
        confirm_password = data.get('confirmPassword', '')
        
        # Validate new password strength
        if not validate_password(new_password):
            return jsonify({
                'success': False,
                'message': 'New password must be at least 8 characters long'
            }), 400
        
        # Check password confirmation
        if confirm_password and new_password != confirm_password:
            return jsonify({
                'success': False,
                'message': 'New passwords do not match'
            }), 400
        
        # Load users
        users = load_users()
        
        # Check if user still exists
        if user_email not in users:
            session.clear()
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        user = users[user_email]
        
        # Verify current password
        if user['password_hash'] != hash_password(current_password):
            return jsonify({
                'success': False,
                'message': 'Current password is incorrect'
            }), 401
        
        # Update password
        user['password_hash'] = hash_password(new_password)
        user['password_changed_at'] = datetime.now().isoformat()
        
        # Save updated user data
        users[user_email] = user
        if not save_users(users):
            return jsonify({
                'success': False,
                'message': 'Failed to save user data'
            }), 500
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to change password: {str(e)}'
        }), 500

@auth_bp.route('/verify-session', methods=['GET'])
def verify_session():
    """Verify if current session is valid."""
    try:
        # Check if user is logged in
        user_email = session.get('user_email')
        session_token = session.get('session_token')
        
        if not user_email or not session_token:
            return jsonify({
                'success': False,
                'message': 'No active session'
            }), 401
        
        # Load users
        users = load_users()
        
        # Check if user still exists and is active
        if user_email not in users or not users[user_email].get('is_active', True):
            session.clear()
            return jsonify({
                'success': False,
                'message': 'Invalid session'
            }), 401
        
        user = users[user_email]
        
        # Return session validity and user data
        user_response = {
            'email': user_email,
            'firstName': user['first_name'],
            'lastName': user['last_name'],
            'company': user['company']
        }
        
        return jsonify({
            'success': True,
            'message': 'Session is valid',
            'user': user_response
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Session verification failed: {str(e)}'
        }), 500

@auth_bp.route('/users', methods=['GET'])
def list_users():
    """List all users (admin endpoint)."""
    try:
        # Check if user is logged in
        user_email = session.get('user_email')
        if not user_email:
            return jsonify({
                'success': False,
                'message': 'Not authenticated'
            }), 401
        
        # Load users
        users = load_users()
        
        # Return list of users (without password hashes)
        user_list = []
        for email, user_data in users.items():
            user_list.append({
                'email': email,
                'firstName': user_data['first_name'],
                'lastName': user_data['last_name'],
                'company': user_data['company'],
                'createdAt': user_data['created_at'],
                'lastLogin': user_data.get('last_login'),
                'isActive': user_data.get('is_active', True)
            })
        
        return jsonify({
            'success': True,
            'users': user_list,
            'total': len(user_list)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to list users: {str(e)}'
        }), 500

